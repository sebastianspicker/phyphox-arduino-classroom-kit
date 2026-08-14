#!/usr/bin/env python3
"""Validate the static demo's local references and keyboard-accessible structure."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = REPO_ROOT / "demo"
ASSET_ATTRIBUTES = {
    "script": ("src",),
    "img": ("src",),
    "audio": ("src",),
    "video": ("src",),
    "source": ("src",),
    "track": ("src",),
    "iframe": ("src",),
    "object": ("data",),
}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}


class DemoParser(HTMLParser):
    """Collect the semantic and reference data required by the static demo."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.fragments: list[str] = []
        self.local_assets: list[str] = []
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.head_titles = 0
        self._open_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        self.tags.append((tag, attributes))
        self._record_structure(tag, attributes)
        self._record_fragment(tag, attributes)
        self._record_assets(tag, attributes)

    def _record_structure(self, tag: str, attributes: dict[str, str]) -> None:
        if tag == "title" and "head" in self._open_tags:
            self.head_titles += 1
        if tag not in VOID_ELEMENTS:
            self._open_tags.append(tag)
        if identifier := attributes.get("id"):
            self.ids.append(identifier)

    def _record_fragment(self, tag: str, attributes: dict[str, str]) -> None:
        href = attributes.get("href")
        if href and tag == "a" and href.startswith("#"):
            self.fragments.append(href[1:])

    def _record_assets(self, tag: str, attributes: dict[str, str]) -> None:
        href = attributes.get("href")
        if tag == "link" and "stylesheet" in attributes.get("rel", "").lower().split():
            if href:
                self.local_assets.append(href)
        for attribute in ASSET_ATTRIBUTES.get(tag, ()):
            if value := attributes.get(attribute):
                self.local_assets.append(value)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._open_tags) - 1, -1, -1):
            if self._open_tags[index] == tag:
                del self._open_tags[index:]
                return


def _is_local_reference(reference: str) -> bool:
    parsed = urlsplit(reference)
    return not parsed.scheme and not parsed.netloc and not reference.startswith("#")


def _validate_asset(demo_dir: Path, reference: str) -> str | None:
    if not _is_local_reference(reference):
        return None
    parsed = urlsplit(reference)
    if parsed.query or parsed.fragment:
        return f"local asset {reference!r} must not include query or fragment data"
    candidate = demo_dir / Path(unquote(parsed.path))
    try:
        candidate.resolve(strict=True).relative_to(demo_dir.resolve(strict=True))
    except (FileNotFoundError, ValueError):
        return f"local asset {reference!r} must exist within demo/"
    if not candidate.is_file():
        return f"local asset {reference!r} must be a file"
    return None


def _find_tags(parser: DemoParser, name: str) -> list[dict[str, str]]:
    return [attributes for tag, attributes in parser.tags if tag == name]


def _validate_structure(parser: DemoParser) -> list[str]:
    return _validate_document_shape(parser) + _validate_accessibility(parser)


def _validate_document_shape(parser: DemoParser) -> list[str]:
    errors: list[str] = []
    html_tags = _find_tags(parser, "html")
    if len(html_tags) != 1 or not html_tags[0].get("lang"):
        errors.append("document must have one html element with a lang attribute")
    if parser.head_titles != 1:
        errors.append("document must have one title element in head")
    for landmark in ("header", "main", "footer"):
        if len(_find_tags(parser, landmark)) != 1:
            errors.append(f"document must have one {landmark} landmark")
    if not _find_tags(parser, "h1"):
        errors.append("document must have an h1")
    return errors


def _validate_accessibility(parser: DemoParser) -> list[str]:
    errors: list[str] = []
    for nav in _find_tags(parser, "nav"):
        if not (nav.get("aria-label") or nav.get("aria-labelledby")):
            errors.append("every nav landmark must have an accessible name")
    for tag, attributes in parser.tags:
        labelledby = attributes.get("aria-labelledby")
        if labelledby:
            for target in labelledby.split():
                if target not in parser.ids:
                    errors.append(f"{tag} aria-labelledby references missing id {target!r}")
        if tag == "button" and not attributes.get("type"):
            errors.append("every button must declare its type")
    return errors


def _validate_focus_contract(stylesheet: Path) -> list[str]:
    try:
        css = stylesheet.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read stylesheet {stylesheet}: {exc}"]

    normalized_css = re.sub(r"\s+", "", css.lower())
    if "--focus-ring:#ffffff" not in normalized_css:
        return ["focus ring token must remain high-contrast white"]

    focus_rules = re.findall(r"([^{}]+:focus-visible[^{}]*)\{([^{}]*)\}", css, re.DOTALL)
    required_selectors = (
        ".mode-button:focus-visible",
        ".site-header nav a:focus-visible",
        "footer nav a:focus-visible",
    )
    for selectors, declarations in focus_rules:
        if all(selector in selectors for selector in required_selectors):
            normalized = re.sub(r"\s+", "", declarations.lower())
            has_visible_outline = re.search(
                r"outline:\s*(?:[0-9.]+px\s+)?(?:solid|dashed|dotted)\b",
                declarations,
                re.IGNORECASE,
            )
            has_positive_offset = re.search(
                r"outline-offset:\s*[1-9][0-9.]*px", declarations, re.IGNORECASE
            )
            if has_visible_outline and has_positive_offset and "var(--focus-ring)" in normalized:
                return []
            if "outline:none" not in normalized:
                return ["focus rule must use the high-contrast outline outside the control"]
    return ["mode buttons and header/footer links must share a visible :focus-visible outline rule"]


def validate_demo(demo_dir: str | Path = DEMO_DIR) -> list[str]:
    """Return deterministic contract violations for a static demo directory."""

    directory = Path(demo_dir)
    index = directory / "index.html"
    try:
        parser = DemoParser()
        parser.feed(index.read_text(encoding="utf-8"))
        parser.close()
    except OSError as exc:
        return [f"cannot read {index}: {exc}"]

    errors = _validate_structure(parser)
    duplicate_ids = sorted(
        {identifier for identifier in parser.ids if parser.ids.count(identifier) > 1}
    )
    errors.extend(f"duplicate id {identifier!r}" for identifier in duplicate_ids)
    errors.extend(
        f"fragment reference #{fragment} does not match an id"
        for fragment in parser.fragments
        if fragment not in parser.ids
    )
    for asset in parser.local_assets:
        if error := _validate_asset(directory, asset):
            errors.append(error)
    errors.extend(_validate_focus_contract(directory / "styles.css"))
    return errors


def main() -> int:
    errors = validate_demo()
    if errors:
        for error in errors:
            print(f"demo validation: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

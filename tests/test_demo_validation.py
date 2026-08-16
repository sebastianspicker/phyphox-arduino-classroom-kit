"""Stdlib-compatible contract tests for tools/validate_demo.py."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tools.validate_demo import validate_demo

REPO_ROOT = Path(__file__).resolve().parents[1]


class DemoValidationTests(unittest.TestCase):
    def copy_demo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        demo_copy = Path(temporary.name) / "demo"
        shutil.copytree(REPO_ROOT / "demo", demo_copy)
        return temporary, demo_copy

    def test_repository_demo_satisfies_static_contract(self) -> None:
        self.assertEqual(validate_demo(), [])

    def test_demo_renders_dynamic_content_with_dom_nodes(self) -> None:
        script = (REPO_ROOT / "demo" / "demo.js").read_text(encoding="utf-8")

        self.assertNotIn("innerHTML", script)
        self.assertNotIn("outerHTML", script)
        self.assertIn("document.createElement(", script)
        self.assertIn("document.createElementNS(", script)
        self.assertIn(".replaceChildren(", script)
        self.assertIn(".textContent =", script)

    def test_missing_local_asset_is_rejected(self) -> None:
        temporary, demo_copy = self.copy_demo()
        self.addCleanup(temporary.cleanup)
        index = demo_copy / "index.html"
        index.write_text(
            index.read_text(encoding="utf-8").replace('href="styles.css"', 'href="missing.css"'),
            encoding="utf-8",
        )
        self.assertIn("local asset 'missing.css' must exist within demo/", validate_demo(demo_copy))

    def test_missing_fragment_target_is_rejected(self) -> None:
        temporary, demo_copy = self.copy_demo()
        self.addCleanup(temporary.cleanup)
        index = demo_copy / "index.html"
        index.write_text(
            index.read_text(encoding="utf-8").replace(
                'href="#how-it-works"', 'href="#missing-target"'
            ),
            encoding="utf-8",
        )
        self.assertIn(
            "fragment reference #missing-target does not match an id",
            validate_demo(demo_copy),
        )

    def test_semantic_accessibility_violations_are_rejected(self) -> None:
        temporary, demo_copy = self.copy_demo()
        self.addCleanup(temporary.cleanup)
        index = demo_copy / "index.html"
        html = index.read_text(encoding="utf-8")
        html = html.replace('<nav aria-label="Primary navigation">', "<nav>", 1)
        html = html.replace(' type="button"', "", 1)
        index.write_text(html, encoding="utf-8")

        errors = validate_demo(demo_copy)

        self.assertIn("every nav landmark must have an accessible name", errors)
        self.assertIn("every button must declare its type", errors)

    def test_focus_indicator_requires_outline_and_offset(self) -> None:
        temporary, demo_copy = self.copy_demo()
        self.addCleanup(temporary.cleanup)
        stylesheet = demo_copy / "styles.css"
        stylesheet.write_text(
            stylesheet.read_text(encoding="utf-8").replace("  outline-offset: 3px;\n", ""),
            encoding="utf-8",
        )
        self.assertIn(
            "focus rule must use the high-contrast outline outside the control",
            validate_demo(demo_copy),
        )

    def test_focus_indicator_requires_high_contrast_token(self) -> None:
        temporary, demo_copy = self.copy_demo()
        self.addCleanup(temporary.cleanup)
        stylesheet = demo_copy / "styles.css"
        stylesheet.write_text(
            stylesheet.read_text(encoding="utf-8").replace(
                "--focus-ring: #ffffff", "--focus-ring: #385057"
            ),
            encoding="utf-8",
        )
        self.assertIn("focus ring token must remain high-contrast white", validate_demo(demo_copy))

    def test_pages_workflow_is_validation_only(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("name: Validate static demo", workflow)
        self.assertIn("  contents: read", workflow)
        self.assertIn("node --check demo/demo.js", workflow)
        self.assertIn("python3 tools/validate_demo.py", workflow)
        self.assertIn("python3 -m unittest tests.test_demo_validation", workflow)
        self.assertIn("pull_request:", workflow)
        for forbidden in (
            "pages: write",
            "id-token: write",
            "configure-pages",
            "upload-pages-artifact",
            "deploy-pages",
        ):
            self.assertNotIn(forbidden, workflow)


if __name__ == "__main__":
    unittest.main()

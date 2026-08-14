"""Shared semantic XML assertions for astronomy experiments."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest
from defusedxml import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parents[1]
ASTRO_DIR = REPO_ROOT / "experiments" / "astronomy"
DOCS_PATH = REPO_ROOT / "docs" / "ASTRONOMY_EXPERIMENTS_COMPANION.md"


def load_experiment(name: str) -> ET.Element:
    """Parse an experiment with defusedxml rather than a standard XML parser."""
    return ET.parse(ASTRO_DIR / name).getroot()


def read_experiment(name: str) -> str:
    """Read a hand-maintained astronomy experiment as UTF-8 text."""
    return (ASTRO_DIR / name).read_text(encoding="utf-8")


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _view(root: ET.Element, label: str) -> ET.Element:
    views = root.find("views")
    assert views is not None
    matching_views = [view for view in views.findall("view") if view.attrib.get("label") == label]
    if matching_views:
        return matching_views[0]
    raise AssertionError(f"missing view {label!r}")


def _graphs(view: ET.Element, label: str) -> list[ET.Element]:
    return [graph for graph in view.findall("graph") if graph.attrib.get("label") == label]


def _graph_inputs(graph: ET.Element) -> list[str]:
    return [element.text.strip() for element in graph.findall("input") if element.text]


def _container_names(root: ET.Element) -> list[str]:
    containers = root.find("data-containers")
    if containers is None:
        pytest.fail("missing data-containers element")
    return [
        container.text.strip()
        for container in containers.findall("container")
        if container.text and container.text.strip()
    ]


def _data_references(root: ET.Element) -> set[str]:
    refs: set[str] = set()
    for element in root.iter():
        tag = _local_name(element.tag)
        if tag not in {"input", "output", "data"}:
            continue
        if tag == "input" and element.attrib.get("type") == "value":
            continue
        if element.text and element.text.strip():
            refs.add(element.text.strip())
    return refs


def assert_unique_container_names() -> None:
    """Verify that each experiment declares every data container once."""
    duplicates: dict[str, list[str]] = {}
    for path in sorted(ASTRO_DIR.glob("*.phyphox")):
        names = _container_names(ET.parse(path).getroot())
        repeated = sorted(name for name, count in Counter(names).items() if count > 1)
        if repeated:
            duplicates[path.name] = repeated
    if duplicates:
        pytest.fail(f"duplicate astronomy containers: {duplicates}")


def assert_no_unknown_container_references() -> None:
    """Verify that data, input, and output references have a declaration."""
    unknown: dict[str, list[str]] = {}
    for path in sorted(ASTRO_DIR.glob("*.phyphox")):
        root = ET.parse(path).getroot()
        containers = set(_container_names(root))
        missing = sorted(ref for ref in _data_references(root) if ref not in containers)
        if missing:
            unknown[path.name] = missing
    if unknown:
        pytest.fail(f"unknown astronomy container references: {unknown}")


def assert_tidal_locking_ambient_graph_contract() -> None:
    root = load_experiment("tidal-locking.phyphox")
    ambient_graphs = _graphs(_view(root, "IR"), "Ambient Temperature")

    assert len(ambient_graphs) == 2
    assert _graph_inputs(ambient_graphs[0]) == ["t1", "ambCal1"]
    assert _graph_inputs(ambient_graphs[1]) == ["t1", "ambCal2"]


def assert_tidal_locking_time_units_contract() -> None:
    root = load_experiment("tidal-locking.phyphox")

    for view_label in ("Temperature", "IR", "Light"):
        for graph in _view(root, view_label).findall("graph"):
            assert graph.attrib.get("unitX") == "s"

    export = root.find("export")
    assert export is not None
    for data in export.findall("./set/data"):
        if data.attrib.get("name", "").startswith("Time ("):
            assert data.attrib["name"] == "Time (s)"


def assert_mars_pressure_range_contract() -> None:
    root = load_experiment("missiontomars.phyphox")
    text = read_experiment("missiontomars.phyphox").lower()

    assert "pressure drop" not in text
    assert "pressure range" in text

    labels = [value.attrib.get("label") for value in root.findall("./views/view/value")]
    assert "Pressure range" in labels


def assert_transit_star_radius_contract() -> None:
    root = load_experiment("transitmethode.phyphox")
    edit = _view(root, "Planet Size").find("edit")

    assert edit is not None
    assert edit.attrib.get("label") == "Star radius"
    assert edit.attrib.get("signed") == "false"
    assert float(edit.attrib.get("default", "0")) > 0
    assert float(edit.attrib.get("min", "0")) > 0


def assert_astronomy_companion_wording() -> None:
    text = DOCS_PATH.read_text(encoding="utf-8").lower()

    assert "pressure range" in text
    assert "pressure drop" not in text
    assert "reflectance proxy" in text


def test_astronomy_files_have_unique_container_names() -> None:
    assert_unique_container_names()


def test_astronomy_files_do_not_reference_unknown_containers() -> None:
    assert_no_unknown_container_references()

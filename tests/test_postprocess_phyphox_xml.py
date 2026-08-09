"""Regression smoke test for phyphox XML postprocessing."""

from postprocess_phyphox_xml import postprocess


def test_postprocess_removes_generated_metadata() -> None:
    xml = (
        '<phyphox xmlns:xi="http://www.w3.org/2001/XInclude" version="1.7">'
        '<container xml:base="includes/containers.xml" size="0">CH0</container>'
        "</phyphox>"
    )

    result = postprocess(xml)

    assert "xmlns:xi" not in result
    assert "xml:base" not in result
    assert 'version="1.7"' in result
    assert "<container" in result

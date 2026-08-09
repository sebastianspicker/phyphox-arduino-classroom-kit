"""Transformation behavior tests for phyphox XML postprocessing."""

from __future__ import annotations

import textwrap

from postprocess_phyphox_xml import postprocess


class TestPostprocessXmlBase:
    """Tests for xml:base attribute removal."""

    def test_removes_single_xml_base(self) -> None:
        xml = '<container xml:base="includes/foo.xml">CH0</container>'
        result = postprocess(xml)
        assert "xml:base" not in result
        assert "<container>CH0</container>" == result

    def test_removes_multiple_xml_base(self) -> None:
        xml = textwrap.dedent("""\
            <root>
                <a xml:base="path/a.xml">A</a>
                <b xml:base="path/b.xml">B</b>
            </root>
        """)
        result = postprocess(xml)
        assert "xml:base" not in result
        assert "<a>A</a>" in result
        assert "<b>B</b>" in result

    def test_preserves_other_attributes(self) -> None:
        xml = '<container size="0" xml:base="x.xml" static="false">CH0</container>'
        result = postprocess(xml)
        assert "xml:base" not in result
        assert 'size="0"' in result
        assert 'static="false"' in result

    def test_no_xml_base_unchanged(self) -> None:
        xml = '<container size="0">CH0</container>'
        assert postprocess(xml) == xml


class TestPostprocessXIncludeNamespace:
    """Tests for XInclude namespace removal."""

    def test_removes_xi_namespace(self) -> None:
        xml = '<phyphox xmlns:xi="http://www.w3.org/2001/XInclude"><title>T</title></phyphox>'
        result = postprocess(xml)
        assert "xmlns:xi" not in result
        assert "<phyphox><title>T</title></phyphox>" == result

    def test_no_xi_namespace_unchanged(self) -> None:
        xml = "<phyphox><title>T</title></phyphox>"
        assert postprocess(xml) == xml


class TestPostprocessEdgeCases:
    """Edge cases for postprocess()."""

    def test_empty_string(self) -> None:
        assert postprocess("") == ""

    def test_whitespace_only(self) -> None:
        assert postprocess("   \n\n  ") == "   \n\n  "

    def test_xml_base_with_special_chars_in_path(self) -> None:
        xml = '<e xml:base="path/with spaces/file.xml">X</e>'
        result = postprocess(xml)
        assert "xml:base" not in result
        assert "<e>X</e>" == result

    def test_xml_base_with_nested_quotes_unmatched(self) -> None:
        # The regex matches up to the closing double-quote; ensure no breakage.
        xml = '<e xml:base="some/path.xml" other="v">X</e>'
        result = postprocess(xml)
        assert "xml:base" not in result
        assert 'other="v"' in result

    def test_preserves_newlines_and_indentation(self) -> None:
        xml = textwrap.dedent("""\
            <root>
                <child>text</child>
            </root>
        """)
        assert postprocess(xml) == xml

    def test_multiple_xi_namespace_declarations(self) -> None:
        # Only the exact xmlns:xi declaration should be removed.
        xml = (
            '<a xmlns:xi="http://www.w3.org/2001/XInclude"> '
            '<b xmlns:xi="http://www.w3.org/2001/XInclude"/></a>'
        )
        result = postprocess(xml)
        assert "xmlns:xi" not in result

"""CLI and input-source tests for phyphox XML postprocessing."""

from __future__ import annotations

import io
import sys

from postprocess_phyphox_xml import main


class TestMainFileArg:
    """Test the CLI entry point with file and standard-input sources."""

    def test_reads_file_and_postprocesses(self, tmp_path, monkeypatch, capsys) -> None:
        xml = '<phyphox xmlns:xi="http://www.w3.org/2001/XInclude"><title>T</title></phyphox>'
        path = tmp_path / "input.xml"
        path.write_text(xml, encoding="utf-8")
        monkeypatch.setattr(sys, "argv", ["postprocess_phyphox_xml.py", str(path)])

        assert main() == 0
        captured = capsys.readouterr()
        assert "xmlns:xi" not in captured.out
        assert "<phyphox>" in captured.out

    def test_missing_file_returns_error(self, tmp_path, monkeypatch, capsys) -> None:
        missing = tmp_path / "missing.xml"
        monkeypatch.setattr(sys, "argv", ["postprocess_phyphox_xml.py", str(missing)])

        assert main() == 1
        assert "Error" in capsys.readouterr().err

    def test_stdin_mode(self, monkeypatch, capsys) -> None:
        xml = '<e xml:base="x.xml">V</e>'
        monkeypatch.setattr(sys, "argv", ["postprocess_phyphox_xml.py"])
        monkeypatch.setattr(sys, "stdin", io.StringIO(xml))

        assert main() == 0
        captured = capsys.readouterr()
        assert "xml:base" not in captured.out
        assert "<e>V</e>" == captured.out

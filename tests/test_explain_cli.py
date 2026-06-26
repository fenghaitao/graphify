"""Regression tests for `graphify explain` arrow direction (#853)."""
from __future__ import annotations
import json
import graphify.__main__ as mainmod


def _write_graph(tmp_path):
    graph_data = {
        "directed": False, "multigraph": False, "graph": {},
        "nodes": [
            {"id": "validate", "label": "validateSanitySession()",
             "source_file": "server/sanity-validate-session.ts", "community": 0},
            {"id": "create_patch", "label": "createPatchHandler()",
             "source_file": "server/create-patch-handler.ts", "community": 0},
            {"id": "create_edit", "label": "createEditHandler()",
             "source_file": "server/create-edit-handler.ts", "community": 0},
            {"id": "stable_stringify", "label": "stableStringify()",
             "source_file": "shared/stringify.ts", "community": 0},
        ],
        "links": [
            {"source": "create_patch", "target": "validate",
             "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "create_edit", "target": "validate",
             "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "validate", "target": "stable_stringify",
             "relation": "calls", "confidence": "EXTRACTED"},
        ],
    }
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(graph_data))
    return p


def _run(monkeypatch, graph_path, label, capsys):
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(mainmod.sys, "argv",
        ["graphify", "explain", label, "--graph", str(graph_path)])
    mainmod.main()
    return capsys.readouterr().out


def test_callee_shows_callers_as_inbound(monkeypatch, tmp_path, capsys):
    p = _write_graph(tmp_path)
    out = _run(monkeypatch, p, "validateSanitySession", capsys)
    assert "<-- createPatchHandler() [calls]" in out
    assert "<-- createEditHandler() [calls]" in out
    assert "--> stableStringify() [calls]" in out
    assert "--> createPatchHandler() [calls]" not in out
    assert "--> createEditHandler() [calls]" not in out


def test_caller_shows_callee_as_outbound(monkeypatch, tmp_path, capsys):
    p = _write_graph(tmp_path)
    out = _run(monkeypatch, p, "createPatchHandler", capsys)
    assert "--> validateSanitySession() [calls]" in out
    assert "<-- " not in out


def _write_doclinked_graph(tmp_path):
    """A code function with a doc rationale (motivates), a doc reference, and a code call."""
    graph_data = {
        "directed": False, "multigraph": False, "graph": {},
        "nodes": [
            {"id": "save_parsed", "label": "save_parsed()", "file_type": "code",
             "source_file": "raw/storage.py", "community": 0},
            {"id": "load_index", "label": "load_index()", "file_type": "code",
             "source_file": "raw/storage.py", "community": 0},
            {"id": "twr", "label": "Transactional Write Risk", "file_type": "concept",
             "source_file": "raw/architecture.md", "community": 1},
            {"id": "arch", "label": "architecture.md", "file_type": "document",
             "source_file": "raw/architecture.md", "community": 1},
        ],
        "links": [
            {"source": "save_parsed", "target": "load_index",
             "relation": "calls", "confidence": "EXTRACTED"},
            {"source": "twr", "target": "save_parsed",
             "relation": "motivates", "confidence": "INFERRED", "_origin": "link"},
            {"source": "arch", "target": "save_parsed",
             "relation": "references", "confidence": "EXTRACTED", "_origin": "link"},
        ],
    }
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(graph_data))
    return p


def test_explain_groups_doc_bridges_by_intent(monkeypatch, tmp_path, capsys):
    """The doc↔code edges are grouped: `motivates` under "Why / rationale", `references`
    under "Documentation", and code calls under "Code" — so the WHY is no longer buried."""
    p = _write_doclinked_graph(tmp_path)
    out = _run(monkeypatch, p, "save_parsed", capsys)

    assert "Why / rationale" in out
    assert "Documentation" in out
    assert "Code" in out

    # The rationale must appear in the Why section, BEFORE the Code section.
    why_idx = out.index("Why / rationale")
    code_idx = out.index("\nCode (")
    assert why_idx < code_idx
    assert out.index("Transactional Write Risk") < code_idx
    assert "<-- architecture.md [references]" in out
    assert "--> load_index() [calls]" in out

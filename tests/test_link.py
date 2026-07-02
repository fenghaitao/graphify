"""Tests for doc↔code linking: code-manifest emission and the deterministic
link-docs pass (graphify/link.py). See docs/doc-code-linking-design.md."""
from __future__ import annotations

import json

import networkx as nx

import graphify.__main__ as mainmod
from graphify import link


def _graph_from_records(nodes, edges):
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n["id"], **{k: v for k, v in n.items() if k != "id"})
    for e in edges:
        G.add_edge(e["source"], e["target"], **{k: v for k, v in e.items() if k not in ("source", "target")})
    return G


# --- manifest builder ----------------------------------------------------------

def test_manifest_attaches_signature_and_doc(tmp_path):
    """A function node gets its signature (from source) and its docstring (via the
    rationale_for edge); a sourceless stub is skipped."""
    src = tmp_path / "mod.py"
    src.write_text(
        'def greet(name: str) -> str:\n'
        '    """Say hello to someone."""\n'
        '    return f"hi {name}"\n'
    )
    nodes = [
        {"id": "mod_greet", "label": "greet()", "file_type": "code",
         "source_file": "mod.py", "source_location": "L1"},
        {"id": "mod_greet_rat", "label": "Say hello to someone.", "file_type": "rationale",
         "source_file": "mod.py", "source_location": "L2"},
        {"id": "ghost", "label": "External", "file_type": "code", "source_file": ""},
    ]
    edges = [{"source": "mod_greet_rat", "target": "mod_greet", "relation": "rationale_for"}]
    G = _graph_from_records(nodes, edges)

    recs = list(link.iter_manifest_records(G, root=tmp_path))
    by_id = {r["id"]: r for r in recs}

    assert "ghost" not in by_id, "sourceless stub must be skipped"
    rec = by_id["mod_greet"]
    assert rec["signature"] == "def greet(name: str) -> str"
    assert rec["doc"] == "Say hello to someone."


# --- Gap 1+2: doc-file container synthesis -------------------------------------

def test_synthesize_doc_containers_groups_entities_under_file_node():
    """A doc's already-extracted concept/rationale nodes get a synthesized document
    file node + contains edges (weight 0.1). Code is untouched."""
    nodes = [
        {"id": "raw_arch_storage_module", "label": "Storage Module", "file_type": "concept",
         "source_file": "raw/architecture.md", "source_location": None},
        {"id": "raw_arch_repository_pattern", "label": "Repository Pattern", "file_type": "rationale",
         "source_file": "raw/architecture.md", "source_location": None},
        {"id": "raw_storage", "label": "storage.py", "file_type": "code",
         "source_file": "raw/storage.py", "source_location": "L1"},
    ]
    G = _graph_from_records(nodes, [])
    added = link.synthesize_doc_containers(G)

    assert added == 1
    assert G.nodes["raw_architecture"]["file_type"] == "document"
    children = [
        v for u, v, d in G.edges("raw_architecture", data=True)
        if d.get("relation") == "contains"
    ]
    assert set(children) == {"raw_arch_storage_module", "raw_arch_repository_pattern"}
    weights = {d["weight"] for u, v, d in G.edges("raw_architecture", data=True)}
    assert weights == {0.1}
    # The code node must NOT be pulled under any document container.
    assert not G.has_edge("raw_architecture", "raw_storage")


def test_synthesize_doc_containers_idempotent_and_codeonly_noop():
    """Re-running adds nothing new; a pure-code graph yields no document nodes."""
    code_only = _graph_from_records(
        [{"id": "m", "label": "m.py", "file_type": "code", "source_file": "m.py",
          "source_location": "L1"}],
        [],
    )
    assert link.synthesize_doc_containers(code_only) == 0

    doc = _graph_from_records(
        [{"id": "d_a", "label": "A", "file_type": "concept", "source_file": "d.md",
          "source_location": None}],
        [],
    )
    assert link.synthesize_doc_containers(doc) == 1
    assert link.synthesize_doc_containers(doc) == 0  # idempotent


# --- deterministic matcher -----------------------------------------------------

def test_matcher_resolves_filenames_and_unique_symbols():
    records = [
        {"id": "raw_storage_py", "label": "storage.py", "source_file": "raw/storage.py"},
        {"id": "raw_storage_save_record", "label": "save_record()", "source_file": "raw/storage.py"},
        {"id": "raw_api_list", "label": "list()", "source_file": "raw/api.py"},
        {"id": "raw_db_list", "label": "list()", "source_file": "raw/db.py"},
    ]
    idx = link._MatchIndex(records)
    text = (
        "The persistence layer lives in `storage.py`. It exposes save_record for "
        "writes. The ambiguous list() helper is intentionally not linked."
    )
    hits = link.scan_doc_references(text, idx)
    assert "raw_storage_py" in hits          # filename via backticks
    assert "raw_storage_save_record" in hits  # unique snake_case symbol
    # `list` is defined in two files → ambiguous → must NOT be linked
    assert "raw_api_list" not in hits and "raw_db_list" not in hits


# --- full pipeline: extract --code-only then link-docs -------------------------

def test_extract_code_only_then_link_docs(monkeypatch, tmp_path):
    """End-to-end: code-only build emits a manifest with no LLM; link-docs then adds
    a document node and a deterministic doc→code reference edge."""
    (tmp_path / "storage.py").write_text(
        'def save_record(rec):\n    """Persist a record."""\n    return True\n'
    )
    (tmp_path / "design.md").write_text(
        "# Design\nPersistence is handled by `storage.py` via save_record.\n"
    )
    out_dir = tmp_path / "out"
    gout = out_dir / "graphify-out"

    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr("graphify.llm.detect_backend", lambda: None)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)

    # Step 1: code-only
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "extract", str(tmp_path), "--code-only", "--out", str(out_dir)],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)
    assert (gout / "code-manifest.jsonl").exists()

    # Step 2: link-docs with the deterministic doc→code matcher enabled.
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--out", str(out_dir), "--match-code"],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)

    graph = json.loads((gout / "graph.json").read_text())
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = graph.get("edges", graph.get("links", []))

    doc_nodes = [n for n in graph["nodes"] if n.get("file_type") == "document"]
    assert doc_nodes, "link-docs must synthesize a document node"

    # There must be at least one doc→code reference edge added by the link pass.
    link_edges = [
        e for e in edges
        if e.get("_origin") == "link" and e.get("relation") == "references"
    ]
    assert link_edges, "link-docs must add a doc→code reference edge"
    for e in link_edges:
        assert nodes[e["source"]].get("file_type") == "document"
        assert nodes[e["target"]].get("file_type") == "code"


def test_link_docs_match_code_is_opt_in(monkeypatch, tmp_path):
    """link-docs creates document nodes always, but doc→code reference edges ONLY with
    --match-code. Default (no flag) must add zero `references` edges."""
    (tmp_path / "storage.py").write_text(
        'def save_record(rec):\n    """Persist a record."""\n    return True\n'
    )
    (tmp_path / "design.md").write_text(
        "# Design\nPersistence is handled by `storage.py` via save_record.\n"
    )
    out_dir = tmp_path / "out"
    gout = out_dir / "graphify-out"

    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr("graphify.llm.detect_backend", lambda: None)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)

    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "extract", str(tmp_path), "--code-only", "--out", str(out_dir)],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)

    def _link_edges():
        graph = json.loads((gout / "graph.json").read_text())
        edges = graph.get("edges", graph.get("links", []))
        return [e for e in edges if e.get("_origin") == "link" and e.get("relation") == "references"]

    # Default: no --match-code → document node created, but no reference edges.
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--out", str(out_dir)],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)
    graph = json.loads((gout / "graph.json").read_text())
    assert any(n.get("file_type") == "document" for n in graph["nodes"])
    assert _link_edges() == [], "no doc→code edges without --match-code"

    # Opt-in: --match-code → reference edges appear.
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--out", str(out_dir), "--match-code"],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)
    assert _link_edges(), "doc→code edges must appear with --match-code"


def _run_code_only(monkeypatch, corpus, out_dir):
    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr("graphify.llm.detect_backend", lambda: None)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "extract", str(corpus), "--code-only", "--out", str(out_dir)],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)


def test_link_docs_reuses_cached_doc_concepts(monkeypatch, tmp_path):
    """If a doc's semantic extraction is already cached, link-docs reuses it (no LLM)
    and builds the contains hierarchy over the cached concepts."""
    (tmp_path / "storage.py").write_text('def save_record(r):\n    """Persist."""\n    return True\n')
    (tmp_path / "design.md").write_text("# Design\nThe storage layer notes.\n")
    out_dir = tmp_path / "out"
    gout = out_dir / "graphify-out"
    _run_code_only(monkeypatch, tmp_path, out_dir)

    # Pre-populate the semantic cache for design.md with a concept node.
    from graphify.cache import save_semantic_cache
    concept = {
        "id": "design_storage_layer", "label": "Storage Layer", "file_type": "concept",
        "source_file": str(tmp_path / "design.md"), "source_location": None,
    }
    save_semantic_cache([concept], [], [], root=out_dir)

    # link-docs with NO backend must still pick up the cached concept.
    monkeypatch.setattr("graphify.llm.detect_backend", lambda: None)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--out", str(out_dir)],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)

    graph = json.loads((gout / "graph.json").read_text())
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = graph.get("edges", graph.get("links", []))
    assert nodes.get("design_storage_layer", {}).get("file_type") == "concept"
    assert nodes.get("design", {}).get("file_type") == "document"
    contains = [
        e for e in edges
        if e.get("relation") == "contains"
        and {e.get("source"), e.get("target")} == {"design", "design_storage_layer"}
    ]
    assert contains, "cached concept must be contained under its document node"


def test_link_docs_extracts_uncached_doc_concepts(monkeypatch, tmp_path):
    """When a doc is not cached, link-docs runs the semantic pass for it (here mocked)
    and merges the extracted concepts."""
    (tmp_path / "storage.py").write_text('def save_record(r):\n    """Persist."""\n    return True\n')
    (tmp_path / "design.md").write_text("# Design\nThe storage layer notes.\n")
    out_dir = tmp_path / "out"
    gout = out_dir / "graphify-out"
    _run_code_only(monkeypatch, tmp_path, out_dir)

    def _fake_extract(paths, **kwargs):
        src = str(paths[0])
        return {
            "nodes": [{"id": "design_x", "label": "Concept X", "file_type": "concept",
                       "source_file": src, "source_location": None}],
            "edges": [], "hyperedges": [], "input_tokens": 10, "output_tokens": 5,
        }

    monkeypatch.setattr("graphify.llm.extract_corpus_parallel", _fake_extract)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--out", str(out_dir), "--backend", "claude"],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)

    graph = json.loads((gout / "graph.json").read_text())
    nodes = {n["id"]: n for n in graph["nodes"]}
    assert nodes.get("design_x", {}).get("file_type") == "concept"
    edges = graph.get("edges", graph.get("links", []))
    assert any(
        e.get("relation") == "contains"
        and {e.get("source"), e.get("target")} == {"design", "design_x"}
        for e in edges
    ), "freshly extracted concept must be contained under its document node"


def test_link_concepts_to_code_validates_targets(monkeypatch):
    """The LLM linker enforces the boundary rule: edges with an unknown target id, an
    unknown source id, or a relation outside the enum are dropped."""
    concepts = [{"id": "d_repo", "label": "Repository Pattern", "description": "..."}]
    records = [{"id": "raw_storage", "label": "storage.py", "source_file": "raw/storage.py"}]
    reply = json.dumps({"edges": [
        {"source": "d_repo", "target": "raw_storage", "relation": "describes",
         "confidence": "INFERRED", "confidence_score": 0.85},
        {"source": "d_repo", "target": "NONEXISTENT", "relation": "describes"},   # bad target
        {"source": "GHOST", "target": "raw_storage", "relation": "describes"},    # bad source
        {"source": "d_repo", "target": "raw_storage", "relation": "frobnicates"}, # bad relation
    ]})
    monkeypatch.setattr("graphify.llm._call_llm", lambda *a, **k: reply)

    edges = link.link_concepts_to_code(concepts, records, backend="claude")
    assert len(edges) == 1
    e = edges[0]
    assert (e["source"], e["target"], e["relation"]) == ("d_repo", "raw_storage", "describes")
    assert e["_origin"] == "link"


def test_link_docs_link_code_adds_concept_to_code_edges(monkeypatch, tmp_path):
    """Full path: --link-code links an extracted concept to a real code node id (both the
    concept extraction and the LLM linker are mocked)."""
    import re as _re

    (tmp_path / "storage.py").write_text('def save_record(r):\n    """Persist."""\n    return True\n')
    (tmp_path / "design.md").write_text("# Design\nThe Repository Pattern wraps storage.\n")
    out_dir = tmp_path / "out"
    gout = out_dir / "graphify-out"
    _run_code_only(monkeypatch, tmp_path, out_dir)

    def _fake_extract(paths, **kwargs):
        return {
            "nodes": [{"id": "design_repository_pattern", "label": "Repository Pattern",
                       "file_type": "concept", "source_file": str(paths[0]), "source_location": None}],
            "edges": [], "hyperedges": [], "input_tokens": 1, "output_tokens": 1,
        }

    def _fake_link(prompt, **kwargs):
        # Pick a real code node id out of the prompt's CODE NODES list.
        m = _re.search(r'"(\w*save_record\w*)"', prompt)
        target = m.group(1) if m else None
        return json.dumps({"edges": [{
            "source": "design_repository_pattern", "target": target,
            "relation": "describes", "confidence": "INFERRED", "confidence_score": 0.85,
        }]})

    monkeypatch.setattr("graphify.llm.extract_corpus_parallel", _fake_extract)
    monkeypatch.setattr("graphify.llm._call_llm", _fake_link)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--out", str(out_dir),
         "--backend", "claude", "--link-code"],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)

    graph = json.loads((gout / "graph.json").read_text())
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = graph.get("edges", graph.get("links", []))
    bridge = [
        e for e in edges
        if e.get("relation") == "describes" and e.get("_origin") == "link"
        and "design_repository_pattern" in (e.get("source"), e.get("target"))
    ]
    assert bridge, "concept→code describes edge must be added with --link-code"
    other = bridge[0]["target"] if bridge[0]["source"] == "design_repository_pattern" else bridge[0]["source"]
    assert nodes[other].get("file_type") == "code"


def test_link_docs_errors_without_manifest(tmp_path, capsys):
    """link-docs must fail clearly when no manifest exists yet."""
    (tmp_path / "graphify-out").mkdir()
    (tmp_path / "graphify-out" / "graph.json").write_text('{"nodes": [], "edges": []}')
    import graphify.__main__ as m
    import pytest

    m.sys.argv = ["graphify", "link-docs", str(tmp_path)]
    with pytest.raises(SystemExit) as exc:
        m.main()
    assert exc.value.code == 1
    assert "code-manifest" in capsys.readouterr().err


def test_link_docs_does_not_count_edges_with_missing_target(monkeypatch, tmp_path):
    """A stale code-manifest target that is absent from the graph must NOT be
    counted as a persisted doc→code edge — build_from_json silently drops such an
    edge. Regression for the doc_edges merge loop that guarded only `source`."""
    (tmp_path / "storage.py").write_text(
        'def save_record(rec):\n    """Persist a record."""\n    return True\n'
    )
    (tmp_path / "design.md").write_text(
        "# Design\nUses `save_record` and the now-removed `ghost_fn` helper.\n"
    )
    out_dir = tmp_path / "out"
    gout = out_dir / "graphify-out"
    _run_code_only(monkeypatch, tmp_path, out_dir)

    # Inject a stale manifest record whose id is NOT a node in graph.json. The
    # matcher will resolve the doc's `ghost_fn` mention to it, producing a
    # reference edge with a dangling target.
    manifest = gout / link.MANIFEST_FILENAME
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(
            {"id": "ghost_missing_id", "label": "ghost_fn", "source_file": "storage.py"}
        ) + "\n")

    summary = link.apply_doc_links(gout, tmp_path, match_code=True, backend=None)

    graph = json.loads((gout / "graph.json").read_text())
    edges = graph.get("edges", graph.get("links", []))
    refs = [e for e in edges if e.get("relation") == "references"]
    # the ghost target was never persisted ...
    assert all(e.get("target") != "ghost_missing_id" for e in refs)
    # ... the real reference still landed ...
    assert len(refs) == 1
    # ... and the reported count matches what actually persisted (no phantom count).
    assert summary["reference_edges_added"] == len(refs)


def test_link_docs_rejects_unknown_backend(monkeypatch, tmp_path, capsys):
    """An invalid --backend is rejected at the CLI boundary (mirrors extract),
    not surfaced as a ValueError traceback from extract_corpus_parallel."""
    import pytest
    (tmp_path / "graphify-out").mkdir()
    (tmp_path / "graphify-out" / "graph.json").write_text('{"nodes": [], "edges": []}')
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(tmp_path), "--backend", "bogus-backend"],
    )
    with pytest.raises(SystemExit) as exc:
        mainmod.main()
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "unknown backend" in err.lower()
    assert "bogus-backend" in err


# --- two-graph mode: extract --doc-only + link-docs --code-graph/--doc-graph ----

def _write_two_graph_fixtures(tmp_path):
    """A repo-side code graph + manifest and a vault-side doc graph + doc file, laid
    out the way `extract --code-only` / `extract --doc-only` would leave them."""
    code_out = tmp_path / "repo" / "graphify-out"
    code_out.mkdir(parents=True)
    code_nodes = [
        {"id": "storage_py", "label": "storage.py", "file_type": "code",
         "source_file": "storage.py", "source_location": None},
        {"id": "storage_save_record", "label": "save_record()", "file_type": "code",
         "source_file": "storage.py", "source_location": "L1"},
    ]
    code_edges = [
        {"source": "storage_py", "target": "storage_save_record", "relation": "contains",
         "confidence": "EXTRACTED", "confidence_score": 1.0,
         "source_file": "storage.py", "source_location": None, "weight": 1.0},
    ]
    (code_out / "graph.json").write_text(json.dumps({"nodes": code_nodes, "edges": code_edges}))
    manifest = [
        {"id": "storage_py", "label": "storage.py", "source_file": "storage.py",
         "source_location": None},
        {"id": "storage_save_record", "label": "save_record()", "source_file": "storage.py",
         "source_location": "L1"},
    ]
    (code_out / "code-manifest.jsonl").write_text(
        "\n".join(json.dumps(r) for r in manifest) + "\n"
    )

    doc_root = tmp_path / "vaultproj"
    doc_out = doc_root / "graphify-out"
    doc_out.mkdir(parents=True)
    (doc_root / "design.md").write_text(
        "# Design\nPersistence is handled by `storage.py` via save_record.\n"
    )
    doc_nodes = [
        {"id": "design_md", "label": "design.md", "file_type": "document",
         "source_file": "design.md", "source_location": None},
        {"id": "design_persistence", "label": "Persistence Strategy", "file_type": "concept",
         "source_file": "design.md", "source_location": None},
    ]
    doc_edges = [
        {"source": "design_md", "target": "design_persistence", "relation": "contains",
         "confidence": "EXTRACTED", "confidence_score": 1.0,
         "source_file": "design.md", "source_location": None, "weight": 0.1},
    ]
    (doc_out / "graph.json").write_text(json.dumps({"nodes": doc_nodes, "edges": doc_edges}))
    return code_out, doc_root, doc_out


def test_link_graphs_composes_bridges_and_stamps_without_mutating_inputs(tmp_path):
    """Two-graph mode: code ⊕ doc merge with deterministic bridges; neither input file
    changes; the output records both input hashes under graph.link_meta."""
    import hashlib

    code_out, doc_root, doc_out = _write_two_graph_fixtures(tmp_path)
    out = doc_out / "merged.json"
    code_before = (code_out / "graph.json").read_bytes()
    doc_before = (doc_out / "graph.json").read_bytes()

    summary = link.link_graphs(
        code_out / "graph.json", doc_out / "graph.json", out,
        doc_root=doc_root, match_code=True,
    )

    assert out.exists()
    assert (code_out / "graph.json").read_bytes() == code_before, "code graph must not be mutated"
    assert (doc_out / "graph.json").read_bytes() == doc_before, "doc graph must not be mutated"

    merged = json.loads(out.read_text())
    ids = {n["id"] for n in merged["nodes"]}
    assert {"storage_py", "storage_save_record", "design_md", "design_persistence"} <= ids

    edges = merged.get("edges", merged.get("links", []))
    refs = [e for e in edges
            if e.get("relation") == "references" and e.get("_origin") == "link"]
    assert refs, "the literal matcher must bridge design.md to the storage code"
    assert summary["reference_edges_added"] == len(refs)

    meta = merged.get("graph", {}).get("link_meta", {})
    assert meta.get("code_graph_sha256") == hashlib.sha256(code_before).hexdigest()
    assert meta.get("doc_graph_sha256") == hashlib.sha256(doc_before).hexdigest()
    assert meta.get("linked_at")


def test_link_graphs_derives_manifest_when_missing(tmp_path):
    """Without a code-manifest.jsonl next to the code graph, the allowed-target list
    is derived from the code graph itself, so any repo graph works as input."""
    code_out, doc_root, doc_out = _write_two_graph_fixtures(tmp_path)
    (code_out / "code-manifest.jsonl").unlink()
    out = doc_out / "merged.json"

    summary = link.link_graphs(
        code_out / "graph.json", doc_out / "graph.json", out,
        doc_root=doc_root, match_code=True,
    )
    assert summary["reference_edges_added"] >= 1


def test_link_docs_cli_two_graph_mode(monkeypatch, tmp_path):
    """CLI: link-docs <doc_root> --code-graph A --doc-graph B --match-code writes
    merged.json next to the doc graph by default."""
    code_out, doc_root, doc_out = _write_two_graph_fixtures(tmp_path)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr("graphify.llm.detect_backend", lambda: None)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(doc_root),
         "--code-graph", str(code_out / "graph.json"),
         "--doc-graph", str(doc_out / "graph.json"),
         "--match-code"],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)
    assert (doc_out / "merged.json").exists()


def test_link_docs_cli_requires_both_graph_flags(monkeypatch, tmp_path, capsys):
    import pytest
    code_out, doc_root, doc_out = _write_two_graph_fixtures(tmp_path)
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "link-docs", str(doc_root),
         "--code-graph", str(code_out / "graph.json")],
    )
    with pytest.raises(SystemExit) as exc:
        mainmod.main()
    assert exc.value.code == 1
    assert "must be given together" in capsys.readouterr().err


# --- extract --doc-only ----------------------------------------------------------

def test_extract_doc_only_skips_ast(monkeypatch, tmp_path):
    """--doc-only runs the semantic pipeline only: code files are detected but never
    AST-extracted, so the graph holds doc entities and no code symbols."""
    (tmp_path / "storage.py").write_text("def save_record(rec):\n    return True\n")
    (tmp_path / "notes.md").write_text("# Notes\nAll about persistence.\n")
    out_dir = tmp_path / "out"

    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr("graphify.llm.detect_backend", lambda: "gemini")
    monkeypatch.setattr("graphify.llm._get_backend_api_key", lambda _b: "test-key")

    def fake_corpus(paths, **kw):
        cb = kw.get("on_chunk_done")
        if cb:
            cb(0, 1, {})
        return {
            "nodes": [{"id": "notes_md_persistence", "label": "Persistence",
                       "file_type": "document", "source_file": "notes.md",
                       "source_location": None}],
            "edges": [], "hyperedges": [], "input_tokens": 10, "output_tokens": 5,
        }
    monkeypatch.setattr("graphify.llm.extract_corpus_parallel", fake_corpus)

    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "extract", str(tmp_path), "--doc-only", "--out", str(out_dir)],
    )
    try:
        mainmod.main()
    except SystemExit as exc:
        assert exc.code in (0, None)

    graph = json.loads((out_dir / "graphify-out" / "graph.json").read_text())
    labels = {n.get("label", "") for n in graph["nodes"]}
    assert not any("save_record" in l for l in labels), "--doc-only must skip AST extraction"
    assert any("Persistence" in l for l in labels)


def test_extract_code_only_doc_only_conflict(monkeypatch, tmp_path, capsys):
    import pytest
    (tmp_path / "a.py").write_text("x = 1\n")
    monkeypatch.setattr(mainmod, "_check_skill_version", lambda _: None)
    monkeypatch.setattr(
        mainmod.sys, "argv",
        ["graphify", "extract", str(tmp_path), "--code-only", "--doc-only"],
    )
    with pytest.raises(SystemExit) as exc:
        mainmod.main()
    assert exc.value.code == 2
    assert "mutually exclusive" in capsys.readouterr().err

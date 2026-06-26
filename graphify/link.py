"""Doc↔code linking: code-manifest emission and (later) the link-docs pass.

This module is the home of the deterministic, post-build linking work described in
``docs/doc-code-linking-design.md``. It never lives inside ``extract.py`` (which stays the
pure AST engine) — everything here operates on the *assembled* code graph.

Step 1 (``graphify extract --code-only``) calls :func:`write_manifest` to emit
``code-manifest.jsonl`` next to ``graph.json``. Step 2 (``graphify link-docs``) reads that
file back as the matcher's lookup table and the LLM's allowed-target list.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

import networkx as nx

MANIFEST_FILENAME = "code-manifest.jsonl"

# Doc-side file extensions that classify_file treats as documents/papers; the link
# pass synthesizes a `document` node for each and scans its text for code mentions.
_DOC_EXTENSIONS = {".md", ".mdx", ".qmd", ".rst", ".txt", ".markdown"}

# source_location is stored as e.g. "L42"; capture the 1-based line number.
_LINE_RE = re.compile(r"^L(\d+)$")
# A line that declares a callable/type across languages contains an opening paren
# (params) or, for class/struct decls, an inheritance/brace opener. We only need a
# cheap "is this a signature-bearing line" gate — the AST already validated structure.
_SIG_CAP = 200


def _resolve_source(source_file: str, root: Path | None) -> Path | None:
    """Resolve a node's source_file to an absolute path, honoring the build root."""
    if not source_file:
        return None
    p = Path(source_file)
    if not p.is_absolute() and root is not None:
        p = root / p
    return p


def _file_lines_cache(path: Path, cache: dict[Path, list[str] | None]) -> list[str] | None:
    """Read and cache a source file's lines; None if unreadable."""
    if path not in cache:
        try:
            cache[path] = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            cache[path] = None
    return cache[path]


def _extract_signature(lines: list[str], line_no: int) -> str | None:
    """Deterministically slice a declaration's signature starting at 1-based line_no.

    Reads the declaration line and, when the parameter list spans lines, continues
    until parentheses balance (capped at a few lines). Returns whitespace-collapsed
    text up to the body opener (``:`` / ``{``), or None when the line carries no
    parameter list (file/import/module nodes fall out here).
    """
    idx = line_no - 1
    if idx < 0 or idx >= len(lines):
        return None
    first = lines[idx]
    if "(" not in first:
        return None  # not a callable/decl signature line — skip files, imports, vars
    buf = [first]
    depth = first.count("(") - first.count(")")
    j = idx + 1
    while depth > 0 and j < len(lines) and j - idx < 4:
        buf.append(lines[j])
        depth += lines[j].count("(") - lines[j].count(")")
        j += 1
    text = " ".join(buf)
    # Cut at the body opener so we keep the signature, not the implementation.
    for opener in (":", "{"):
        pos = text.find(opener, text.rfind(")") if ")" in text else 0)
        if pos != -1:
            text = text[:pos]
            break
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > _SIG_CAP:
        text = text[: _SIG_CAP - 1].rstrip() + "…"
    return text or None


def _doc_map(G: nx.Graph) -> dict[str, str]:
    """Map code node id → docstring text via `rationale_for` edges.

    The rationale node's label *is* the (truncated) docstring (see
    `extract._extract_python_rationale`). Currently Python-only by design; other
    languages simply produce no rationale nodes and so get no `doc`.
    """
    out: dict[str, str] = {}
    for u, v, data in G.edges(data=True):
        if data.get("relation") != "rationale_for":
            continue
        # Edge direction may be lost in an undirected Graph; identify endpoints by type.
        ft_u = G.nodes[u].get("file_type")
        ft_v = G.nodes[v].get("file_type")
        if ft_u == "rationale" and ft_v == "code":
            rat, code = u, v
        elif ft_v == "rationale" and ft_u == "code":
            rat, code = v, u
        else:
            continue
        # First rationale wins (module/def docstring); don't clobber on later edges.
        out.setdefault(code, str(G.nodes[rat].get("label", "")).strip())
    return out


def iter_manifest_records(G: nx.Graph, root: Path | None = None) -> Iterable[dict]:
    """Yield one manifest record per real code symbol in the graph.

    Skips sourceless stub nodes (cross-file reference placeholders). `signature` and
    `doc` are optional and omitted rather than fabricated when unavailable.
    """
    doc_map = _doc_map(G)
    line_cache: dict[Path, list[str] | None] = {}
    for nid, attrs in G.nodes(data=True):
        if attrs.get("file_type") != "code":
            continue
        source_file = attrs.get("source_file") or ""
        if not source_file:
            continue  # sourceless stub — nothing to point a doc edge at
        loc = attrs.get("source_location") or ""
        rec: dict = {
            "id": nid,
            "label": attrs.get("label", ""),
            "source_file": source_file,
            "source_location": loc or None,
        }
        m = _LINE_RE.match(loc) if isinstance(loc, str) else None
        if m:
            abs_path = _resolve_source(source_file, root)
            if abs_path is not None:
                lines = _file_lines_cache(abs_path, line_cache)
                if lines is not None:
                    sig = _extract_signature(lines, int(m.group(1)))
                    if sig:
                        rec["signature"] = sig
        doc = doc_map.get(nid)
        if doc:
            rec["doc"] = doc
        yield rec


def write_manifest(G: nx.Graph, out_path: str | Path, root: str | Path | None = None) -> int:
    """Write the code-manifest as JSONL to out_path. Returns the record count."""
    root_path = Path(root) if root is not None else None
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out.open("w", encoding="utf-8") as fh:
        for rec in iter_manifest_records(G, root_path):
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_manifest_from_extraction(
    extraction: dict, out_path: str | Path, root: str | Path | None = None
) -> int:
    """Build a throwaway graph from a raw nodes/edges dict, then emit the manifest.

    Used by the ``--no-cluster`` path, which writes the merged dict directly without
    ever materializing the clustered graph.
    """
    G: nx.DiGraph = nx.DiGraph()
    for node in extraction.get("nodes", []):
        if isinstance(node, dict) and "id" in node:
            G.add_node(node["id"], **{k: v for k, v in node.items() if k != "id"})
    for edge in extraction.get("edges", extraction.get("links", [])):
        src, tgt = edge.get("source"), edge.get("target")
        if src in G and tgt in G:
            G.add_edge(src, tgt, **{k: v for k, v in edge.items() if k not in ("source", "target")})
    return write_manifest(G, out_path, root)


def load_manifest(path: str | Path) -> list[dict]:
    """Read a code-manifest.jsonl file into a list of records."""
    out: list[dict] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# --- deterministic literal-mention matcher -------------------------------------
#
# The matcher resolves a doc-side token to exactly one code node id, conservatively:
# a filename (`storage.py`) → that file's node; a snake_case/CamelCase symbol or a
# backtick-quoted identifier → a code node whose label matches, but ONLY when the
# match is unambiguous. Everything it cannot resolve is the residual for the (future)
# LLM concept pass. See docs/doc-code-linking-design.md.

_BACKTICK_RE = re.compile(r"`([^`\n]+)`")
_FILENAME_RE = re.compile(r"\b[\w-]+\.[A-Za-z]\w*\b")
# snake_case (has `_`) or camelCase (a lowercase run then an uppercase) — tokens that
# are unlikely to be ordinary prose words, so safe to attempt outside backticks.
_CODEISH_RE = re.compile(r"\b(?:\w*_\w+|[a-z]+[A-Z]\w*)\b")


def _normalize_symbol(label: str) -> str:
    """Strip a trailing call marker so `handle_upload()` matches the doc's `handle_upload`."""
    return label.strip().rstrip(")").rstrip("(").strip()


class _MatchIndex:
    """Lookup tables over a manifest for the deterministic matcher."""

    def __init__(self, records: list[dict]):
        self.by_filename: dict[str, str] = {}      # basename -> file node id
        self.by_symbol: dict[str, set[str]] = {}   # symbol label -> ids (ambiguity check)
        for rec in records:
            nid = rec.get("id")
            label = str(rec.get("label", ""))
            source_file = str(rec.get("source_file", ""))
            if not nid:
                continue
            base = Path(source_file).name if source_file else ""
            # The file node is the record whose label is the bare filename.
            if base and label == base:
                self.by_filename.setdefault(base, nid)
            sym = _normalize_symbol(label)
            if sym and sym != base:
                self.by_symbol.setdefault(sym, set()).add(nid)

    def resolve(self, token: str) -> str | None:
        """Resolve one doc token to a unique code node id, or None."""
        t = _normalize_symbol(token)
        if not t:
            return None
        base = t.split("/")[-1]
        if base in self.by_filename:
            return self.by_filename[base]
        sym = t.split(".")[-1]  # qualified `Storage.write` → `write`
        ids = self.by_symbol.get(sym)
        if ids and len(ids) == 1:
            return next(iter(ids))
        return None


def scan_doc_references(text: str, index: _MatchIndex) -> set[str]:
    """Return the set of code node ids literally referenced in a doc's text."""
    hits: set[str] = set()
    # Backtick-quoted spans are explicit code references — trust them most.
    for span in _BACKTICK_RE.findall(text):
        nid = index.resolve(span)
        if nid:
            hits.add(nid)
    # Bare filename mentions (e.g. storage.py) and code-ish identifiers.
    for token in _FILENAME_RE.findall(text):
        nid = index.resolve(token)
        if nid:
            hits.add(nid)
    for token in _CODEISH_RE.findall(text):
        nid = index.resolve(token)
        if nid:
            hits.add(nid)
    return hits


def synthesize_doc_links(
    doc_files: list[Path], records: list[dict], root: Path, *, match_code: bool = False
) -> tuple[list[dict], list[dict]]:
    """Create one `document` node per doc file, plus — only when ``match_code`` is set —
    deterministic `references` edges to code from literal mentions.

    The doc→code literal matcher is **opt-in (off by default)**: it can produce
    false-positive bridges, and the intended primary doc→code mechanism is the (future)
    LLM concept pass. With ``match_code=False`` this returns doc-file nodes only.

    Returns (nodes, edges). Edge `_origin` is "link" so the synthesized layer is
    distinguishable from AST/LLM provenance. No new code nodes are ever created.
    """
    from graphify.extract import _file_node_id  # local import: avoid heavy import at module load

    index = _MatchIndex(records)
    nodes: list[dict] = []
    edges: list[dict] = []
    for path in doc_files:
        try:
            rel = path.resolve().relative_to(root.resolve())
        except ValueError:
            rel = Path(path.name)
        doc_nid = _file_node_id(rel)
        nodes.append({
            "id": doc_nid,
            "label": path.name,
            "file_type": "document",
            "source_file": str(rel),
            "source_location": None,
            "_origin": "link",
        })
        if not match_code:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for code_id in sorted(scan_doc_references(text, index)):
            edges.append({
                "source": doc_nid,
                "target": code_id,
                "relation": "references",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "source_file": str(rel),
                "source_location": None,
                "weight": 1.0,
                "_origin": "link",
            })
    return nodes, edges


def synthesize_doc_containers(G: nx.Graph, weight: float = 0.1) -> int:
    """Gap 1+2: give documents a file node and a `contains` hierarchy over their own
    extracted entities.

    For each doc `source_file` present in the graph (concept/rationale nodes from
    semantic extraction), synthesize one ``document`` node and add a ``contains`` edge
    from it to every node from that file. Mutates G in place; returns the number of
    document nodes added.

    Run **after** ``build_from_json`` and **before** ``cluster()`` so the hierarchy is
    reflected in community detection. ``weight`` defaults to 0.1 — the edge exists for
    traversal (Gap 2) but stays near-neutral for clustering, so doc concepts can still
    gravitate to the code they describe rather than re-forming a doc-only island.
    See docs/doc-code-graph-gaps.md (Gap 1+2) and docs/doc-code-linking-design.md.
    """
    from graphify.extract import _file_node_id  # local: avoid heavy import at module load

    by_file: dict[str, list[str]] = {}
    for nid, attrs in G.nodes(data=True):
        sf = attrs.get("source_file") or ""
        if sf and Path(sf).suffix.lower() in _DOC_EXTENSIONS:
            by_file.setdefault(sf, []).append(nid)

    added = 0
    for sf, members in by_file.items():
        rel = Path(sf)
        doc_nid = _file_node_id(rel)
        if doc_nid not in G:
            G.add_node(
                doc_nid,
                label=rel.name,
                file_type="document",
                source_file=str(rel),
                source_location=None,
                _origin="link",
            )
            added += 1
        for member in members:
            if member == doc_nid or G.has_edge(doc_nid, member):
                continue
            G.add_edge(
                doc_nid,
                member,
                relation="contains",
                confidence="EXTRACTED",
                confidence_score=1.0,
                source_file=str(rel),
                source_location=None,
                weight=weight,
                _origin="link",
            )
    return added


# --- LLM concept→code linking (code-aware, edge-only) --------------------------

LINK_RELATIONS = ("specifies", "motivates", "describes")

_LINK_SYSTEM = """\
You connect documentation concepts to the code they describe. You are given DOC CONCEPTS
(already extracted) and CODE NODES (the real code graph). Output EDGES ONLY.

HARD RULES:
- Never create or invent a node. Output edges only.
- An edge "target" MUST be an id copied verbatim from CODE NODES. If a concept refers to
  code not in CODE NODES, skip it.
- Link only when the concept clearly refers to THAT specific entity. Use signature + doc to
  disambiguate same-named functions.
- A concept may link to zero, one, or several code nodes. No edge is a valid answer.
- When two targets are equally plausible and you cannot decide, mark the edge AMBIGUOUS.

Choose the relation — the most specific that applies, in priority order:
  specifies — the doc states a requirement/spec/rule the code must satisfy.   [code implements doc]
  motivates — the doc explains WHY the code is the way it is (rationale, trade-off, risk).
  describes — the doc explains what existing code is/does (no requirement, no rationale).

Output JSON only, no prose:
{"edges":[{"source":"<concept id>","target":"<code id, verbatim>",
  "relation":"specifies|motivates|describes","confidence":"EXTRACTED|INFERRED|AMBIGUOUS",
  "confidence_score":0.0}]}
confidence_score (never 0.5): EXTRACTED 1.0 · INFERRED 0.85 or 0.65 · AMBIGUOUS 0.2
"""


def concept_description(attrs: dict) -> str:
    """Grounding text for a concept node: its label plus any rationale attribute."""
    label = str(attrs.get("label", "")).strip()
    rationale = str(attrs.get("rationale", "")).strip()
    return f"{label} — {rationale}" if rationale else label


def _manifest_for_prompt(records: list[dict]) -> list[dict]:
    out = []
    for r in records:
        item = {"id": r.get("id"), "label": r.get("label"), "file": r.get("source_file")}
        if r.get("signature"):
            item["signature"] = r["signature"]
        if r.get("doc"):
            item["doc"] = r["doc"]
        out.append(item)
    return out


def build_concept_link_prompt(concepts: list[dict], records: list[dict]) -> str:
    """Assemble the single-call prompt: system rules + DOC CONCEPTS + CODE NODES."""
    return (
        _LINK_SYSTEM
        + "\nDOC CONCEPTS:\n"
        + json.dumps(concepts, ensure_ascii=False)
        + "\n\nCODE NODES (link targets — copy ids verbatim):\n"
        + json.dumps(_manifest_for_prompt(records), ensure_ascii=False)
        + "\n"
    )


def _parse_edges_json(text: str) -> list[dict]:
    """Parse the model reply into an edge list, tolerating code fences / preamble."""
    if not text:
        return []
    s = text.strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1] if "```" in s[3:] else s
        s = s.lstrip("json").strip("`").strip()
    try:
        obj = json.loads(s)
    except Exception:
        start, end = s.find("{"), s.rfind("}")
        if start == -1 or end <= start:
            return []
        try:
            obj = json.loads(s[start : end + 1])
        except Exception:
            return []
    edges = obj.get("edges") if isinstance(obj, dict) else None
    return edges if isinstance(edges, list) else []


def link_concepts_to_code(
    concepts: list[dict],
    records: list[dict],
    *,
    backend: str,
    model: str | None = None,
) -> list[dict]:
    """Ask the LLM to link doc concepts to real code nodes; return validated edges.

    ``concepts`` are ``{id, label, description}`` dicts (the residual the deterministic
    matcher didn't resolve). ``records`` is the code manifest (the only allowed targets).
    Edges whose source/target/relation are not valid are dropped — the boundary rule is
    *enforced* here, not merely requested in the prompt. See docs/doc-code-linking-design.md.
    """
    if not concepts or not records:
        return []
    from graphify.llm import _call_llm

    prompt = build_concept_link_prompt(concepts, records)
    reply = _call_llm(prompt, backend=backend, model=model, max_tokens=4096)
    raw = _parse_edges_json(reply)

    valid_concept_ids = {c.get("id") for c in concepts}
    valid_code_ids = {r.get("id") for r in records}
    edges: list[dict] = []
    seen: set[tuple] = set()
    for e in raw:
        if not isinstance(e, dict):
            continue
        src, tgt, rel = e.get("source"), e.get("target"), e.get("relation")
        if src not in valid_concept_ids or tgt not in valid_code_ids or rel not in LINK_RELATIONS:
            continue
        key = (src, tgt, rel)
        if key in seen:
            continue
        seen.add(key)
        edges.append({
            "source": src,
            "target": tgt,
            "relation": rel,
            "confidence": e.get("confidence", "INFERRED"),
            "confidence_score": e.get("confidence_score", 0.65),
            "source_location": None,
            "weight": 1.0,
            "_origin": "link",
        })
    return edges


def _find_doc_files(target_root: Path) -> list[Path]:
    """Detect doc files under target_root, reusing graphify's classifier."""
    from graphify.detect import detect

    detection = detect(target_root)
    files_by_type = detection.get("files", {})
    out: list[Path] = []
    for kind in ("document", "paper"):
        for p in files_by_type.get(kind, []):
            path = Path(p)
            if path.suffix.lower() in _DOC_EXTENSIONS:
                out.append(path)
    return out


def load_or_extract_doc_concepts(
    doc_files: list[Path],
    *,
    cache_root: Path,
    extract_root: Path,
    backend: str | None = None,
    model: str | None = None,
) -> tuple[list[dict], list[dict], list[dict], dict]:
    """Cache-first doc concept extraction.

    For each doc file, reuse a cached semantic extraction when one exists; otherwise
    run the semantic LLM pass (``backend`` required) and write the result to cache.
    Returns ``(nodes, edges, hyperedges, info)``. With no ``backend``, uncached docs are
    left unextracted (their count is reported in ``info['skipped_uncached']``) rather than
    failing — cached docs and doc-file synthesis still proceed.
    """
    from graphify.cache import check_semantic_cache, save_semantic_cache

    info = {
        "cache_hits": 0, "cache_misses": 0, "extracted": 0, "skipped_uncached": 0,
        "input_tokens": 0, "output_tokens": 0,
    }
    paths = [str(p) for p in doc_files]
    if not paths:
        return [], [], [], info

    nodes, edges, hyper, uncached = check_semantic_cache(paths, root=cache_root)
    info["cache_hits"] = len(paths) - len(uncached)
    info["cache_misses"] = len(uncached)
    if not uncached:
        return nodes, edges, hyper, info

    if backend is None:
        info["skipped_uncached"] = len(uncached)
        return nodes, edges, hyper, info

    from graphify.llm import extract_corpus_parallel

    fresh = extract_corpus_parallel(
        [Path(p) for p in uncached], backend=backend, model=model, root=extract_root
    )
    try:
        save_semantic_cache(
            fresh.get("nodes", []), fresh.get("edges", []), fresh.get("hyperedges", []),
            root=cache_root,
        )
    except Exception:
        pass  # cache write is best-effort; never block the link pass on it
    info["extracted"] = len(uncached)
    info["input_tokens"] = fresh.get("input_tokens", 0)
    info["output_tokens"] = fresh.get("output_tokens", 0)
    return (
        nodes + fresh.get("nodes", []),
        edges + fresh.get("edges", []),
        hyper + fresh.get("hyperedges", []),
        info,
    )


def apply_doc_links(
    graphify_out: str | Path,
    target_root: str | Path,
    *,
    match_code: bool = False,
    link_code: bool = False,
    backend: str | None = None,
    model: str | None = None,
) -> dict:
    """Link-docs pass: ensure doc concepts, build the doc hierarchy, optionally link to
    code, then merge + re-cluster.

    Steps: (1) cache-first doc concept extraction (cached → reuse, else LLM-extract);
    (2) synthesize a ``document`` node per doc file; (3) optional deterministic doc→code
    ``references`` edges (``match_code``); (4) build the graph, add the Gap 1+2 ``contains``
    hierarchy over the concepts, re-cluster, and write ``graph.json``. Returns a summary.

    ``match_code`` (default False) is opt-in — literal matching can produce false-positive
    bridges. See docs/doc-code-linking-design.md.
    """
    graphify_out = Path(graphify_out)
    target_root = Path(target_root)
    graph_path = graphify_out / "graph.json"
    manifest_path = graphify_out / MANIFEST_FILENAME
    if not graph_path.exists():
        raise FileNotFoundError(f"no graph.json at {graph_path} — run `graphify extract --code-only` first")
    if not manifest_path.exists():
        raise FileNotFoundError(f"no {MANIFEST_FILENAME} at {manifest_path} — run `graphify extract --code-only` first")

    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    existing_edges = graph.get("edges", graph.get("links", []))
    existing_by_id = {n.get("id"): n for n in graph.get("nodes", []) if isinstance(n, dict)}
    records = load_manifest(manifest_path)
    doc_files = _find_doc_files(target_root)

    # 1. cache-first doc concepts (the doc's extracted entities).
    concept_nodes, concept_edges, _concept_hyper, info = load_or_extract_doc_concepts(
        doc_files,
        cache_root=graphify_out.parent,
        extract_root=target_root,
        backend=backend,
        model=model,
    )
    # 2. one document file node per doc file (+ optional doc→code reference edges).
    doc_nodes, doc_edges = synthesize_doc_links(
        doc_files, records, target_root, match_code=match_code
    )

    # Assemble merged nodes with dedup + collision safety net: a synthesized/extracted
    # node must never shadow an existing CODE node id (the "no new code nodes" rule).
    seen_ids = set(existing_by_id)
    merged_nodes = list(graph.get("nodes", []))
    concept_added = dropped = docnode_added = 0
    for n in concept_nodes:
        nid = n.get("id")
        if not nid or nid in seen_ids:
            continue
        merged_nodes.append(n); seen_ids.add(nid); concept_added += 1
    for n in doc_nodes:
        nid = n["id"]
        clash = existing_by_id.get(nid)
        if clash is not None and clash.get("file_type") == "code":
            dropped += 1
            continue
        if nid in seen_ids:
            continue
        merged_nodes.append(n); seen_ids.add(nid); docnode_added += 1

    # Merge edges, deduped; keep only edges whose endpoints exist.
    seen_edges = {(e.get("source"), e.get("target"), e.get("relation")) for e in existing_edges}
    merged_edges = list(existing_edges)
    concept_edge_added = ref_added = 0
    for e in concept_edges:
        key = (e.get("source"), e.get("target"), e.get("relation"))
        if key in seen_edges:
            continue
        if e.get("source") in seen_ids and e.get("target") in seen_ids:
            merged_edges.append(e); seen_edges.add(key); concept_edge_added += 1
    for e in doc_edges:
        key = (e["source"], e["target"], e["relation"])
        if key in seen_edges:
            continue
        # Guard BOTH endpoints (like the concept/LLM loops below): a stale or
        # mismatched code-manifest.jsonl can name a target symbol that is not in
        # the graph, which build_from_json silently drops — counting it here
        # would report a doc→code edge that never persists.
        if e["source"] in seen_ids and e["target"] in seen_ids:
            merged_edges.append(e); seen_edges.add(key); ref_added += 1

    # LLM concept→code linking (code-aware, edge-only) on the residual: doc concepts not
    # already linked by the deterministic matcher. Opt-in via link_code + a backend.
    link_edge_added = 0
    if link_code and backend:
        node_by_id = {n.get("id"): n for n in merged_nodes if isinstance(n, dict)}
        already_linked = {
            e.get("source") for e in merged_edges if e.get("relation") in LINK_RELATIONS
        }
        residual = [
            {"id": nid, "label": n.get("label", ""), "description": concept_description(n)}
            for nid, n in node_by_id.items()
            if n.get("file_type") in ("concept", "rationale")
            and Path(n.get("source_file") or "").suffix.lower() in _DOC_EXTENSIONS
            and nid not in already_linked
        ]
        if residual:
            try:
                llm_edges = link_concepts_to_code(
                    residual, records, backend=backend, model=model
                )
            except Exception as exc:  # never let the LLM bridge abort the pass
                print(f"[graphify link-docs] warning: concept→code linking failed: {exc}", file=sys.stderr)
                llm_edges = []
            for e in llm_edges:
                key = (e["source"], e["target"], e["relation"])
                if key in seen_edges or e["source"] not in seen_ids or e["target"] not in seen_ids:
                    continue
                merged_edges.append(e); seen_edges.add(key); link_edge_added += 1

    merged = {"nodes": merged_nodes, "edges": merged_edges}

    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.export import to_json, backup_if_protected

    G = build_from_json(merged, root=target_root)
    # 3. Gap 1+2: contains hierarchy over the now-present doc concepts, before clustering.
    synthesize_doc_containers(G)
    communities = cluster(G)
    score_all(G, communities)
    backup_if_protected(graphify_out)
    to_json(G, communities, str(graph_path), force=True)

    return {
        "doc_files": len(doc_files),
        "concept_nodes_added": concept_added,
        "doc_nodes_added": docnode_added,
        "reference_edges_added": ref_added,
        "link_edges_added": link_edge_added,
        "dropped_collisions": dropped,
        "communities": len(communities),
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        **info,
    }

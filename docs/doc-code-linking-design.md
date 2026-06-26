# Design: code-first, code-aware doc↔code linking

**Status:** Partially implemented — deterministic pipeline landed; LLM concept pass pending
**Date:** 2026-06-25

## Implementation status

Two **distinct, complementary** deterministic mechanisms now exist — don't conflate them:

- **Gap 1+2 — `contains` hierarchy (within a doc).** On a *full* extract (doc concepts
  already present), group each doc's own extracted `concept`/`rationale` entities under a
  synthesized `document` node via `contains` edges. Runs at the build→cluster seam.
- **Gap 3 (partial) — literal-mention bridges (doc→code).** On a `--code-only` graph +
  manifest, scan doc text for literal code references and emit `references` edges to real
  code nodes. Runs as `graphify link-docs --match-code`. **Opt-in / off by default** — literal
  matching can produce false-positive bridges, and the intended *primary* doc→code mechanism
  is the LLM concept pass; the deterministic matcher is a supplementary opt-in. Plain
  `graphify link-docs` (no flag) synthesizes the doc-file nodes but adds no doc→code edges.

| Piece | State | Where |
|---|---|---|
| `graphify extract --code-only` | **done** | `__main__.py` (extract cmd); skips semantic extraction, no API key |
| code-manifest emitter (`code-manifest.jsonl`) | **done** | `link.py` `write_manifest` / `iter_manifest_records`; signature via source slice, `doc` via `rationale_for` (Python) |
| **Gap 1+2** doc-file node + `contains` (weight **0.1**) over a doc's own entities | **done, default-on** | `link.py` `synthesize_doc_containers`; wired into extract at the build→cluster seam |
| **Gap 3 (partial)** `link-docs` — literal-mention doc→code `references` edges | **done, opt-in** | `link.py` `synthesize_doc_links` / `_MatchIndex`; **off by default**, enable with `link-docs --match-code` |
| `link-docs` — **cache-first doc concept pass** (reuse cached semantic extraction, else LLM-extract) | **done** | `link.py` `load_or_extract_doc_concepts`; merged + contains-hierarchied in `apply_doc_links` |
| `link-docs` — merge + re-cluster + collision safety net | **done** | `link.py` `apply_doc_links` |
| `link-docs` — **LLM concept→code linking** (code-aware, edge-only, validated) | **done, opt-in** | `link.py` `link_concepts_to_code`; **off by default**, enable with `link-docs --link-code`; relations `describes`/`specifies`/`motivates` |
| Non-Python doc-comment extraction | **deferred** | see "Deferred" |

**Concept→code linking verified with a real model** (`worked/example` + `kimi`): +36 concept→code
edges, **0 invalid targets** (return-validation enforces the boundary rule), relations 24
`describes` / 12 `motivates`. Doc-side mirror nodes get *bridged* — `API Module (api.py)`
(concept) → `api.py` (code) — and semantic concepts the matcher cannot resolve get linked
(`Document Pipeline` → `handle_upload()`). Failures (missing backend pkg/key) warn and continue,
never abort. Tests: `test_link_concepts_to_code_validates_targets`,
`test_link_docs_link_code_adds_concept_to_code_edges` (both mock the LLM).

**Cache-first concept loading:** `link-docs` ensures the doc concepts exist before building
the hierarchy — for each doc it reuses a cached semantic extraction when present, otherwise
runs the semantic LLM pass (`--backend`/auto-detected) and writes the result to cache. Cached
docs (and a code-only re-run) need no API key; uncached docs without a backend are reported and
skipped, not fatal. Verified on `worked/example` (with its cache copied in): code-only → 73
nodes; `link-docs` → 2 docs cached + 1 extracted, +23 concept nodes, +3 document nodes, +23
`contains` edges, re-clustered. **Note:** this currently reuses the *existing* semantic
extraction, which still mints the doc-side mirror nodes — the **code-aware grounding** that
points concepts at real code nodes is the pending refinement (the manifest is already emitted
for it).

**Weight decision:** `contains` edges use **0.1** (not 1.0). The weight affects clustering
only — traversal (Gap 2's goal) works at any weight because the edge exists. 0.1 keeps the
hierarchy near-neutral so doc concepts can gravitate to the code they describe instead of
re-forming the doc-only island the gaps doc diagnosed.

Verified on `worked/example` (the gaps-doc corpus):
- `synthesize_doc_containers` on the existing full graph → **0→2 `document` nodes, +23
  `contains` edges @0.1** (`architecture` owns 17 entities, `notes` owns 6) where the gaps
  doc measured **0** doc `contains` edges.
- `--code-only` → 37-symbol manifest, pure code+rationale graph; `link-docs` → +3 `document`
  nodes and +28 doc→code `references` edges (gaps doc measured **0** doc↔code edges).

Tests: `tests/test_link.py`,
`tests/test_extract_cli.py::test_extract_code_only_skips_llm_and_writes_manifest`.


**Builds on:** [`doc-code-graph-gaps.md`](./doc-code-graph-gaps.md) (the problem) and
`THREE_LAYER_KB_SPEC.md` (the L2/L3 target).

---

## Problem (recap)

When graphify ingests code + prose, the two halves come out as disconnected islands.
The doc-extraction LLM runs **blind** — it is never told what the real code nodes are — so
it mints its own *mirror* concept nodes (`raw_architecture_storage_module`,
`file_type: concept`) instead of pointing at the real AST node (`raw_storage`,
`file_type: code`). Every doc→code reference lands doc→doc. See `doc-code-graph-gaps.md`
Gap 3 for the verified evidence.

## Core idea

Invert the order: **build the code graph first, then do doc linking *code-aware*.** Hand the
LLM the real code nodes (as a structured manifest) so its references can target actual node
IDs. The LLM's job becomes **matching**, never **describing** or **inventing** code nodes.

This is a two-step pipeline on two cadences (matches `THREE_LAYER_KB_SPEC.md` §9):

```
Step 1 (cheap, deterministic, per-commit):
  graphify extract <path> --code-only
    → AST extract → build → cluster → graph.json (+ wiki, + node manifest)   [no API key]

Step 2 (LLM, scoped, on docs/** change):
  graphify link-docs <path>
    → docs + code-manifest → deterministic match, then LLM on the residual
    → emits doc→code edges → build_merge → re-cluster                        [LLM]
```

`link-docs` is **one pass** over the docs, not several commands. The manifest from Step 1 is
its shared input — used both to resolve literal mentions (b) and as the LLM's target list (c):

```
graphify link-docs <path>   (manifest from Step 1 as input)
  a. synthesize doc-file nodes + `contains`        — Gap 1/2, deterministic, no LLM
  b. deterministic matcher: literal file/symbol mentions → edges   — uses manifest
  c. LLM: concept extraction + concept→code links on the RESIDUAL  — manifest as grounding;
        the edges from (b) are handed in as "already linked" so tokens go only to the
        genuinely ambiguous/conceptual references
  d. collision check → build_merge → re-cluster
```

## Agreed decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Gap 3 model** | Keep the doc concept node **separate**; add a **bridge edge** (`documents`/`describes`) to the real code node. | Preserves the doc's mental model *and* enables cross-layer ("where doc meets code") queries — the spec's reason to exist. NOT a merge. |
| **L2 storage** | **Single `graph.json`** + provenance tags (`file_type`, `_origin`), links as tagged edges. | Far less pipeline change than the spec's three-file split; still supports layer-scoped / bridge / cross-layer queries. |
| **What the LLM is fed** | A structured **code-node manifest** (id, label, file, line, signature, doc), **not the prose wiki**. | The wiki is narrative for humans — token-heavy and lossy for grounding. The model needs exact IDs to target, or it re-creates ghost duplicates. |
| **Linking method** | **Deterministic match first**, LLM only on the **residual**. | Filename-labeled mirrors (`Storage Module (storage.py)` → regex `(\w+\.\w+)`) resolve for free; the LLM handles only the semantic references. |
| **Signature source** | Deterministic — **AST / `file_slice` byte text**, never the LLM. Derived **lazily at manifest time** (function/method nodes only). | The tree-sitter parse already has it (`extract.py:3115+` grabs `parameters`/`return_type`). Keeps `graph.json` lean and the code graph unchanged. |
| **Function "purpose" grounding** | **Python docstrings now** (already in the graph as `rationale` nodes via `rationale_for`); other languages **later**. | Lets the LLM know *what a function is*, not just its shape. Python coverage is free today; non-Python degrades to `label + signature` gracefully. |
| **LLM role** | **Match only.** Never generate stored descriptions. `source_location` is an escape hatch so the LLM can read a body on demand for hard cases. | Avoids paying to summarize the whole repo; pays for comprehension only on the residual that needs it. |
| **Where the logic lives** | A post-build pass (new `link.py`), **not** in `extract.py`. | `extract.py` stays the pure, deterministic, LLM-free AST engine. Linking is a graph-level concern. |

## Code-manifest

A **derived view** of the code graph — *not* a second extraction. It is a pure projection of
`graph.json` (+ `file_slice` for `signature`, + `rationale_for` for `doc`), stripped of
edges/communities/stub noise: the matcher's lookup table and the LLM's allowed-target list in
one.

**It is emitted as a file by `--code-only` (Step 1) and read back by `link-docs` (Step 2).**

- **Path:** `graphify-out/code-manifest.jsonl` (alongside `graph.json`).
- **Format: JSONL** — one record per line; streams, and chunks by community for large repos.
  The full `graph.json` is *not* fed to the LLM (too large, edge/cluster noise).
- `--code-only` builds it right after `build`/`cluster`, from the graph it just produced.
- `link-docs` consumes the file directly (no re-derivation) — and the subagent linking path
  hands the same file to the linker subagent.
- Because the code graph and manifest are written together by the same `--code-only` run, they
  stay consistent; an incremental code update re-emits both.

The builder is a shared helper in `link.py`, called by `--code-only` to write the file.

### Record shape

One record per code symbol:

```
id              # canonical AST node id — the edge target
label           # symbol name
source_file     # file path
source_location # e.g. "L42" — also the escape hatch for on-demand body reads
signature?      # function/method nodes only; sliced via file_slice; all languages
doc?            # Python only for now: text of the rationale node reached via rationale_for
```

- `signature` / `doc` are **optional** — omit rather than fabricate when unavailable.
- Non-Python functions ship as `label + signature` (no `doc`); still enough to match common
  cases and to drill in via `source_location`.
- When deterministic doc-comment extraction is later added for other languages (emitting
  `rationale` nodes like Python does), the manifest builder needs **no change** — it already
  follows `rationale_for`.

## Linker output (Step 2)

A pure edge list, merged via `build_merge` (no code-graph rewrite):

```json
{ "source": "<doc concept node id>", "target": "<code node id from manifest>",
  "relation": "documents", "confidence": "EXTRACTED|INFERRED", "confidence_score": 1.0,
  "_origin": "link" }
```

Linker boundary rule (prevents regression to ghost mirrors):
**concept nodes allowed · new *code* nodes forbidden · cross-layer targets MUST be a manifest id.**

## Concept→code linking (LLM, code-aware) — task #4

With concepts now loaded cache-first, the LLM step is **edge-only linking, not re-extraction**:
feed it the *existing* doc concepts + the code manifest and ask only for edges. This reuses the
cache, costs less, and *bridges* the doc-side mirror nodes (`Storage Module (storage.py)`) to
the real code node — consistent with the "keep separate node + bridge edge" decision. It runs on
the **residual** — concepts the deterministic `--match-code` matcher could not resolve.

### Relation ontology (doc-concept → code, single canonical direction)

| Relation | doc→code meaning | inverse (code-side reading) | Source |
|---|---|---|---|
| `references` | doc *file* literally mentions this code | mentioned-by | deterministic matcher |
| `describes` | doc concept **explains** existing code | described-by | LLM linker |
| `specifies` | doc concept is a **spec/requirement** the code realizes | **implements** | LLM linker |
| `motivates` | doc rationale is the **why** behind the code | motivated-by | LLM linker |

All anchored doc-concept→code (per the spec's "store one direction, backlinks give the inverse"
rule); "code implements the spec" is the backlink of `specifies`. Kept deliberately small —
`constrains`/`illustrates`/`deprecates` fold into these or are dropped (the spec warns
over-granular ontologies collapse into noise). Extend only when a real query need appears.

### Prompt (single-call, via `llm._call_llm`)

System + task in one prompt; output is strict JSON edges. Hard rules carry the design:

```
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

Choose the relation — most specific that applies, in priority order:
  specifies — the doc states a requirement/spec/rule the code must satisfy.   [code implements doc]
  motivates — the doc explains WHY the code is the way it is (rationale, trade-off, risk).
  describes — the doc explains what existing code is/does (no requirement, no rationale).

DOC CONCEPTS: [{"id","label","description"}]   # description = label + rationale text
CODE NODES:   [{"id","label","file","signature","doc"}]   # link targets, copy ids verbatim

Output JSON only:
{"edges":[{"source":"<concept id>","target":"<code id, verbatim>",
  "relation":"specifies|motivates|describes","confidence":"EXTRACTED|INFERRED|AMBIGUOUS",
  "confidence_score":0.0}]}
confidence_score rubric (never 0.5): EXTRACTED 1.0 · INFERRED 0.85 / 0.65 · AMBIGUOUS 0.2
```

### Return validation (enforces the guardrail, not just requests it)

After the call, **drop any edge** whose `target` is not a real manifest id, whose `source` is
not a real concept id, or whose `relation` is outside the enum. Tag survivors `_origin: "link"`.
Token control: include the full manifest under a budget; above it, pre-filter CODE NODES to the
files the deterministic matcher already hit for that doc + community neighbors. Gated behind
`link-docs --link-code` (off by default — costs tokens), paralleling `--match-code`.

## Insertion points in the existing pipeline

- **`--code-only` flag** on `graphify extract` (`__main__.py` arg loop ~`4192–4256`): force
  `semantic_files = []` so the `needs_llm` branch is skipped — pure AST + cluster, no key.
  (Today the only ways to get this are `--exclude '*.md' …` or the `update` command.)
- **Link pass** runs **after `_build` / before `_cluster`** (`__main__.py:4696→4706`), and must
  also be wired into the **incremental `_build_merge`** branch and the **`--no-cluster`**
  branch (`~4629`) so it is never silently skipped.
- Re-clustering after merge is required so bridge edges influence community detection (the
  whole point of the gaps doc — pull the doc cluster next to the code it describes).

**No ghost-merge problem (unlike the old single-pass design).** Because extraction is now
**staged** — code-only first, docs linked separately — and the linker is code-aware, the
mirror-node collision the old blind pass produced cannot occur:
- Step 1's graph contains no doc nodes, so there is nothing to collapse.
- Step 2's LLM is forbidden from minting code nodes; it emits genuine doc `concept` nodes
  + edges to real code IDs. A genuine concept node does not share a code node's
  `(basename, label)` key, so the `build.py:207+` ghost-merge never matches it.

No exemption in `build.py` is needed. The only safety net required is cheap and lives in the
linker: **reject (or re-slug) any emitted node whose id collides with an existing code node id**
— enforcing the "new code nodes forbidden" boundary rule at merge time.

## Why this aligns with the existing codebase

- `THREE_LAYER_KB_SPEC.md` §5.1's "deterministic code-graph hook, no LLM" **already exists** as
  `graphify update` / `watch._rebuild_code`. `--code-only` is the from-scratch sibling.
- §5.3's "subagent fed the code graph's node list (ids + labels), emit edges only" is exactly
  the Step-2 manifest approach.
- The two cadences (cheap code refresh vs scoped doc-link) map onto two existing commands.

## Consuming the bridges (explain + query)

The doc↔code edges are only worth minting if retrieval *surfaces* them. Both
read commands are now layer-aware, keyed off the same relation buckets so the
two stay consistent:

- **`explain <symbol>`** (`__main__.py` ~3142) groups a node's connections into
  **Why / rationale** (`motivates`, `rationale_for`, `caused_by`), **Documentation**
  (`describes`, `specifies`, `references`, `documents`, plus `contains` into a
  `document` node), and **Code** (everything else). The rationale that explains
  *why* a symbol exists is low-degree, so the old flat degree-sort buried it
  (position 8/9 on `save_parsed`); it now leads under its own header.
- **`query "<question>"`** (`serve.py` `_intent_relations` → `_subgraph_to_text`)
  infers intent from question wording ("why/rationale/purpose" ⇒ the Why
  relations; "documented/spec/describe" ⇒ the Doc relations) and **promotes the
  matching edges and the non-seed nodes they touch ahead of the degree-sorted
  bulk**, so an intent-relevant bridge survives the token-budget truncation
  instead of being cut as a low-degree leaf. A neutral query (a bare symbol)
  triggers no boosting and the ranking is byte-identical to before. The header
  reports the detected intent (`Intent: why (promoting motivates, …)`).

  Verified on `worked/example`: `query "why does save_parsed exist"` leads with
  `save_parsed --motivates--> Transactional Write Risk` and renders the
  rationale node in the top group; the neutral `query "save_parsed"` keeps
  `calls`/`contains` first with that same `motivates` edge demoted to ~position 8.
  Tests: `tests/test_serve.py::test_intent_relations_detects_why_and_doc`,
  `::test_subgraph_boost_promotes_rationale_node_and_edge`,
  `::test_query_graph_text_reports_intent_in_header`;
  `tests/test_explain_cli.py::test_explain_groups_doc_bridges_by_intent`.

- **`query --context doc|code`** (`serve.py` `_split_layer_filters` →
  `_apply_layer_filter`) — directed cross-layer retrieval. The same `--context`
  flag that prunes edges by AST context (`call`/`import`/…) also accepts two
  **layer** values; these are split out and applied as a *node* filter **after**
  traversal (the edge-context filter runs before BFS, so the two compose
  cleanly). `doc` keeps `file_type ∈ {document, concept, rationale}`; `code`
  keeps `file_type == code`. The **seed always survives** so the anchor shows
  even when it is the opposite layer — that is what makes the two directed
  helpers work:
  - `query "save_parsed" --context doc` ⇒ "docs for X": the seed plus the
    docstring (`rationale_for`), the doc concepts that `describe`/`motivate` it,
    and the `document` files that `contain`/`reference` it — every code neighbour
    stripped.
  - `query "<concept>" --context code` ⇒ "code for Y": the doc concept seed plus
    only the real code symbols it maps to.

  Layer values: `doc`/`docs`/`document`/`documentation`/`concept`/`spec`/
  `rationale` → doc; `code`/`implementation`/`impl`/`source` → code. The header
  reports `Layer: doc`. Filtering is **explicit-only** (no NL auto-restriction) —
  free-text intent gets the gentler ranking boost above, not a hard cut. Tests:
  `tests/test_serve.py::test_split_layer_filters_partitions_values`,
  `::test_query_layer_doc_keeps_only_doc_nodes_plus_seed`,
  `::test_query_layer_code_keeps_only_code_nodes_plus_seed`,
  `::test_query_layer_and_edge_context_compose`.

## Deferred / later

- Deterministic leading-doc-comment extraction for non-Python (JSDoc, `///`, Go doc comments)
  → emit as `rationale` nodes so the manifest's `doc` field fills in automatically.
- L3 (Obsidian) frontmatter schema, cache/original split, hash-staleness, gardening — separate
  subsystem per `THREE_LAYER_KB_SPEC.md` §7–10; `export.to_obsidian` is scaffolding only.

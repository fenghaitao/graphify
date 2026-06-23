# Gap: Documents and code are disconnected in the graph

**Status:** Open — documented, not yet fixed
**Found:** 2026-06-25, on `worked/example/` (5 `.py` modules + `architecture.md` + `notes.md`)
**Scope:** how AST extraction and semantic (doc) extraction produce structurally incompatible subgraphs.

---

## Summary

When graphify ingests a mixed corpus of code and prose, the two halves come out as
**two disconnected islands**. Code files get a file node and a containment hierarchy;
documents get only loose concept nodes; and the documentation's *references to the code
never land on the actual code nodes*. Three concrete gaps, in increasing severity:

1. **No file node for documents** — a `.md` file is not represented as a node.
2. **No `contains` hierarchy for documents** — doc concepts have no structural parent.
3. **No doc↔code edges at all** — the documentation layer never structurally touches
   the code it describes.

All three were verified on the `worked/example` graph (96 nodes, 150 edges, 7 communities).

---

## Gap 1 — Documents have no file node

Code files produce a module node; documents produce nothing for the file itself.

| | Code (`.py`) | Docs (`.md`) |
|---|---|---|
| File node in graph? | yes — e.g. `raw_parser` (`file_type: code`) | **none** |
| `file_type` counts in example | `code: 38` | `document: 0` (only `concept: 17`, `rationale: 41`) |

The only link from a doc concept back to its file is the flat `source_file` **attribute**
(e.g. `source_file: "architecture.md"`), which is metadata, not a traversable edge.

**Root cause.** Code goes through `graphify.extract` (AST), which deterministically emits
a module node per file. Docs go through the semantic subagent, whose prompt
(`references/extraction-spec.md`) says *"Only create a node for something that is itself a
named entity or concept."* — it is never told to emit a node for the document file.

## Gap 2 — Documents have no `contains` hierarchy

AST emits `module --contains--> function` edges (32 of them in the example). Documents emit
none: their concept/rationale nodes float free, with no structural parent grouping them by
source file.

| | Code | Docs |
|---|---|---|
| `contains` edges file→children | 32 | **0** |

Consequence: there is no way to traverse "everything `architecture.md` talks about" as a
subtree. You can only filter by the `source_file` attribute out-of-band.

## Gap 3 — No doc↔code edges (most severe)

**Zero** edges in the graph connect a doc-sourced node to a code-sourced node.

The cause is a *parallel-node* problem, not just a missing edge. When the subagent read
`architecture.md`, it minted its **own** "module concept" nodes that mirror the code but are
separate entities:

| | Doc's mirror node | Real code node |
|---|---|---|
| id | `raw_architecture_storage_module` | `raw_storage` |
| label | `Storage Module (storage.py)` | `storage.py` |
| file_type | `concept` | `code` |
| source_file | `architecture.md` | `raw/storage.py` |

Every reference the docs make — including the ones surfaced as **Surprising Connections**
in the report (`Repository Pattern → Storage Module`, `SQLite Migration → Storage Module`,
`Transactional Write Risk → Parser Module`) — points at the **doc-side mirror node**, never
at the real AST code node. They are all **doc→doc**, not doc→code.

Net effect: the graph holds the documentation's *mental model* of the architecture as a
self-contained subgraph that structurally never touches the code it describes. In community
detection this shows up as the doc cluster ("Pipeline Architecture & Design") sitting apart
from each per-module code cluster.

---

## Why this matters

- Queries that should cross the doc/code boundary (e.g. "what does the architecture doc say
  about `storage.py`?") cannot be answered by graph traversal — there is no path between the
  two nodes.
- Documents are second-class: invisible to file-level navigation, absent from the `contains`
  hierarchy, and unreachable from code.
- Fixing Gap 1/2 alone does **not** fix Gap 3: bundling doc concepts under a doc file node
  still leaves the doc's "Storage Module" concept disconnected from the real `storage.py`.

## Possible fixes (not yet implemented)

- **Gap 1 + 2** — deterministic post-build pass: synthesize one `document` node per distinct
  `.md`/`.txt` `source_file`, add `contains` edges to every node from that file. No LLM cost.
  Must run **after** `build_from_json` and **before** `cluster()` so the new nodes/edges are
  included in community detection. Algorithm itself is unchanged (Leiden/Louvain are
  graph-agnostic); clustering simply re-runs on the augmented graph. Use `contains`
  weight `1.0` for code/doc symmetry, or `0.1` to keep clustering near-neutral.
- **Gap 3** — entity-resolution / alias pass: match doc mirror nodes to code nodes by label
  (the doc labels embed the filename, e.g. `Storage Module (storage.py)`; regex `(\w+\.\w+)`).
  Then either **merge** the mirror into the code node, or add a `documents` / `describes`
  edge between them. Deterministic, no LLM needed for this corpus.

## Reproduction

```bash
cd worked/example
PY=$(cat graphify-out/.graphify_python)

# Gap 1: zero document file nodes
$PY -c "import json,collections; g=json.load(open('graphify-out/graph.json')); print(collections.Counter(n.get('file_type') for n in g['nodes']))"

# Gap 2: contains edges only exist for code
$PY -c "import json,collections; g=json.load(open('graphify-out/graph.json')); print(collections.Counter(e['relation'] for e in g['edges']))"

# Gap 3: zero doc<->code edges
$PY -c "
import json; g=json.load(open('graphify-out/graph.json')); N={n['id']:n for n in g['nodes']}
def o(i):
    s=N.get(i,{}).get('source_file') or ''
    return 'doc' if s.endswith('.md') else 'code' if s.endswith('.py') else 'other'
print(sum(1 for e in g['edges'] if {o(e['source']),o(e['target'])}=={'doc','code'}), 'doc<->code edges')
"
```

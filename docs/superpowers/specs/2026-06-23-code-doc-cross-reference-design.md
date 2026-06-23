# Code-Doc Cross-Reference Pass

**Date**: 2026-06-23
**Status**: Draft

## Problem

graphify currently merges code (AST) and doc (LLM) nodes that share the same name into a single node via ghost deduplication in `build.py`. This loses the distinction between "the code entity" and "the documented concept." Users want code and doc nodes to remain separate but connected by explicit edges.

## Design

### Current flow

```
AST extraction (code) ──┐
                         ├── build() ──→ graph (ghost dedup merges same-name nodes)
Semantic extraction (docs)┘
```

### Proposed flow

```
AST extraction (code) ──→ code entity catalog ──┐
                                                  ├── cross-reference pass (LLM) ──→ documents edges
Semantic extraction (docs) ──────────────────────┘
                                                          │
                    ┌─────────────────────────────────────┘
                    ▼
              build() ──→ graph (ghost dedup disabled for code↔doc pairs)
```

### Changes

#### 1. Code entity catalog

After AST extraction completes, produce a compact JSON catalog of all code entities. Each entry:

```json
{
  "id": "auth_session_validatetoken",
  "label": "ValidateToken",
  "kind": "function",
  "source_file": "src/auth/session.py"
}
```

Where `kind` is one of: `module`, `class`, `function`, `method`.

This catalog is the input to the cross-reference LLM pass, giving it exact node IDs to target.

#### 2. Cross-reference LLM pass

A single LLM call (or one per doc chunk, matching the existing chunking strategy) that receives:

- Doc extraction results (nodes + edges from the semantic pass)
- The code entity catalog

The LLM emits `documents` edges:

```json
{
  "source": "docs_readme_authservice",
  "target": "auth_session_validatetoken",
  "relation": "documents",
  "confidence": "INFERRED",
  "confidence_score": 0.85,
  "source_file": "docs/README.md"
}
```

Direction: doc node → code node. The doc "documents" the code entity.

Since the LLM has exact code node IDs from the catalog, edges are precise -- no fuzzy name matching needed.

#### 3. Disable ghost dedup for cross-type pairs

In `build.py`'s `build_from_json()`, the ghost dedup pass (lines ~200-260) currently merges any non-AST node into an AST node when they share `(basename, label)`. Change this to skip the merge when the two nodes have different `file_type` values:

- `code` ↔ `document`: never merge
- `code` ↔ `concept`: never merge
- `code` ↔ `code`: merge as before (same-type dedup)
- `document` ↔ `document`: merge as before (same-type dedup)

#### 4. New edge relation: `documents`

Add `documents` to the set of recognized relations. It is distinct from existing relations:

- `references` -- type annotation references (code→code)
- `calls` -- function call graph (code→code)
- `imports` -- module imports (code→code)
- `documents` -- doc describes a code entity (doc→code)

### Where the LLM call lives

The cross-reference pass is orchestrated in the skill (skill.md Step 3), between Part C (merge semantic results) and Part D (build graph). A Python helper module (`graphify/crossref.py`):

1. Reads `.graphify_ast.json` → builds the code entity catalog
2. Reads `.graphify_semantic.json` → gets doc nodes
3. Formats a prompt with both
4. Calls the LLM (Claude subagent or Gemini API, matching the existing backend selection)
5. Writes cross edges to `.graphify_crossref.json`
6. Part C merge includes this file

### Token cost

The code entity catalog is compact: ~50 tokens per entity (id + label + kind). For a 500-class codebase, that's ~25K tokens -- well within a single LLM call budget. For larger codebases, the catalog can be chunked by community or directory, matching the existing doc chunking strategy.

### Files to modify

| File | Change |
|------|--------|
| `graphify/extract.py` | Add `build_code_catalog()` function that produces the catalog from AST results |
| `graphify/crossref.py` | New module: prompt formatting, LLM call, edge emission |
| `graphify/build.py` | Skip ghost dedup when `file_type` differs between the two nodes |
| `graphify/skill.md` | Add cross-reference step between Part C and Part D |
| `graphify/skills/*/references/extraction-spec.md` | Add `documents` to the edge relation list in the subagent prompt schema |

### Non-goals

- Embedding-based similarity matching (stays LLM-driven)
- Bidirectional edges (doc→code only; reverse traversal uses graph direction)
- Changing how code-code or doc-doc dedup works

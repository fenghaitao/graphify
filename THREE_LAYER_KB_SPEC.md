# Three-Layer Knowledge Base — Specification

**Status:** Draft v0.1
**Scope:** A tiered, progressively-disclosed knowledge system over a single codebase + its docs, built on graphify (L2) and an Obsidian vault (L3).
**Author:** design captured from session `ba7ff4c9` (graphify repo, branch v8).

---

## 1. Purpose & principles

Answer questions about a codebase + its documentation at the **minimum token cost that resolves the question**, while keeping a verifiable path back to ground truth.

Three load-bearing principles:

1. **Build bottom-up, query top-down.** Artifacts are produced L1 → L2 → L3. Queries try the cheapest synthesized layer first and fall through to ground truth only on demand.
2. **Each layer must independently answer some class of queries and route the rest.** A layer that only ever forwards is deleted as pure overhead.
3. **Store judgment, point to mechanics.** Anything a tool can regenerate is referenced by handle, never copied. Only human/conversational judgment is stored as content.

Underlying cost gradient (why the ordering exists): scanning an index ≈ hundreds of tokens · expanding a note ≈ hundreds · a graph query ≈ hundreds · reading raw files ≈ thousands. Retrieval is breadth-first-shallow, then depth-on-demand applied only to the unresolved residual.

## 2. Goals & non-goals

**Goals**
- Conceptual / "why" / navigational questions answered without reading code.
- Exact structural questions ("all callers of X") answered precisely and freshly.
- A durable home for rationale that no graph stores.
- Self-healing staleness: cheap layers never silently lie.

**Non-goals**
- Mirroring every symbol/concept into Obsidian (vault bloat, duplicate of L2).
- A merged code+doc graph (code and docs stay separate; see §4.2).
- A second LLM extraction stack: **graphify is the sole L2 engine** (no LightRAG).

## 3. Architecture overview

```
L3  Obsidian vault — synthesized notes, typed links, rationale     [query first]
        │  drill-down handle (graphify node id + hash)
        ▼
L2  graphify graphs — code graph ▸ doc graph ▸ link layer          [exact structure]
        │  source anchor (file:line / doc §)
        ▼
L1  raw code + docs on disk — grep / ripgrep / file read           [ground truth]
```

- **Build** flows up: L1 changes → L2 re-extract → L3 synthesis.
- **Query** flows down: L3 router resolves or descends.

## 4. Layer definitions

### 4.1 L1 — Ground truth
The raw files. Accessed by literal search (ripgrep) and file reads. Always correct, most expensive to consume. The final verification anchor for every L3 note (`source.l1`).

### 4.2 L2 — graphify graphs (separate, not merged)

Three artifacts, all in graphify's `graph.json` format:

| Artifact | Produced by | Node types | Path |
|---|---|---|---|
| **Code graph** | `graphify <code-dir>` — AST only, deterministic, ~0 tokens | `file_type: code` | `src/graphify-out/graph.json` |
| **Doc graph** | `graphify <docs-dir>` — semantic extraction | `document`, `concept`, `rationale` | `docs/graphify-out/graph.json` |
| **Link layer** | dedicated cross-reference pass (see §5.3) | edges only | `links.json` |

**Separation requirement:** code and doc nodes MUST remain distinct nodes. graphify already enforces this — code nodes are never label-merged (`dedup.py`), and `document`/`rationale` are file-anchored. The link layer is the *only* thing joining the two graphs; it MUST NOT be folded into either graph file.

**Querying L2:** compose the three artifacts into one in-memory `nx` graph at query time (`load_linked()`), never persisting a merged file. Node ids are preserved, so `nx.shortest_path` crosses doc → link edge → code transparently. Alternative: `graphify global add … --as code/--as docs` produces an ID-namespaced composed file for the `graphify query` CLI; link edges must then target prefixed ids.

The split buys three query capabilities a merged graph cannot offer: **layer-scoped** queries (filter to `file_type==code`), **bridge** queries (link edges incident to a node), **cross-layer paths** (show *where* doc meets code).

### 4.3 L3 — Synthesized Obsidian vault

Curated, human/agent-authored notes that hold the synthesis L2 cannot: *why*, *how-it-fits*, *where-to-look*. L3 is itself progressively disclosed (§7). Every note is either a regenerable **cache** over L2 or an irreplaceable **original** (§7.2).

## 5. Build pipeline (bottom-up)

### 5.1 Code graph
Git **post-commit hook**, no LLM. Deterministic AST re-extraction of changed files. Trustworthy to rebuild on every commit.

### 5.2 Doc graph
Hook on `docs/**` change → graphify incremental (`--update`) semantic extraction, scoped to changed docs. LLM-based, kept off the main agent.

### 5.3 Link layer
Cross-reference pass producing edges from doc nodes → code node ids. Recommended method: a **code-aware semantic pass** — one subagent fed the code graph's node list (ids + labels), instructed to emit edges only (`references` / `documents` / `rationale_for`), no new nodes. Cheaper alternative: deterministic label/symbol matching against code ids (`{dir}_{file}_{entity}`). Output is a pure edge list keyed to real code node ids.

### 5.4 L3 synthesis
**SessionEnd subagent** (see §9). Runs on the session delta only, while conversation context is warm, because rationale lives only in the conversation — a later batch job has lost the *why*.

## 6. Query / retrieval model (top-down)

L3 answers one class outright and routes the rest with a precise anchor.

| Question class | L3 move | Resolved by |
|---|---|---|
| Conceptual / why | read note abstract + ADR body, cite via wikilinks | **L3** |
| Navigational | scan MOC, return the map | **L3** |
| Cross-domain ("which doc motivated this module?") | follow `specifies` edge | **L3** |
| Structural / exhaustive ("all callers", "exact precedence") | grab `source.anchor`, `graphify query` it | **L2** |
| Stale / miss | descend, then write-back a new cache note | L2 / L1 |

### 6.1 Router (descent) contract
1. Scan MOC `contains` → candidate notes.
2. Read candidate **frontmatter only** (abstract, typed links, `status`, `source`).
3. **Resolve in L3** iff a typed-link path answers the question AND `status: fresh`.
4. **Descend to L2** on exactly three triggers:
   - **Specificity gap** — structural/exhaustive question that prose summarizes lossily.
   - **Staleness** — `status: stale` (hash mismatch); trust the live query over the cached summary.
   - **Miss** — no note covers it; fall through to L2/L1 and, on success, **write a new cache note** so the vault learns the gap.
5. `source.l1` is the final ground-truth anchor for verification.

## 7. L3 note model

### 7.1 Note types & internal disclosure ladder

| Type | Class | `source` | Primary links | Role |
|---|---|---|---|---|
| `moc` | cache | none | `contains` | L0 navigation spine, ~200-line cap, **holds no knowledge** |
| `component` | cache | **graphify required** | `implements`, `depends-on`, `part-of` | "what/why" of a code unit |
| `doc-concept` | cache | **graphify required** | `specifies`, `relates-to`, `part-of` | synthesized doc idea |
| `decision` (ADR) | **original** | none | `supersedes`, `relates-to` | the **why** + rejected alternatives |
| `gotcha` | original | optional | `fixes`, `caused-by` | failure modes, conventions |
| `session-log` | append-only | optional | `relates-to` | narrative; distilled upward then archived |

Note body shape (recursive disclosure): `# Title` → one-line abstract → body → `## References` (echoes `source`).

### 7.2 Cache vs original
- **cache** — regenerable from `source.anchor`, hash-checked, disposable. Gardener MAY rebuild.
- **original** — pure captured judgment, no anchor, the only content permanently lost if deleted. Gardener MUST NOT auto-overwrite.

### 7.3 Content budget — what each note may contain
Litmus test: **"Would re-running graphify reproduce this fact?"** Yes → store an *anchor*, not the content. No → store it, mark `original`.

**Store in L3:** rationale/decisions, synthesized one-paragraph abstractions, code↔doc bridges, gotchas/lessons, MOCs, provenance handles.
**Never store in L3:** exhaustive caller/callee lists, exact signatures, full call chains, anything mechanically regenerable. Point to L2 instead.

## 8. Frontmatter schema

```yaml
---
id: cmp-auth-validate-token          # stable slug; survives renames; never regenerated
type: component                      # moc | component | decision | doc-concept | gotcha | session-log
class: cache                         # cache | original
title: Token Validation
status: fresh                        # fresh | stale | orphan   (gardener-owned)
tags: [auth, security]
created: 2026-06-23
updated: 2026-06-23

source:                              # present on cache notes; omit on originals
  layer2: graphify                   # graphify | none
  anchor: auth_session_validatetoken # graphify node id / qualified symbol
  l1: src/auth/session.py#L42-L88    # ground-truth anchor (file:line | doc §)
  hash: 9f3a1c7e                      # sha256 of the L1 source region at synthesis time
  synthesized_at: 2026-06-23T09:00Z

# typed links — store ONE canonical direction; Obsidian backlinks give the inverse.
implements:  ["[[adr-jwt-over-session]]"]
depends-on:  ["[[cmp-token-store]]"]
specifies:   []
part-of:     ["[[moc-auth]]"]
relates-to:  ["[[gotcha-clock-skew]]"]
---
```

Field notes: `id` is independent of title/filename (links resolve on `id`). `hash` covers the **L1 region**, not the L2 graph, so a mere re-cluster does not falsely invalidate the vault.

## 9. Synthesis ownership & triggers

Split the work by *which layer changed* and *whether it needs judgment*:

| Stream | Owner | Trigger | Why there |
|---|---|---|---|
| Code graph refresh | git hook, no LLM | post-commit | deterministic, cheap, trustworthy |
| Doc graph refresh | hook → graphify `--update` | `docs/**` change | LLM but scoped; off the main agent |
| Wiki capture (delta notes, code↔doc links, rationale) | dedicated subagent (cheap model) | session end / `/save` | rationale lives only in warm context |
| Vault gardening | cron, headless (Haiku) | nightly | global, latency-tolerant, no live context |

## 10. Gardening (lint) contract
- Recompute `sha256(L1 region)` vs stored `source.hash` → set `status: stale` on mismatch.
- **Never touch `class: original`.**
- `status: orphan` when a note has no `part-of` and no backlinks.
- Repair dangling `[[...]]`.

Stale-cache sweep (Dataview):
```dataview
TABLE source.anchor AS "rebuild from", source.synthesized_at AS "stale since"
FROM "" WHERE type != "decision" AND class = "cache" AND status = "stale"
SORT source.synthesized_at ASC
```

## 11. Typed-link ontology

| Field | Connects | Following it gets |
|---|---|---|
| `implements` / *(implemented-by)* | component → decision/doc | rule → code, or back |
| `specifies` / *(specified-by)* | doc-concept → component | **the code↔doc bridge — L3's reason to exist** |
| `depends-on` / *(used-by)* | component ↔ component | local dependency neighborhood |
| `supersedes` / *(superseded-by)* | ADR → ADR | how rationale evolved |
| `part-of` / `contains` | note ↔ MOC | navigation spine |
| `fixes` / `caused-by` | gotcha ↔ decision/commit | failure that motivated a choice |
| `relates-to` | any ↔ any | weak lateral discovery |

A few meaningful typed edges per note. Over-linking with `relates-to` collapses back to untyped and destroys signal.

## 12. Storage layout

| Artifact | Path |
|---|---|
| Code graph | `<code-dir>/graphify-out/graph.json` |
| Doc graph | `<docs-dir>/graphify-out/graph.json` |
| Link layer | `links.json` |
| Composed global graph (optional) | `~/.graphify/global-graph.json` |
| L3 vault | Obsidian vault dir (TBD) |
| Session transcripts (synthesis input) | `~/.claude/projects/<cwd-slug>/<session-uuid>.jsonl` |
| Persistent memory facts | `~/.claude/projects/<cwd-slug>/memory/` |

Session JSONL is an append-only operational record, not a stable API — read it as a source, do not depend on its schema.

## 13. Operational guardrails
- **Cheap models for grunt work.** Delta note-drafting and gardening target Haiku/Sonnet; reserve the expensive model for the coding session.
- **Non-blocking hooks.** Every hook exits 0 on all paths. A failed synthesizer leaves the note unwritten and its hash stale; the next session detects the mismatch and re-synthesizes — failures self-heal.
- **Concurrency.** If more than one session can touch the vault, use a single-writer queue or per-note locking (last-write-wins clobbers notes). Non-issue for a solo dev.

## 14. Rollout
1. Post-commit hook → code graph. *(highest value, zero risk)*
2. SessionEnd synthesizer subagent → delta notes + provenance. *(captures rationale)*

Steps 1–2 are ~80% of the value. Then:

3. Doc-graph hook + link-layer pass.
4. Nightly gardening cron.
5. `/sync` on-demand full re-synthesis escape hatch.
6. PreCompact checkpoint hook — only once sessions run long enough to compact before wrap-up.

## 15. Open questions
- Where do `save-result` / session-log Q&A nodes land? (proposed: a separate `qa/graph.json`, never the code graph).
- Vault path and Dataview-vs-core-Obsidian decision.
- Link-layer method: code-aware semantic pass (accurate) vs deterministic matcher (free).

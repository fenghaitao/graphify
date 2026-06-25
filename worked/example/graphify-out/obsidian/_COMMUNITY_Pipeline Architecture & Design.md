---
type: community
cohesion: 0.17
members: 16
---

# Pipeline Architecture & Design

**Cohesion:** 0.17 - loosely connected
**Members:** 16 nodes

## Members
- [[Add keyword index and cross-references to a validated document.]] - rationale - raw/processor.py
- [[Enrich a validated document and persist it. Returns the record ID.]] - rationale - raw/processor.py
- [[Look up the index and return IDs of related documents by keyword overlap.]] - rationale - raw/processor.py
- [[Lowercase, strip extra whitespace, remove control characters.]] - rationale - raw/processor.py
- [[Processor module - transforms validated documents into enriched records ready fo]] - rationale - raw/processor.py
- [[Pull non-stopword tokens from text, deduplicated.]] - rationale - raw/processor.py
- [[Re-enrich a document to pick up new cross-references.]] - rationale - raw/api.py
- [[Re-enrich all records in the index. Returns count of records updated.]] - rationale - raw/processor.py
- [[enrich_document()]] - code - raw/processor.py
- [[extract_keywords()]] - code - raw/processor.py
- [[find_cross_references()]] - code - raw/processor.py
- [[handle_enrich()]] - code - raw/api.py
- [[normalize_text()]] - code - raw/processor.py
- [[process_and_save()]] - code - raw/processor.py
- [[processor.py]] - code - raw/processor.py
- [[reprocess_all()]] - code - raw/processor.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_Architecture__Design
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Storage & Index Persistence]]
- 2 edges to [[_COMMUNITY_Document Enrichment & Processing]]
- 1 edge to [[_COMMUNITY_Schema Validation]]

## Top bridge nodes
- [[handle_enrich()]] - degree 5, connects to 3 communities
- [[find_cross_references()]] - degree 8, connects to 1 community
- [[process_and_save()]] - degree 6, connects to 1 community
- [[normalize_text()]] - degree 5, connects to 1 community
- [[reprocess_all()]] - degree 4, connects to 1 community
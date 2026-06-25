---
type: community
cohesion: 0.25
members: 15
---

# Storage & Index Persistence

**Cohesion:** 0.25 - loosely connected
**Members:** 15 nodes

## Members
- [[Fetch a single document by ID.]] - rationale - raw/storage.py
- [[Load the full document index from disk.]] - rationale - raw/storage.py
- [[Persist the index to disk.]] - rationale - raw/storage.py
- [[Remove a document and its index entry. Returns True if it existed.]] - rationale - raw/storage.py
- [[Storage module - persists documents to disk and maintains the search index. All]] - rationale - raw/storage.py
- [[Write a parsed document to storage. Returns the assigned record ID.]] - rationale - raw/storage.py
- [[Write an enriched document to storage, updating the index with keywords.]] - rationale - raw/storage.py
- [[_ensure_storage()]] - code - raw/storage.py
- [[delete_record()]] - code - raw/storage.py
- [[load_index()]] - code - raw/storage.py
- [[load_record()]] - code - raw/storage.py
- [[save_index()]] - code - raw/storage.py
- [[save_parsed()]] - code - raw/storage.py
- [[save_processed()]] - code - raw/storage.py
- [[storage.py]] - code - raw/storage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Storage__Index_Persistence
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Schema Validation]]
- 4 edges to [[_COMMUNITY_Pipeline Architecture & Design]]
- 1 edge to [[_COMMUNITY_Input Parsing]]

## Top bridge nodes
- [[load_index()]] - degree 13, connects to 2 communities
- [[load_record()]] - degree 6, connects to 2 communities
- [[storage.py]] - degree 15, connects to 1 community
- [[save_processed()]] - degree 11, connects to 1 community
- [[save_parsed()]] - degree 9, connects to 1 community
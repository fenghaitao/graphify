---
type: community
cohesion: 0.14
members: 14
---

# Schema Validation

**Cohesion:** 0.14 - loosely connected
**Members:** 14 nodes

## Members
- [[API module - exposes the document pipeline over HTTP. Thin layer over parser, va]] - rationale - raw/api.py
- [[Accept a list of file paths, run the full pipeline on each,     and return a sum]] - rationale - raw/api.py
- [[Delete a document by ID.]] - rationale - raw/api.py
- [[Fetch a document by ID and return it.]] - rationale - raw/api.py
- [[List all document IDs in storage.]] - rationale - raw/api.py
- [[Return all record IDs currently in storage.]] - rationale - raw/storage.py
- [[Simple keyword search over the index.     Returns documents whose keyword list o]] - rationale - raw/api.py
- [[api.py]] - code - raw/api.py
- [[handle_delete()]] - code - raw/api.py
- [[handle_get()]] - code - raw/api.py
- [[handle_list()]] - code - raw/api.py
- [[handle_search()]] - code - raw/api.py
- [[handle_upload()]] - code - raw/api.py
- [[list_records()]] - code - raw/storage.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Schema_Validation
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Storage & Index Persistence]]
- 1 edge to [[_COMMUNITY_Pipeline Architecture & Design]]
- 1 edge to [[_COMMUNITY_Input Parsing]]

## Top bridge nodes
- [[api.py]] - degree 11, connects to 1 community
- [[handle_upload()]] - degree 6, connects to 1 community
- [[list_records()]] - degree 5, connects to 1 community
- [[handle_delete()]] - degree 3, connects to 1 community
- [[handle_get()]] - degree 3, connects to 1 community
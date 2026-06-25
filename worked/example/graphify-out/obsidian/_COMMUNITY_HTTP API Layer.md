---
type: community
members: 12
---

# HTTP API Layer

**Members:** 12 nodes

## Members
- [[API module - exposes the document pipeline over HTTP. Thin layer over parser, va]] - rationale - raw/api.py
- [[Accept a list of file paths, run the full pipeline on each,     and return a sum]] - rationale - raw/api.py
- [[Delete a document by ID.]] - rationale - raw/api.py
- [[Fetch a document by ID and return it.]] - rationale - raw/api.py
- [[List all document IDs in storage.]] - rationale - raw/api.py
- [[Simple keyword search over the index.     Returns documents whose keyword list o]] - rationale - raw/api.py
- [[api.py]] - code - raw/api.py
- [[handle_delete()]] - code - raw/api.py
- [[handle_get()]] - code - raw/api.py
- [[handle_list()]] - code - raw/api.py
- [[handle_search()]] - code - raw/api.py
- [[handle_upload()]] - code - raw/api.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/HTTP_API_Layer
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Storage & Index Persistence]]
- 1 edge to [[_COMMUNITY_Document Enrichment & Processing]]
- 1 edge to [[_COMMUNITY_Input Parsing]]

## Top bridge nodes
- [[api.py]] - degree 7, connects to 1 community
- [[handle_upload()]] - degree 3, connects to 1 community
- [[handle_get()]] - degree 3, connects to 1 community
- [[handle_delete()]] - degree 3, connects to 1 community
- [[handle_list()]] - degree 3, connects to 1 community
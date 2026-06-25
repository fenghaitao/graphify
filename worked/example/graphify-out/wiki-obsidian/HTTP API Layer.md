# HTTP API Layer

> 12 nodes

## Key Concepts

- **api.py** (7 connections) — `raw/api.py`
- **handle_upload()** (3 connections) — `raw/api.py`
- **handle_get()** (3 connections) — `raw/api.py`
- **handle_delete()** (3 connections) — `raw/api.py`
- **handle_list()** (3 connections) — `raw/api.py`
- **handle_search()** (3 connections) — `raw/api.py`
- **API module - exposes the document pipeline over HTTP. Thin layer over parser, va** (1 connections) — `raw/api.py`
- **Accept a list of file paths, run the full pipeline on each,     and return a sum** (1 connections) — `raw/api.py`
- **Fetch a document by ID and return it.** (1 connections) — `raw/api.py`
- **Delete a document by ID.** (1 connections) — `raw/api.py`
- **List all document IDs in storage.** (1 connections) — `raw/api.py`
- **Simple keyword search over the index.     Returns documents whose keyword list o** (1 connections) — `raw/api.py`

## Relationships

- [[Storage & Index Persistence]] (4 shared connections)
- [[Document Enrichment & Processing]] (1 shared connections)
- [[Input Parsing]] (1 shared connections)

## Source Files

- `raw/api.py`

## Audit Trail

- EXTRACTED: 23 (82%)
- INFERRED: 5 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*
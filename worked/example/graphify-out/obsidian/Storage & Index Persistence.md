# Storage & Index Persistence

> 17 nodes

## Key Concepts

- **load_index()** (10 connections) — `raw/storage.py`
- **storage.py** (9 connections) — `raw/storage.py`
- **_ensure_storage()** (7 connections) — `raw/storage.py`
- **save_index()** (6 connections) — `raw/storage.py`
- **save_parsed()** (6 connections) — `raw/storage.py`
- **save_processed()** (6 connections) — `raw/storage.py`
- **delete_record()** (6 connections) — `raw/storage.py`
- **load_record()** (5 connections) — `raw/storage.py`
- **list_records()** (4 connections) — `raw/storage.py`
- **Storage module - persists documents to disk and maintains the search index. All** (1 connections) — `raw/storage.py`
- **Load the full document index from disk.** (1 connections) — `raw/storage.py`
- **Persist the index to disk.** (1 connections) — `raw/storage.py`
- **Write a parsed document to storage. Returns the assigned record ID.** (1 connections) — `raw/storage.py`
- **Write an enriched document to storage, updating the index with keywords.** (1 connections) — `raw/storage.py`
- **Fetch a single document by ID.** (1 connections) — `raw/storage.py`
- **Remove a document and its index entry. Returns True if it existed.** (1 connections) — `raw/storage.py`
- **Return all record IDs currently in storage.** (1 connections) — `raw/storage.py`

## Relationships

- [[HTTP API Layer]] (4 shared connections)
- [[Document Enrichment & Processing]] (4 shared connections)
- [[Input Parsing]] (1 shared connections)

## Source Files

- `raw/storage.py`

## Audit Trail

- EXTRACTED: 58 (87%)
- INFERRED: 9 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*
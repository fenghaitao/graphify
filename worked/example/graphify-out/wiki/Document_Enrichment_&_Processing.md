# Document Enrichment & Processing

> 16 nodes

## Key Concepts

- **processor.py** (7 connections) — `raw/processor.py`
- **process_and_save()** (6 connections) — `raw/processor.py`
- **handle_enrich()** (5 connections) — `raw/api.py`
- **enrich_document()** (5 connections) — `raw/processor.py`
- **normalize_text()** (4 connections) — `raw/processor.py`
- **extract_keywords()** (4 connections) — `raw/processor.py`
- **find_cross_references()** (4 connections) — `raw/processor.py`
- **reprocess_all()** (4 connections) — `raw/processor.py`
- **Re-enrich a document to pick up new cross-references.** (1 connections) — `raw/api.py`
- **Processor module - transforms validated documents into enriched records ready fo** (1 connections) — `raw/processor.py`
- **Lowercase, strip extra whitespace, remove control characters.** (1 connections) — `raw/processor.py`
- **Pull non-stopword tokens from text, deduplicated.** (1 connections) — `raw/processor.py`
- **Add keyword index and cross-references to a validated document.** (1 connections) — `raw/processor.py`
- **Look up the index and return IDs of related documents by keyword overlap.** (1 connections) — `raw/processor.py`
- **Enrich a validated document and persist it. Returns the record ID.** (1 connections) — `raw/processor.py`
- **Re-enrich all records in the index. Returns count of records updated.** (1 connections) — `raw/processor.py`

## Relationships

- [[Storage & Index Persistence]] (4 shared connections)
- [[Schema Validation]] (2 shared connections)
- [[HTTP API Layer]] (1 shared connections)

## Source Files

- `raw/api.py`
- `raw/processor.py`

## Audit Trail

- EXTRACTED: 39 (83%)
- INFERRED: 8 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*
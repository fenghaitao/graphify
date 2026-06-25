# Graph Report - worked/example  (2026-06-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 110 nodes · 273 edges · 8 communities
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fd9c9aac`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Pipeline Architecture & Design|Pipeline Architecture & Design]]
- [[_COMMUNITY_Storage & Index Persistence|Storage & Index Persistence]]
- [[_COMMUNITY_Document Enrichment & Processing|Document Enrichment & Processing]]
- [[_COMMUNITY_Schema Validation|Schema Validation]]
- [[_COMMUNITY_Input Parsing|Input Parsing]]
- [[_COMMUNITY_HTTP API Layer|HTTP API Layer]]
- [[_COMMUNITY_Keyword Relevance & Cross-referencing|Keyword Relevance & Cross-referencing]]
- [[_COMMUNITY_Community 7|Community 7]]

## God Nodes (most connected - your core abstractions)
1. `load_index()` - 13 edges
2. `parse_and_save()` - 12 edges
3. `save_processed()` - 11 edges
4. `validate_document()` - 11 edges
5. `save_parsed()` - 9 edges
6. `Processing Stage` - 9 edges
7. `Storage Module (storage.py)` - 9 edges
8. `parse_file()` - 8 edges
9. `extract_keywords()` - 8 edges
10. `enrich_document()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Document Pipeline` --describes--> `handle_upload()`  [EXTRACTED]
  README.md → raw/api.py
- `Document Pipeline` --describes--> `parse_and_save()`  [EXTRACTED]
  README.md → raw/parser.py
- `Transactional Write Risk` --motivates--> `save_parsed()`  [INFERRED]
  raw/notes.md → raw/storage.py
- `Document Pipeline` --describes--> `handle_upload()`  [EXTRACTED]
  raw/architecture.md → raw/api.py
- `Parsing Stage` --describes--> `parse_file()`  [EXTRACTED]
  raw/architecture.md → raw/parser.py

## Import Cycles
- None detected.

## Communities (8 total, 0 thin omitted)

### Community 0 - "Pipeline Architecture & Design"
Cohesion: 0.21
Nodes (20): Flat JSON File Storage, Storage Index, Storage Stage, SQLite Migration, delete_record(), _ensure_storage(), list_records(), load_index() (+12 more)

### Community 1 - "Storage & Index Persistence"
Cohesion: 0.18
Nodes (20): Cross-reference Detection, Keyword Index, Keyword Overlap Threshold, Processing Stage, Embedding-based Similarity, Keyword Extraction, TF-IDF Weighting, enrich_document() (+12 more)

### Community 2 - "Document Enrichment & Processing"
Cohesion: 0.19
Nodes (13): Exception, check_format(), check_required_fields(), normalize_fields(), Validator module - checks that parsed documents meet schema requirements before, Run all validation checks on a parsed document. Raises ValidationError on failur, Raise if any required field is missing., Raise if the format is not in the allowed list. (+5 more)

### Community 3 - "Schema Validation"
Cohesion: 0.15
Nodes (11): handle_delete(), handle_enrich(), handle_get(), handle_list(), handle_search(), API module - exposes the document pipeline over HTTP. Thin layer over parser, va, Fetch a document by ID and return it., Delete a document by ID. (+3 more)

### Community 4 - "Input Parsing"
Cohesion: 0.21
Nodes (13): handle_upload(), Accept a list of file paths, run the full pipeline on each,     and return a sum, Linear Pipeline Design, Pipeline Orchestration, Transactional Write Risk, batch_parse(), parse_and_save(), Full pipeline: parse, validate, save. Returns the saved record ID. (+5 more)

### Community 5 - "HTTP API Layer"
Cohesion: 0.27
Nodes (9): parse_file(), parse_json(), parse_markdown(), parse_plaintext(), Parser module - reads raw input documents and converts them into a structured fo, Read a file from disk and return a structured document., Extract title, sections, and links from markdown., Parse a JSON document into a structured dict. (+1 more)

### Community 6 - "Keyword Relevance & Cross-referencing"
Cohesion: 0.39
Nodes (9): API Module (api.py), Document Pipeline, Parser Module (parser.py), Parsing Stage, Processor Module (processor.py), Storage Module (storage.py), Validation Stage, Validator Module (validator.py) (+1 more)

### Community 7 - "Community 7"
Cohesion: 1.00
Nodes (7): api.py, architecture.md, notes.md, parser.py, processor.py, storage.py, validator.py

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `validate_document()` connect `Document Enrichment & Processing` to `Pipeline Architecture & Design`, `Schema Validation`, `Input Parsing`, `Keyword Relevance & Cross-referencing`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `load_index()` connect `Pipeline Architecture & Design` to `Storage & Index Persistence`, `Schema Validation`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `parse_and_save()` connect `Input Parsing` to `Pipeline Architecture & Design`, `Document Enrichment & Processing`, `HTTP API Layer`, `Keyword Relevance & Cross-referencing`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `load_index()` (e.g. with `handle_search()` and `Flat JSON File Storage`) actually correct?**
  _`load_index()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `parse_and_save()` (e.g. with `Linear Pipeline Design` and `Transactional Write Risk`) actually correct?**
  _`parse_and_save()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `save_processed()` (e.g. with `SQLite Migration` and `process_and_save()`) actually correct?**
  _`save_processed()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `validate_document()` (e.g. with `handle_enrich()` and `parse_and_save()`) actually correct?**
  _`validate_document()` has 2 INFERRED edges - model-reasoned connections that need verification._
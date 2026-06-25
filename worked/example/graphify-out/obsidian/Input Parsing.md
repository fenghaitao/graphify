# Input Parsing

> 14 nodes

## Key Concepts

- **parser.py** (7 connections) — `raw/parser.py`
- **parse_file()** (6 connections) — `raw/parser.py`
- **parse_and_save()** (6 connections) — `raw/parser.py`
- **batch_parse()** (4 connections) — `raw/parser.py`
- **parse_markdown()** (3 connections) — `raw/parser.py`
- **parse_json()** (3 connections) — `raw/parser.py`
- **parse_plaintext()** (3 connections) — `raw/parser.py`
- **Parser module - reads raw input documents and converts them into a structured fo** (1 connections) — `raw/parser.py`
- **Read a file from disk and return a structured document.** (1 connections) — `raw/parser.py`
- **Extract title, sections, and links from markdown.** (1 connections) — `raw/parser.py`
- **Parse a JSON document into a structured dict.** (1 connections) — `raw/parser.py`
- **Split plaintext into paragraphs.** (1 connections) — `raw/parser.py`
- **Full pipeline: parse, validate, save. Returns the saved record ID.** (1 connections) — `raw/parser.py`
- **Parse a list of files and return their record IDs.** (1 connections) — `raw/parser.py`

## Relationships

- [[Storage & Index Persistence]] (1 shared connections)
- [[Schema Validation]] (1 shared connections)
- [[HTTP API Layer]] (1 shared connections)

## Source Files

- `raw/parser.py`

## Audit Trail

- EXTRACTED: 36 (92%)
- INFERRED: 3 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*
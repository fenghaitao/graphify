# Schema Validation

> 14 nodes

## Key Concepts

- **validate_document()** (8 connections) — `raw/validator.py`
- **validator.py** (7 connections) — `raw/validator.py`
- **ValidationError** (4 connections) — `raw/validator.py`
- **check_required_fields()** (4 connections) — `raw/validator.py`
- **check_format()** (4 connections) — `raw/validator.py`
- **normalize_fields()** (4 connections) — `raw/validator.py`
- **validate_batch()** (3 connections) — `raw/validator.py`
- **Exception** (1 connections)
- **Validator module - checks that parsed documents meet schema requirements before** (1 connections) — `raw/validator.py`
- **Run all validation checks on a parsed document. Raises ValidationError on failur** (1 connections) — `raw/validator.py`
- **Raise if any required field is missing.** (1 connections) — `raw/validator.py`
- **Raise if the format is not in the allowed list.** (1 connections) — `raw/validator.py`
- **Clean up text fields using the processor.** (1 connections) — `raw/validator.py`
- **Validate a list of documents. Returns (valid_docs, errors).** (1 connections) — `raw/validator.py`

## Relationships

- [[Document Enrichment & Processing]] (2 shared connections)
- [[Input Parsing]] (1 shared connections)

## Source Files

- `raw/validator.py`

## Audit Trail

- EXTRACTED: 38 (93%)
- INFERRED: 3 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*
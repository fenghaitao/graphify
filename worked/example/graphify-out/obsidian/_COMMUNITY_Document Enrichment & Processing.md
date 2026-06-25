---
type: community
cohesion: 0.21
members: 14
---

# Document Enrichment & Processing

**Cohesion:** 0.21 - loosely connected
**Members:** 14 nodes

## Members
- [[Clean up text fields using the processor.]] - rationale - raw/validator.py
- [[Exception]] - code
- [[Raise if any required field is missing.]] - rationale - raw/validator.py
- [[Raise if the format is not in the allowed list.]] - rationale - raw/validator.py
- [[Run all validation checks on a parsed document. Raises ValidationError on failur]] - rationale - raw/validator.py
- [[Validate a list of documents. Returns (valid_docs, errors).]] - rationale - raw/validator.py
- [[ValidationError]] - code - raw/validator.py
- [[Validator module - checks that parsed documents meet schema requirements before]] - rationale - raw/validator.py
- [[check_format()]] - code - raw/validator.py
- [[check_required_fields()]] - code - raw/validator.py
- [[normalize_fields()]] - code - raw/validator.py
- [[validate_batch()]] - code - raw/validator.py
- [[validate_document()]] - code - raw/validator.py
- [[validator.py]] - code - raw/validator.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Document_Enrichment__Processing
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Pipeline Architecture & Design]]
- 1 edge to [[_COMMUNITY_Input Parsing]]

## Top bridge nodes
- [[validate_document()]] - degree 11, connects to 2 communities
- [[normalize_fields()]] - degree 4, connects to 1 community
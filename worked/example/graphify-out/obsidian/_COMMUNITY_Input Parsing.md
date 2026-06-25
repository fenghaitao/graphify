---
type: community
cohesion: 0.20
members: 14
---

# Input Parsing

**Cohesion:** 0.20 - loosely connected
**Members:** 14 nodes

## Members
- [[Extract title, sections, and links from markdown.]] - rationale - raw/parser.py
- [[Full pipeline parse, validate, save. Returns the saved record ID.]] - rationale - raw/parser.py
- [[Parse a JSON document into a structured dict.]] - rationale - raw/parser.py
- [[Parse a list of files and return their record IDs.]] - rationale - raw/parser.py
- [[Parser module - reads raw input documents and converts them into a structured fo]] - rationale - raw/parser.py
- [[Read a file from disk and return a structured document.]] - rationale - raw/parser.py
- [[Split plaintext into paragraphs.]] - rationale - raw/parser.py
- [[batch_parse()]] - code - raw/parser.py
- [[parse_and_save()]] - code - raw/parser.py
- [[parse_file()]] - code - raw/parser.py
- [[parse_json()]] - code - raw/parser.py
- [[parse_markdown()]] - code - raw/parser.py
- [[parse_plaintext()]] - code - raw/parser.py
- [[parser.py]] - code - raw/parser.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Input_Parsing
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Schema Validation]]
- 1 edge to [[_COMMUNITY_Storage & Index Persistence]]
- 1 edge to [[_COMMUNITY_Document Enrichment & Processing]]

## Top bridge nodes
- [[parse_and_save()]] - degree 12, connects to 2 communities
- [[batch_parse()]] - degree 4, connects to 1 community
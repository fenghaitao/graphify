---
type: community
members: 8
---

# Community 7

**Members:** 8 nodes

## Members
- [[Masked interrupt status register bit 0 is the raw status ANDed with INTEN, i.e. the interrupt as seen by the interrupt controller.]] - rationale - wdt_dml/wdt.dml
- [[Raw interrupt status register bit 0 reflects the pending interrupt before masking by INTEN.]] - rationale - wdt_dml/wdt.dml
- [[WDOGMIS]] - code - wdt_dml/wdt.dml
- [[WDOGMIS Register]] - document - wdt_en.md
- [[WDOGRIS]] - code - wdt_dml/wdt.dml
- [[WDOGRIS Register]] - document - wdt_en.md
- [[read_register()_3]] - code - wdt_dml/wdt.dml
- [[read_register()_4]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_7
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Community 0]]
- 2 edges to [[_COMMUNITY_Community 1]]
- 1 edge to [[_COMMUNITY_Community 5]]

## Top bridge nodes
- [[WDOGMIS Register]] - degree 4, connects to 2 communities
- [[WDOGRIS]] - degree 4, connects to 1 community
- [[WDOGMIS]] - degree 4, connects to 1 community
- [[WDOGRIS Register]] - degree 3, connects to 1 community
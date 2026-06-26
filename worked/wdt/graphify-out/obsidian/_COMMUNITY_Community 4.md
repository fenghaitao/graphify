---
type: community
members: 14
---

# Community 4

**Members:** 14 nodes

## Members
- [[Lock register writing the magic value 0x1ACCE551 unlocks the device; any other write locks it. Reads return 1 when locked, 0 when unlocked.]] - rationale - wdt_dml/wdt.dml
- [[WDOGLOCK]] - code - wdt_dml/wdt.dml
- [[WDOGLOCK Register]] - document - wdt_en.md
- [[Watchdog Module]] - document - wdt_en.md
- [[prst_n APB Reset Signal]] - document - wdt_en.md
- [[read_register()_5]] - code - wdt_dml/wdt.dml
- [[signal_3]] - code - wdt_dml/wdt.dml
- [[signal_lower()_2]] - code - wdt_dml/wdt.dml
- [[signal_raise()_2]] - code - wdt_dml/wdt.dml
- [[wdt_en]] - document - wdt_en.md
- [[write_register()_3]] - code - wdt_dml/wdt.dml
- [[wrst_n]] - code - wdt_dml/wdt.dml
- [[wrst_n Reset Signal]] - document - wdt_en.md
- [[wrst_n input (active-low watchdog reset) a falling edge performs a full device reset; the deasserted (high) level is normal operation.]] - rationale - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_4
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Community 0]]
- 9 edges to [[_COMMUNITY_Community 3]]
- 4 edges to [[_COMMUNITY_Community 7]]
- 4 edges to [[_COMMUNITY_Community 5]]
- 2 edges to [[_COMMUNITY_Community 1]]
- 2 edges to [[_COMMUNITY_Community 6]]
- 1 edge to [[_COMMUNITY_Community 2]]

## Top bridge nodes
- [[wdt_en]] - degree 32, connects to 5 communities
- [[WDOGLOCK]] - degree 5, connects to 1 community
- [[Watchdog Module]] - degree 5, connects to 1 community
- [[wrst_n]] - degree 4, connects to 1 community
- [[signal_3]] - degree 4, connects to 1 community
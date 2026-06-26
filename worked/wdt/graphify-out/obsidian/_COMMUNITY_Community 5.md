---
type: community
members: 13
---

# Community 5

**Members:** 13 nodes

## Members
- [[Control register INTEN enables the watchdog and RESEN enables reset on a second timeout. Toggling INTEN reloads or freezes the counter and (re)schedules the countdown; STEP_VALUE selects the _27ac1234]] - rationale - wdt_dml/wdt.dml
- [[INTEN Bit]] - document - wdt_en.md
- [[Maps the WDOGCONTROL.STEP_VALUE field to the clock divider (124816), defaulting to 1 for reserved encodings. The divider sets how many input clock cycles correspond to one decrement of the wa_7eaa5102]] - rationale - wdt_dml/wdt.dml
- [[RESEN Bit]] - document - wdt_en.md
- [[WDOGCONTROL]] - code - wdt_dml/wdt.dml
- [[WDOGCONTROL Register]] - document - wdt_en.md
- [[WDOGITCR Register]] - document - wdt_en.md
- [[WDOGITOP Register]] - document - wdt_en.md
- [[get_divider()]] - code - wdt_dml/wdt.dml
- [[read_register()_2]] - code - wdt_dml/wdt.dml
- [[step_value Field]] - document - wdt_en.md
- [[wdogint Signal]] - document - wdt_en.md
- [[wdogres Signal]] - document - wdt_en.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_5
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Community 1]]
- 3 edges to [[_COMMUNITY_Community 2]]
- 3 edges to [[_COMMUNITY_Community 3]]
- 1 edge to [[_COMMUNITY_Community 0]]
- 1 edge to [[_COMMUNITY_Community 6]]
- 1 edge to [[_COMMUNITY_Community 8]]
- 1 edge to [[_COMMUNITY_Community 7]]

## Top bridge nodes
- [[WDOGCONTROL Register]] - degree 9, connects to 3 communities
- [[WDOGCONTROL]] - degree 8, connects to 2 communities
- [[get_divider()]] - degree 5, connects to 2 communities
- [[WDOGITOP Register]] - degree 5, connects to 2 communities
- [[wdogint Signal]] - degree 5, connects to 2 communities
---
type: community
members: 21
---

# Community 3

**Members:** 21 nodes

## Members
- [[Control register INTEN enables the watchdog and RESEN enables reset on a second timeout. Toggling INTEN reloads or freezes the counter and (re)schedules the countdown; STEP_VALUE selects the _27ac1234]] - rationale - wdt_dml/wdt.dml
- [[INTEN Bit]] - document - wdt_en.md
- [[Integration test control register enables integration test mode, in which the output signals are driven directly via WDOGITOP. Leaving test mode restores the normal interrupt and reset signal states.]] - rationale - wdt_dml/wdt.dml
- [[Masked interrupt status register bit 0 is the raw status ANDed with INTEN, i.e. the interrupt as seen by the interrupt controller.]] - rationale - wdt_dml/wdt.dml
- [[RESEN Bit]] - document - wdt_en.md
- [[Raw interrupt status register bit 0 reflects the pending interrupt before masking by INTEN.]] - rationale - wdt_dml/wdt.dml
- [[WDOGCONTROL]] - code - wdt_dml/wdt.dml
- [[WDOGCONTROL Register]] - document - wdt_en.md
- [[WDOGITCR]] - code - wdt_dml/wdt.dml
- [[WDOGITCR Register]] - document - wdt_en.md
- [[WDOGITOP Register]] - document - wdt_en.md
- [[WDOGMIS]] - code - wdt_dml/wdt.dml
- [[WDOGMIS Register]] - document - wdt_en.md
- [[WDOGRIS]] - code - wdt_dml/wdt.dml
- [[WDOGRIS Register]] - document - wdt_en.md
- [[read_register()_2]] - code - wdt_dml/wdt.dml
- [[read_register()_3]] - code - wdt_dml/wdt.dml
- [[read_register()_4]] - code - wdt_dml/wdt.dml
- [[read_register()_6]] - code - wdt_dml/wdt.dml
- [[wdogint Signal]] - document - wdt_en.md
- [[wdogres Signal]] - document - wdt_en.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_3
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Community 4]]
- 4 edges to [[_COMMUNITY_Community 0]]
- 4 edges to [[_COMMUNITY_Community 1]]
- 3 edges to [[_COMMUNITY_Community 2]]
- 2 edges to [[_COMMUNITY_Community 5]]
- 2 edges to [[_COMMUNITY_Community 7]]

## Top bridge nodes
- [[wdogint Signal]] - degree 9, connects to 4 communities
- [[WDOGCONTROL Register]] - degree 9, connects to 3 communities
- [[wdogres Signal]] - degree 6, connects to 3 communities
- [[WDOGCONTROL]] - degree 8, connects to 2 communities
- [[WDOGITCR]] - degree 5, connects to 2 communities
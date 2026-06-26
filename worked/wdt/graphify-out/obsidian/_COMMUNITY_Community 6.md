---
type: community
members: 11
---

# Community 6

**Members:** 11 nodes

## Members
- [[Device initialization sets the counter and all state variables to their power-on defaults (device unlocked, clock assumed enabled, output signals low).]] - rationale - wdt_dml/wdt.dml
- [[Performs a full watchdog reset cancels pending events, clears the counter and interruptreset state, restores the key registers to their defaults, and lowers both output signals.]] - rationale - wdt_dml/wdt.dml
- [[Resets the counter to its power-on value (0xFFFFFFFF).]] - rationale - wdt_dml/wdt.dml
- [[init()]] - code - wdt_dml/wdt.dml
- [[perform_reset()]] - code - wdt_dml/wdt.dml
- [[prst_n]] - code - wdt_dml/wdt.dml
- [[prst_n input (active-low power-on reset) a falling edge performs a full device reset; the deasserted (high) level is normal operation.]] - rationale - wdt_dml/wdt.dml
- [[reset()]] - code - wdt_dml/wdt.dml
- [[signal_4]] - code - wdt_dml/wdt.dml
- [[signal_lower()_3]] - code - wdt_dml/wdt.dml
- [[signal_raise()_3]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_6
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Community 1]]
- 2 edges to [[_COMMUNITY_Community 4]]
- 1 edge to [[_COMMUNITY_Community 2]]
- 1 edge to [[_COMMUNITY_Community 7]]

## Top bridge nodes
- [[perform_reset()]] - degree 6, connects to 2 communities
- [[prst_n]] - degree 4, connects to 2 communities
- [[reset()]] - degree 4, connects to 1 community
- [[signal_4]] - degree 4, connects to 1 community
- [[init()]] - degree 3, connects to 1 community
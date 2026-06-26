---
type: community
members: 16
---

# Community 4

**Members:** 16 nodes

## Members
- [[Device initialization sets the counter and all state variables to their power-on defaults (device unlocked, clock assumed enabled, output signals low).]] - rationale - wdt_dml/wdt.dml
- [[Performs a full watchdog reset cancels pending events, clears the counter and interruptreset state, restores the key registers to their defaults, and lowers both output signals.]] - rationale - wdt_dml/wdt.dml
- [[Resets the counter to its power-on value (0xFFFFFFFF).]] - rationale - wdt_dml/wdt.dml
- [[init()]] - code - wdt_dml/wdt.dml
- [[perform_reset()]] - code - wdt_dml/wdt.dml
- [[reset()]] - code - wdt_dml/wdt.dml
- [[signal]] - code - wdt_dml/wdt.dml
- [[signal_1]] - code - wdt_dml/wdt.dml
- [[signal_2]] - code - wdt_dml/wdt.dml
- [[signal_3]] - code - wdt_dml/wdt.dml
- [[signal_4]] - code - wdt_dml/wdt.dml
- [[signal_lower()_1]] - code - wdt_dml/wdt.dml
- [[signal_lower()_2]] - code - wdt_dml/wdt.dml
- [[signal_lower()_3]] - code - wdt_dml/wdt.dml
- [[signal_raise()_2]] - code - wdt_dml/wdt.dml
- [[signal_raise()_3]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_4
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Community 1]]
- 3 edges to [[_COMMUNITY_Community 3]]
- 2 edges to [[_COMMUNITY_Community 2]]

## Top bridge nodes
- [[perform_reset()]] - degree 6, connects to 2 communities
- [[signal]] - degree 4, connects to 2 communities
- [[signal_2]] - degree 4, connects to 2 communities
- [[reset()]] - degree 4, connects to 1 community
- [[signal_3]] - degree 4, connects to 1 community
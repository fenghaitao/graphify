---
type: community
members: 19
---

# Community 3

**Members:** 19 nodes

## Members
- [[Drives the WDOGRES output to match reset state asserts when a reset is pending, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the signal directly.]] - rationale - wdt_dml/wdt.dml
- [[Integration test control register enables integration test mode, in which the output signals are driven directly via WDOGITOP. Leaving test mode restores the normal interrupt and reset signal states.]] - rationale - wdt_dml/wdt.dml
- [[USER-TODO implement wclk signal handling here.]] - rationale - wdt_dml/wdt.dml
- [[WDOGITCR]] - code - wdt_dml/wdt.dml
- [[read_register()_6]] - code - wdt_dml/wdt.dml
- [[signal_5]] - code - wdt_dml/wdt.dml
- [[signal_6]] - code - wdt_dml/wdt.dml
- [[signal_lower()]] - code - wdt_dml/wdt.dml
- [[signal_lower()_4]] - code - wdt_dml/wdt.dml
- [[signal_lower()_5]] - code - wdt_dml/wdt.dml
- [[signal_raise()]] - code - wdt_dml/wdt.dml
- [[signal_raise()_4]] - code - wdt_dml/wdt.dml
- [[signal_raise()_5]] - code - wdt_dml/wdt.dml
- [[update_reset_signal()]] - code - wdt_dml/wdt.dml
- [[wdogint]] - code - wdt_dml/wdt.dml
- [[wdogint output the watchdog interrupt line. Raiseslowers the connected signal with a NULL-object guard, so an unconnected interrupt is a no-op.]] - rationale - wdt_dml/wdt.dml
- [[wdogres]] - code - wdt_dml/wdt.dml
- [[wdogres output the watchdog reset line. Raiseslowers the connected signal with a NULL-object guard, so an unconnected reset is a no-op.]] - rationale - wdt_dml/wdt.dml
- [[write_register()_4]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_3
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Community 2]]
- 3 edges to [[_COMMUNITY_Community 1]]
- 3 edges to [[_COMMUNITY_Community 6]]
- 3 edges to [[_COMMUNITY_Community 5]]
- 3 edges to [[_COMMUNITY_Community 4]]
- 1 edge to [[_COMMUNITY_Community 0]]

## Top bridge nodes
- [[signal_raise()]] - degree 7, connects to 3 communities
- [[signal_lower()]] - degree 7, connects to 3 communities
- [[update_reset_signal()]] - degree 6, connects to 2 communities
- [[wdogint]] - degree 6, connects to 2 communities
- [[wdogres]] - degree 6, connects to 2 communities
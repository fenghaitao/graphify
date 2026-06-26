---
type: community
members: 27
---

# Community 1

**Members:** 27 nodes

## Members
- [[Drives the WDOGINT output to match interrupt state asserts when an interrupt is pending and INTEN is set, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the sign_a7201293]] - rationale - wdt_dml/wdt.dml
- [[Drives the WDOGRES output to match reset state asserts when a reset is pending, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the signal directly.]] - rationale - wdt_dml/wdt.dml
- [[Integration test output register in test mode, directly drives the WDOGINT and WDOGRES output signals from bits 1 and 0 respectively.]] - rationale - wdt_dml/wdt.dml
- [[Returns true while the device is locked. When locked, all register writes are ignored; the lock is cleared only by writing the magic unlock value 0x1ACCE551 to WDOGLOCK.]] - rationale - wdt_dml/wdt.dml
- [[USER-TODO implement wclk signal handling here.]] - rationale - wdt_dml/wdt.dml
- [[WDOGITOP]] - code - wdt_dml/wdt.dml
- [[is_device_locked()]] - code - wdt_dml/wdt.dml
- [[signal_5]] - code - wdt_dml/wdt.dml
- [[signal_6]] - code - wdt_dml/wdt.dml
- [[signal_lower()]] - code - wdt_dml/wdt.dml
- [[signal_lower()_4]] - code - wdt_dml/wdt.dml
- [[signal_lower()_5]] - code - wdt_dml/wdt.dml
- [[signal_raise()]] - code - wdt_dml/wdt.dml
- [[signal_raise()_4]] - code - wdt_dml/wdt.dml
- [[signal_raise()_5]] - code - wdt_dml/wdt.dml
- [[simicsdevssignal.dml]] - code - wdt_dml/wdt.dml
- [[update_interrupt_signal()]] - code - wdt_dml/wdt.dml
- [[update_reset_signal()]] - code - wdt_dml/wdt.dml
- [[wdogint]] - code - wdt_dml/wdt.dml
- [[wdogint output the watchdog interrupt line. Raiseslowers the connected signal with a NULL-object guard, so an unconnected interrupt is a no-op.]] - rationale - wdt_dml/wdt.dml
- [[wdogres]] - code - wdt_dml/wdt.dml
- [[wdogres output the watchdog reset line. Raiseslowers the connected signal with a NULL-object guard, so an unconnected reset is a no-op.]] - rationale - wdt_dml/wdt.dml
- [[wdt-registers.dml_1]] - code - wdt_dml/wdt.dml
- [[wdt.dml]] - code - wdt_dml/wdt.dml
- [[write_register()_2]] - code - wdt_dml/wdt.dml
- [[write_register()_4]] - code - wdt_dml/wdt.dml
- [[write_register()_5]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_1
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Community 2]]
- 4 edges to [[_COMMUNITY_Community 6]]
- 4 edges to [[_COMMUNITY_Community 7]]
- 4 edges to [[_COMMUNITY_Community 3]]
- 2 edges to [[_COMMUNITY_Community 0]]
- 2 edges to [[_COMMUNITY_Community 4]]
- 2 edges to [[_COMMUNITY_Community 5]]

## Top bridge nodes
- [[wdt.dml]] - degree 19, connects to 5 communities
- [[is_device_locked()]] - degree 7, connects to 2 communities
- [[signal_lower()]] - degree 7, connects to 2 communities
- [[write_register()_2]] - degree 5, connects to 2 communities
- [[WDOGITOP]] - degree 4, connects to 2 communities
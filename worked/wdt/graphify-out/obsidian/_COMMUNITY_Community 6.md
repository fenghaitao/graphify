---
type: community
members: 9
---

# Community 6

**Members:** 9 nodes

## Members
- [[Integration test output register in test mode, directly drives the WDOGINT and WDOGRES output signals from bits 1 and 0 respectively.]] - rationale - wdt_dml/wdt.dml
- [[Load register the value reloaded into the counter on each timeout and on interrupt clear. Writes are ignored while locked and do not reload the counter immediately unless INTEN transitions 0-1.]] - rationale - wdt_dml/wdt.dml
- [[Returns true while the device is locked. When locked, all register writes are ignored; the lock is cleared only by writing the magic unlock value 0x1ACCE551 to WDOGLOCK.]] - rationale - wdt_dml/wdt.dml
- [[WDOGITOP]] - code - wdt_dml/wdt.dml
- [[WDOGLOAD]] - code - wdt_dml/wdt.dml
- [[is_device_locked()]] - code - wdt_dml/wdt.dml
- [[read_register()]] - code - wdt_dml/wdt.dml
- [[write_register()]] - code - wdt_dml/wdt.dml
- [[write_register()_5]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_6
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Community 3]]
- 2 edges to [[_COMMUNITY_Community 2]]
- 2 edges to [[_COMMUNITY_Community 0]]
- 1 edge to [[_COMMUNITY_Community 1]]
- 1 edge to [[_COMMUNITY_Community 8]]
- 1 edge to [[_COMMUNITY_Community 5]]

## Top bridge nodes
- [[is_device_locked()]] - degree 7, connects to 3 communities
- [[WDOGLOAD]] - degree 5, connects to 2 communities
- [[WDOGITOP]] - degree 4, connects to 2 communities
- [[write_register()_5]] - degree 4, connects to 1 community
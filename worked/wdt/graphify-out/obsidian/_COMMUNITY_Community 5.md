---
type: community
members: 13
---

# Community 5

**Members:** 13 nodes

## Members
- [[32-bit Down Counter]] - document - wdt_en.md
- [[Interrupt clear register any write clears the pending interrupt, lowers WDOGINT, reloads the counter from WDOGLOAD and reschedules the countdown.]] - rationale - wdt_dml/wdt.dml
- [[Load register the value reloaded into the counter on each timeout and on interrupt clear. Writes are ignored while locked and do not reload the counter immediately unless INTEN transitions 0-1.]] - rationale - wdt_dml/wdt.dml
- [[Value register (read-only) returns the live counter value via lazy evaluation rather than a continuously decremented field.]] - rationale - wdt_dml/wdt.dml
- [[WDOGINTCLR]] - code - wdt_dml/wdt.dml
- [[WDOGINTCLR Register]] - document - wdt_en.md
- [[WDOGLOAD]] - code - wdt_dml/wdt.dml
- [[WDOGLOAD Register]] - document - wdt_en.md
- [[WDOGVALUE]] - code - wdt_dml/wdt.dml
- [[WDOGVALUE Register]] - document - wdt_en.md
- [[read_register()]] - code - wdt_dml/wdt.dml
- [[read_register()_1]] - code - wdt_dml/wdt.dml
- [[write_register()]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_5
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Community 4]]
- 3 edges to [[_COMMUNITY_Community 0]]
- 2 edges to [[_COMMUNITY_Community 1]]
- 2 edges to [[_COMMUNITY_Community 2]]
- 2 edges to [[_COMMUNITY_Community 3]]

## Top bridge nodes
- [[32-bit Down Counter]] - degree 5, connects to 3 communities
- [[WDOGINTCLR]] - degree 4, connects to 2 communities
- [[WDOGINTCLR Register]] - degree 4, connects to 2 communities
- [[WDOGLOAD]] - degree 5, connects to 1 community
- [[WDOGLOAD Register]] - degree 5, connects to 1 community
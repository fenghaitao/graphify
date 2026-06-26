---
type: community
members: 25
---

# Community 1

**Members:** 25 nodes

## Members
- [[32-bit Down Counter]] - document - wdt_en.md
- [[Signal interface implementations. Ports model input signals into the device; connects model output signals the device drives. wclk is the watchdog clock input; because counting is modeled laz_b82a9da6]] - rationale - wdt_dml/wdt.dml
- [[Value register (read-only) returns the live counter value via lazy evaluation rather than a continuously decremented field.]] - rationale - wdt_dml/wdt.dml
- [[WDOGVALUE]] - code - wdt_dml/wdt.dml
- [[WDOGVALUE Register]] - document - wdt_en.md
- [[Watchdog Module]] - document - wdt_en.md
- [[Watchdog countdown event fires when the counter reaches zero. On the first timeout it latches the interrupt and reloads the counter; on a second timeout (interrupt still pending) it asserts t_9f71f624]] - rationale - wdt_dml/wdt.dml
- [[prst_n]] - code - wdt_dml/wdt.dml
- [[prst_n APB Reset Signal]] - document - wdt_en.md
- [[prst_n input (active-low power-on reset) a falling edge performs a full device reset; the deasserted (high) level is normal operation.]] - rationale - wdt_dml/wdt.dml
- [[read_register()_1]] - code - wdt_dml/wdt.dml
- [[simicsdevssignal.dml]] - code - wdt_dml/wdt.dml
- [[simple_cycle_event]] - code - wdt_dml/wdt.dml
- [[timeout_event]] - code - wdt_dml/wdt.dml
- [[wclk]] - code - wdt_dml/wdt.dml
- [[wclk Clock Signal]] - document - wdt_en.md
- [[wclk_en]] - code - wdt_dml/wdt.dml
- [[wclk_en Clock Enable Signal]] - document - wdt_en.md
- [[wclk_en input (clock enable) raising it resumes counting (refreshes the counter and reschedules the event when enabled); lowering it pauses the timer by cancelling the pending countdown event.]] - rationale - wdt_dml/wdt.dml
- [[wdt-registers.dml_1]] - code - wdt_dml/wdt.dml
- [[wdt.dml]] - code - wdt_dml/wdt.dml
- [[wdt_en]] - document - wdt_en.md
- [[wrst_n]] - code - wdt_dml/wdt.dml
- [[wrst_n Reset Signal]] - document - wdt_en.md
- [[wrst_n input (active-low watchdog reset) a falling edge performs a full device reset; the deasserted (high) level is normal operation.]] - rationale - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_1
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Community 0]]
- 9 edges to [[_COMMUNITY_Community 5]]
- 6 edges to [[_COMMUNITY_Community 2]]
- 6 edges to [[_COMMUNITY_Community 4]]
- 4 edges to [[_COMMUNITY_Community 8]]
- 3 edges to [[_COMMUNITY_Community 3]]
- 2 edges to [[_COMMUNITY_Community 7]]
- 1 edge to [[_COMMUNITY_Community 6]]

## Top bridge nodes
- [[wdt.dml]] - degree 19, connects to 6 communities
- [[wdt_en]] - degree 32, connects to 4 communities
- [[32-bit Down Counter]] - degree 7, connects to 2 communities
- [[timeout_event]] - degree 4, connects to 1 community
- [[WDOGVALUE]] - degree 4, connects to 1 community
---
type: community
members: 22
---

# Community 2

**Members:** 22 nodes

## Members
- [[(Re)posts the countdown event. Cancels any pending event, then, when the timer is enabled (INTEN set and clock running), schedules the event for the number of cycles until the counter reaches_5d6acdcf]] - rationale - wdt_dml/wdt.dml
- [[Backing store for the watchdog down-counter. Holds the count and models it lazily the live value is derived from elapsed cycles and the clock divider only when read, instead of being decremen_264d0e40]] - rationale - wdt_dml/wdt.dml
- [[Folds the lazily-computed live value back into the stored counter.]] - rationale - wdt_dml/wdt.dml
- [[Lazily computes the current count from the cycles elapsed since the last update, scaled by the clock divider. Returns 0 once the counter has underflowed, and the stored value while the timer _1a8c53b9]] - rationale - wdt_dml/wdt.dml
- [[Maps the WDOGCONTROL.STEP_VALUE field to the clock divider (124816), defaulting to 1 for reserved encodings. The divider sets how many input clock cycles correspond to one decrement of the wa_7eaa5102]] - rationale - wdt_dml/wdt.dml
- [[Returns the stored counter value without recomputing elapsed time.]] - rationale - wdt_dml/wdt.dml
- [[Stores a new counter value (used on reload and when freezing the counter).]] - rationale - wdt_dml/wdt.dml
- [[Watchdog countdown event fires when the counter reaches zero. On the first timeout it latches the interrupt and reloads the counter; on a second timeout (interrupt still pending) it asserts t_9f71f624]] - rationale - wdt_dml/wdt.dml
- [[counter_value]] - code - wdt_dml/wdt.dml
- [[curr_value()]] - code - wdt_dml/wdt.dml
- [[event()]] - code - wdt_dml/wdt.dml
- [[get_divider()]] - code - wdt_dml/wdt.dml
- [[get_value()]] - code - wdt_dml/wdt.dml
- [[refresh()]] - code - wdt_dml/wdt.dml
- [[schedule_timeout()]] - code - wdt_dml/wdt.dml
- [[set_value()]] - code - wdt_dml/wdt.dml
- [[signal_raise()_1]] - code - wdt_dml/wdt.dml
- [[simple_cycle_event]] - code - wdt_dml/wdt.dml
- [[step_value Field]] - document - wdt_en.md
- [[timeout_event]] - code - wdt_dml/wdt.dml
- [[uint64_attr]] - code - wdt_dml/wdt.dml
- [[write_register()_1]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_2
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Community 1]]
- 3 edges to [[_COMMUNITY_Community 3]]
- 2 edges to [[_COMMUNITY_Community 5]]
- 1 edge to [[_COMMUNITY_Community 6]]
- 1 edge to [[_COMMUNITY_Community 7]]
- 1 edge to [[_COMMUNITY_Community 4]]

## Top bridge nodes
- [[counter_value]] - degree 9, connects to 3 communities
- [[write_register()_1]] - degree 6, connects to 2 communities
- [[step_value Field]] - degree 4, connects to 2 communities
- [[schedule_timeout()]] - degree 8, connects to 1 community
- [[curr_value()]] - degree 6, connects to 1 community
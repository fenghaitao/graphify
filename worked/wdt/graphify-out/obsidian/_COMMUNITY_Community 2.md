---
type: community
members: 21
---

# Community 2

**Members:** 21 nodes

## Members
- [[(Re)posts the countdown event. Cancels any pending event, then, when the timer is enabled (INTEN set and clock running), schedules the event for the number of cycles until the counter reaches_5d6acdcf]] - rationale - wdt_dml/wdt.dml
- [[Backing store for the watchdog down-counter. Holds the count and models it lazily the live value is derived from elapsed cycles and the clock divider only when read, instead of being decremen_264d0e40]] - rationale - wdt_dml/wdt.dml
- [[Drives the WDOGINT output to match interrupt state asserts when an interrupt is pending and INTEN is set, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the sign_a7201293]] - rationale - wdt_dml/wdt.dml
- [[Folds the lazily-computed live value back into the stored counter.]] - rationale - wdt_dml/wdt.dml
- [[Interrupt clear register any write clears the pending interrupt, lowers WDOGINT, reloads the counter from WDOGLOAD and reschedules the countdown.]] - rationale - wdt_dml/wdt.dml
- [[Lazily computes the current count from the cycles elapsed since the last update, scaled by the clock divider. Returns 0 once the counter has underflowed, and the stored value while the timer _1a8c53b9]] - rationale - wdt_dml/wdt.dml
- [[Returns the stored counter value without recomputing elapsed time.]] - rationale - wdt_dml/wdt.dml
- [[Stores a new counter value (used on reload and when freezing the counter).]] - rationale - wdt_dml/wdt.dml
- [[WDOGINTCLR]] - code - wdt_dml/wdt.dml
- [[counter_value]] - code - wdt_dml/wdt.dml
- [[curr_value()]] - code - wdt_dml/wdt.dml
- [[event()]] - code - wdt_dml/wdt.dml
- [[get_value()]] - code - wdt_dml/wdt.dml
- [[refresh()]] - code - wdt_dml/wdt.dml
- [[schedule_timeout()]] - code - wdt_dml/wdt.dml
- [[set_value()]] - code - wdt_dml/wdt.dml
- [[signal_raise()_1]] - code - wdt_dml/wdt.dml
- [[uint64_attr]] - code - wdt_dml/wdt.dml
- [[update_interrupt_signal()]] - code - wdt_dml/wdt.dml
- [[write_register()_1]] - code - wdt_dml/wdt.dml
- [[write_register()_2]] - code - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_2
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Community 1]]
- 4 edges to [[_COMMUNITY_Community 3]]
- 3 edges to [[_COMMUNITY_Community 5]]
- 2 edges to [[_COMMUNITY_Community 6]]
- 2 edges to [[_COMMUNITY_Community 4]]
- 1 edge to [[_COMMUNITY_Community 0]]
- 1 edge to [[_COMMUNITY_Community 8]]

## Top bridge nodes
- [[counter_value]] - degree 9, connects to 2 communities
- [[schedule_timeout()]] - degree 8, connects to 2 communities
- [[update_interrupt_signal()]] - degree 8, connects to 2 communities
- [[curr_value()]] - degree 6, connects to 2 communities
- [[write_register()_1]] - degree 6, connects to 2 communities
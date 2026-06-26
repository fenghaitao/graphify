---
type: community
members: 10
---

# Community 7

**Members:** 10 nodes

## Members
- [[Signal interface implementations. Ports model input signals into the device; connects model output signals the device drives. wclk is the watchdog clock input; because counting is modeled laz_b82a9da6]] - rationale - wdt_dml/wdt.dml
- [[signal]] - code - wdt_dml/wdt.dml
- [[signal_1]] - code - wdt_dml/wdt.dml
- [[signal_2]] - code - wdt_dml/wdt.dml
- [[signal_lower()_1]] - code - wdt_dml/wdt.dml
- [[wclk]] - code - wdt_dml/wdt.dml
- [[wclk Clock Signal]] - document - wdt_en.md
- [[wclk_en]] - code - wdt_dml/wdt.dml
- [[wclk_en Clock Gate Signal]] - document - wdt_en.md
- [[wclk_en input (clock enable) raising it resumes counting (refreshes the counter and reschedules the event when enabled); lowering it pauses the timer by cancelling the pending countdown event.]] - rationale - wdt_dml/wdt.dml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Community_7
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Community 1]]
- 4 edges to [[_COMMUNITY_Community 4]]
- 2 edges to [[_COMMUNITY_Community 3]]
- 1 edge to [[_COMMUNITY_Community 6]]
- 1 edge to [[_COMMUNITY_Community 2]]

## Top bridge nodes
- [[wclk Clock Signal]] - degree 6, connects to 2 communities
- [[signal_1]] - degree 4, connects to 2 communities
- [[wclk]] - degree 4, connects to 1 community
- [[signal]] - degree 4, connects to 1 community
- [[wclk_en]] - degree 4, connects to 1 community
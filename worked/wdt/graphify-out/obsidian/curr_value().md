---
source_file: "wdt_dml/wdt.dml"
type: "code"
community: "Community 2"
location: "L78"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Community_2
---

# curr_value()

## Connections
- [[Lazily computes the current count from the cycles elapsed since the last update, scaled by the clock divider. Returns 0 once the counter has underflowed, and the stored value while the timer _1a8c53b9]] - `rationale_for` [EXTRACTED]
- [[counter_value]] - `contains` [EXTRACTED]
- [[get_divider()]] - `calls` [INFERRED]
- [[read_register()_1]] - `calls` [INFERRED]
- [[refresh()]] - `calls` [INFERRED]
- [[write_register()_1]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Community_2
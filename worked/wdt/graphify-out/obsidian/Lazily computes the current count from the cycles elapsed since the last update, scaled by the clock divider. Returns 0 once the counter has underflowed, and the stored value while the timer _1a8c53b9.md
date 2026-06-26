---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 2"
location: "L75"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_2
---

# Lazily computes the current count from the cycles elapsed since the last update, scaled by the clock divider. Returns 0 once the counter has underflowed, and the stored value while the timer is not running.

## Connections
- [[curr_value()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_2
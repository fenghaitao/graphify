---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 2"
location: "L27"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_2
---

# Watchdog countdown event: fires when the counter reaches zero. On the first timeout it latches the interrupt and reloads the counter; on a second timeout (interrupt still pending) it asserts the reset signal when RESEN is enabled, then keeps reloading and counting.

## Connections
- [[timeout_event]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_2
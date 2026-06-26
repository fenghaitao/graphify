---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 2"
location: "L65"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_2
---

# Backing store for the watchdog down-counter. Holds the count and models it lazily: the live value is derived from elapsed cycles and the clock divider only when read, instead of being decremented every cycle.

## Connections
- [[counter_value]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_2
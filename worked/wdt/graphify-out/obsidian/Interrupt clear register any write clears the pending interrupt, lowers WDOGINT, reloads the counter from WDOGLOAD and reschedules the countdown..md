---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 5"
location: "L272"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_5
---

# Interrupt clear register: any write clears the pending interrupt, lowers WDOGINT, reloads the counter from WDOGLOAD and reschedules the countdown.

## Connections
- [[WDOGINTCLR]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_5
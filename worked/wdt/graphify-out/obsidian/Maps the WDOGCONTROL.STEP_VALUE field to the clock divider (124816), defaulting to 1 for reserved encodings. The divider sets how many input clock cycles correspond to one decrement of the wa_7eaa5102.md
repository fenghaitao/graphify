---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 2"
location: "L111"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_2
---

# Maps the WDOGCONTROL.STEP_VALUE field to the clock divider (1/2/4/8/16), defaulting to 1 for reserved encodings. The divider sets how many input clock cycles correspond to one decrement of the watchdog counter.

## Connections
- [[get_divider()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_2
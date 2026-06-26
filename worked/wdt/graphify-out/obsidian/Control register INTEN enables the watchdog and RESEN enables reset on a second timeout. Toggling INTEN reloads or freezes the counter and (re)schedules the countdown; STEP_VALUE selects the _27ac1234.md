---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 3"
location: "L216"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_3
---

# Control register: INTEN enables the watchdog and RESEN enables reset on a second timeout. Toggling INTEN reloads or freezes the counter and (re)schedules the countdown; STEP_VALUE selects the clock divider.

## Connections
- [[WDOGCONTROL]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_3
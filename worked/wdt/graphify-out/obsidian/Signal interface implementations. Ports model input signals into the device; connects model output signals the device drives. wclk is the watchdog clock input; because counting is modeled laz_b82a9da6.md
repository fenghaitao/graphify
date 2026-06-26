---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 7"
location: "L489"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_7
---

# Signal interface implementations. Ports model input signals into the device; connects model output signals the device drives. wclk is the watchdog clock input; because counting is modeled lazily, its edges need no handling.

## Connections
- [[wclk]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_7
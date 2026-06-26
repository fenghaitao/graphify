---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 8"
location: "L313"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_8
---

# Lock register: writing the magic value 0x1ACCE551 unlocks the device; any other write locks it. Reads return 1 when locked, 0 when unlocked.

## Connections
- [[WDOGLOCK]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_8
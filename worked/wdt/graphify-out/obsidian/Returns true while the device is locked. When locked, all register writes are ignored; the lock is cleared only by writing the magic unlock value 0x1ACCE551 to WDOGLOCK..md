---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 6"
location: "L58"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_6
---

# Returns true while the device is locked. When locked, all register writes are ignored; the lock is cleared only by writing the magic unlock value 0x1ACCE551 to WDOGLOCK.

## Connections
- [[is_device_locked()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_6
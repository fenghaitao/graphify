---
source_file: "wdt_dml/wdt.dml"
type: "code"
community: "Community 6"
location: "L61"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Community_6
---

# is_device_locked()

## Connections
- [[Returns true while the device is locked. When locked, all register writes are ignored; the lock is cleared only by writing the magic unlock value 0x1ACCE551 to WDOGLOCK.]] - `rationale_for` [EXTRACTED]
- [[wdt.dml]] - `contains` [EXTRACTED]
- [[write_register()_1]] - `calls` [INFERRED]
- [[write_register()_2]] - `calls` [INFERRED]
- [[write_register()_4]] - `calls` [INFERRED]
- [[write_register()_5]] - `calls` [INFERRED]
- [[write_register()]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Community_6
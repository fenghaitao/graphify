---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 5"
location: "L186"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_5
---

# Load register: the value reloaded into the counter on each timeout and on interrupt clear. Writes are ignored while locked and do not reload the counter immediately unless INTEN transitions 0->1.

## Connections
- [[WDOGLOAD]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_5
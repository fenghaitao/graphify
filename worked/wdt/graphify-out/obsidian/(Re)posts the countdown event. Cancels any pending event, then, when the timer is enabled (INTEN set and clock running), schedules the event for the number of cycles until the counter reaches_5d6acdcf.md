---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 2"
location: "L124"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_2
---

# (Re)posts the countdown event. Cancels any pending event, then, when the timer is enabled (INTEN set and clock running), schedules the event for the number of cycles until the counter reaches zero (remaining count * divider).

## Connections
- [[schedule_timeout()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_2
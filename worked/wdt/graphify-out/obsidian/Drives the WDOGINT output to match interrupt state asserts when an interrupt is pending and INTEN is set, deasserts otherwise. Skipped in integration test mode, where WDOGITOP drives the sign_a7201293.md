---
source_file: "wdt_dml/wdt.dml"
type: "rationale"
community: "Community 2"
location: "L140"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_2
---

# Drives the WDOGINT output to match interrupt state: asserts when an interrupt is pending and INTEN is set, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the signal directly.

## Connections
- [[update_interrupt_signal()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_2
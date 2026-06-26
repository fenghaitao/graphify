---
source_file: "wdt_dml/wdt.dml"
type: "code"
community: "Community 1"
location: "L143"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Community_1
---

# update_interrupt_signal()

## Connections
- [[Drives the WDOGINT output to match interrupt state asserts when an interrupt is pending and INTEN is set, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the sign_a7201293]] - `rationale_for` [EXTRACTED]
- [[event()]] - `calls` [INFERRED]
- [[signal_lower()]] - `calls` [INFERRED]
- [[signal_raise()]] - `calls` [INFERRED]
- [[wdt.dml]] - `contains` [EXTRACTED]
- [[write_register()_1]] - `calls` [INFERRED]
- [[write_register()_2]] - `calls` [INFERRED]
- [[write_register()_4]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Community_1
---
source_file: "wdt_dml/wdt.dml"
type: "code"
community: "Community 3"
location: "L165"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Community_3
---

# update_reset_signal()

## Connections
- [[Drives the WDOGRES output to match reset state asserts when a reset is pending, deasserts otherwise. Skipped in integration test mode, where WDOGITOP drives the signal directly.]] - `rationale_for` [EXTRACTED]
- [[event()]] - `calls` [INFERRED]
- [[signal_lower()]] - `calls` [INFERRED]
- [[signal_raise()]] - `calls` [INFERRED]
- [[wdt.dml]] - `contains` [EXTRACTED]
- [[write_register()_4]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/Community_3
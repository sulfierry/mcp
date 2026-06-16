---
description: Show the current state of the GMMSB machine fleet.
---

1. Call `list_machines` to get the inventory.
2. For each machine that isn't `skipped`, also call `rank_machines_for_tool`
   for a representative tool (the first one registered) — this triggers a
   live probe. If the user asked about a specific tool, use that one
   instead.
3. Render a single table with: machine, status (online/offline), GPU model,
   free VRAM, CPU load, free RAM, tools installed (with provenance).
4. Highlight any machine where SSH is failing or where every required tool
   would fail to fit (low free VRAM, high load).

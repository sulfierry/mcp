---
description: Run a GMMSB tool on a remote machine, with the full plan-confirm-submit-follow loop.
argument-hint: <tool> [free-form description of inputs]
---

The user wants to run **$1** with the following intent:

> $ARGUMENTS

Follow the workflow from the `gmmsb-toolkit` skill exactly:

1. Call `describe_tool("$1")` to get the input schema.
2. Match what the user wrote to required fields. Ask only about what's missing.
3. Echo the resolved inputs back and ask for confirmation.
4. Call `rank_machines_for_tool("$1")`. Show the top 3 candidates.
   - If `no_install_anywhere`, do not proceed — explain and offer to draft
     a request to the admin.
5. Default to the top-ranked machine unless the user picked one.
6. Call `submit_job({tool: "$1", inputs: <resolved>, machine: <chosen>,
   input_paths: [<absolute paths>]})`.
7. Poll `job_status(id)` until status leaves `running`. Surface log tail on
   change.
8. On `completed`, call `fetch_job(id)` and walk through `summary`.
9. On `failed`, show the log tail and any `error` field. Do not retry on
   your own.

---
name: gmmsb-toolkit
description: Use when the user asks to run a GMMSB-supported molecular-modelling tool (DockThor, DockTDeep, AlphaFold, Boltz-2, ...) on a remote machine — or anything like "dock these ligands", "predict the structure of X", "screen a library against Y". Drives the gmmsb MCP server (list_tools_registered, describe_tool, tool_input_template, rank_machines_for_tool, submit_job, job_status, fetch_job) end-to-end.
category: cheminformatics
tags: [gmmsb, docking, structure-prediction, remote-jobs, molecular-modelling, mcp]
license: MIT
source: gmmsb-agent-toolkit
---

# GMMSB Toolkit

The user is part of GMMSB. They want to run a molecular-modelling tool on one of
the group's remote GPU/CPU workstations without leaving the chat. This skill
drives the `gmmsb` MCP server to do that.

> **Dependency:** requires the external `gmmsb` MCP server (from
> [gmmsb-agent-toolkit](https://github.com/gmmsb-lncc/gmmsb-agent-toolkit)) to be
> registered. See [`docs/EXTERNAL-MCPS.md`](../../docs/EXTERNAL-MCPS.md).

## When to use

- "Run Boltz-2 on this FASTA."
- "Predict the structure of this sequence."
- "Dock these ligands against that PDB."
- "Screen this library on workstation-03."
- "What tools can I run?" / "Which machines are free for AlphaFold?"

## Workflow (do not skip steps)

1. **Identify the tool.** If the user names one directly, use it. Otherwise call
   `list_tools_registered` and ask which one fits the task.
2. **Get the input schema.** Call `describe_tool(name)`. Read `inputs_schema`
   and figure out which required inputs are missing from the user's message.
   Ask only for what's missing — do not make the user repeat themselves.
   For tools with many parameters where the user wants to review the whole
   knob set before submitting, call `tool_input_template(name)` instead and
   show them the scaffold (defaults pre-filled, must-fill-in fields on
   top); they can edit it and you can parse it back into `inputs`.
3. **Show the plan.** Echo the resolved inputs, the tool requirements
   (GPU VRAM, cores, RAM), and a one-sentence summary of what will happen.
   Ask the user to confirm before submitting. Research jobs cost GPU-hours.
4. **Rank machines.** Call `rank_machines_for_tool(name)`. Show the user the
   top 3 candidates with their GPU/free-VRAM/load info. If a machine is
   marked "auto", the user will probably say "just pick one" — go with the
   top-ranked.
5. **Submit.** Call `submit_job({tool, inputs, machine, input_paths})`.
   - `input_paths` should hold absolute local paths to any files the user
     referenced. Resolve relative paths against their current directory.
   - The call returns immediately with a job ID and `status=running`.
6. **Follow.** Poll `job_status(id)` every ~10 seconds and surface the tail
   of the log to the user when it changes. When `status` becomes
   `completed` or `failed`, stop polling and either:
   - call `fetch_job(id)` to ensure outputs are local and get the final
     `summary`; or
   - if `failed`, show the user the log tail and any `error`.
7. **Summarise & offer follow-ups.** Walk the user through `summary` (output
   paths, key metrics). Suggest natural next steps (open a file, chain
   another tool).
8. **Offer remote cleanup.** Once outputs are local (after `fetch_job`),
   ask the user: *"results are saved locally — delete the remote workdir
   on `<machine>`? (recommended)"*. If they say yes, call
   `cleanup_remote_job(job_id)`. Default to asking — never delete silently.
   If the user always wants cleanup, suggest they add it as a habit; the
   toolkit doesn't yet have a global config flag for it.

## What you must NOT do

- Do not run `gmmsb init-agent`, `gmmsb machine override`, `gmmsb tool install`,
  `ssh-copy-id`, or any other credential-touching command yourself. Print
  the command and let the user run it.
- Do not invent machine names, IPs, or paths. Always read from the MCP
  responses.
- Do not submit a job without showing the resolved inputs to the user first.
- Do not auto-retry failures.

## Tool provenance

`describe_tool` and `list_machines` surface a `provenance` per tool-on-machine:

- `managed` — installed by the toolkit; we could re-install it.
- `admin` — installed by a sysadmin (licenses, weights, in-house code).
- `user` — installed by the user themselves.

If the requested tool isn't installed anywhere, `rank_machines_for_tool`
returns `no_install_anywhere: true` with `advice`. Relay that to the user
and offer to draft a message they can send to the admin.

## Quick reference

| Need to know…                 | Call this                              |
|-------------------------------|----------------------------------------|
| What tools exist              | `list_tools_registered`                |
| A tool's inputs & requirements | `describe_tool(name)`                  |
| Editable scaffold of a tool's inputs | `tool_input_template(name)`     |
| Which machines exist          | `list_machines`                        |
| Where to run a tool right now | `rank_machines_for_tool(name)`         |
| Start a job                   | `submit_job({...})`                    |
| Job state + log tail          | `job_status(id)`                       |
| Wait for it & get summary     | `fetch_job(id)`                        |

## Related

- `job-runner` agent — babysits a single long-running job to completion.

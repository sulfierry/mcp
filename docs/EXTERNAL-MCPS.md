# External MCP servers

`server/external_mcps/` hosts vendored third-party MCP servers that expose domain-specific tools (not general skill retrieval).

## Layout

```
server/external_mcps/
└── blatant_why/                      # vendored from 001TMF/blatant-why (MIT)
    ├── README.md
    ├── _shared/                       # base helpers, imported by others
    ├── pdb/server.py                  # RCSB PDB REST (5 tools)
    ├── uniprot/server.py              # UniProt REST (4 tools)
    ├── sabdab/server.py               # SAbDab antibody DB (4 tools)
    ├── tamarind/server.py             # Tamarind Bio compute (10 tools)
    ├── adaptyv/server.py              # Adaptyv lab testing (5 tools)
    ├── research/server.py             # PubMed + bioRxiv + PDB + UniProt + SAbDab (5 tools)
    └── knowledge/server.py            # campaign knowledge base (6 tools)
```

Each subdir is a standalone MCP server with PEP 723 inline script deps — invoked via `uv run --script`.

## Free servers (no API key)

| Server | Endpoints |
|--------|-----------|
| `pdb` | RCSB PDB search, core/entry fetch, file download |
| `uniprot` | rest.uniprot.org (sequence + metadata) |
| `sabdab` | Oxford OPIG antibody DB (scraped; 24h cache) |
| `research` | aggregates PubMed, bioRxiv, PDB, UniProt, SAbDab |
| `knowledge` | local project knowledge (requires `KNOWLEDGE_DIR`) |

## API-gated

| Server | Env var | Where to get |
|--------|---------|--------------|
| `tamarind` | `TAMARIND_API_KEY` | tamarind.bio free tier, 10 jobs/month |
| `adaptyv` | `ADAPTYV_API_TOKEN` | adaptyvbio.com |

## Register individually

```bash
BW="$(pwd)/server/external_mcps/blatant_why"
claude mcp add --scope user bw-pdb       uv run --script $BW/pdb/server.py
claude mcp add --scope user bw-uniprot   uv run --script $BW/uniprot/server.py
claude mcp add --scope user bw-research  uv run --script $BW/research/server.py
claude mcp add --scope user bw-sabdab    uv run --script $BW/sabdab/server.py
```

Prereq: `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

## Token cost

Each registered server adds its tool schemas to every assistant session.

- `pdb`: 5 tools (~500 tokens)
- `uniprot`: 4 tools (~400)
- `sabdab`: 4 tools (~400)
- `research`: 5 tools (~500)
- `tamarind`: 10 tools (~1000)

Scope-register (not user-scope) to pay the cost only in relevant directories. Example in `mol-scope/.mcp.json`.

## Project scope example

`~/work/mol-scope/.mcp.json` registers three free servers (pdb, uniprot, research) at project scope — loaded only when `cd ~/work/mol-scope/` before launching an assistant. See [`SCOPES.md`](SCOPES.md).

## Updating vendored code

`scripts/sync_skills.sh` includes `sync_blatant_why()` which re-pulls:

```bash
./scripts/sync_skills.sh --force     # re-syncs, overwrites
```

Upstream changes propagate on next sync.

## License

Each vendored server carries upstream license (blatant-why: MIT). Root `server/external_mcps/<project>/README.md` mirrors upstream license file when present.

## Adding a new external MCP

1. `mkdir server/external_mcps/<name>/`
2. Drop `server.py` (PEP 723 header or pyproject) + `README.md`
3. Document env vars + registration in README
4. Optionally add sync function in `scripts/sync_skills.sh` for reproducibility

## Referenced (not vendored)

Some skills/agents drive an external MCP server that lives in its own package
rather than under `server/external_mcps/`. They are documented here but not
shipped in this repo — the user installs and registers them separately.

| Server | Package | Drives | Skills / agents |
|--------|---------|--------|-----------------|
| `gmmsb` | `gmmsb-mcp` ([gmmsb-agent-toolkit](https://github.com/gmmsb-lncc/gmmsb-agent-toolkit)) | Run molecular-modelling tools (DockThor, DockTDeep, AlphaFold, Boltz-2, …) on the lab's remote GPU/CPU fleet over SSH + Docker | `gmmsb-toolkit` skill, `job-runner` agent, `commands/gmmsb-*` |

### gmmsb registration

```bash
pipx install gmmsb-mcp        # or: uv tool install gmmsb-mcp
claude mcp add --scope user gmmsb gmmsb-mcp
gmmsb init-agent              # SSH key + machine wire-up (run by the user)
```

Tools exposed: `list_tools_registered`, `describe_tool`, `tool_input_template`,
`list_machines`, `rank_machines_for_tool`, `submit_job`, `job_status`,
`fetch_job`, `cleanup_remote_job`. The `gmmsb-toolkit` skill and `job-runner`
agent are inert without this server registered.

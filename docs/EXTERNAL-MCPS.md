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

# Blatant-Why External MCP Servers

Protein design / antibody workflow MCP servers vendored from
[001TMF/blatant-why](https://github.com/001TMF/blatant-why) (MIT License).

Each subdirectory is a standalone MCP server (`server.py` + `__init__.py`) using
PEP 723 inline script dependencies — invoke via `uv run --script`.

## Servers

| Server        | Purpose                                                    | Auth |
|---------------|------------------------------------------------------------|------|
| `pdb`         | RCSB PDB lookup, structure fetch                           | none |
| `uniprot`     | UniProt sequence/metadata fetch                            | none |
| `sabdab`      | SAbDab antibody database                                   | none |
| `tamarind`    | Tamarind Bio compute (BoltzGen, Protenix, PXDesign, etc.)  | `TAMARIND_API_KEY` |
| `adaptyv`     | Adaptyv lab testing submission                             | `ADAPTYV_API_TOKEN` |
| `research`    | Literature / prior-art research                            | none |
| `knowledge`   | Campaign knowledge base                                    | none |
| `_shared`     | Common helpers (imported by other servers)                 | —    |

## Registering with Claude Code

Each server must be registered individually. Example for `pdb`:

```bash
claude mcp add --scope user bw-pdb \
  /Users/sulfierry/mcp/server/external_mcps/blatant_why/pdb/server.py
```

Or via `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "bw-pdb":    { "command": "uv", "args": ["run", "--script",
        "/Users/sulfierry/mcp/server/external_mcps/blatant_why/pdb/server.py"] },
    "bw-uniprot":{ "command": "uv", "args": ["run", "--script",
        "/Users/sulfierry/mcp/server/external_mcps/blatant_why/uniprot/server.py"] },
    "bw-sabdab": { "command": "uv", "args": ["run", "--script",
        "/Users/sulfierry/mcp/server/external_mcps/blatant_why/sabdab/server.py"] },
    "bw-tamarind":{"command": "uv", "args": ["run", "--script",
        "/Users/sulfierry/mcp/server/external_mcps/blatant_why/tamarind/server.py"],
      "env": { "TAMARIND_API_KEY": "<your-key>" } },
    "bw-adaptyv":{"command": "uv", "args": ["run", "--script",
        "/Users/sulfierry/mcp/server/external_mcps/blatant_why/adaptyv/server.py"],
      "env": { "ADAPTYV_API_TOKEN": "<your-token>" } }
  }
}
```

`uv` required: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Token cost

Registering N external MCP servers adds N tool schemas to the always-loaded
context. Only register the ones you actively use in a session. `pdb` + `uniprot`
+ `sabdab` are safe defaults (no API keys, read-only public DBs).

## Updating

```
./scripts/sync_skills.sh --force
```

Will re-clone `001TMF/blatant-why` and overwrite these dirs.

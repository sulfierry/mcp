# Sync

`scripts/sync_skills.sh` pulls curated skills from upstream repositories and (re)configures your assistants' MCP settings.

## Usage

```bash
./scripts/sync_skills.sh              # curated sync (recommended)
./scripts/sync_skills.sh --all        # pull every skill from every source
./scripts/sync_skills.sh --force      # overwrite existing skill dirs
./scripts/sync_skills.sh --list       # show available source repos
```

Flags compose: `./scripts/sync_skills.sh --all --force`.

## Source repositories

| Repo | Curation | Focus |
|------|----------|-------|
| `ClawBio/ClawBio` | all | bioinformatics + pharma (~47) |
| `K-Dense-AI/scientific-agent-skills` | all | scientific skills (~134) |
| `GPTomics/bioSkills` | nested scan | bioinformatics (~438) |
| `jaechang-hits/SciAgent-Skills` | nested scan | scientific (~197) |
| `K-Dense-AI/claude-scientific-writer` | curated | writing |
| `zhangchenhaobest/academic-research-skills` | curated | academic |
| `VoltAgent/awesome-claude-code-subagents` (⭐16K) | curated | 100+ subagents |
| `tech-leads-club/agent-skills` (⭐2K) | all | skills catalog |
| `guanyang/antigravity-skills` | curated | Antigravity |
| `rmyndharis/antigravity-skills` | curated | Antigravity |
| `safishamsi/graphify` (v4) | single-file | code/knowledge graph |
| `001TMF/blatant-why` | curated | protein-design stack + MCP servers |

Curated subsets defined at top of `sync_skills.sh` (e.g., `CURATED_VOLTAGENT`, `CURATED_GUANYANG`, `CURATED_WRITING`, `CURATED_ACADEMIC`).

## Phases

1. **Sync** — clone/pull each source into `tmp_sync/`, copy skills into `skills/`.
2. **Merge agents** — `agents/*` copied into `skills/` for universal discovery.
3. **IDE symlinks** — `skills/` linked into `~/.claude/skills`, `~/.codex/skills`, `~/.qwen/skills`, `.github/skills` (VS Code), `~/.gemini/antigravity/skills`.
4. **MCP server config** — injects `skills-server` entry into each IDE's MCP config (Claude Code, Copilot CLI, VS Code, Cursor, Qwen, Claude Desktop, Antigravity).
5. **Catalog** — runs `scripts/build_catalog.py` to regenerate `skills_index.json`.

## Opt-out flags

### `SKIP_CLAUDE_USER_SCOPE=1`
Skip user-scope registration in Claude Code + Copilot CLI. Use when you rely exclusively on project-scope `.mcp.json` (see [`SCOPES.md`](SCOPES.md)):

```bash
SKIP_CLAUDE_USER_SCOPE=1 ./scripts/sync_skills.sh
```

Set permanently in `~/.zshrc` if you always run scoped.

## Idempotency

- Skill dirs are only copied if missing (unless `--force`).
- MCP config injections check for existing `skills-server` entry and skip if present.
- Symlinks are recreated only when pointing elsewhere.
- Catalog rebuild is always run (cheap, ~150 ms).

Safe to re-run anytime.

## Adding a new source

Edit `scripts/sync_skills.sh`:

1. Add `clone_and_sync "<owner>/<repo>" "<git-url>" "<subdir>" "$CURATED_LIST"` or `clone_and_sync_nested` for nested repos.
2. Optionally define a new `CURATED_*` constant.
3. Test with `--list` to confirm display.

For single-file sources (like graphify), follow the `sync_graphify()` function pattern using curl.

## Cache

`tmp_sync/` holds shallow clones reused across runs. `git pull` is performed each sync. To force fresh clone: `rm -rf tmp_sync/<repo-dir>` then rerun.

## Exit codes

- `0` — success
- non-zero — network / git failure (script continues past individual source failures with warnings)

## Logs

Sync prints colored status per skill. Skip noise:
```bash
./scripts/sync_skills.sh 2>&1 | grep -E '✓|⚠|❌'
```

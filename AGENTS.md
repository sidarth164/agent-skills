# AGENTS.md

## Project overview

This repository collects and maintains Agent Skills — self-contained folders of instructions, scripts, and resources that AI coding agents load dynamically to improve at specialized tasks. Each skill follows the [Agent Skills Specification](https://agentskills.io/specification).

## Repository layout

```
agent-skills/
├── skills/                  # One subdirectory per skill
│   └── <skill-name>/
│       ├── SKILL.md         # Required: instructions + YAML frontmatter
│       ├── evals/
│       │   └── trigger-evals.json   # Optional: trigger quality evals
│       ├── scripts/         # Optional: agent-callable scripts
│       ├── references/      # Optional: reference docs loaded on demand
│       └── assets/          # Optional: templates and static files
├── scripts/                 # Repo-level tooling
│   ├── install.sh           # Symlink skills into ~/.claude/skills/
│   └── uninstall.sh         # Remove symlinks
├── tests/                   # Eval suite
│   ├── conftest.py          # Skill discovery and pytest fixtures
│   ├── test_structure.py    # Layer 1: structural validation
│   └── test_trigger.py      # Layer 2: trigger quality evals
├── pyproject.toml           # Python deps and pytest config
└── uv.lock                  # Locked dependencies
```

## Build and test

There is no build step. Skills are plain Markdown plus optional scripts.

### Install skills

```bash
./scripts/install.sh          # symlink all skills into ~/.claude/skills/
./scripts/install.sh gitbook-docs   # symlink a single skill
./scripts/uninstall.sh        # remove all symlinks from this repo
```

### Run evals

```bash
uv run pytest                         # all tests
uv run pytest -m structure            # structure validation only (no API key needed)
uv run pytest -m trigger              # trigger evals (requires ANTHROPIC_API_KEY)
uv run pytest --skill gitbook-docs    # all tests for one skill
uv run pytest -m trigger -n 5         # trigger evals in parallel
```

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` with required YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: What the skill does and when to trigger it.
   ---
   ```
2. Add any supporting files in `scripts/`, `references/`, or `assets/` subdirectories within the skill folder.
3. Run `./scripts/install.sh` to symlink into `~/.claude/skills/`.

## Adding evals for a skill

Create `skills/<skill-name>/evals/trigger-evals.json`. The test suite discovers it automatically.

```json
[
  {"query": "a realistic prompt that should invoke the skill", "should_trigger": true},
  {"query": "a near-miss prompt that should not invoke the skill", "should_trigger": false}
]
```

**Writing good trigger evals:**
- `should_trigger: true` — express the documentation/task need without referencing specific files that would need to exist in the test workspace. Test organic triggering, not just explicit skill-name mentions.
- `should_trigger: false` — use near-misses: adjacent domains, same keywords in the wrong context, or tasks the skill explicitly skips. Avoid obviously irrelevant queries.
- Keep queries realistic: include specific context (tech stacks, tool names, scenarios) as a real user would write them.

## Eval architecture

The eval suite has two layers:

**Layer 1 — Structure** (`test_structure.py`): validates every skill using `skills-ref`. No API calls, runs on every commit.

**Layer 2 — Trigger** (`test_trigger.py`): for each query in `trigger-evals.json`, spawns an isolated `claude -p` process with only that skill loaded (`CLAUDE_CONFIG_DIR` pointing to a fresh temp directory seeded from `tests/.claude-template/`). Detects whether Claude invokes the `Skill` tool for that skill and asserts it matches `should_trigger`.

Failed trigger tests write a `raw.ndjson` transcript to `.pytest-artifacts/` for inspection:

```bash
# View what Claude did during a failing test
jq 'select(.type == "result")' .pytest-artifacts/<test-dir>/raw.ndjson
jq 'select(.type == "stream_event") | .event | select(.type == "content_block_delta") | .delta | select(.type == "thinking_delta") | .thinking' .pytest-artifacts/<test-dir>/raw.ndjson
```

## Code style and conventions

- Skill names use lowercase kebab-case (e.g., `mcp-builder`, `plan-design-build`).
- Keep `SKILL.md` under 500 lines. Move detailed reference material to `references/` and link from `SKILL.md`.
- Scripts can be in any language; Python and Bash are most common in this repo.
- Do not hardcode secrets or API keys in any skill file.
- Scripts bundled inside a skill (under `skills/<name>/scripts/`) are agent tools — they are invoked by Claude as part of using that skill, not by developers directly.

## Commit conventions

- Use conventional commit messages (e.g., `feat(mcp-builder): add pagination helper`).
- One skill per commit when possible.

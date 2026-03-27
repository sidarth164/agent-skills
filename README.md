# Agent Skills

Collection of [Agent Skills](https://agentskills.io/specification) — curated instructions, scripts, and resources that extend AI coding agents with specialized capabilities.

Skills follow the open [Agent Skills Specification](https://agentskills.io/specification) and work with any compatible agent.

## Setup

Symlink all skills into `~/.claude/skills/`:

```bash
./scripts/install.sh
```

To remove symlinks (without deleting skills from this repo):

```bash
./scripts/uninstall.sh
```

## Adding a New Skill

1. Create a new directory under `skills/`:
   ```
   skills/my-new-skill/
   └── SKILL.md        # Required: instructions + YAML frontmatter
   ```
2. Run `./scripts/install.sh` to symlink it.

Each skill directory can also include `scripts/`, `references/`, `assets/`, and other bundled resources.

## Testing

This repo has a pytest-based eval suite covering two layers:

| Layer | What it tests | Command |
|---|---|---|
| Structure | Every skill has valid `SKILL.md` frontmatter | `uv run pytest -m structure` |
| Trigger | Skills invoke (or don't) for the right prompts | `uv run pytest -m trigger` |

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Test a single skill
uv run pytest --skill gitbook-docs
```

Trigger tests require `ANTHROPIC_API_KEY` to be set. Structure tests have no external dependencies.

### Adding evals for a skill

Create `skills/<skill-name>/evals/trigger-evals.json`:

```json
[
  {"query": "a realistic prompt that should invoke the skill", "should_trigger": true},
  {"query": "a near-miss prompt that should not invoke the skill", "should_trigger": false}
]
```

The test suite discovers this file automatically — no registration needed.

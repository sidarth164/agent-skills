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

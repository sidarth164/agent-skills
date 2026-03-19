# AGENTS.md

## Project overview

This repository collects and maintains Agent Skills — self-contained folders of instructions, scripts, and resources that AI coding agents load dynamically to improve at specialized tasks. Each skill follows the [Agent Skills Specification](https://agentskills.io/specification).

## Repository layout

- `skills/` — Each subdirectory is a standalone skill. Every skill **must** contain a `SKILL.md` with YAML frontmatter (`name`, `description`). May also contain `scripts/`, `references/`, `assets/`, and other bundled resources.
- `scripts/` — Repo-level tooling (`install.sh`, `uninstall.sh`) for symlinking skills into `~/.claude/skills/`.

## Build and test

There is no build step. Skills are plain Markdown + optional scripts.

To install all skills (symlink into `~/.claude/skills/`):

```
./scripts/install.sh
```

To remove symlinks:

```
./scripts/uninstall.sh
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

## Code style and conventions

- Skill names use lowercase kebab-case (e.g., `mcp-builder`, `plan-design-build`).
- Keep `SKILL.md` under 500 lines. Move detailed reference material to `references/` and link from `SKILL.md`.
- Scripts can be in any language; Python and Bash are most common in this repo.
- Do not hardcode secrets or API keys in any skill file.

## Testing skills

There is no automated test suite yet. Individual skills may include their own eval tooling. Eval workspaces are created per-skill as sibling directories (e.g., `<skill-name>-workspace/`).

## Commit conventions

- Use conventional commit messages (e.g., `feat(mcp-builder): add pagination helper`).
- One skill per commit when possible.

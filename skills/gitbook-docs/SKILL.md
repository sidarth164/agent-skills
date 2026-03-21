---
name: gitbook-docs
description: >-
  Opinionated skill for setting up, migrating, and maintaining GitBook project documentation
  that lives alongside code. Use this whenever a project needs documentation — whether initializing
  docs for a repo that has none, migrating existing docs (mdBook, scattered markdown) into GitBook,
  restructuring a README, authoring new pages, or updating docs after code changes. Trigger on
  requests involving GitBook setup, SUMMARY.md, .gitbook.yaml, doc structure, architecture docs,
  README restructuring, or any mention of project documentation.
---

# GitBook Documentation Skill

This skill manages project documentation using GitBook, with an opinionated structure optimized
for both human developers and AI agent consumption. GitBook auto-generates `llms.txt`, an MCP
server, and markdown endpoints from your published docs — your job is writing well-structured
content in the repo.

## Modes

### 1. Init — Scaffold docs for a project

Analyze the codebase (language, structure, existing docs, dependencies) and generate
the scaffolding. Fill in project-specific content by analyzing the project's manifest
files, existing READMEs, code structure, and dependency graphs.

Use these templates as starting points, reading each before creating the corresponding file:

- `assets/templates/gitbook.yaml` → `.gitbook.yaml` at repo root
- `assets/templates/vars.yaml` → `docs/.gitbook/vars.yaml`
- `assets/templates/SUMMARY.md` → `docs/SUMMARY.md`
- `assets/templates/pages/README.md` → root `README.md` (restructure if one exists)
- `assets/templates/pages/architecture-overview.md` → `docs/architecture/README.md`
- `assets/templates/pages/architecture-subsystem.md` → one per subsystem identified
- `assets/templates/pages/getting-started.md` → `docs/getting-started/README.md`
- `assets/templates/pages/development-setup.md` → `docs/getting-started/development-setup.md`
- `assets/templates/pages/CONTRIBUTING.md` → `docs/guides/CONTRIBUTING.md`
- `assets/templates/pages/troubleshooting.md` → `docs/operations/troubleshooting.md`

Not every project needs every section. Recommend sections based on what you find:
- **Libraries/tools**: skip `operations/`
- **Services**: include everything
- **GitOps/infra repos**: thin `architecture/`, heavy `operations/`
- **Monorepo with multiple packages**: explain organization in architecture subsystem pages

### 2. Migrate — Convert existing docs to GitBook

Detect existing documentation systems and convert:

- **mdBook** (`book.toml`, `src/SUMMARY.md`): Map chapters to GitBook pages, convert mdBook
  syntax to GitBook custom blocks
- **Plain `docs/` directory**: Reorganize into the standard structure, add SUMMARY.md
- **Scattered READMEs**: Consolidate into proper sections, replace originals with links
- **Inline code docs**: Extract architectural knowledge into `architecture/` pages

When restructuring a README, follow the format in `assets/templates/pages/README.md`.
Use the page templates from `assets/templates/pages/` when creating new pages during
migration. Read `references/custom-blocks.md` for GitBook syntax when converting from
other formats.

Preserve all existing content — reorganize and restructure, don't delete.

### 3. Author — Create or update pages

When writing or editing documentation pages:

- Use the relevant template from `assets/templates/pages/` when creating a new page
- Use GitBook custom block syntax for rich content (read `references/custom-blocks.md`)
- Add frontmatter with `description` on every page (feeds into `llms.txt`)
- Make each page self-contained enough that an agent reading just that page gets actionable info
- Use clear, descriptive headings — agents navigate by heading
- Cross-link related pages to give GitBook's MCP server richer context
- Keep pages focused: one topic per page, not mega-pages

---

## Standard Project Structure

```
repo-root/
  .gitbook.yaml                # root: ./, summary: docs/SUMMARY.md
  README.md                    # Project homepage (GitHub + GitBook)
  docs/
    .gitbook/
      vars.yaml                # Project metadata
    SUMMARY.md                 # Navigation (paths relative to this file's location)
    getting-started/
      README.md                # Quick start — clone, build, run
      development-setup.md     # Full dev environment setup
    architecture/
      README.md                # System overview — component map, tech stack, how it all fits
      authentication.md        # Example: one page per major subsystem
      api-gateway.md           # Example: pages are project-specific, not prescribed
      ...
    guides/
      CONTRIBUTING.md          # PR process, code style, testing expectations
    operations/                # Only for projects that run as services
      troubleshooting.md       # Common failures and diagnosis
```

---

## Architecture Docs — The Priority

The `architecture/` section is the highest-value documentation for AI agents. Be aggressive
about generating these from code analysis:

### architecture/README.md (System Overview)
The overview page is the map. It should contain:
- What the project does in 2-3 paragraphs
- Where it fits in the broader system (upstream/downstream services)
- A component map — the major subsystems, their responsibilities, and how they relate
- Key technologies and frameworks used
- Links to each subsystem deep-dive page

This page should help a reader (or agent) understand the system at a glance and know
which subsystem page to read next for details.

### Subsystem Pages
The skill does not prescribe which subsystem pages to create — that depends entirely
on the project. Analyze the codebase to identify the major subsystems/topics that
deserve their own page, then create one page per subsystem.

Use the template in `assets/templates/pages/architecture-subsystem.md`. Each page covers:
- **Code** — which crates/modules/packages this page describes
- **Key Concepts** (optional) — domain-specific abstractions needed to understand the code
- **Component / Stage sections** — one per major component or pipeline stage, as deep as
  needed. This is the core of the page.
- **Interfaces** (optional) — public API surface, when consumed by multiple other subsystems
- **Testing** (optional) — notable testing patterns specific to this subsystem
- **Design Decisions** — key architectural choices and reasoning, inline

Name the files after the subsystem they describe. Each page should be self-contained —
a developer or agent reading just that page should be able to understand and work on
that subsystem.

When analyzing a codebase for init, look for implicit design decisions in the code and
document them in the appropriate subsystem page.

---

## AI-Native Documentation Principles

These docs will be consumed by AI agents via GitBook's auto-generated MCP server. Structure
content so agents can find and use it effectively:

1. **Frontmatter `description` on every page** — this is what appears in `llms.txt` and helps
   agents decide which page to read
2. **Self-contained pages** — an agent reading one page should get actionable information
   without needing to read five other pages first
3. **Clear headings** — agents scan headings to find relevant sections; be specific
   ("PostgreSQL Connection Configuration" not "Setup")
4. **Cross-link related pages** — helps the MCP server provide richer context when answering
   questions
5. **One topic per page** — don't combine unrelated content; a focused page is easier for
   agents to retrieve and reason about
6. **Explicit over implicit** — spell out configuration values, expected formats, and
   environment variables rather than saying "see the code"

---

## Reference Files

- **`references/custom-blocks.md`** — Full syntax for GitBook custom blocks (tabs, stepper,
  hints, expandable, columns, updates, cards, embeds, files, buttons, icons, reusable content,
  OpenAPI). Read this when authoring pages with rich formatting.

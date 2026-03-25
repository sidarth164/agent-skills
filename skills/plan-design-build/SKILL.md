---
name: plan-design-build
description: >-
  Structured methodology for engineering tasks that span multiple components and require upfront
  design decisions. Use when the user asks to build a new system from scratch, architect or
  design before implementing, or migrate between architectures — or when they say "plan",
  "design", "architect", or "think through". Skip for bug fixes, single-file changes, routine
  refactors, or tasks the user prefaces with "just" or "quickly".
---

# Plan, Design, Build

Skip for: bug fixes, single-file changes, features with an obvious path. If the user says "just do it", respect that.

## Setup

At the start of the project, create `<PROJECT>_PLAN.md` at the project root from `assets/PLAN_TEMPLATE.md`. This document is the single source of truth — fill each section as you progress. The WORKING RULES block and inline notes encode where everything belongs; do not remove them.

**Returning mid-session:** re-read `<PROJECT>_PLAN.md` before acting.

## Gates

Do not proceed past a gate without explicit user sign-off. A checkpoint means: produce a written artifact, present it clearly, wait for approval — don't bundle questions and proceed on a partial answer.

- **Gate 1** — Share research summary before any design decisions
- **Gate 2** — Present Sections 1–2 of the plan (problem + open questions) before architecture
- **Gate 3** — Present Sections 3–4 (architecture + module map) before writing code
- **Gate 4** — User reviews each implementation phase before the next begins

## Principles

Things that don't happen without explicit instruction:

- **Challenge the premise first.** Before designing, make an honest case for and against building this at all.
- **Don't pre-engineer ergonomics.** Ship the simplest API that works; add convenience only when real usage justifies it.
- **Validate the API against the full ecosystem** before locking in — a choice that works for one backend may break for others.
- **Group by domain/feature, not technical layer.** `controllers/`, `services/` scatters concerns; feature grouping keeps them together.
- **Fail-fast over silent fallback.** Explicit rejection at the boundary beats silent approximation behind passing tests.
- **Curate the public API surface.** After implementation, cut anything not deliberately needed by consumers; every type gets one canonical path.
- **When a design decision changes mid-implementation**, update the plan first, then implement.

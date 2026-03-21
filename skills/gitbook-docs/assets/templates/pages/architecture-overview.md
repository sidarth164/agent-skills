---
description: "High-level architecture of {{ project_name }} — how it works and where code lives"
---

# Architecture Overview

{{ 1-2 sentence summary of what this page covers. }}

## How It Works

{{ Conceptual overview of the system's core pipeline — what happens from
input to output, in 2-4 short paragraphs. Cover the primary flow, any
secondary capabilities (e.g., checkpointing, caching), and how the system
is deployed/exposed if it's a service.

Keep this high-level. The goal is to orient the reader before they dive
into crate tables and subsystem pages. Avoid implementation details —
those belong in subsystem pages. }}

## Code Organization

{{ For multi-crate (Rust workspace) or multi-module projects. Group
crates/modules by their role (e.g., core, service, integration, tooling).
Dependencies flow downward — service layer depends on core, never the
reverse.

For single-crate or small projects, this section can be replaced with a
brief "Project Structure" listing key directories.

This serves as a codemap — the first thing a developer or AI agent checks
to answer "where does X live?" }}

### {{ Group name }} (e.g., Core)

| Crate / Module | Role |
| ---------------- | ------ |
| {{ name }} | {{ one-line description }} |

### {{ Group name }} (e.g., Service)

| Crate / Module | Role |
| ---------------- | ------ |
| {{ name }} | {{ one-line description }} |

## Service Layer

{{ Optional — include if the project runs as a service. Describe the
deployment model and external interfaces: API protocols (gRPC, REST),
async messaging (Kafka, queues), key endpoints/commands.

Omit this section for libraries or CLI-only tools. }}

## Subsystem Deep Dives

{{ Link to each subsystem architecture page with a one-line summary. }}

- [{{ Subsystem }}]({{ filename }}.md) — {{ one-line summary }}
- [{{ Subsystem }}]({{ filename }}.md) — {{ one-line summary }}

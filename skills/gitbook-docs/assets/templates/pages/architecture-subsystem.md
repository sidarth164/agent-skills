---
description: "How {{ subsystem_name }} works in {{ project_name }}"
---

# {{ Subsystem Name }}

**Code:** {{ list the crate(s), package(s), or module(s) this page covers }}

{{ 1-3 sentence intro — what this subsystem does and how. }}

## Key Concepts

{{ Optional — include when the subsystem has domain-specific abstractions
that aren't self-evident from the code (e.g., FlowType, narrowing, union
dispatch for a type checker). Define the mental model a developer needs
before reading further.

Omit when concepts emerge naturally in the component sections below. }}

## {{ Component / Stage Name }}

{{ The core explanation, organized as one section per major component or
pipeline stage. Walk through the logic, algorithms, state transitions,
and data structures.

Go as deep as needed. This is where the real architectural knowledge
lives — the stuff that takes weeks to reverse-engineer from code.

Use GitBook's {% stepper %} for sequential pipelines, {% tabs %} for
variant behaviors, diagrams (Mermaid) if helpful. }}

## {{ Another Component / Stage }}

{{ Additional component sections as needed. }}

## Interfaces

{{ Optional — include when this subsystem exposes a public API consumed
by multiple other subsystems. Describe inputs, outputs, trait names,
function signatures.

Omit for internal subsystems where interfaces are better described inline
within the component sections above. }}

## Testing

{{ Optional — include when the subsystem has notable testing patterns
(golden files, integration test setup, test fixtures). Describe the
approach and link to relevant commands.

Omit for subsystems that follow standard unit test conventions. }}

## Design Decisions

{{ Significant architectural choices that shaped this subsystem.

**{{ Decision title }}.** {{ 2-3 sentences: what was chosen and why.
Include what the alternative was and why it was rejected. }} }}

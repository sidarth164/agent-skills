# [Project Name] — Design

<!--
WORKING RULES — read this before every update to this document:
  - New design or structural decision discovered mid-implementation → Section 3 (Architecture), not Section 5
  - New open question → Section 2 (Open); resolve it before continuing implementation
  - Resolved question → move from Open to Resolved in Section 2
  - Implementation progress and details → Section 5 only (scope, algorithms, files, tests)
  - Never put design rationale in Section 5; never put progress tracking in Sections 2–4
  - Completed phase → mark all items [x], move from Pending to Completed in Section 5, document what was built
  - If you are unsure where something belongs, add it to Section 2 as an open question first
-->

## 1. Problem Statement
<!-- What the system must do (requirements, not implementation).
     Do not update this section once baselined unless the problem itself changes. -->

### What we need

### Why it doesn't exist
<!-- Evidence from research: what was found, why it's insufficient -->

### Direction

**Goals:**

**Non-goals:**
<!-- Explicit non-goals prevent scope creep — be specific -->

---

## 2. Open Questions & Decisions
<!-- The decision log. Every unresolved design question lives here until closed.
     Do NOT record implementation details here — only decisions that affect architecture or behaviour. -->

### Open
<!-- Add new questions here. Each question that could fork the architecture belongs here, even mid-implementation. -->

### Resolved

#### Q1: [Question]

- **Decision:** ...
- **Reasoning:** ...
- **Alternatives rejected:** ...

---

## 3. Architecture
<!-- Structural choices: abstractions, interfaces, data flow, module boundaries.
     If you are mid-implementation and make a structural choice, update THIS section first, then implement.
     Do not record progress or task status here. -->

---

## 4. Code Organisation
<!-- File/module map only — no design rationale, no implementation code.
     For each entry: what it owns, visibility (public/internal), dependency direction. -->

```text
[project-root]/
├── module-a/   # owns X (public)
└── module-b/   # owns Y (internal)
```

**Dependencies:** module-a → module-b

---

## 5. Implementation Plan
<!-- Progress tracking and implementation documentation.
     Do not add design decisions or architecture changes here — those belong in Sections 2–3.
     The distinction: "We use AstFold with per-variant overrides" is architecture (Section 3).
     "NormalizeEarlyReturns overrides fold_block, scans for X, wraps Y" is implementation (here). -->

### Completed
<!-- Move phases here when done. Mark all items [x], add a **Built:** summary. -->

### Pending

#### Phase 1: [Name]

- [ ] ...
- [ ] ...

#### Phase 2: [Name]

- [ ] ...
- [ ] ...

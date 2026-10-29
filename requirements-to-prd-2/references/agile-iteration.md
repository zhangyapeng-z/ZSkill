# Agile Iteration Planning For Requirement Analysis And PRD

Use this reference when a raw requirement, requirement analysis, or PRD must support phased delivery, version iteration, or agile development.

## Goals

- Ensure every requirement is either delivered in a planned version or explicitly deferred/out of scope.
- Turn functional atoms into delivery-sized Epics or Stories without losing traceability.
- Keep MVP/V1 small enough to validate the core business loop.
- Preserve downstream handoff to `prd-to-dev-spec` and `engineering-delivery`.

## Planning Rules

1. Start from functional atoms, not raw feature labels.
2. Define MVP/V1 as the smallest closed loop that creates user-visible or stakeholder-verifiable value.
3. Assign each FA/FR/AC to one of: MVP/V1, V1.x, V2+, Backlog, or Out of Scope.
4. Use MoSCoW or RICE to explain priority decisions.
5. Record dependencies that affect sequencing: data, permissions, external systems, UI foundations, operational readiness, AI evaluation, and compliance.
6. Mark deferred items with a reason and a trigger for reconsideration.
7. Do not hide scope cuts. If a requested requirement is not in MVP/V1, say where it goes and why.

## Agile Mapping

| Product Item | Agile Equivalent | Notes |
|--------------|------------------|-------|
| Business goal / scenario | Epic | Use for large outcome areas. |
| Functional atom | Story or thin Epic | Must have Input -> Process -> Output and acceptance signal. |
| FR | Story requirement | Express in EARS when useful. |
| AC | Story acceptance criteria | Express in Given-When-Then. |
| Business rule / data rule | Story constraint | Link to affected FR/AC. |
| NFR | Cross-cutting acceptance or quality gate | Assign to relevant version. |

## Required Tables

### Version Roadmap

| Version | Goal | Included FA/FR/AC | Dependencies | Validation Focus | Deferred Items |
|---------|------|-------------------|--------------|------------------|----------------|

### Requirement Coverage

| FA | FR | AC | Version | Status | Rationale |
|----|----|----|---------|--------|-----------|

### Story Backlog

| Epic/Story | Related FA/FR/AC | Suggested Sprint | Priority | Dependencies | Definition of Done |
|------------|-------------------|------------------|----------|--------------|--------------------|

## Self-Check

- Every FA has a version or backlog status.
- Every FR has at least one AC and a version assignment.
- MVP/V1 contains a complete user/business loop, not only setup work.
- Later versions are not vague buckets; each has a goal and acceptance focus.
- Deferred or out-of-scope items have rationale.

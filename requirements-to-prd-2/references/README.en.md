# requirements-to-prd · references

[简体中文](README.md)

**Requirement analysis / PRD methodology references**

This folder is the **progressive reference layer** for the Agent skill [`requirements-to-prd`](../SKILL.md): the parent `SKILL.md` holds the dual-document workflow and templates; here we keep requirement decomposition, feasibility, AI PRD patterns, acceptance/testing boundaries, methodology, and diagram rules so the main skill stays lean.

| Main skill | Parent |
|------------|--------|
| [../SKILL.md](../SKILL.md) | `requirements-to-prd/` |

---

## What this folder is for

- **Analysis before PRD** — functional atoms, feasibility, AI vs traditional fit → see the decomposition and feasibility files below.
- **Seven-layer methodology** without pasting theory every turn → [`methodology.md`](methodology.md).
- **When to add diagrams and safe Mermaid** → [`diagram-guide.md`](diagram-guide.md), [`mermaid-compatibility.md`](mermaid-compatibility.md).

## Before / After

| | Everything in `SKILL.md` | With `references/` (current) |
|---|:---:|:---:|
| **Methodology** | Bloated main file | Templates in `SKILL.md`, theory in `methodology.md` |
| **Decomposition & acceptance** | Scattered in chat | Dedicated reference files |

---

## File layout

```
references/
├── README.md / README.en.md
├── methodology.md
├── requirement-decomposition.md
├── solution-feasibility.md
├── ai-prd-patterns.md
├── acceptance-testing.md
├── diagram-guide.md
├── mermaid-compatibility.md
└── agile-iteration.md
```

| File | Use when |
|------|----------|
| [methodology.md](methodology.md) | You need the seven-layer map or core tools |
| [requirement-decomposition.md](requirement-decomposition.md) | Vague input, atomization, EARS, traceability |
| [solution-feasibility.md](solution-feasibility.md) | User brought a solution; you need the real problem path |
| [ai-prd-patterns.md](ai-prd-patterns.md) | AI-enhanced or AI-core products |
| [acceptance-testing.md](acceptance-testing.md) | AC vs separate test-case document |
| [diagram-guide.md](diagram-guide.md) | Choosing flow/sequence/state/ER diagrams |
| [mermaid-compatibility.md](mermaid-compatibility.md) | Cross-platform Mermaid self-check |
| [agile-iteration.md](agile-iteration.md) | MVP and iteration scope |

---

## Split with the main skill

| Content | Location |
|---------|----------|
| Dual-document workflow, naming, templates, self-check | [../SKILL.md](../SKILL.md) |
| Decomposition, atoms, EARS | [requirement-decomposition.md](requirement-decomposition.md) |
| Feasibility and solution choice | [solution-feasibility.md](solution-feasibility.md) |
| AI PRD patterns | [ai-prd-patterns.md](ai-prd-patterns.md) |
| Acceptance vs test cases | [acceptance-testing.md](acceptance-testing.md) |
| Diagram signals | [diagram-guide.md](diagram-guide.md) |

Default deliverables are **Markdown** (in chat or user-specified local paths). Publishing to wikis or doc platforms is up to the user; this skill does not depend on any third-party CLI.

---
name: requirements-to-prd
version: "1.1.0"
display_name: "需求分析与 PRD 生成"
display_name_en: "Requirements to PRD"
description_zh: "将零散、模糊或方案化的产品需求整理为需求分析文档和可评审的产品需求文档（PRD）。"
description_en: "Transform raw, fragmented, or solution-shaped product requirements into a requirement analysis document and a reviewable PRD."
description: >-
  Transform raw, fragmented, or solution-shaped product requirements into two coordinated Markdown
  deliverables: a requirement analysis document and a product requirements document (PRD). Use
  when a vague, fragmented, or solution-shaped business/product request needs requirement
  decomposition, functional atomization, feasibility-aware solution discovery, traditional-vs-AI
  solution classification, standard PRD structure, AI/Agent PRD extensions, EARS/GWT requirement
  expression, acceptance criteria, prioritization, validation metrics, and diagrams.
---

# Requirements To Product Docs

Produce **two coordinated documents** by default:

1. **Requirement Analysis Document**: explain the real problem, goals, users, scenarios, constraints, functional atoms, candidate solutions, feasibility, AI/traditional fit, risks, and open questions.
2. **PRD**: define the committed product scope, functional requirements, rules, permissions, data, exceptions, NFRs, acceptance criteria, priorities, roadmap, and success metrics.

If the user asks for only one document, produce only that document. If the user asks to write files, use project-name file names:

```text
{project-name}-需求分析文档.md
{project-name}-产品需求文档-PRD.md
```

When the project name is missing, infer a concise name from the requirement. If inference is risky, use `待命名项目` in the document title and ask the user to confirm before writing final files.

## Operating Rules

1. Start from the user's source words, then separate **facts**, **inferences**, **assumptions**, and **questions to confirm**.
2. Do not copy the user's proposed solution blindly. First identify the real problem and evaluate whether the proposed solution solves the root cause.
3. Atomize requirements before writing EARS. A functional atom must have independent value and a clear **Input -> Process -> Output** chain, plus constraints and acceptance signal.
4. Use EARS for system behavior and Given-When-Then for acceptance. Keep every FR traceable to one or more AC items.
5. Treat AI as a solution pattern, not a default answer. Decide whether the product is traditional, AI-enhanced, or AI-core before writing the PRD. Traditional software uses the standard PRD structure; AI-enhanced/AI-core products must add AI/Agent-specific sections.
6. Keep PRD acceptance criteria inside the PRD. Put full test cases in a separate document only when the user asks for test cases.
7. Include standard PRD visualizations by scenario signal. Every **core scenario / MVP main path** must include at least one business flowchart unless the scenario is truly atomic and the PRD explicitly explains why no diagram is useful. Add sequence/state/ER/architecture diagrams when their signals are present. Use Mermaid by default for Codex, Claude Code, Cursor, and other Markdown-capable agents. See [references/diagram-guide.md](references/diagram-guide.md).
8. Mermaid diagrams must use cross-platform compatible syntax. Use English/digit/underscore IDs, put Chinese in display labels or aliases, avoid high-risk edge-label syntax such as `-.label.->`, keep version numbers and punctuation-heavy text out of edge labels, and run a Mermaid compatibility self-check before delivery.
9. Treat generated documents as **drafts** until human review. When the user says the PRD is approved, mark it as **baselined** and prepare handoff inputs for the downstream `prd-to-dev-spec` skill.
10. Demo files are for regression and maintenance only. Do not read demo files during normal generation unless the user asks to run or inspect the demo.
11. Use stable IDs across the monorepo pipeline (see **ID conventions** below). Prefer numbered open questions `OQ-{nn}` with owner and impact over bare **待补充** on execution-critical fields (amount rules, auth, deployment, data store).
12. Include a **traceability table** (goal or FA → FR → AC) in the PRD for human review and downstream agents. Optional: append `{project-name}-追溯矩阵.md` when the project is large.
13. Bound every core scenario by actor, trigger, struggle moment, intended outcome, and exit condition. Keep facts, assumptions, and unknowns separate, and attach a validation method to assumptions that can change scope.
14. Maintain a lightweight decision log for solution choices that affect scope: decision, alternatives, evidence, trade-off, owner, date, and revisit condition. Do not hide product decisions inside prose.
15. When revising an existing PRD, start with a change-impact table. Preserve stable IDs for unchanged items, create new IDs only for new requirements, mark deletions explicitly, and list downstream documents or tests that must be regenerated.
16. Use qualitative priority when evidence is thin. RICE, ROI, market size, and conversion targets must include their source or calculation; otherwise label them as assumptions to validate.

When the user wants only a decomposition or execution-unit list rather than the two-document PRD workflow, route to `atomic-breakdown`.

### ID conventions (pipeline-wide)

| Type | Format | Example |
|------|--------|---------|
| Functional atom | `FA-{nnn}` | FA-001 |
| Functional requirement (EARS) | `FR-{nnn}` | FR-001 |
| Acceptance criterion (GWT) | `AC-{nn}` | AC-01 |
| Open question | `OQ-{nn}` | OQ-01 |
| Business rule | `BR-{nnn}` | BR-001 |
| Use case (optional) | `UC-{nn}` | UC-01 |

Do **not** mix `AC-001` and `AC-01`. Test cases (`TC-{nnn}`) are produced by `prd-to-dev-spec`, not this skill.

## Reference Loading

Load only the references needed for the current request:

| Need | Reference |
|------|-----------|
| Seven-layer product methodology | [references/methodology.md](references/methodology.md) |
| Requirement analysis, functional atomization, EARS conversion | [references/requirement-decomposition.md](references/requirement-decomposition.md) |
| Real solution discovery and feasibility judgement | [references/solution-feasibility.md](references/solution-feasibility.md) |
| AI-enhanced or AI-core PRD patterns | [references/ai-prd-patterns.md](references/ai-prd-patterns.md) |
| Acceptance criteria vs test cases | [references/acceptance-testing.md](references/acceptance-testing.md) |
| Diagram selection | [references/diagram-guide.md](references/diagram-guide.md) |
| Mermaid rendering compatibility | [references/mermaid-compatibility.md](references/mermaid-compatibility.md) |

## Agent Compatibility

Keep outputs portable across Codex, Claude Code, Cursor, and other Markdown-capable agents:

- Use plain Markdown, tables, and Mermaid diagrams.
- Do not rely on proprietary canvas/design tools unless the user explicitly asks.
- If an agent cannot load `references/`, summarize the needed reference rules into the current response.
- If an agent cannot write files, output the file names and Markdown bodies in chat.

## Bilingual Usage

Match the user's requested output language. If the user writes in Chinese or does not specify a language, Chinese output is acceptable; if the user asks for English, produce English documents. Keep frontmatter metadata in English for cross-agent compatibility.

Common Chinese requests that should trigger this skill include:

- 需求分析
- 需求拆解
- 功能原子化
- 产品需求文档 / PRD
- AI应用方案
- 传统方案与AI方案结合
- 验收标准
- 需求转PRD

## Workflow

### 1. Intake And Classification

Extract:

| Item | Output |
|------|--------|
| User source text | Quote or summarize the original requirement |
| Project name | Infer or mark `待补充` |
| Requirement type | New product / feature / process optimization / AI application / integration / reporting / other |
| Current shape | Problem statement / feature wish / proposed solution / mixed |
| Delivery mode | Analysis + PRD by default; local files if requested |
| Existing baseline | New document / revision; source version, changed request, and impacted downstream artifacts |

### 2. Requirement Analysis

Build the analysis before the PRD:

1. Background and opportunity
2. Problem statement and root cause
3. Users, roles, bounded scenarios, struggle moments, and current workflow
4. Goals, constraints, dependencies, and non-goals
5. Functional atom table
6. Candidate solution comparison and feasibility decision
7. AI/traditional solution classification
8. MVP scenario recommendation: the smallest closed-loop V1 scenario, later versions, and out of scope
9. Risks, assumptions, open questions, and validation plan

Use [references/requirement-decomposition.md](references/requirement-decomposition.md) and [references/solution-feasibility.md](references/solution-feasibility.md) when the request is vague, complex, solution-shaped, or AI-related.

### 3. PRD

Convert the approved or recommended analysis into a PRD:

1. Background and goals
2. Problem definition
3. Users, scenarios, and current state
4. Product solution and scope, including the smallest MVP scenario
5. Functional requirements with EARS
6. Business rules
7. Exceptions, boundaries, and error handling
8. Permissions and data
9. Non-functional requirements
10. Acceptance criteria with GWT
11. Priority, versioning, roadmap, metrics, risks, and traceability

For AI-enhanced or AI-core products, add AI/Agent sections for Agent work design, AI/Agent function list, prompt design, data/privacy, evaluation, fallback, and monitoring. Use [references/ai-prd-patterns.md](references/ai-prd-patterns.md).

### 4. Visualization

Include Mermaid diagrams when they help standard PRD communication:

| Signal | Recommended Diagram |
|--------|---------------------|
| Core scenario or MVP main path | At least one `flowchart`, unless explicitly explained as unnecessary |
| User or business steps across roles | `flowchart` |
| Object lifecycle, approval, order, ticket, task states | `stateDiagram` |
| Multiple systems or roles exchanging messages | `sequenceDiagram` |
| Key entities and relationships | `erDiagram` |
| System/module boundaries | Architecture `flowchart` or lightweight C4-style diagram |

Diagram decision rules:

1. For each **core scenario** in the requirement analysis, decide whether it is part of the MVP main path.
2. For the MVP main path, include a business flowchart by default.
3. If the scenario involves two or more systems, roles, or services exchanging messages, add a sequence diagram.
4. If a business object has states, approvals, lifecycle, or allowed/forbidden transitions, add a state diagram.
5. If entities/fields/relationships are important for implementation or reporting, add an ER/data relationship diagram.
6. If module/system boundaries matter, add an architecture/module diagram.
7. If a diagram type is not useful, explicitly say why in the PRD.

Use [references/diagram-guide.md](references/diagram-guide.md) for detailed selection. Keep all diagrams as Markdown/Mermaid so the skill remains portable across Codex, Claude Code, Cursor, and other agents. Use [references/mermaid-compatibility.md](references/mermaid-compatibility.md) before final delivery.

### 5. Optional Test Cases

If the user asks for test cases, produce a separate file:

```text
{project-name}-测试用例.md
```

Derive test cases from PRD acceptance criteria, not directly from raw requirements. Use [references/acceptance-testing.md](references/acceptance-testing.md).

### 6. Human Review And Baseline

Use this status model:

| Status | Meaning | Next Step |
|--------|---------|-----------|
| Draft | AI-generated initial document | Human product/business review |
| In Review | Reviewer comments are pending or being addressed | Revise and summarize changes |
| Baselined | Human-approved product scope | Hand off to `prd-to-dev-spec` |
| Changed | Approved PRD was modified after baseline | Create change note and re-review |

When reviewers provide comments, revise the analysis/PRD and output a concise change summary. Do not silently change baselined scope.

Before downstream handoff, ensure the PRD contains:

- [ ] Baselined version and approval status
- [ ] MVP scenario and V1 scope
- [ ] Functional atoms, FR, AC, and traceability
- [ ] Business rules, data, permissions, exceptions, NFRs
- [ ] Diagrams or explicit explanation for omitted diagrams
- [ ] Open questions either closed or assigned owners

Downstream file names should use the same project name:

```text
{project-name}-开发说明文档.md
{project-name}-测试用例.md
{project-name}-开发任务确认单.md
```

## Requirement Analysis Template

```markdown
# {项目名} 需求分析文档

> **文档状态**：草案
> **版本**：v0.1  **日期**：YYYY-MM-DD  **作者**：Agent+用户
> **评审状态**：待评审 | 评审中 | 已基线
> **关联PRD**：{项目名}-产品需求文档-PRD.md

## 0. 需求来源与分析说明

| 类型 | 内容 |
|------|------|
| 用户原文 | ... |
| 已知事实 | ... |
| 合理推断 | ... |
| 待确认 | ... |

## 1. 背景与机会

## 2. 问题定义与根因

### 2.1 问题陈述
**谁** 在 **什么场景** 下遇到 **什么问题**，导致 **什么影响**。

### 2.2 根因/JTBD

## 3. 用户、场景与现状

## 4. 目标、约束与不做范围

## 5. 需求拆解与功能原子化

| 原始需求点 | 功能原子ID | 功能原子 | Input（输入/触发） | Process（处理/规则） | Output（输出/结果） | 约束 | 验收信号 |
|------------|------------|----------|--------------------|-------------------|-------------------|------|----------|
| ... | FA-001 | ... | ... | ... | ... | ... | ... |

## 6. 候选方案与可行性分析

| 方案 | 解决的问题 | 依赖条件 | 复杂度 | 风险 | 推荐结论 |
|------|------------|----------|--------|------|----------|
| ... | ... | ... | 低/中/高 | ... | 推荐/暂缓/不建议 |

## 7. AI/传统方案适配判断

| 能力点 | 推荐模式 | 理由 | 兜底策略 |
|--------|----------|------|----------|
| ... | 传统/AI增强/AI核心/人工 | ... | ... |

## 8. AI/Agent 工作设计（AI应用适用）

### 8.1 Agent 工作流
（说明单 Agent / 多 Agent / 工具调用 / 人工介入的工作链路。）

### 8.2 Agent 职责说明
| Agent/能力 | 目标 | 输入 | 处理 | 输出 | 工具/数据 | 兜底 |
|------------|------|------|------|------|-----------|------|

### 8.3 关键时序流程
（涉及多 Agent、模型、工具、外部系统、人审时，用 Mermaid `sequenceDiagram`。）

### 8.4 大模型/Agent 功能点清单
| 功能点 | 类型 | 触发场景 | 输入 | 输出 | 质量指标 | 失败兜底 |
|--------|------|----------|------|------|----------|----------|

### 8.5 提示词设计草案
| Prompt | 目标 | 输入变量 | 输出格式 | 安全边界 | 评估样例 |
|--------|------|----------|----------|----------|----------|

## 9. MVP 场景与 V1 范围建议

### 9.1 最小闭环 MVP 场景

用一句话说明 V1 最小可交付闭环：

> 当「目标用户」在「核心场景」中，需要完成「关键任务」时，系统通过「最小能力组合」帮助其得到「可验证结果」。

### 9.2 V1 / 后续 / 不做

## 10. 风险、未决问题与验证计划
```

## PRD Template

```markdown
# {项目名} 产品需求文档（PRD）

> **文档状态**：草案
> **版本**：v0.1  **日期**：YYYY-MM-DD  **作者**：Agent+用户
> **评审状态**：待评审 | 评审中 | 已基线
> **关联需求分析**：{项目名}-需求分析文档.md

## 1. 背景与目标

### 1.1 背景
### 1.2 业务目标与指标
| 目标 | 指标 | 基线/目标值 | 备注 |
|------|------|-------------|------|

## 2. 问题定义

## 3. 用户、场景与现状

## 4. 方案与范围

### 4.1 产品形态与信息架构
### 4.2 业务流程、状态或系统协作
### 4.3 标准可视化图（按需）

- **MVP主路径业务流程图**：（核心/MVP 场景默认必填；若不画，写明原因）
- **其他业务场景流程图**：
- **系统/模块架构图**：
- **时序图**：
- **状态图**：
- **ER/数据关系图**：
- **不采用某类图的原因**：

### 4.4 最小闭环 MVP 场景

**MVP 场景**：当「目标用户」在「核心场景」中，需要完成「关键任务」时，系统通过「最小能力组合」帮助其得到「可验证结果」。

### 4.5 MVP 范围
**V1 必须达到**：...
**明确推迟**：...
**Out of Scope**：...
### 4.6 方案取舍

## 5. 功能需求（EARS）

| FR | EARS类型 | 需求描述 | 来源功能原子 | 优先级 |
|----|----------|----------|--------------|--------|
| FR-001 | Event-driven | 当...时，系统应... | FA-001 | Must |

## 5A. AI/Agent 功能清单（AI应用适用）

| AI/Agent功能 | 类型 | 关联FR | 触发 | 输入 | 处理 | 输出 | 置信度/质量 | 兜底 |
|--------------|------|--------|------|------|------|------|-------------|------|

## 5B. Agent 工作设计（AI应用适用）

### 5B.1 Agent 工作流

### 5B.2 Agent 职责说明
| Agent/角色 | 职责 | 输入 | 输出 | 可用工具/数据 | 权限边界 | 失败兜底 |
|------------|------|------|------|---------------|----------|----------|

### 5B.3 关键时序流程
（多 Agent / 模型 / 工具 / 外部系统 / 人审协作时，用 Mermaid `sequenceDiagram`。）

## 5C. 提示词设计（AI应用适用）

| Prompt | 使用场景 | System Prompt 摘要 | User Prompt 模板 | 输入变量 | 输出格式 | 安全边界 | 评估样例 |
|--------|----------|--------------------|------------------|----------|----------|----------|----------|

## 6. 业务规则

## 7. 异常、边界与错误处理

## 8. 权限与数据

### 8.1 角色与权限
### 8.2 数据定义
### 8.3 外部系统/接口

## 9. 非功能需求（NFR）

| 类型 | 要求 | 验收方式 |
|------|------|----------|

## 10. 验收标准

| AC | 场景 | Given-When-Then | 关联FR |
|----|------|-----------------|--------|
| AC-01 | ... | Given ... When ... Then ... | FR-001 |

## 11. 优先级、版本与成功度量

### 11.1 MoSCoW 或 RICE
### 11.2 路线图
### 11.3 指标与埋点
### 11.4 风险与未决问题
### 11.5 需求追溯
| 业务目标 | 功能原子 | FR | AC |
|----------|----------|----|----|
| ... | FA-001 | FR-001 | AC-01 |

（大项目可另附 `{项目名}-追溯矩阵.md`，列 FA/FR/AC/OQ 与章节引用。）

## 12. 下游交付准备

| 检查项 | 状态 | 说明 |
|--------|------|------|
| PRD 是否已人工评审 | 待确认/已通过 | ... |
| 是否可进入开发说明生成 | 是/否 | ... |
| 未决问题是否关闭或有负责人 | ... | ... |
| 交付给 prd-to-dev-spec 的输入 | PRD vX.X + 需求分析 vX.X | ... |
```

## Self-Check

Before final delivery, verify:

- [ ] The analysis document identifies the real problem, not only the requested feature.
- [ ] The analysis document defines the smallest closed-loop MVP scenario.
- [ ] Every major requirement has a functional atom with clear Input -> Process -> Output before becoming an FR.
- [ ] The PRD includes at least one flowchart for the core/MVP scenario, or explicitly explains why the MVP scenario is atomic and does not need one.
- [ ] The PRD includes sequence/state/ER/architecture diagrams when their signals are present, or explicitly explains omissions.
- [ ] Every Mermaid block passes compatibility checks: closed code fence, valid diagram type, English IDs, Chinese only in labels/aliases, no high-risk edge labels such as `-.label.->`, and no punctuation-heavy labels on edges.
- [ ] Candidate solutions include feasibility, dependencies, risks, and recommendation.
- [ ] AI usage is classified as traditional, AI-enhanced, or AI-core, with fallback where needed.
- [ ] Traditional software PRDs use the standard PRD structure; AI-enhanced/AI-core PRDs include AI/Agent function list, Agent work design, key sequence flow, and prompt design.
- [ ] The PRD has FR, BR, data, permission, NFR, exception, and AC sections.
- [ ] FR items trace to functional atoms, and AC items trace to FR items.
- [ ] IDs follow pipeline conventions (`FA-001`, `FR-001`, `AC-01`, `OQ-01`); no mixed `AC-001` style.
- [ ] Open questions use `OQ-{nn}` with owner/impact where they block or skew implementation; execution-critical fields are not left as vague **待补充** without an OQ link.
- [ ] PRD includes a traceability table (§11.5 or companion matrix file) for downstream `prd-to-dev-spec`.
- [ ] PRD contains acceptance criteria, while detailed test cases are separate unless explicitly requested.
- [ ] File names include the project name when writing documents.
- [ ] Draft/baseline status is explicit, and the PRD is ready for `prd-to-dev-spec` only after human approval.
- [ ] Demo files were not loaded as generation context unless the user asked for demo validation.

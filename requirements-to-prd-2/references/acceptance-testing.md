# Acceptance Criteria And Test Cases

Use this reference when deciding what belongs in the PRD and what belongs in a separate test case document.

## Boundary

| Artifact | Belongs In | Purpose |
|----------|------------|---------|
| Acceptance criteria (AC) | PRD | Defines what "done" means for product review |
| Given-When-Then | PRD | Makes main paths and key failures verifiable |
| Acceptance checklist | PRD | Objective review checklist |
| Full test cases (TC) | Separate test case document | QA execution, data setup, edge cases, regression |
| Automation scripts | Test repository, not PRD | Engineering/QA automation |

Default: include AC in PRD, not full TC.

## AC Quality Rules

Acceptance criteria should be:

1. Observable by reviewer or tester.
2. Linked to one or more FR items.
3. Focused on outcome, not implementation internals.
4. Cover main success and key failure paths.
5. Avoid vague words unless quantified in NFR or metrics.

## GWT Pattern

```text
Given <precondition/context>
When <user action/system event>
Then <observable result>
```

Examples:

```text
AC-01: Given a user has entered a valid bill amount and date, When the user saves the bill, Then the bill shall appear in the bill list and be included in analysis totals.
AC-03: Given the amount is empty, When the user clicks save, Then the system shall reject saving and show a message asking for amount.
```

## Derive Test Cases From AC

Use this mapping:

```text
FR -> AC -> TC
```

Test cases add details not suitable for PRD:

| Test Case Field | Meaning |
|-----------------|---------|
| TC ID | TC-001 |
| Related AC/FR | Traceability |
| Priority | P0/P1/P2 |
| Preconditions | Environment, account, data |
| Test data | Concrete values |
| Steps | Executable QA steps |
| Expected result | Specific expected result |
| Type | Functional, boundary, compatibility, security, performance |

## Test Case Template

```markdown
# {项目名} 测试用例

> **关联PRD**：{项目名}-产品需求文档-PRD.md

| TC | 关联AC/FR | 优先级 | 类型 | 前置条件 | 测试数据 | 步骤 | 预期结果 |
|----|-----------|--------|------|----------|----------|------|----------|
| TC-001 | AC-01 / FR-001 | P0 | 功能 | ... | ... | 1. ... | ... |
```

## Coverage Checklist

- [ ] Main success paths
- [ ] Required field validation
- [ ] Permission denial
- [ ] Data boundary values
- [ ] Empty states
- [ ] External system failures
- [ ] State transitions
- [ ] AI low-confidence / timeout / unsafe output when AI is used
- [ ] NFR verification approach
- [ ] Regression cases for edited or high-risk behavior

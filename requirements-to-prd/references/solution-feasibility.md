# Solution Discovery And Feasibility

Use this reference when the user proposes a solution, asks for an executable PRD, or the project has delivery risk.

## Principle

Do not assume the first proposed feature is the right solution. Identify the root problem, compare candidate solutions, then recommend the smallest feasible path that can prove value.

## Solution Discovery Steps

1. Restate the problem independently from the proposed solution.
2. Identify the desired outcome and success metric.
3. List constraints: data, system, process, permission, legal, team, schedule, cost.
4. Generate at least two candidate solutions when the path is not obvious.
5. Evaluate feasibility and risk.
6. Recommend V1, later versions, and out-of-scope items.

## Feasibility Dimensions

| Dimension | Questions |
|-----------|-----------|
| Business fit | Does it solve the root problem? Is the user behavior realistic? |
| Data readiness | Is required data available, structured, timely, and lawful to use? |
| System fit | Can existing systems expose, receive, or store needed data? |
| Process fit | Who acts before/after the system behavior? Is manual review needed? |
| Cost | Build cost, operating cost, model/API cost, maintenance cost |
| Risk | Compliance, security, accuracy, user trust, rollback difficulty |
| Verification | Can success be measured within V1? |

## Candidate Solution Table

```markdown
| 方案 | 解决的问题 | 关键机制 | 依赖条件 | 复杂度 | 风险 | 验证方式 | 推荐结论 |
|------|------------|----------|----------|--------|------|----------|----------|
| ... | ... | ... | ... | 低/中/高 | ... | ... | 推荐/暂缓/不建议 |
```

## Recommendation Rules

- Prefer deterministic rules when the domain rules are clear and data volume is small.
- Prefer workflow/process changes when the bottleneck is ownership, handoff, or approval rather than information processing.
- Prefer AI only when it handles ambiguity, natural language, prediction, classification, extraction, or generation better than rules at acceptable risk.
- Use AI as assistive first when wrong answers create business, legal, safety, financial, or user-trust risk.
- Require human confirmation when confidence is low, impact is high, or reversibility is poor.
- Put expensive or uncertain technology behind V1.1+, experiment, or PoC unless it is core to the problem.

## V1 Scope Decision

Use this decision form:

```markdown
### V1 Recommendation

- **Must solve**:
- **Can prove value by**:
- **Lowest feasible implementation**:
- **AI involvement**:
- **Manual/operational fallback**:
- **Explicitly excluded**:
- **Decision rationale**:
```

## MVP Scenario

Before writing PRD scope, define the smallest closed-loop MVP scenario. It should prove value with the fewest necessary actors, data, rules, and screens.

Template:

```text
When <target user> is in <core scenario> and needs to <key task>,
the system provides <minimum capability set>,
so the user can get <verifiable result>.
```

Check the MVP scenario:

- [ ] It has one primary user and one primary task.
- [ ] It starts from a real trigger and ends with an observable result.
- [ ] It can be accepted with a small set of FR/AC items.
- [ ] It excludes optional integrations, advanced AI, batch operations, and edge cases unless they are essential to prove value.
- [ ] It can produce a measurable signal after launch or pilot.

## Common Anti-Patterns

| Anti-pattern | Better Move |
|--------------|-------------|
| User asks for AI, but no data exists | Start with rules/manual labeling and collect data |
| User asks for dashboard, but decision process is unclear | Define decisions and actions before charts |
| User asks for automation, but exceptions dominate | Design human-in-the-loop workflow |
| User asks for integration, but no stable interface exists | Define import/export or staging process first |
| User asks for all features in V1 | Use MoSCoW/RICE and prove one closed loop |

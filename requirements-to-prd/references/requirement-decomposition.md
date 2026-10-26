# Requirement Decomposition And EARS

Use this reference when the input is vague, fragmented, written as a feature wish, or needs EARS/functional atomization.

## Decomposition Chain

```text
User source
-> intent classification
-> problem and goal
-> roles and scenarios
-> constraints and dependencies
-> functional atoms
-> EARS functional requirements
-> GWT acceptance criteria
```

## Separate Five Things

| Type | Meaning | Example |
|------|---------|---------|
| Problem | The pain or business issue | Operators cannot identify delayed orders early |
| Goal | Desired measurable outcome | Reduce manual follow-up time |
| Scenario | Where the problem happens | Daily order review before production scheduling |
| Requirement | Capability the system must provide | Show risky delayed orders |
| Solution | One possible implementation | AI predicts delay probability |

If the user gives a solution first, rewrite it back into problem and goal before accepting it.

## Bound The Scenario

Avoid treating an entire journey or user segment as one scenario. A useful scenario has:

| Field | Question |
|-------|----------|
| Actor | Who is trying to make progress? |
| Trigger | What event or state starts this episode? |
| Struggle moment | Where does the current method become costly, confusing, risky, or emotionally difficult? |
| Intended outcome | What observable progress should the actor achieve? |
| Exit condition | Where does this scenario end or hand off? |

Split scenarios when the trigger, goal, decision owner, or success condition changes. Do not split merely because the UI changes screens.

## Evidence And Assumptions

Classify important inputs before solution design:

| Type | Treatment |
|------|-----------|
| Fact/evidence | Preserve the source and note its scope or date when relevant |
| Inference | Explain the reasoning and confidence |
| Assumption | State what decision depends on it and how to validate it |
| Unknown | Turn it into an open question; do not fill it with invented detail |

Use lightweight `5 Whys` only when each answer is supported or explicitly marked as a hypothesis. Stop when evidence runs out.

## Functional Atom Definition

A functional atom is the smallest product capability that can be designed, developed, and accepted while still having independent value.

Each functional atom must include a clear **Input -> Process -> Output** chain:

| Field | Question |
|-------|----------|
| ID | FA-001, FA-002, ... |
| Name | What capability is this? |
| User/value | Who benefits and why? |
| Input | What trigger, user action, data, state, or external event enters the atom? |
| Process | What processing, rule, decision, calculation, workflow, or AI inference happens? |
| Output | What observable result, data change, message, state, or downstream event is produced? |
| Constraints | Rules, permissions, data, performance, policy |
| Acceptance signal | How do we know it works? |

## Atomization Rules

1. Split by user intent, not by UI component.
2. Split when trigger, permission, data source, or acceptance standard differs.
3. Do not split CRUD mechanically unless each action has different business value or rule.
4. Keep AI inference, user correction, human review, and audit logging as separate atoms when they can fail independently.
5. Mark atoms as `Must`, `Should`, `Could`, or `Won't` before writing PRD scope.
6. Include success and failure behavior when they produce different observable outcomes.
7. Recombine fragments that have no independent user/system value or cannot be accepted separately.
8. Make dependencies explicit; small size alone does not make a unit atomic.

## Functional Atom Table

```markdown
| 原始需求点 | 功能原子ID | 功能原子 | 角色/价值 | Input（输入/触发） | Process（处理/规则） | Output（输出/结果） | 约束 | 验收信号 |
|------------|------------|----------|-----------|--------------------|-------------------|-------------------|------|----------|
| ... | FA-001 | ... | ... | ... | ... | ... | ... | ... |
```

## Convert Atoms To EARS

Use the functional atom as the source of truth.

| EARS Type | Pattern | Use When |
|-----------|---------|----------|
| Ubiquitous | The system shall ... | Always-on behavior |
| Event-driven | When `<event>`, the system shall ... | Triggered by an event |
| State-driven | While `<state>`, the system shall ... | Behavior depends on state |
| Unwanted | If `<bad condition>`, the system shall ... | Error, exception, invalid input |
| Optional | Where `<feature enabled>`, the system shall ... | Feature flag, configuration, optional module |

Good EARS sentences:

```text
FR-001 (Event-driven): When a user saves a new bill, the system shall generate a suggested category from enabled classification rules.
FR-002 (Unwanted): If the amount is missing or invalid, the system shall reject saving and show a corrective message.
FR-003 (State-driven): While a bill is in Draft state, the system shall exclude it from analysis totals.
```

Avoid:

```text
The system should be smart and user-friendly.
The page should quickly show useful data.
```

Replace vague terms with measurable NFR or AC items.

## Traceability

Keep a lightweight chain:

```text
Goal -> FA -> FR -> AC -> optional TC
```

Use this table in the PRD when the project is complex:

```markdown
| 业务目标 | 功能原子 | FR | AC |
|----------|----------|----|----|
| ... | FA-001 | FR-001 | AC-01 |
```

# Compact Task Status Template

<!-- frontend-canonical-state
{"schemaVersion":"1.0","sourceType":"task-status","frontendAutoRunId":"missing","status":"in-progress","repairDispatchStatus":"not-applicable","repairClosureHash":"not-applicable"}
-->

建议路径：`sdd-workspace/changes/{change-id}/frontend/tasks/task-status.md`
用途：只保存当前 lane、状态迁移、blocker、Review 和 Verification 链接，不复制 Task Breakdown 正文。

## Status Source
- Feature：
- Task Breakdown：`sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md`
- Tracking Mode：ai-kanban
- Current Stage：Task Breakdown
- Overall Progress：
- Last Updated At：

规则：本文件是唯一 canonical 任务状态源。禁止创建根级 `frontend/task-status.md` 或 by-reference 副本。
机器读取的 `dependencies`、`blockers` 等 list cell 使用逗号分隔值、`none/not-applicable` 或 `[]`；状态投影格式由 Task owner 内部规范化，不作为外层门禁。
规则：每次更新 Board、Review/Verification 状态或 repair closure 时，必须在同一次写入中更新顶部 `frontend-canonical-state`。`status` 只允许 `done / partial / blocked / in-progress`；run id、repair status 和 hash 必须原样复制 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py --repair-closure-stage-result <frontend-stage-result.json>` 的输出，不得自行计算或由 Handoff preflight request 自报。helper 失败只修状态源，不重跑业务阶段。

## Board
| taskId | sliceId | lane | status | dependencies | blockers | reviewStatus | verificationStatus | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-001 | SL-SHARED | Ready | pending | [] | [] | not-run | not-run |  |

状态口径：只有依赖已满足且 Gate 允许派发的任务使用 `Ready`。未满足依赖保留 `Backlog`，它不是 `Blocked`；外部契约、写范围、validator、Review 或 Verification 无法继续时才使用 `Blocked`。

## Execution Groups
| executionGroupId | groupDispatchId | groupType | dispatchMode | taskIds | sliceIds | status | plannedTodoCount | requiredOwningAgentDispatchCount | plannedOwningAgentDispatchCount | actualOwningAgentDispatchCount | implementationAgentCallCount | planStatus | agentDispatchTraceCheck | dispatchPlanPath | dispatchValidationPath | dispatchLeasePath | dispatchLeaseId | dispatchLeaseIssuedAt | serialFallbackPolicy | serialFallbackReason | next |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | not-applicable | serial / parallel / integration | serial-task / parallel-slice / serial-integration | [] | [] | planned / completed / internal-repair / serial-fallback | 0 | 0 | 0 | 0 | 0 | not-run / ready / parallel-dispatch-internal-repair | not-run | `frontend/evidence/implementation-dispatch-plan.json` | `frontend/evidence/implementation-dispatch-validation.json` | `frontend/evidence/implementation-dispatch-lease-G1.json` | not-run | not-run | internal-repair / serial-fallback-with-reason | none |  |

规则：本表同时承载 dispatch plan 当前摘要和执行结果，不再维护第二张计划表。`planStatus=ready` 前必须运行 Implementation dispatch validator；实际派发前必须取得当前组 `passed=true + leaseGranted=true` 的 Dispatch Lease。并行组 fan-out 取得调用句柄后立即执行 `Dispatch Acknowledgement Check`；每个 slice 必须有独立 `frontend-implementation-agent` trace，`actualOwningAgentDispatchCount` 与 `implementationAgentCallCount` 必须按唯一 session/tool evidence 计数并等于 required。Todo/trace 数不能代替实际调用数；多个并行 slice 只有一条 implementation trace、复用 evidence 或数量不足时 `agentDispatchTraceCheck=failed`；只补发未 acknowledged slice，不重派已启动 slice。无法实际并行只能在发令前写 `serial-fallback/blocked + serialFallbackReason`。

## Gate Snapshot
| gate | passed | implementationEligible | warningCount | resultPath |
| --- | --- | --- | ---: | --- |
| task-ready-gate | false | false | 0 | `frontend/evidence/task-ready-validation.json` |

规则：本表必须逐字段复制 Task Ready validation，不得把 warning 文案或 eligibility 重新解释成另一状态。compact 与 expanded 共用该行；expanded optimization 结果只作为 Task Ready 内部条件 gate。

## Dispatch Evidence Pointers
- sliceDispatchStatus：not-run / passed / failed / partial
- agentDispatchTraceSource：`frontend-stage-result.json#agentDispatchTrace`
- runtimeTraceValidationPath：`frontend/evidence/runtime-trace-validation.json`

规则：逐 slice 的 `delegatedAgent / actualAgentCall / sessionOrToolEvidence / changedFiles` 只在最终 `agentDispatchTrace` 和 runtime trace validation 中维护；本文件只保留当前状态与指针。Gate 失败、前置 shared 输出未就绪、只能形成一个整包 Todo、缺唯一 `sliceId` 或输入 hash 已变化时，不得派发 Implementation。

## Status Updates
| timeOrStage | executionGroupId | groupDispatchId | taskId | sliceId | from | to | changedFiles | agentDispatchTrace | evidence | blockersOpened | blockersResolved | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task Breakdown | not-applicable | not-applicable |  |  | none | Backlog / Ready / Blocked | [] | not-applicable |  | [] | [] |  |

## Blockers
| blockerId | ownerGate | relatedTaskIds | status | openedAt | resolvedAt | evidence | next |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | target-and-write-scope / contract-readiness / validator-required / review-blocking / verification-failed |  | open / resolved |  |  |  |  |

规则：Gate 从 failed 变为 passed 时必须保留一条 resolved 迁移，不得直接删除 blocker 历史。

## Review And Verification Links
| type | relatedTaskIds / slices | result | artifact | unverifiedReason / next |
| --- | --- | --- | --- | --- |
| Review |  | not-run |  |  |
| Verification |  | not-run |  |  |

## Stage Telemetry
| stageDurationMs | agentDurationMs | toolDurationMs | readCallCount | readOutputChars | skillReferenceReadCount | capsuleReuseRate | retryCount | retryReason |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |  |  |  |

规则：telemetry 由编排器或工具事实回填，不由 Agent 猜测。普通超预算只做诊断；重复 owner reference 注入仍按 hard evidence gate 处理。

# Full Task Status Template

<!-- frontend-canonical-state
{"schemaVersion":"1.0","sourceType":"task-status","frontendAutoRunId":"missing","status":"in-progress","repairDispatchStatus":"not-applicable","repairClosureHash":"not-applicable"}
-->

建议路径：`sdd-workspace/changes/{change-id}/frontend/tasks/task-status.md`
适用范围：`taskProfile=expanded / audit`、production-ready、多模块完整验收。普通 `taskProfile=compact` 使用 `task-status.compact.md`。

路径规则：`sdd-workspace/changes/{change-id}/frontend/` 必须位于当前 SDD 项目根目录下。

用途：作为 AI 驱动任务状态的持久台账。本文只维护当前 lane/status、状态流水、阻塞、Review/Verification 链接和反馈回灌；任务定义、依赖图、文件映射、并行切片和完整验收标准以 `task-breakdown.md` 为基线。

## Status Source
- Feature：
- Feature Root：
- Task Breakdown：`sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md`
- Tracking Mode：ai-kanban
- Iteration / Sprint：optional；无迭代管理时写 `not-applicable`
- 当前阶段：
- backfillKey：none / stable key
- backfillPackage.attemptCount：non-negative integer
- backfillPackage.repairDiagnosisRevision：non-negative integer
- backfillPackage.repairPlanFingerprint：stable fingerprint
- backfillPackage.repairMode：evidence-backfill / not-applicable
- backfillPackage.repairBudgetClass：execution-proof / result-contract-backfill / not-applicable
- backfillPackage.consumesRepairBudget：false
- backfillPackage.contractDiffDomains / businessChangedFiles：[]
- taskLoopGuardStatus：clear / backfill-allowed / re-diagnosis-required / terminal-gate / not-applicable
- stopCondition：none / identical-fingerprint-consumed / terminal-block-whitelist / not-applicable
- Created At：
- Last Updated At：
- Last Updated Stage：
- 状态来源：task-status.md
- Overall Progress：0 / 0 done，0 blocked，0 in progress

## Task Checklist
- [ ] FE-001 - <title>（lane: Backlog，status: pending，review: not-run，verify: not-run）

Checklist 规则：
- `Task Checklist` 是给人快速阅读的进度摘要，必须与 Task List 的 taskId、lane、status、reviewStatus 和 verificationStatus 保持一致。
- 勾选 `[x]` 只允许表示该任务已达到 `Done`，即 `reviewStatus=review-passed` 且 `verificationStatus=verified`。
- 代码已写完但未 Review/Verify 时不得勾选；应在 Task List / Status Updates 中写 `completed`、`mock-completed`、`partial`、`partial-needs-rework`、`blocked-needs-rework` 或对应 lane。
- `mock-completed`、`code-generated`、`Implementation Generated`、`Implementation Complete` 只表示实现阶段产出了代码，不表示 Done；这些状态不得使用 `[x]`。若历史产物写了 `Implementation Complete`，必须映射为 lane `Review/Verify/In Progress/Blocked` 中的实现阶段状态，而不是 Done。
- Task 的 `Rejection Criteria`、`mustPassBeforeMockCompleted` 或 `staticRejectionScan` 未扫描/未通过时，不得写 `mock-completed`；应写 `partial-needs-rework`、`blocked-needs-rework` 或 `blocked`，并在 Blockers / Status Updates 记录命中的拒收条件。
- 父工程托管子模块的 mock plugin 集成任务不得只凭“子模块 mock 文件已生成”“`config/packages-config.js` 已注册”“validator scoped passed”或自然语言实现摘要关闭。若 acceptanceRef 要求父工程 `config/config.ts` 顶层 plugin 注册，Status Updates.evidence 必须包含 `parentMockPluginSourceEvidence=changed-parent-config / already-satisfied-exact-source / parent-aggregator-source`、`checkedParentConfigPath` 和 expected `require.resolve(...)`；缺失时任务只能保持 `partial-needs-rework / blocked-needs-rework / blocked`，Checklist 不得勾选。
- `assetBaseline`、`generatedCandidate`、`mock-demo`、`figma-unverified`、`questionGateQueue` 和 `productionReplacement` 是累积状态，不是串行完成态；`follow-asset-baseline` 不得把未解决真实契约、非标准 mock 链路偏离、写入范围冲突或 questionGate 变成完成证据。任一未解决门禁存在时，不得写 `mock-completed`、`completed`、`Review`、`Verify` 或 `Done`。
- demo、用户有条件接受、未运行页面运行态验证或未接真实 API 的完成状态，不得仅靠 checklist 勾选表达，必须保留 lane/status、Review/Verification Links 和 Handoff 限制。非 canonical 交付状态必须回原 owning stage，Task Status 不负责转换。

## Time Policy
- 时间字段只用于状态事件追踪和跨轮恢复，不用于 AI 任务排期估算。
- `Created At`、`Last Updated At`、`openedAt`、`resolvedAt` 和 `timeOrStage` 可写 ISO 时间、日期时间、或阶段名；无法获取准确时间时写阶段名，例如 `Implementation`。
- 不维护任务负责人字段；当前执行者由阶段 agent 和阶段结果体现。外部依赖归属只在 Blockers 中写 `externalOwner`。

## Complexity Policy
| workflow | tracking requirement | required sections |
| --- | --- | --- |
| small regular-change / single-file fix / pure question | 可不落盘 task 文件；阶段结果说明 `null + reason` | 不适用 |
| page regular-change / normal slice | 使用最小 `ai-kanban`：Status Source、Board Summary、Task List、Status Updates、Blockers；并行/返工/Review/Verify 相关表按需填写 | 必填最小表 |
| demo-slice / production-replacement / multi-file | 使用标准 `ai-kanban`，必须维护 acceptanceRef、changedFilesSource、Review/Verification Links 和必要 Rework Links | 标准表 |
| production-ready / multi-page / parallel slices / strict gates | 使用完整 `ai-kanban`，必须维护 parallel slice 映射、shared file locks、Review/Verification Links、Rework Links、lessons learned 和 Handoff 一致性 | 完整表 |

原则：简单任务走最小状态，复杂任务才填完整表；不得为了省略表格而丢失 Review、Verify、changedFilesSource 或 blocker 证据。

Canonical state 规则：每次汇总 Task Checklist、Board Summary、Review/Verification Links 或 repair closure 时，必须在同一次写入中更新顶部 `frontend-canonical-state`。`status=done` 仅用于全部 required task 达到 Done；允许 conditional Handoff 但尚有外部未验证项时可写 `partial`；内部失败写 `blocked`。run id、repair status 和 hash 必须原样复制 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py --repair-closure-stage-result <frontend-stage-result.json>` 的输出，不得自行计算、从其它 owner 文档反推或由 Handoff primary 事后代填；helper 失败只修状态源，不重跑业务阶段。

## Board Summary
| lane | taskIds | count | exitCriteria |
| --- | --- | --- | --- |
| Backlog |  | 0 | 契约/设计已足够拆入 Ready |
| Ready |  | 0 | 依赖满足，可进入 Implementation |
| In Progress |  | 0 | 正在实现或修复 |
| Review |  | 0 | 等待或正在 Review |
| Verify |  | 0 | 等待或正在 Verification |
| Done |  | 0 | Review + Verify 均通过，且状态已回写 |
| Blocked |  | 0 | 缺契约、设计冲突、验证失败或外部依赖阻塞 |

## Board
| taskId | type | sliceId | integrationTaskId | title | priority | iteration | lane | status | acceptanceRef | dependencies | blockers | reviewStatus | verificationStatus | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-001 | story/task/bug/spike | not-applicable | not-applicable |  | P1 | not-applicable | Backlog | pending | task-breakdown.md#FE-001 | [] | [] | not-run | not-run | Ready |

## Status State Machine
| fromLane | allowedToLane | requiredEvidence |
| --- | --- | --- |
| Backlog | Ready / Blocked | 设计、契约和依赖足以进入实现；或记录阻塞项 |
| Ready | In Progress / Blocked | write-scope manifest 或阻塞项 |
| In Progress | Review / Verify / Blocked | changedFiles、changedFilesSource、实现摘要和未验证项；跳过 Review 时必须有 reason |
| Review | Verify / In Progress / Blocked | Review Links；阻塞 finding 回退 In Progress 或 Blocked |
| Verify | Done / In Progress / Blocked | Verification Links；失败项回退 In Progress 或 Blocked |
| Blocked | Backlog / Ready / In Progress | resolvedBlockers 和恢复原因 |
| Done | In Progress | 仅允许 Review/Verify/用户手测发现回归时回退，并记录 rework task 或 blocker |

状态规则：
- `Done` 必须同时满足 `reviewStatus=review-passed` 和 `verificationStatus=verified`。
- 未运行验证时不得进入 `Done`；只能保持 `Review`、`Verify`、`partial`、`mock-completed` 或 `not-run`。
- `Implementation Generated / Implementation Complete` 不能作为 lane 名或 Done 证据；如需保留历史文案，只能放入 evidence，并同步 lane 到 Review / Verify / In Progress / Blocked。
- `mock-completed` 需要 Task Acceptance Scan 通过、无 required 能力拒收项、且所有 `mustPassBeforeMockCompleted` 已满足；否则必须降为 `partial-needs-rework / blocked-needs-rework / blocked`。
- lane 与 status 必须一致；不一致时以 Status Updates 的最新事件为准并修正 Task List。

## Status Updates
| timeOrStage | executionGroupId | groupDispatchId | dispatchMode | taskId | sliceId | integrationTaskId | laneFrom | laneTo | statusFrom | statusTo | changedFiles | changedFilesSource | cumulativeChangedFiles | sharedFilesTouched | blockersOpened | resolvedBlockers | evidence | agentDispatchTrace | artifact | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task Breakdown | not-applicable | not-applicable | not-applicable | FE-001 | not-applicable | not-applicable | none | Backlog | none | pending | [] | [] | [] | [] | [] | [] | initialized | not-applicable | task-breakdown.md | Ready |

## Execution Groups
并行或多 slice 执行时，每个执行组完成后必须追加一行；单任务组也可记录，便于恢复。

| timeOrStage | executionGroupId | groupDispatchId | groupType | dispatchMode | taskIds | sliceIds | integrationTaskIds | status | plannedTodoCount | requiredOwningAgentDispatchCount | plannedOwningAgentDispatchCount | actualOwningAgentDispatchCount | implementationAgentCallCount | planStatus | dispatchPlanPath | dispatchValidationPath | dispatchLeasePath | dispatchLeaseId | dispatchLeaseIssuedAt | agentDispatchTraceCheck | runtimeTraceValidationPath | runtimeTraceStatus | serialFallbackPolicy | serialFallbackReason | blockersImpact | persistedBy | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| not-run | G1 | not-applicable | serial / parallel / integration | serial-task / parallel-slice / serial-integration | [] | [] | [] | not-run | 0 | 0 | 0 | 0 | 0 | not-run / ready / parallel-dispatch-internal-repair | `frontend/evidence/implementation-dispatch-plan.json` | `frontend/evidence/implementation-dispatch-validation.json` | `frontend/evidence/implementation-dispatch-lease-G1.json` | not-run | not-run | not-run | `frontend/evidence/runtime-trace-validation.json` | not-run | internal-repair / serial-fallback-with-reason | none | none | not-persisted | next-group |

规则：
- `changedFilesCheck=pass` 要求组内所有 changedFiles 都能映射到 File Mapping、targetFiles、parallel-slices.writeFiles、integrationTaskId 或 approved recommendedFixPackage。
- `sharedFilesCheck=pass` 要求 feature slice 未写 shared-file-locks 中的共享文件；若共享文件被写入，必须是锁持有 integration task，且 `changedFilesSource=integrationTaskId`。
- `statusUpdatesCheck=pass` 要求每个 taskId / sliceId / integrationTaskId 都有 Status Updates 或明确 `not-run + reason`；并发子任务只返回 proposal 时，必须由 primary / owning stage 汇总后统一落盘。
- `agentDispatchTraceCheck=pass` 只能在 fan-out 调用句柄返回后的 `Dispatch Acknowledgement Check` 通过后写入：`groupType=parallel` / `dispatchMode=parallel-slice` 时，每个 slice 都有独立 `frontend-implementation-agent` trace，`actualOwningAgentDispatchCount` 与 `implementationAgentCallCount` 均按唯一、真实存在的 session/tool evidence 计数且等于 `requiredOwningAgentDispatchCount`，每条 trace 均为 `actualAgentCall=true`。Todo 数、slice trace 数或声明字段不能代替实际调用数；多个并行 slice 只有一条 implementation trace 或不同 slice 复用同一 evidence 时必须写 failed。数量不足时只补发未 acknowledged slice，不重派已启动 slice；`dispatchMode=serial-fallback` 仍逐 slice 直调 owning Agent，只有另行命中通用协调 fallback 时才要求 General 转交 trace。
- 本表同时承载 dispatch plan 当前摘要和执行结果，不再维护第二张计划表。`groupType=parallel` 且 `requiredOwningAgentDispatchCount > 1` 时，`plannedTodoCount` 和 `plannedOwningAgentDispatchCount` 必须等于可并行 slice 数量；`planStatus=ready` 只允许在每个 Todo 有唯一 slice、明确 taskIds 和独立写入范围时填写。
- `dispatchValidationPath` 必须指向当前 group 的 passed Implementation dispatch validator，`dispatchLeasePath/dispatchLeaseId` 必须指向并匹配 `passed=true + leaseGranted=true` 的 Dispatch Lease。并行组进入 Handoff 前，`runtimeTraceValidationPath` 必须指向读取真实 root session 的 strict 结果，且 `runtimeTraceStatus=passed`；report-only 或 fixture 结果无效。
- 若无法实际并行，`status` 只能写 `serial-fallback` 或 `blocked`，并填写 `serialFallbackReason`；不得写 `completed`。
- 任一执行前检查或 Dispatch Acknowledgement Check 为 failed / blocked 时，后续执行组不得推进；`next` 只能是补发未启动 slice / Task Breakdown / Integration task / Implementation rework / 用户确认。若事后 runtime 只发现 owning Agent 数量不足或零重叠，且 slice quality closure 已 passed，则保留业务阶段结果并写 `costGovernancePassed=false`，不得重跑已闭合 slice。

## Gate Snapshot
| gate | passed | implementationEligible | warningCount | resultPath |
| --- | --- | --- | ---: | --- |
| task-ready-gate | false | false | 0 | `frontend/evidence/task-ready-validation.json` |

规则：本表必须逐字段复制 Task Ready validation。Gate 失败时 Blockers 必须存在 open TASK-READY；恢复通过后保留 resolved 行和 resolvedAt，不得删除历史。expanded optimization failure 归入同一 Task Ready gate，不建立第二个通用 dispatch 状态源。

## Slice Quality Evidence
- sliceLocalQualityStatus：not-run / pass / failed / partial / not-applicable
- gateResultPath：`frontend/evidence/slice-quality-gates.json`
- gateValidationPath：`frontend/evidence/slice-quality-gates-validation.json`
- next：integration / slice Implementation rework / Task Breakdown / 用户确认 / serial fallback

规则：逐 slice 的 changedFiles 映射、Task Acceptance Scan、validator、slice-local Review 和未验证项只在上述 canonical JSON 中维护。每个 `canRunInParallel=yes` slice 都必须被 gate result 覆盖；validation 未 `passed=true + progressionDecision=allow-integration` 时，Execution Groups 的 `agentDispatchTraceCheck/status` 必须反映失败且后续组不得推进。

## Blockers
| blockerId | relatedTaskId | relatedSliceId | relatedIntegrationTaskId | source | severity | status | externalOwner | openedAt | resolvedAt | evidence | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | none | not-applicable | not-applicable | not-applicable | not-applicable | none |

`externalOwner` 仅用于非 AI 执行依赖归属，例如 `user`、`backend`、`platform`、`main-flow`、`target-project` 或 `not-applicable`。

## Repair Dispatch Links
| repairAttemptKey | frontendAutoRunId | sourceStage | sourceResultPath | fixRouting | targetStage | generalDispatchRequired | implementationAgentRequired | findingIds | failureIds | targetFiles | completionCriteria | reworkSequence | nextRecheck | recheckSequence | closureStatus | closureEvidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | [] | [] | [] | [] | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable |

规则：Review / Verification / 用户反馈产生的代码修复必须记录本表，并区分 `fixRouting=direct-fix` 与 `fixRouting=owner-needed`。`direct-fix` 可由主编排在当前前端子流程内执行最小 delta，必须记录 direct-fix closure、targeted validator / rerun 和 closure evidence；`owner-needed + targetStage=IMPLEMENTATION` 才通过 `frontend-implementation-agent` 执行，fallback 模式可经 `frontend-general-agent -> frontend-implementation-agent` 透传。`changedFilesSource` 必须映射到 `recommendedFixPackage`、targetFiles 或 integrationTaskId。自动修复必须记录同一 `frontendAutoRunId` 下的 direct-fix / rework / recheck sequence 和 closure evidence；缺 recheck/rerun 或 closure 未 closed 时不得进入 Handoff。

## Lessons Learned / Asset Feedback
| issue | category | rootCause | fixedBy | assetSuggestion | status |
| --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | none |

## Review Links
| findingId | relatedTaskId | relatedSliceId | relatedIntegrationTaskId | severity | status | evidence | resolution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | not-run | not-applicable | not-applicable |

## Verification Links
| verificationItem | relatedTaskId | relatedSliceId | relatedIntegrationTaskId | result | artifact | unverifiedReason |
| --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-run | not-applicable | not-applicable |

## Rework Links
| reworkTaskId | sourceType | sourceId | originalTaskId | reason | status | evidence | next |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FE-FIX-001 / FE-REV-001 | review-finding / verification-failure / manual-finding / design-gap / task-gap |  | FE-001 |  | pending / in_progress / completed / blocked |  |  |

## Rules
- `task-status.md` 是当前状态持久源；Implementation / Review / Verification / Final Review 必须优先回写本文件。
- `task-breakdown.md` 是任务定义和计划基线；只有任务定义、依赖、文件边界或汇总状态快照变化时才同步更新。
- `Tracking Mode=ai-kanban` 表示 AI agent 驱动的轻量看板，不代表完整 Scrum；`Iteration / Sprint` 无人工迭代管理时写 `not-applicable`。
- `Task Checklist` 必须作为 Task List 的人读摘要同步维护；勾选项不得覆盖 Task List、Status Updates、Review Links 或 Verification Links 的事实。
- 运行时 Todo 不是持久状态源。
- 状态更新必须按 taskId 逐项记录，不得只写“全部完成”。
- 存在 `parallel-slices` 时，Task List、Status Updates、Review Links 和 Verification Links 必须能映射到 `taskId / sliceId / integrationTaskId`；无法映射时写 `unmapped + reason`，不得推进整组状态。
- Implementation 后 Status Updates 必须记录 `changedFilesSource`；每个 changedFile 都必须能映射到 file mapping、targetFiles、parallel-slices.writeFiles、integrationTaskId 或 approved recommendedFixPackage。无法证明来源时，该任务不得进入 Review / Verify / Done。
- Implementation 后 Status Updates 必须记录 required file mapping 对账结果。required file 未出现在 changedFiles 时，evidence 必须写 `alreadySatisfiedEvidence` 并指向真实源码片段或验证命令；仅写“任务已完成/文件存在/参考 validator”不算证据。mock-request 的父工程 `config/config.ts` 注册尤其必须记录 exact `require.resolve(...)` 或聚合 plugin 源码证据。
- `changedFiles`、`cumulativeChangedFiles` 和 `sharedFilesTouched` 以 Status Updates 为流水事实源；Task List 只保留当前状态摘要，避免重复维护。
- `sharedFilesTouched` 只能记录实际触碰的共享文件；并行 slice 不得写入 `shared-file-locks` 中由 integration task 持有的共享文件。
- 并发执行时，子任务不得直接并发写 `task-status.md`；它们只能返回 `task-status-updates` proposal。`Execution Group Summary.persistedBy` 必须记录最终统一落盘者；无法统一落盘时写 `not-persisted + reason`，且后续阶段只能按 partial / blocked 继承。
- `Execution Group Summary` 是推进下一组的门禁；缺少当前组 summary、summary 检查失败、agent dispatch 覆盖不足、或 blockersImpact 指向后续组时，不得把下一组任务移入 In Progress / Review / Verify。
- 每个任务必须能在 Board Summary 的一个 lane 中找到；lane 与 status 必须一致。
- 每个任务必须有 priority、type、acceptanceRef、dependencies、blockers、reviewStatus、verificationStatus 和 next；暂缺时写 `missing + reason`，不得留空。
- 任务验收的完整内容在 `task-breakdown.md` 中按 `Contract Acceptance`、`UI Acceptance`、`Verification Acceptance` 三段维护；task-status 只引用 `acceptanceRef`。
- 阻塞项必须进入 Blockers 表，并在 Status Updates 中记录 blockersOpened / resolvedBlockers；外部归属写 `externalOwner`，不写任务负责人。
- blocker 细节、changedFiles 和残余风险应有单一事实源；若存在 `handoff/blocker-resolution-log.md`，本文件只保留 blockerId、状态和引用，不重复维护长描述和 changedFiles 明细。
- Review/人工测试发现实现遗漏时，必须判断是否属于设计/任务验收缺口；若是，新增 `design-task-misalignment` 类 blocker，并回写设计/任务补强要求。
- Task Breakdown 内部 backfill 往返必须受 `progressionDecision.backfillPackage.backfillKey + sourceRevisionHash` 约束。同一 repair plan fingerprint 不得重复执行；复查仍失败时保持稳定 root-cause key、递增 `repairDiagnosisRevision`、记录前一方案不足并生成新的 `repairPlanFingerprint` 后继续内部闭合。预算或轮次本身不得把任务保持为 Blocked；只有 Terminal Block Whitelist 命中时才写外层 blocker。
- 小范围修复可让原 task 回退；跨文件、跨契约、跨 UI Contract 或影响并行边界的返工必须新增 `FE-FIX-*` 或 `FE-REV-*`，并写入 Rework Links。
- 未运行验证时，不得把任务推进到 Done；人工查看代码只能记录为静态证据，不能等价于 reachable/usable。

# Frontend Feature Index Template

<!-- frontend-canonical-state
{"schemaVersion":"1.0","sourceType":"frontend-index","frontendAutoRunId":"missing","status":"not-started","repairDispatchStatus":"not-applicable","repairClosureHash":"not-applicable"}
-->

建议路径：`sdd-workspace/changes/{change-id}/frontend/index.md`

用途：作为前端 feature 跨阶段、跨 agent 和跨轮恢复的过程入口。本文只维护路径、当前状态、单一事实源和开放事项，不复制设计、任务、验证、Review 或 Handoff 的长正文。

## Feature
- Feature：
- Feature Root：`sdd-workspace/changes/{change-id}/`
- Frontend Root：`sdd-workspace/changes/{change-id}/frontend/`
- Target Frontend Project：
- Current Stage：Explore / Evidence / Contract Check / Frontend Design / Design Confirm / Task Breakdown / Implementation / Review / Verification / Final Review / Handoff
- Current Owner Agent：
- Last Updated Stage：
- Last Updated Reason：

## Flow Cutoff And Stage Decisions
| item | value | source | notes |
| --- | --- | --- | --- |
| frontendEntryMode | standalone / lite-integrated | Lite / frontend-auto | `lite-integrated` 表示 Lite 集成进入企业前端执行子流程；`standalone` 表示用户直接进入企业前端执行子流程。两者均要求 Frontend Design / Design Confirm 已由 Lite、外层 `frontend-design-agent` 或等价 handoff 完成，前端子流程从 Task Breakdown 接续 |
| terminalStageRequested | Implementation / Review / Verification / Handoff / full-flow / not-applicable | user / Lite / frontend-auto | 代码实现终点裁剪时写 Implementation |
| frontendExecutionMode | demo-slice / regular-change | frontend-auto | 前端内部只按这两类执行模式分流；Router 的全局等级写入 changeLevel |
| changeLevel | L0 / L1 / L2 / null | Lite / Router | 只作全局 SDD 上下文，不授权前端自行改判或按本地等级分流 |
| flowCutoff | after-implementation / after-review / after-verification / full-flow / not-applicable | user / Lite / frontend-auto | 只描述流程终点，不授权跳过前置阶段 |
| skippedPostImplementationStages | Review, Verification, Handoff, Artifact / [] | user / Lite / frontend-auto | 不做 review/verify/handoff 只能落在这里 |
| requiredPreImplementationStages | Frontend Design, Design Confirm, Task Breakdown / not-applicable | frontend-auto | 页面交付、demo-slice、状态回写或 production-ready 目标默认必须包含 Task Breakdown |
| taskBreakdownDecision | required / generated / reused / skipped / not-applicable / blocked | task-breakdown.md / frontend-auto / user-question | 页面交付、demo-slice 或状态回写默认 required；skipped 必须有用户明确跳过任务拆分的确认来源 |
| taskBreakdownDecisionSource | task-breakdown / existing-artifact / user-explicit-task-skip / direct-no-task / not-applicable |  | 代码实现终点裁剪或实现后阶段裁剪不是合法来源 |
| taskBreakdownSkipReason | null / user-explicit-task-skip / target-file-direct / direct-no-task / blocked-by-contract / invalid-inferred-skip |  | 若为 invalid-inferred-skip，下一阶段必须回 Task Breakdown |
| allowedNext | Task Breakdown / Implementation / Review / Verification / Handoff / blocked / user-question | progressionDecision | 进入 Implementation 前必须满足 taskBreakdownDecision=generated/reused/not-applicable 且来源合法 |

## Runtime And UI Authority
| item | value | source | notes |
| --- | --- | --- | --- |
| stateTransitionVerified | true / false / null | verification-report / handoff | 有状态 mock/demo 动作写 `usable=true` 前必须为 true |
| runtimeStoreConsistency | pass / failed / not-run / not-applicable / null | verification-report / handoff | 证明动作处理、刷新查询和 DataSet/request adapter 使用同一 dev-only runtime store |
| stateTransitionGuard | ui-action-handler / ui-action-only / handler-only / missing / not-applicable / null | implementation / verification | 有状态 mock/demo 动作写 `usable=true` 前必须为 ui-action-handler |
| editableAuthority | routeContext + UI Contract + business status guard / project wrapper / not-applicable | design / task / implementation | DataSet editFlag 不能作为 UI 编辑态权威来源 |

## Canonical Sources
| sourceType | path | status | ownerStage | notes |
| --- | --- | --- | --- | --- |
| evidence | `frontend/evidence/evidence.md` / `null + reason` | missing | Explore / Evidence |  |
| engineering-context-pack | `frontend/evidence/frontend-context-pack.json` / embedded in `evidence.engineeringEvidencePack` / not-applicable + reason | missing | Explore / Evidence / Frontend Design | package、route、request、mock、validator、script 等工程事实摘要；ready+reused 时后续阶段优先读本包 |
| exploration-gate | embedded in `frontend/evidence/evidence.md` / embedded below / not-applicable | missing | Explore / Evidence / Frontend Design | engineeringExplorationRequired、engineeringExplorationLevel；依赖目标工程事实时必须适用目标工程探索 |
| baseline-comparison | embedded in `frontend/evidence/evidence.md` / embedded in `frontend/design/frontend-design.md` / not-applicable + reason | missing | Explore / Evidence / Frontend Design | 工程现状与标准范式差异，不复制完整表 |
| choerodon-enum-import-map | embedded in `frontend/evidence/evidence.md#Choerodon Enum Import Map` / not-applicable + reason | missing | Explore / Evidence | DataSet/Table/Form/组件枚举导入风格，不复制完整表 |
| contract | `frontend/design/contract-check.md` | missing | Frontend Design | 契约状态和 Backend Asset Coverage 单一事实源 |
| design | `frontend/design/frontend-design.md` | missing | Frontend Design | 设计和 UI Contract 单一事实源 |
| ui-contract | embedded in `frontend-design.md` / `frontend/design/ui-contract.md` / not-applicable + reason | embedded | Frontend Design |  |
| production-replacement-draft | embedded in `contract-check.md` / `frontend/design/production-replacement-draft.md` / not-applicable + reason | missing | Frontend Design |  |
| task-breakdown | `frontend/tasks/task-breakdown.md` | missing | Task Breakdown | 任务定义和依赖基线 |
| task-status | `frontend/tasks/task-status.md` | missing | Task Breakdown / Implementation / Review / Verification | 当前状态持久源 |
| verification | `frontend/verification/verification-report.md` | missing | Verification | buildable/reachable/usable 单一事实源 |
| verification-result | `frontend/verification/verification-result.json` / not-written + reason | missing | Verification | 机器可读聚合结果；Handoff 优先消费 |
| manual-checklist | `frontend/verification/manual-checklist.md` / embedded in verification-report.md / not-run + reason | missing | Verification |  |
| review | `frontend/review/review-report.md` / `frontend/review/pre-review.md` / `frontend/review/final-review.md` / not-run + reason | missing | Review / Final Review | 独立 Review 报告；必须由 frontend-review-agent 产出或写 not-run reason |
| handoff | `frontend/handoff/frontend-handoff.md` | missing | Handoff | 最终交付摘要 |
| artifact-index | `frontend/handoff/artifact-index.md` | missing | Handoff | 最终资产索引 |
| production-replacement-checklist | `frontend/handoff/production-replacement-checklist.md` / not-applicable + reason | missing | Handoff | 最终生产替换清单 |
| lessons-learned | `frontend/handoff/lessons-learned.md` / not-applicable + reason | missing | Handoff | 手测反馈和资产增强建议 |
| cost-telemetry | `frontend/diagnostics/cost-telemetry.json` / `frontend/diagnostics/cost-telemetry.md` / not-written + reason | missing | Verification / Handoff | P2 诊断产物；记录累计样本、根阶段墙钟、trace 关键路径/活跃/排队和 top cost rows；累计样本不得当作墙钟 |
| figma-cache | `frontend/figma-cache/` / not-applicable + reason | missing | Figma / Evidence | figmaFetchStatus、cacheStatus、fallbackMode、retryPlan source |

## Current Status
| item | status | source | next |
| --- | --- | --- | --- |
| contractStatus | ready / partial / blocked / demo-only / unknown | contract-check.md |  |
| designConfirmation | draft / 待人确认 / 已确认 / auto-confirmed-for-demo / blocked-by-contract / not-applicable | frontend-design.md / confirmationSource |  |
| taskStatus | not-started / in-progress / blocked / partial / done / not-applicable | task-status.md |  |
| implementationStatus | not-started / in-progress / partial / complete / blocked / not-applicable | task-status.md / implementation summary |  |
| reviewStatus | not-run / pass / conditional / blocked | review report / task-status.md |  |
| reviewMode | targeted-blocking / full-scan / fix-package-recheck / final-delta / reuse-existing-review / not-run | review report / frontend-auto |  |
| reviewReuseStatus | new / reused / narrowed / invalidated + reason / not-applicable | review report / frontend-auto | 未失效时不得重复 full Review |
| reviewScopeFingerprint | changedFiles + taskIds + contract/design/task source versions/hash 摘要 / missing | review report | changedFiles、任务或契约变化时失效 |
| reviewedChangedFiles | list / missing / not-applicable | review report | 用于跨轮判断是否复用 |
| reviewedByAgent | frontend-review-agent / not-run / missing | review report / agentDispatchTrace | 缺失时不得复用 Review 或 Handoff ready |
| reviewReportPath | `frontend/review/review-report.md` / `frontend/review/pre-review.md` / `frontend/review/final-review.md` / not-run + reason | review report | `reviewStatus=pass/conditional/blocked` 时必填 |
| agentDispatchTraceStatus | ready / incomplete / missing / not-applicable | frontend-stage-result / stage result | 已进入 Task/Implementation/Review/Verification/Handoff 的阶段必须有 direct owning-agent 或 frontend-general-agent fallback -> owning agent 证据 |
| verificationStatus | not-run / pass / failed / partial / blocked | verification-report.md / task-status.md |  |
| verificationReuseStatus | new-run / reused / invalidated / not-applicable | verification-report.md | 命令级复用状态；页面运行态观察不复用为 passed |
| verificationScopeFingerprint | changedFilesHash + command + validatorTarget + packageDir + mockNamespace + envKey 摘要 / missing | verification-report.md | 用于判断是否需要重跑对应验证 |
| handoffStatus | production-ready / conditional / blocked / not-started | frontend-handoff.md / artifact-index.md | 其它值均为 `invalid-stage-result`，必须回原 owning stage |
| buildable | true / false / unknown | verification-report.md |  |
| reachable | true / false / unknown | verification-report.md |  |
| usable | true / false / unknown | verification-report.md |  |

## Cost Control Summary
| item | value | source | notes |
| --- | --- | --- | --- |
| sameStageDeltaFastPath | true / false / not-applicable | stage result / task-status | true 时仍必须有真实 owning agent trace |
| ownerReferenceCapsule | ready / missing / invalidated / not-applicable | stageSummary | 只记录 owner skill、source hash、gateIds 和摘要 |
| evidenceCapsule | ready / missing / oversize / not-applicable | stageSummary / artifacts | 关键证据最多 20 行，长日志只给路径 |
| telemetryStatus | collected / partial / unverified | stageSummary / agentDispatchTrace | 诊断项，不作为交付阻断；unverified 必须有 reason |

## Figma Evidence Summary
| item | value | source | next |
| --- | --- | --- | --- |
| figmaStatus | confirmed / confirmed-from-cache / figma-unverified / screenshot-only / cache-only / not-applicable | figma-cache/readme.md / page-schema.json |  |
| figmaFetchStatus | success / partial / rate-limited-429 / permission-denied / node-not-found / failed / cache-only / not-applicable | figma-cache/readme.md |  |
| figmaFetchErrorCode | 429 / 403 / 404 / timeout / unknown / not-applicable | figma-cache/readme.md |  |
| cacheStatus | new / updated / reused / missing / not-written | figma-cache/readme.md |  |
| fallbackMode | confirmed-from-cache / cache-only / screenshot-only / figma-unverified / not-applicable | figma-cache/readme.md |  |
| partialCoverage | readNodes / missingNodes / coverageNote | page-schema.json / readme.md |  |
| retryPlan | required / attemptedCount / nextRetryAfter / splitTargets | figma-cache/readme.md |  |

## Engineering Evidence Summary
| item | value | source | next |
| --- | --- | --- | --- |
| engineeringExplorationRequired | yes / no / unknown | evidence.md / frontend-design.md |  |
| engineeringExplorationLevel | E1 minimal / E2 standard / E3 submodule / not-applicable / unknown | evidence.md / frontend-design.md |  |
| explorationSkipReason | not-applicable / user-provided-evidence / target-file-direct / target-unreadable / user-requested-draft / other | evidence.md / frontend-design.md |  |
| scopeFingerprint | sha256:<64hex> / missing | Lite preflight + evidence.md | 规范化 changeId/确认后的目标工程绝对路径/parentFrontendRoot/packageDir/pageScope 的稳定指纹；目标工程路径不是 SDD Frontend Root 产物目录，范围变化必须产生新值 |
| preDesignEvidenceDecision | reuse-ready / initial-explore / targeted-delta / full-reexplore / needs-user / blocked / not-applicable | Lite preflight + evidence.md | 前端设计准备阶段唯一工程证据路由结论 |
| evidenceReuseSource | new-explore / existing-evidence / user-provided-packet / targeted-delta-explore / existing-evidence-conflict / not-applicable | evidence.md / frontend-design.md |  |
| evidenceReuseStatus | reusable / stale / conflict / missing-required-field / target-changed / not-applicable | index + evidence.md | ready evidence 且目标范围未变时必须 reusable |
| engineeringEvidencePack | ready / partial / missing / stale / conflict / not-applicable；reuseStatus=reused / new-run / targeted-delta / stale / conflict / not-applicable | frontend-context-pack.json / evidence.engineeringEvidencePack | ready+reused 时 Task/Implementation/Review/Verification 不再重复全量读取 package、route、request、mock、script 证据 |
| deltaExploreReason | null / target-changed / index-evidence-conflict / missing-target-placement / missing-enum-map / missing-baseline-comparison / missing-scripts / write-scope-unclear / open-item-requested / other | progressionDecision / Open Items | 非 null 时才允许补工程证据 |
| targetedDeltaScope | null / target-placement / validator-command / component-import-map / enum-map / similar-page-quality / package-route-registration / mock-request-path / baseline-comparison / scripts / write-scope / other | progressionDecision / evidence.md | 非 null 时只能补对应缺口 |
| targetedDeltaRequests | [] / batched request summaries | progressionDecision / evidence.md | Design 多个缺口必须一次批量调度，request 内保留单项 targetedDeltaScope |
| targetedDeltaResults | [] / matched result summaries | evidence.md | 必须按 deltaKey 与 requests 一一对应 |
| fullExploreAttemptCount | 0 / 1 | Lite preflight + evidence.md | 同一 scopeFingerprint 不得超过 1 |
| targetedDeltaAttemptKeys | [] / unique delta keys | Lite preflight + evidence.md | 记录唯一一次批量调度的全部 key；一旦非空，不得追加第二批、新 key 或重试 |
| nextExploreAllowed | none / targeted-delta / full-reexplore / user-confirmation-required | index + evidence.md | ready evidence 且范围未变时为 none |
| fullExploreForbiddenReason | ready-evidence-reusable / targeted-delta-only / target-scope-unchanged / not-applicable | index + evidence.md | 禁止“再确认一下”触发 full Explore |
| lastExploreMode | quick / medium / thorough / targeted-delta / reused / not-applicable | evidence.md |  |
| standardBaselineApplied | true / false / not-applicable / unknown | evidence.md / frontend-design.md | 有参考模块时仍应为 true |
| baselineComparisonStatus | not-needed / ready / partial / blocked / needs-confirmation / unknown | evidence.md / frontend-design.md |  |
| goldenBaselineStatus | confirmed / not-confirmed / rejected / conflict / not-applicable / unknown | evidence.md / frontend-design.md / task-breakdown.md / review report | 不能由搜索自动确认 |
| baselineConfirmationSource | user-explicit / owner-doc / design-confirmed-from-owner / none / not-applicable / unknown | evidence.md / frontend-design.md | golden 必须有确认来源 |
| similarPageEvidenceQualityStatus | ready / partial / missing / not-applicable / unknown | evidence.md / frontend-design.md / task-breakdown.md / review report |  |
| assetBaselineStatus | active / not-applicable / blocked / unknown | evidence.md / frontend-design.md / task-breakdown.md | 空 HZEROJS 项目、参考资产缺失/不可读或无可采纳参考模块时必须 active |
| assetBaselineSource | hzerojs-asset-baseline / not-applicable / unknown | evidence.md / frontend-design.md / task-breakdown.md |  |
| assetBaselineDecision | follow-asset-baseline / not-applicable / unknown | evidence.md / frontend-design.md / task-breakdown.md |  |
| questionGatePreservationStatus | required / clear / blocked / unknown | frontend-design.md / contract-check.md / task-breakdown.md | `required` 时不得进入 runnable implementation |
| enumImportMapStatus | ready / partial / missing / not-applicable / unknown | evidence.md |  |
| legacyRiskCount | 0 / number / unknown | evidence.md / frontend-design.md / review report |  |
| blocksRunnableImplementation | yes / no / unknown | evidence.md / frontend-design.md / task-breakdown.md |  |

## Open Items
| type | item | source | owner | blockingProductionReady | blockingDemoVerified | next |
| --- | --- | --- | --- | --- | --- | --- |
| blocker / missingContract / conflict / userConfirmation / verificationGap / productionReplacement / reviewFinding / manualFinding |  |  | user / frontend / backend / platform / main-flow | yes/no | yes/no |  |

## Handoff Read Order
1. `frontend/index.md`
2. `frontend/design/contract-check.md`
3. `frontend/design/frontend-design.md`
4. `frontend/tasks/task-status.md`
5. 当前阶段需要的具体产物，例如 `task-breakdown.md`、Review 报告、`verification-report.md` 或 Handoff 文件。

## Context Compression Rules

- 存在 `frontend/index.md` 时，跨轮恢复、agent 换手和长上下文继续执行必须先读取本文件，再按 `Current Stage`、`Current Status`、`Open Items` 和 `Canonical Sources` 裁剪输入。
- 本文件是导航入口，不是事实覆盖源；发现 index 与 canonical source 冲突时，读取对应 canonical source 修正 index，不得用长对话记忆覆盖事实源。
- `Engineering Evidence Summary` 只记录探索等级和 comparison 摘要；完整 `baselineComparison` 必须留在 `evidence.md` 或 `frontend-design.md`，不得复制长表格到 index。
- 当 `evidenceReuseStatus=reusable`、`evidenceStatus=ready`、`scopeFingerprint` 一致且目标工程/模块/页面范围未变化时，后续阶段必须直接复用 evidence，`preDesignEvidenceDecision=reuse-ready`、`nextExploreAllowed=none`，不得重新调度 Explore 或从仓库根重新搜索。若确需补证据，必须先把 `evidenceReuseStatus` 改为 `missing-required-field / target-changed / conflict`，写明 `deltaExploreReason`，并把所有缺口批量写入 `targetedDeltaRequests[]`；每个 request 保留单项 `targetedDeltaScope`。除 `target-changed / index-evidence-conflict` 外，只允许一次批量 targeted-delta，不允许 full medium/thorough re-explore。
- 当 `reviewStatus=pass/conditional`，Review 报告存在，且 `reviewScopeFingerprint`、`reviewedChangedFiles`、reviewPurpose、Contract/Task/Design 来源、acceptedReviewFindings 和 Open Items 均未变化时，后续阶段必须复用 Review 结果；返工复查默认 `reviewMode=fix-package-recheck`，不得无失效原因重新 full-scan。
- 默认不得全量回读 FDS/TDS/MDS/FSS、design、task、review、verification、handoff 和源码。只有当前阶段读范围要求、Open Items 指向、状态冲突、缺失证据或用户明确要求时，才读取额外材料。
- 每次阶段输出或换手时，只更新路径、状态摘要、开放事项和下一步；长表格、完整 findings、完整验证日志和生产替换明细必须留在对应 canonical source。
- 每次更新 `Current Status` 时必须在同一次写入中更新顶部 `frontend-canonical-state`。`status` 取 `handoffStatus`；`frontendAutoRunId/repairDispatchStatus/repairClosureHash` 必须原样复制 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py --repair-closure-stage-result <frontend-stage-result.json>` 的输出，禁止手算或从其它 owner 文档反推。该状态块由 Handoff preflight 读取，不得由 preflight request 另行声明 observed/sync 状态；helper 失败只修当前状态源，不触发业务阶段重跑。

## Stage Read Scope

| currentStage | mustRead | readIfNeeded | doNotReadByDefault |
| --- | --- | --- | --- |
| Explore / Evidence | `frontend/index.md`、已有 `frontend/evidence/evidence.md` | FDS/TDS/MDS/FSS、figma-cache、目标工程最小目录证据 | task-status、review、verification、handoff |
| Frontend Design / Contract Check | `frontend/index.md`、FDS/TDS/MDS/FSS、evidence、contract-check/frontend-design 草稿 | figma-cache、后端 readiness、生产替换草稿 | task-status、review、verification、handoff |
| Design Confirm | `frontend/index.md`、frontend-design、contract-check、Open Items | clarifications、ui-contract、production-replacement-draft | verification、handoff、源码全量扫描 |
| Task Breakdown | `frontend/index.md`、frontend-design、contract-check、task-status 当前快照 | evidence、production-replacement-draft、backend readiness | verification、review、handoff、源码全量扫描 |
| Implementation | `frontend/index.md`、task-breakdown、task-status、design 摘要、目标文件/相似实现 | contract-check、evidence、ownerReferenceCapsule、validator 结论 | review、verification、handoff、全量 FDS/MDS/FSS |
| Review / Final Review | `frontend/index.md`、changedFiles/diff、task-status、design/task 验收 | verification-report、contract-check、handoff checklist、sourceReviewPath、recommendedFixPackage | 全量 FDS/MDS/FSS、无关源码目录 |
| Verification | `frontend/index.md`、changedFiles、task-status、验证目标、候选命令证据 | design/task 验收、review findings、contract-check | handoff、全量源码扫描 |
| Handoff | `frontend/index.md`、task-status、review、verification、artifact-index、production-replacement-checklist | design、task-breakdown、contract-check、lessons-learned | 全量源码、全量历史对话 |

## Index Boundary
- 本文件是过程索引，不是业务设计、任务、验证或交付正文；不得复制长表格、长 findings、完整验证日志或完整生产替换清单。
- 每个阶段只更新自己负责的状态摘要和路径指针；事实细节必须回写对应 canonical source。
- `handoff/artifact-index.md` 是最终交付索引；本文件是跨轮恢复和阶段换手入口。两者状态冲突时，Handoff 阶段必须回读 canonical sources 并修正冲突，不得直接覆盖事实源。

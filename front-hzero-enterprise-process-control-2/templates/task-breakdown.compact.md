# Compact Task Breakdown Template

建议路径：`sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md`
适用范围：`taskProfile=compact`，以及普通 `demo-slice / regular-change` 的默认可执行视图；`taskProfile=expanded` 也可先从本模板起步再按需展开并行/共享矩阵。本模板不复制 Frontend Design 的完整矩阵。

## Document Status
- Feature：
- Feature Root：`sdd-workspace/changes/{change-id}/`
- Frontend Root：`sdd-workspace/changes/{change-id}/frontend/`
- Design Source：`frontend/design/frontend-design.md`
- Contract Check：`frontend/design/contract-check.md`
- Task Status：`frontend/tasks/task-status.md`
- frontendExecutionMode：demo-slice / regular-change
- taskProfile：compact / expanded / audit
- taskSizeHint：direct / standard / large
- taskCount：
- taskProfileReason：none / evidence
- ownerReferenceCapsule：ready / reused / invalidated + reason
- specialtyTriggers：trigger-only / owner-loaded / not-applicable + riskDomains
- validationHandoff：intent / riskDomains / acceptanceSignals / candidateVerificationEntries / unresolvedVerificationInputs / downstreamOwners
- optimizationExecutionManifest：仅 `optimizationProfile=expanded` 时为 `frontend/evidence/optimization-execution-manifest.json`；compact 写 not-required
- Task Ready Result：`frontend/evidence/task-ready-result.json`
- implementationDispatchPlan：`frontend/evidence/implementation-dispatch-plan.json`
- Can Enter Implementation：yes / no + reason
- parallelFeasibilityDecision：parallel-ready / shared-first-required / serial-only / blocked / not-applicable

规则：本文件是唯一 canonical 任务定义。禁止创建根级 `frontend/task-breakdown.md`、映射桩或 by-reference 副本。
机器读取的 list cell 只能使用逗号分隔值、`none/not-applicable` 或 `[]`；禁止把整个数组写成 `` `[FE-001]` ``。Task Execution validator 对该历史格式直接失败，不保留兼容解析。

任务计数只设上限、不设下限：`direct` 最多 3 项，`compact/standard` 最多 7 项。任务按独立写入所有权、真实依赖和可独立验收结果拆分，不为满足 profile 数量机械拆分；单一可执行交付物允许只保留 1 个任务。

## Write Scope And Placement
| field | value |
| --- | --- |
| packageDir / pageDir |  |
| allowedArtifactRoots | `frontend/tasks/**`；Task optimization evidence 固定路径 |
| allowedBusinessWriteFiles | Task 阶段必须为 `[]` |
| readOnlyRefs | Design、Contract Check、ownerReferenceCapsule、validationHandoff、context pack |
| targetPlacement | placementType / parent registration / forbidden paths / status |

## File Mapping
| path | action | ownerTaskId | sliceId | writeMode | source |
| --- | --- | --- | --- | --- | --- |
|  | create / modify / verify |  |  | slice / shared / integration | Design / Contract / generated scaffold |

## Shared Contract
| contract | value / sourceRef | ownerTaskId | consumers | status |
| --- | --- | --- | --- | --- |
| route / service / mock / permission / i18n |  |  |  | frozen / candidate / blocked |

## Task Overview
| taskId | title | sliceId | type | status | dependencies | changedFilesPlan | acceptanceRef | next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FE-001 |  | SL-SHARED | task | Ready | [] | [] | `#FE-001` |  |

## Parallel Slices
| sliceId | taskIds | prerequisites | writeFiles | evidenceWriteFiles | prerequisiteOutputs | readOnlySharedFiles | canRunInParallel | integrationTaskId | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SL-SHARED |  | none |  | [] |  |  | no |  | shared-first |

规则：单任务、单文件组、无 feature lane 且无 shared 写入时，可写 `parallelFeasibilityDecision=not-applicable`，不需要 `serialOnlyDecisionEvidence`。`serial-only` 只用于存在多个候选 feature lane 但 shared-first 后仍无法并行的场景，必须逐 lane 证明真实依赖或写冲突。用户未要求并发、当前只生成 Task 产物、任务数量较少或保守起见均不是有效串行理由。

所有权门禁：路径统一为 frontend-root-relative；feature slice（如 `SL-LIST/SL-DETAIL/SL-LINE`）不得拥有 shared constants、平台 locale ledger、servicePrefix、`dev-mock` 聚合入口、shared mock store、跨页 response schema、router/config、父工程注册或 package registry；这些文件只能归 shared/integration lane，并写入 `prerequisiteOutputs` / `sharedPrerequisiteFiles` / `integrationWriteFiles`，不得混进普通 feature `writeFiles`。页面私有且路径不重叠的 mock handler/fixture 可由 feature slice 持有；禁止通过 merge 字段把 shared 文件重新授权给 feature slice。

详情页只在合同先冻结且写入集合完全不重叠时才可拆 `detail-contract` / `detail-ui` 两个 lane。前者持有 DataSet、service、页面级 mock fixture/handler、LOV contract fragment 与 response shape，并以 `prerequisiteOutputs` 输出 contract/fixture/字段 shape 引用；后者只持有 Form、LineTable、Attachment、layout、交互组件和局部样式，并依赖前者。合同未冻结、文件重叠、或 UI 需反向改写同一数据/mock 文件时，必须合并为同一 owning slice 或串行，不得伪造并行。

## Execution Groups
| executionGroupId | groupType | sliceIds | taskIds | prerequisites | sharedPrerequisiteFiles | integrationWriteFiles | contractFidelityRequired | dispatchMode | requiredOwningAgentDispatchCount | serialFallbackPolicy | completionGate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| G1 | serial / parallel / integration | [] | [] | none | [] | [] | yes / no | serial-task / parallel-slice / serial-integration | 1 | blocked / serial-fallback-with-reason / not-applicable |  |

规则：并行组的 `requiredOwningAgentDispatchCount` 必须等于 `canRunInParallel=yes` slice 数量。Implementation 前必须生成结构化 dispatch plan，并使用已确认的绝对 `targetRoot` 运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_dispatch.py --target-root <targetRoot>`；所有业务路径只能相对该根，禁止重复目标工程目录名。运行期不能并发时只在首次调用前将 plan/lease 改为逐 slice owning Agent 直调的 `serial-fallback + reason + affectedSliceIds`，不回写 Task DAG；失败时不得创建任何 Implementation Agent 调用。

## Design Coverage Mapping
| ledgerId | taskId | mappingStatus | acceptanceRef | reason |
| --- | --- | --- | --- | --- |
|  | FE-001 / replacement / blocker / no-code | mapped / blocked / replacement / not-applicable | `#FE-001` |  |

规则：本节只承接 Design Coverage Ledger 的 ID 映射，不复制完整 Design Coverage Ledger、UI Contract、Button Semantic Matrix、字段状态机或生产矩阵。`required=yes` 的 ledgerId 必须映射到具体 task、replacement、blocker 或 `not-applicable + reason`；可执行映射必须与任务详情 `coverageRefs` 双向一致。

## Task Details
### FE-001 - <title>
- sliceIds：[]
- coverageRefs：[]
- changedFilesPlan：[]
- Contract Acceptance：
- UI Acceptance：
- Verification Acceptance：
- Rejection Criteria：
- validatorPlan：
- statusUpdateProposal：

规则：同一任务合并多个并行 slice 时必须写 `sliceIds` 或 `parallelizableSubtasks`。详细字段、按钮、状态和生产矩阵只写 `coverageRefs`、轻量 acceptance 摘要和 owner reference，不得从 Design 复制长表。命中基础信息 / HeaderForm 的 `Basic Info Form Layout Contract` 且满足默认布局的统一触发条件时，`UI Acceptance` 必须保留 `default-form-layout-by-design-rule` 的 `containerWidthPolicy=content-available`、`lg=3` 列、`labelWidth=120`、横向标签、`responsiveColumns=xs=1, sm=1, md=2, lg=3` 和 `colSpan/valueOverflowPolicy` 的可检查摘要，或保留基于可用宽度、字段密度、标签/值长度和字段语义的 `layoutAdjustmentReason`；调整 `3/2/1` 列、labelWidth、跨度或断点不需外部设计来源，也不设字段数自动阈值。审计/后端生成字段的显隐、只读和 `submitPolicy` 必须继承 Field Visibility / Editability Matrix 的逐字段验收。固定 max-width、居中仍需来源；字段顺序和卡片化按独立合同验收。
专项 trigger 默认只映射为 Contract/UI/Verification Acceptance、validatorPlan、riskDomain 和 downstream owner；ownerReferenceCapsule 未加载的专项不得在 Task 阶段整包读取。只有 capsule invalidated、新增风险域、任务验收无法由模板/摘要闭合、production-ready、conflict 或 blocked 时，才允许增量加载 owner reference 并记录原因。

Risk-driven validatorPlan 固定路由：DataSet/Lov/bind/Form/Table/Modal/enum-like props 命中 `c7nComponentApiValidator`；`queryMode=mock-request` 命中 `mockRequestValidator`；Import/ExcelExportPro 或 import-export risk domain 命中 `importExportPermissionsValidator`；详情/主从、保存后跳转、状态动作、权限承载、generatedCandidate/对象 LOV、只读动作、导入导出、mock ID/enum 或附件 carrier 命中 `contractFidelityValidator(schemaVersion=1.1)`。每个命中项必须写 command、target、owning task 和 pre-Review 时点；未命中项写 `not-applicable + reason`。不得因为 changedFiles 中存在普通 `.tsx` 就全跑 import-export/contract-fidelity，也不得为运行这些静态 validator 新增领域路由 Agent。

并行组命中 contract fidelity 时，Execution Group 必须写 `contractFidelityRequired=yes`，每个 slice 的 `evidenceWriteFiles` 必须包含唯一 `evidence/contract-fidelity/slices/<sliceId>.json`，slice 只写 schemaVersion=1.0 fragment。`evidenceWriteFiles` 统一为 frontend feature-root-relative，不得进入 frontend-root-relative `writeFiles`，也不得在 `targetRoot` 下解析。canonical `evidence/contract-fidelity.json` 和 `evidence/contract-fidelity-merge.json` 归 fan-out 后的确定性 merge step，不归任一并行 slice、Design 或 shared business integration task；Task 不为该 merge 新增 Agent 或 execution group。

## Task Gate
| gate | result | evidence / unresolved |
| --- | --- | --- |
| Readiness | pass / fail | Design Confirm、Contract Check、Target Placement、UI/API/route/mock/replacement 合同是否足够拆 runnable task |
| Mapping | pass / fail | `coverageRefs`、`changedFilesPlan`、`acceptanceRef` 和 Design Coverage Mapping 是否守恒 |
| Execution | pass / fail | `writeFiles`、`prerequisiteOutputs`、`sharedPrerequisiteFiles`、`integrationWriteFiles` 统一为 frontend-root-relative；`evidenceWriteFiles` 为 feature-root-relative 且不在 `targetRoot` 下解析 |
| Dispatch | pass / fail / not-applicable | pre-Implementation 使用同一个绝对 `targetRoot` 运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_dispatch.py --target-root <targetRoot>` 和 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/authorize_frontend_implementation_dispatch.py` 生成 dispatch lease；失败时不得创建任何 Implementation Agent 调用；单任务 direct-no-task 例外写 not-applicable + reason |
| Closeout | pass / fail | Task Ready validation 通过；`task-status.md` 初始投影由 Task owner 内部同步，不作为外层 blocker |

Validator 分层：Task 阶段只运行 schema 1.1 Task Ready validation；进入 Implementation 前再分别运行当前 execution group 的 `implementation-dispatch` 与 `implementation-dispatch-lease`。Task Ready 内部重算 canonical、coverage mapping、task/dependency、path/shared-write 和 execution group 安全；不读取 Task Profile、Task Execution Plan、Task Closeout 的独立结果。可自动修复的路径或映射缺字段最多窄修一次；业务决策、扩大写入范围或真实越权风险立即止损。

存在只读 `frontend/design/lov-candidate-contracts.json` 时不扩展 Task 文档：它必须已作为 Design canonical frozen source；Task Ready 通过重跑 canonical validator 直接复核 manifest/hash/`contractFreezeId`，不复制子 validator 结果。mock-request、contract-fidelity 使用同一 `--lov-candidate-manifest`；不得由 Task/Implementation 生成兼容候选或自报 N/A。

Task Ready Result：Task owner 写 `frontend/evidence/task-ready-result.json`，字段只包含 `schemaVersion=1.1`、`owner=frontend-task-agent`、`optimizationProfile`、`createsSubmodule`、canonical task paths、`readyForDispatchPlanning`、`primaryAction=consume-only` 和 blockers；不写 `gateResults`、command 或中间 resultPath。随后运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_task_ready_result.py --input <feature-root>/evidence/task-ready-result.json --root <feature-root> --out <feature-root>/evidence/task-ready-validation.json`。validation 现场重算四类检查并绑定 Design/Task 当前哈希，是 dispatch 唯一 eligibility 输入。

Blockers / Replacement：阻塞项和生产替换项直接写入相关 `Task Details.statusUpdateProposal` 或 `task-status.md` 初始 blocker 表，本 compact 文件不重复维护长表。

## Implementation Handoff
| field | value |
| --- | --- |
| taskBreakdownPath | `sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md` |
| taskStatusPath | `sdd-workspace/changes/{change-id}/frontend/tasks/task-status.md` |
| implementationDispatchPlanPath | `sdd-workspace/changes/{change-id}/frontend/evidence/implementation-dispatch-plan.json` |
| implementationDispatchValidationPath | `sdd-workspace/changes/{change-id}/frontend/evidence/implementation-dispatch-validation.json` |
| implementationDispatchLeasePath | `sdd-workspace/changes/{change-id}/frontend/evidence/implementation-dispatch-lease-<group-id>.json` |
| taskReadyResultPath | `sdd-workspace/changes/{change-id}/frontend/evidence/task-ready-result.json` |
| taskReadyValidationPath | `sdd-workspace/changes/{change-id}/frontend/evidence/task-ready-validation.json` |
| implementationOrder |  |
| firstDispatchableTaskIds |  |
| productionBoundary | mock-demo / production-ready + replacement status |

规则：`task-status.md` 只保存 Task List、Board Summary、Status Updates、blockers 和后续阶段 result proposal；不得重复复制任务验收正文、Design 长矩阵或专项 SOP。

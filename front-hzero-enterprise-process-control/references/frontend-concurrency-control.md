# Frontend Concurrency Control

本文是 HZERO Lite 主流程与企业前端子流程的运行时并发控制参考，用于统一前后端并行启动、前端内部多 slice 并行、共享文件锁、汇合判定和降级处理。它不是交付产物，也不写入业务 Change 工作区。

## 阅读路由
- 判断是否适用并发规则时读 `适用范围` 和 `并发层级`。
- Lite 前后端并行前读 `全局并行启动条件` 和 `全局禁止并行`。
- 前端内部多 slice 并行前读 `Shared-First Lane Model`、`前端内部并行启动条件`、`共享文件锁` 和 `串行 Integration Task`。
- 阶段结果回写、暂停或返工时读 `状态回写`、`暂停与回退`。
- 汇合或 Handoff 前读 `全局汇合判定` 和 `Agent 引用要求`。

## 适用范围

- Lite 主流程中的后端 `编码实现` 与前端 `frontend-auto-agent` 并行组。
- `frontend-auto-agent` 内部由 Task Breakdown 产出的多模块、多页面或多 feature slice 并行执行。
- Review、Verify、Handoff 对并发执行结果的状态回写和汇合判断。

不适用于：

- 单阶段问答、纯探索、纯设计或纯 Review 请求。
- 未进入编码实现的 Contract Check、Frontend Design 或 Task Breakdown 阶段。
- `hzero-auto-agent` 完整主流程。

## 并发层级

| 层级 | 发起者 | 并发对象 | 稳定输入 | 汇合点 |
| --- | --- | --- | --- | --- |
| 全局并行组 | `hzero-auto-agent-lite` | 后端 `编码实现` + 前端 `frontend-auto-agent` | 已确认 TDS、元数据、前端设计、共享契约、默认 mock/demo 决策、验证范围 | Lite `并行汇合` |
| 前端内部并行 | `frontend-auto-agent` | Task Breakdown 中的 `parallel-slices` | `task-breakdown.md`、`task-status.md`、`parallel-slices`、`shared-file-locks` | 前端 Integration / Review / Verify / Handoff |
| 串行集成收口 | `frontend-auto-agent` / `frontend-task-agent` | route/menu/i18n/shared service/mockPluginIntegration/mockHandlerRegistration/runtime/config 及 test entry 等共享写入 | `integrationTaskId`、共享文件锁释放条件 | 前端统一 Review / Verify |

## Shared-First Lane Model

多功能并行不能只按“模块不同”判断，必须按写入面、共享文件锁和契约依赖判断。推荐模型是：先串行冻结 shared-scope，再并行执行互不交叉的 feature lane，最后串行处理 integration / drift / handoff 收口。

`shared-scope-present` 只能说明需要 shared-first，不得直接说明 `serial-only`。Task Breakdown 必须先把共享写入移动到 shared serial / integration task，并评估剩余 feature-scope 是否可并行；只有 `parallelFeasibilityMatrix` 证明候选 feature lane 仍存在同文件写入、硬顺序依赖、未冻结契约、无法移动的共享写入、工具限制或用户选择时，才允许输出 `serial-only`。

Task Breakdown 必须先做 scope partition：

| scope | 典型文件 / 行为 | 并发策略 |
| --- | --- | --- |
| shared-scope | 父工程配置、根 `package.json` / lockfile / workspace、packages 注册、route / microConfig 聚合、全局权限 / i18n、公共组件、公共 service/helper、公共 mock/plugin 聚合入口、同一共享文件 | 必须串行；多个模块同时需要写同一父工程配置时，由一个 shared-scope task 一次性生成合并 patch |
| feature-scope | 各自模块 / feature 内页面、DataSet、service、model、mock handler、局部样式、局部组件、局部 i18n | shared contract 冻结后可并行；不得写 shared-scope 文件 |
| handoff-scope | Review / Verification / Handoff 产物、artifact index、production replacement checklist、集成验证记录 | 汇合阶段串行或单 owner 写入 |

单任务、单文件组、无 feature lane 且无 shared 写入时，不进入 shared-first 评估，允许 `parallelFeasibilityDecision=not-applicable`、`parallelFeasibilityMatrixStatus=not-applicable`、`serialOnlyDecisionEvidence=not-applicable`。该路径不得用于规避多页面、多模块、多 feature lane 或 shared-scope 的并行判断；一旦存在两个及以上候选 feature lane、parallel execution group、shared-file-locks 或 integration task，就必须按 shared-first 模型判断 `parallel-ready / shared-first-required / serial-only / blocked`。

Shared-first 执行顺序：

1. `Shared Planning`：枚举所有候选功能的 shared-scope、feature-scope、handoff-scope，合并公共改造点。
2. `Shared Serial Patch`：串行完成父工程配置、包注册、route/microConfig、mock plugin 聚合、公共权限/i18n 等 shared-scope patch。
3. `Shared Contract Freeze`：冻结 `packageName`、`packageDir`、`routePrefix`、`menuGroup`、`permissionPrefix`、`i18nPrefix`、`mockMountPath`、`parentRegistrationFiles`、`allowedSharedFiles` 和 `sharedContractVersion`。
4. `Parallel Dispatch Plan`：把 parallel execution group 展开为多个独立 slice Todo，记录 `executionGroupId`、`groupDispatchId`、`sliceIds`、每个 slice 的 `writeFiles/sharedFiles/taskIds`、`requiredOwningAgentDispatchCount` 和 `serialFallbackPolicy`。
5. `Parallel Feature Lane`：各 feature lane 只消费 frozen shared contract，并只写自身 feature-scope。
6. `G3.5 Slice Local Quality Gate`：每个 slice 完成后先做局部 changedFiles 映射、Task Acceptance Scan、适用 validator 预跑、slice-local targeted Review 和未验证项登记；通过后才允许进入共享 integration。
7. `Shared Drift Gate`：Implementation / Review / Verify 发现遗漏 shared-scope 改造点时，暂停受影响 lane，回到 shared-scope 串行补丁，更新 shared contract 后恢复并行。
8. `Final Integration Gate`：统一检查父工程注册、route/microConfig、mock plugin、权限/i18n namespace、构建入口、共享文件版本和各 lane 依赖的 shared contract 是否一致。

可验证锚点：

- `scopePartitionStatus=ready | partial | blocked`
- `sharedContractStatus=frozen | updated-after-drift | missing | blocked | not-applicable`
- `sharedContractVersion=<string>`
- `sharedScopeTaskIds=[]`
- `featureLaneIds=[]`
- `parallelDispatchPlanStatus=ready | blocked | serial-fallback`
- `parallelFeasibilityDecision=parallel-ready | shared-first-required | serial-only | blocked | not-applicable`
- `parallelFeasibilityMatrixStatus=ready | missing | partial | not-applicable`
- `serialOnlyDecisionEvidence=present | missing | not-applicable`
- `sliceLocalQualityStatus=pass | failed | partial | not-run`
- `blockedBySharedScope=[]`
- `sharedDriftFindings=[]`

`sharedContractStatus` 不是口头确认。必须能追溯到 Task Breakdown 的 scope partition、shared-file-locks、integrationTaskId 和 task-status 回写。缺少这些锚点时，多个 feature lane 不得进入并行 Implementation。

`serial-only` 也不是口头确认。必须能追溯到 Task Breakdown 的 `Parallel Feasibility Matrix` 和 `Serial Only Decision Evidence`：每个候选 lane 为什么不能变成 `feature-parallel`，共享写入为什么不能由 integration task 收口，是否存在工具/环境限制，或用户是否明确选择串行。缺少这些证据时，Task Gate 应回到 Task Breakdown 修正，不得把整包 Implementation 当作合规串行计划。

## 全局并行启动条件

Lite 只有在以下条件全部满足时，才允许创建后端 + 前端并行组：

- TDS 已确认，且与 FDS 无未解决冲突。
- 元数据生成完成，并输出 API、字段、权限、菜单、值集、导入导出等前端可用契约摘要。
- 前端设计完成且已通过统一人工确认。
- API、字段、权限、路由、菜单、LOV/lookup、附件、导入导出等共享契约已冻结，或已明确降级为 mock/demo / temporary contract。
- 默认 Mock demo 决策和 Mock 接线状态明确；只有当前 Mock 必需契约或 Mock 接线无法闭合时，不得启动前端 runnable 实现。用户拒绝 Mock 或要求真实 API 不改变本轮 Mock 目标，只进入后续 advisory。
- 后端和前端的写入边界、共享资产归属、共享文件锁和集成收口条件明确。
- 前端子模块输入包含 FDS、TDS、元数据、前端设计、契约冻结摘要、前后端边界、验证范围和最终编译命令或候选命令。

## 全局禁止并行

任一条件命中时，Lite 不得启动并行组：

- API 契约未确认，且前端实现依赖真实接口。
- 前端工程目录、父工程 / 子模块落点或 Frontend Root 未确认。
- 权限码、路由、菜单未确认，且用户要求 production-ready。
- 前后端需要修改同一共享资产，但未定义锁归属和释放条件。
- FDS、TDS、元数据或前端设计存在未解决冲突。
- 当前 Mock 必需契约缺失，或 Mock 接线无法闭合。
- 前端 Task Breakdown 尚未给出可执行任务、任务状态源或不可落盘原因。

## 前端内部并行启动条件

`frontend-auto-agent` 只有在 Task Breakdown 给出明确并行计划时，才允许内部并行调度多个 slice。

必须具备：

- `sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md`
- `sdd-workspace/changes/{change-id}/frontend/tasks/task-status.md`
- `parallel-slices` 表，且每个 slice 有 `sliceId`、`taskIds`、`writeFiles`、`sharedFiles`、`prerequisites`、`canRunInParallel`、`integrationTaskId` 和 `verificationScope`
- `execution-groups` 表，且每个 group 有 `executionGroupId`、`groupType=serial/parallel/integration`、`sliceIds`、`dispatchMode`、`requiredOwningAgentDispatchCount`、`mergeOwner` 和 `serialFallbackPolicy`
- `shared-file-locks` 表，且 route/menu/i18n/shared constants/shared service/mockPluginIntegration/mockHandlerRegistration/runtime/config 及 test entry 等共享文件均由串行 integration task 持有
- `scope-partition` 和 `shared-contract-freeze` 信息；多功能、多模块或多 package 并行时必须有 `scopePartitionStatus=ready` 和 `sharedContractStatus=frozen/updated-after-drift/not-applicable + reason`
- 每个 slice 的目标文件、changedFiles、验收点和回滚边界独立
- 执行前已形成 `Parallel Dispatch Plan`；`groupDispatchId` 是唯一批次身份。若运行环境不能并发，可在首次 owning Agent 调用前把 plan 整体改为 `serial-fallback + serialFallbackReason + affectedSliceIds`，仍保持一 slice 一 Todo；只能形成单个整包 Todo 时必须 `parallel-dispatch-internal-repair` 并回 Task owner 重建 slice contract
- 每个执行组必须形成 `implementation-dispatch-plan.json` 并使用同一个已确认的绝对目标工程根通过 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_dispatch.py --task-breakdown <task-breakdown.md> --task-ready-validation <task-ready-validation.json> --dispatch-plan <dispatch-plan.json> --target-root <target-root> --out <dispatch-validation.json>`；实际发令前再运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/authorize_frontend_implementation_dispatch.py --task-breakdown <task-breakdown.md> --task-status <task-status.md> --task-ready-validation <task-ready-validation.json> --dispatch-plan <dispatch-plan.json> --target-root <target-root> --execution-group <group-id> --out <implementation-dispatch-lease-<group-id>.json>`。Task Ready validation 固定为 schema 1.1，两个消费者对账 Task、Design canonical 与 Coverage Ledger 绑定 hash；源结果或冻结 DAG 变化时旧 proof 失效，只回 Task owner重跑原子 validation。dispatch validator 拒绝 Todo 数量不足、缺唯一 slice、scope 漂移、重复目标工程前缀或整包目标；lease 把当前 Task/status/Task Ready validation/plan hash 与 `groupDispatchId` 绑定，并拒绝 Task Gate failed、前置组未完成或 shared 输出缺失。任一失败时不得调用 Implementation Agent，也不得路由 General；lease 到 agent call 之间不得改写输入。
- 路径基准固定：`writeFiles`、`prerequisiteOutputs`、`sharedPrerequisiteFiles`、`integrationWriteFiles`、dispatch plan file scope 和 prerequisite file scope 一律使用 `frontend-root-relative`；`targetRoot` 只用于把这些相对路径解析到物理文件系统，不得改变字段口径，且其目录名不得再次出现在相对路径首段。举例：`targetRoot=/Users/david/Desktop/sdd-all/h0-demo-test` 时的正确写入是 `packages/prm/...`，`h0-demo-test/packages/prm/...` 必须在 dispatch validation / lease 阶段拒绝。若文件在真实文件系统存在，但 `targetRoot + relative` 拼接失败，应判定为 path-baseline mismatch，而不是普通 missing file。
- 若已进入 Implementation，但 manifest 仍为 `dispatchLeases=[]` 或缺少当前组 passed/leaseGranted 的 resultPath，必须立即回到 Task closeout / Parallel Dispatch Plan / dispatch lease 修复点，内部路由码固定为 `implementation-dispatch-internal-repair` 或 `optimization_execution_dispatch_lease_missing`，并写 `requiresUserDecision=false`。这类问题说明实际发令证据不存在，不允许在 Handoff 阶段降级成普通风险，也不允许用一个整包 Implementation session 反向补写为并行完成，但不得形成用户可见 blocker。

同一并行组内 slice 必须满足：

- 不写同一文件。
- 不依赖彼此尚未完成的产物。
- 不共享同一未确认 API、权限、LOV/lookup、附件 bucket、导入模板或平台协议。
- 不共同修改全局 model、runtime config、microConfig、app.tsx、request/interceptor 或父应用注册入口。
- 不写入锁定中的共享文件。
- 不新增 shared-scope 写入；发现需要新增 shared-scope 时，当前 slice 必须暂停并产生 `shared-scope finding`，不得顺手修改公共文件。

已有前端文件只要已列入当前 slice 的 `writeFiles` 或串行 `integrationTaskId` 的写入范围，就按普通可写文件处理，不因其是存量文件而触发逐文件人工确认。若需要写入映射外已有文件、只读参考文件或锁定共享文件，必须暂停并按 `front-hzero-enterprise-process-control` 的写入范围合同回到 Task Breakdown / Integration task / 人工确认。

## 共享文件锁

共享文件必须通过 `shared-file-locks` 串行控制。

锁表至少包含：

| 字段 | 说明 |
| --- | --- |
| sharedFile | 共享文件相对目标工程路径 |
| lockOwnerTaskId | 持锁任务，必须是串行 integration task |
| writeStage | 允许写入阶段 |
| readOnlySlices | 只能只读该文件的 slice |
| releaseCondition | 锁释放条件 |
| conflictAction | 冲突时动作：暂停并回到 Task Breakdown / Integration task / 人工确认 |

共享文件包括但不限于：

- 父工程 package / workspace / lockfile / packages 注册入口
- route/menu 注册入口
- i18n 聚合入口
- shared constants / shared service / shared DataSet
- mockPluginIntegration / mockHandlerRegistration / mock store
- runtime / config / microConfig / app.tsx
- test setup / e2e entry / verification entry

锁未释放前，任何并行 slice 都不得写入该共享文件。发现 slice 需要写共享文件时，必须把写入移动到 `integrationTaskId`，或暂停并回到 Task Breakdown 修正并行计划。

## 串行 Integration Task

以下工作必须作为串行 integration task，不得放入普通并行 slice：

- 多模块 package 注册、父工程配置、根 workspace / package / lockfile / scripts 变更。
- route/menu 注册与权限资源汇总。
- i18n 聚合和导出入口更新。
- shared service、shared constants、shared DataSet、mockPluginIntegration/mockHandlerRegistration 的统一收口。
- 父应用、微前端、runtime、config、app.tsx、microConfig 级变更。
- 最终编译命令、统一验证入口和 Handoff 状态汇总。
- 多 slice 的生产替换清单合并。

`integrationTaskId` 必须出现在 `parallel-slices` 表和任务详情中，并写明依赖哪些 slice、持有哪些共享文件锁、什么时候释放锁、失败后如何回滚或暂停。
多个功能都需要改同一个 shared-scope 文件时，应优先创建一个合并后的 shared-scope integration task，一次性写入完整 patch；不得让多个 feature lane 分别并行修改同一父工程配置、注册文件或公共入口。

## 状态回写

每个并行 slice 完成后，必须回写 `task-status.md`：

- `executionGroupId`
- `groupDispatchId`
- `dispatchMode`
- `taskId`
- `sliceId`
- `integrationTaskId`
- `laneFrom / laneTo`
- `statusFrom / statusTo`
- `changedFiles`
- `changedFilesSource`
- `cumulativeChangedFiles`
- `sharedFilesTouched`
- `blockersOpened`
- `resolvedBlockers`
- `reviewStatus`
- `verificationStatus`
- `evidence`
- `agentDispatchTrace`
- `next`

不得只写“slice 完成”或“全部完成”。每个 changedFile 必须能映射到 File Mapping、targetFiles、parallel-slices.writeFiles、integrationTaskId 或 approved recommendedFixPackage；并行 slice 的 `sharedFilesTouched` 必须为空，除非当前任务就是锁持有 integration task 且 `changedFilesSource=integrationTaskId`。

并发执行时，子任务默认只返回 `task-status-updates` proposal，不得直接并发写 `task-status.md`。同一执行组全部返回后，由 primary / owning stage 汇总落盘，并追加 `Execution Group Summary`，检查 changedFiles 来源、sharedFilesTouched、状态更新覆盖、blockers 对后续组的影响和 agent dispatch 覆盖。缺少 group summary、summary failed/blocked、同组任一 slice 缺独立 `frontend-implementation-agent` trace，或未能统一落盘时，后续组不得推进到 In Progress / Review / Verify。只有实际使用通用协调 fallback 时才需要额外的 `frontend-general-agent -> frontend-implementation-agent` trace；`dispatchMode=serial-fallback` 仍为 owning Agent 直调。

`parallel-ready` execution group 中有 2 个及以上 `canRunInParallel=yes` slice 时，必须实际调度多个独立 `frontend-implementation-agent` Todo。运行环境不能并发时，必须在发令前把 dispatch plan/lease 写为 `serial-fallback`，记录 `serialFallbackReason` 和完整 `affectedSliceIds`；slice 执行合同不完整时写 `parallel-dispatch-internal-repair` 并回 Task owner。fallback 仍逐 slice 直调 `frontend-implementation-agent`，不得因串行降级增加 General 中转，也不得把线性实现冒充并行执行。只有 owner 不明确、合同冲突或异常恢复等通用协调 fallback 条件命中时才使用 `frontend-general-agent`，且每个 General 只能承接一个 slice 后转交一个 owning Agent。

并行批次发令取得 session/tool handle 后，primary 必须立即执行 `Dispatch Acknowledgement Check`，按唯一 handle/evidence 计数，不按 Todo、slice trace 或声明字段计数。`acknowledgedOwningAgentDispatchCount` 必须等于 `requiredOwningAgentDispatchCount`，每个 slice 恰好对应一个 `actualAgentCall=true` 的 `frontend-implementation-agent` 调用，且不同 slice 不得复用同一 `sessionOrToolEvidence`。数量不足时只补发未 acknowledged 的 slice，不重派已启动 slice；补发仍失败则停止该 execution group。该 checkpoint 位于现有 fan-out 内，不新增流程阶段、Review、Verification 或 Agent。

并行实现进入 Artifact/Handoff 前必须对最终 stage-result、canonical Task Breakdown 和当前企业前端编排 root session 运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_runtime_trace.py --stage-result <stage-result.json> --task-breakdown <task-breakdown.md> --root-session-id <root-session-id> --strict --out <runtime-trace-validation.json>`。计划 slice 缺 trace、required/observed 数量不足、session evidence 不存在、多个 slice 复用同一 evidence 或真实 session 只有一个整包 Implementation 时不得伪报 owning Agent 调度通过。若实际调用不足但已有至少一个真实 owning Agent 调用，且 `slice-quality-gates-validation.json` 已证明 `passed=true + progressionDecision=allow-integration`，事后只写 `executionOutcome=under-dispatched-observed + costGovernancePassed=false + businessStageRerunAllowed=false`，允许 conditional Handoff，不得为补并发数据重跑已闭合的业务实现；缺 slice quality closure、零真实调用或伪造/复用 evidence 仍是 delivery 失败。report-only、fixture 结果或没有读取真实 session 的 shadow 结果不能作为交付证据。

G3.5 slice-local quality gate 必须在 parallel feature lane 完成后、integration task 或统一 Review/Verify 前完成。每个 slice 至少记录：

- `sliceId`
- `taskIds`
- `changedFilesMappingCheck`
- `taskAcceptanceScan`
- `validatorTargets`
- `validatorResults`
- `sliceLocalReviewStatus`
- `unverifiedItems`
- `next`

任一 slice 的局部门禁 failed / blocked / not-run 且无 `not-applicable + reason` 时，后续 integration、统一 Review、Verification 和 Handoff 不得推进；只能回对应 slice Implementation、Task Breakdown 或记录明确降级。

机械汇合门禁：每个 slice 只写自己的 feature-root-relative `evidence/slice-gates/<sliceId>.json`，申报 changedFiles、acceptance 和 requiredValidators；命中 contract fidelity 时还必须独占写 feature-root-relative `evidence/contract-fidelity/slices/<sliceId>.json`，该 fragment 路径必须进入对应 slice `evidenceWriteFiles` 与 dispatch lease 的 `allowedEvidenceWriteFiles`，不得进入 frontend-root-relative `writeFiles` 或在 `targetRoot` 下解析，禁止多个 slice 写同一 canonical evidence。当前 execution group 的 fan-out 全部返回后，primary 先运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/merge_frontend_contract_fidelity.py --fragment <slice-fragment>... --out <feature-root>/evidence/contract-fidelity.json --result-out <feature-root>/evidence/contract-fidelity-merge.json`；该脚本只做确定性 union、identity conflict 检查和 canonical 输出，不生成业务事实，不新增 Agent。随后 primary 串行求当前组 validator 并集，并用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/run_frontend_group_validator.py` 按 `validatorId + scope fingerprint` 各执行一次；TypeScript 必须传 `--package-dir <packageDir>`，runner 对旧调用缺参或误传 config 路径时从显式值、`validatorTarget` 或 `tsc -p` 最近的 `package.json` 确定性归一并记录来源，不得再把 config 文件当目录拼接 `package.json`。contract-fidelity 只消费合并后的 canonical manifest。顶层 `validatorRuns[]` 保存 coveredSlices/coveredFiles/resultPath/fingerprint，各 slice 用 `validatorRefs[]` 复用。随后聚合 `<feature-root>/evidence/slice-quality-gates.json` 并运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_slice_quality_gates.py --task-breakdown <task-breakdown.md> --gate-result <feature-root>/evidence/slice-quality-gates.json --root <feature-root> --out <feature-root>/evidence/slice-quality-gates-validation.json`；脚本按 gate result 的 `executionGroupId` 读取 Task `Execution Groups.sliceIds`，只校验当前组，Task 无 Execution Groups 的历史单组输入才 fallback 到完整 Parallel Slices，调用方也可重复传 `--slice-id` 显式限组。fragment missing/conflict、同一 fingerprint 重复执行、共享 validator 缺组结果、scope/fingerprint 过期或 slice 再内联同一 validator 都必须停留在当前组内部修复；package/config 参数混传和跨组 expected slice 是 invocation defect，只修参数并原地重跑，不生成业务 blocker。owner references 在组级只允许完整加载一次，`ownerReferenceCache.fullReferenceLoadCount=1`，当前组所有 slice 复用同一 capsule 且各自 `skillReferenceReadCount=0`。只有 merge 与 validator 输出都 passed 且 `progressionDecision=allow-integration` 才允许 integration。该门禁位于并行组之后，不减少、不串行化 feature slice。

组级 validator 失败时，按同一 validator/fingerprint/rootCause 合并一个 `group-local-repair`，仅在 affected slice write scopes 互斥或属于 integration scope 时一次调度；修复后只重跑失效 fingerprint。根因不同、write scope 冲突或需要扩大合同/任务时才拆包。该策略只合并机械返工，不合并正常 fan-out Todo。

运行时并行证据：Task 已声明 `groupType=parallel + dispatchMode=parallel-slice` 时，同组 trace 必须使用同一 `groupDispatchId`，并由 primary 完整记录 `dispatchRequestedAt / startedAt / completedAt`。严格 runtime trace 校验按唯一、真实存在的 session/tool evidence 计算 acknowledged owning Agent 调用，Todo 数、slice trace 数、`actualOwningAgentDispatchCount` 声明值和复用 evidence 均不能制造调用数。真实重叠为 `executionOutcome=parallel-confirmed`，缺时序为 `parallel-unproven`，完整时序但零重叠为 `serialized-observed`。后两者必须写 `costGovernancePassed=false`，不得宣称并行收益，但不触发业务代码重跑，也不覆盖已成立的实现、Review、Verification 或允许的 conditional Handoff。若因环境、锁、dirty/conflict 或不可拆上下文无法并发，必须在首次 owning Agent 调用前由 dispatch plan/lease 冻结 `serial-fallback`，所有受影响 trace 与 lease 使用同一 `groupDispatchId`、同一 `serialFallbackReason` 和完整 `affectedSliceIds`；不得混用 `parallel-slice` 与 `serial-fallback`，不得事后补写 fallback。本规则不保留缺时序、复用 evidence 或无 pre-dispatch lease 的历史兼容通过分支。

如果用户禁止落盘，阶段结果必须返回 `task-status-updates`、`Execution Group Summary` proposal 和 `not-persisted + reason`，且 Handoff 不得声明 `production-ready`。

## 暂停与回退

以下情况必须暂停受影响 lane；不得因单个 lane 的内部状态或 execution proof 漂移默认暂停整个并行组：

- 任一 slice 写入未授权共享文件。
- 任一 slice 发现新的 shared-scope 写入需求、父工程注册遗漏、公共 mock/plugin 聚合遗漏、全局权限/i18n namespace 冲突或 shared contract 漂移。
- 任一 slice 发现契约缺失、契约冲突或需要改变 production-ready / mock/demo 判断；必须先按真实 `parallelGroupStarted` 和 frozen source evidence 分类，不能只凭投影状态回 Design。
- 任一 slice Review 出现阻塞 finding，且影响共享文件、共享契约或其它 slice。
- Verify 发现 buildable / reachable / usable 结果与并行计划假设冲突。
- `task-status.md`、`frontend/index.md` 或其它 projection 与 canonical changedFiles、Review、Verify 结果不一致；此类不一致只暂停状态持久化/消费 lane，由 primary 自动同步 canonical projection。

暂停后的处理：

| 情况 | 回退点 |
| --- | --- |
| 文件边界或锁冲突 | 只暂停冲突 lane，内部回 Task Breakdown / Integration 修正 `parallel-slices`、`shared-file-locks` 和 dispatch lease；未相交 lane 可继续到安全 checkpoint |
| shared-scope 漂移或公共注册遗漏 | 暂停受影响 feature lane，回到 shared-scope integration task 串行补丁，更新 shared contract 后恢复并行 |
| canonical/task-status/index 状态投影不一致 | primary 以 canonical source 为准执行 internal canonical sync，记录 `reasonClass=execution-proof + requiresUserDecision=false` 后恢复受影响 lane；不得重跑业务实现或返回 Lite |
| 并行启动前发现 frozen Design 缺失/冲突 | 返回 `design-closeout-internal-repair` 给 primary，由原 Design owner 同一 run 闭合；不需要用户授权，除非存在真实业务多选项 |
| 并行启动后 frozen Design/FDS/TDS 事实确需改变 | 只暂停与 `affectedContractAreas/contractAreaLocks` 相交的 lane，返回 `parallel-baseline-invalidated` amendment；未相交 lane 可继续到不消费失效合同的安全 checkpoint |
| 实现缺陷且不改变契约 | 回到对应 slice Implementation |
| 共享集成失败 | 回到 Integration task |
| 降级交付需用户接受 | 回到 Lite 人工确认或 frontend-auto 的统一 question |

“真实并行已启动”必须由 dispatch lease/trace 证明；仅 `task-status.md`、Index 或 stage projection 自报 `parallelGroupStarted=true` 且与 canonical trace 不一致时，先做 internal canonical sync，不得据此创建 amendment 或用户确认。共享文件/锁冲突若可在已授权 write scope 内通过 Task/Integration 重排闭合，也不属于 terminal blocker；只有真实 dirty/conflict 或扩大写入范围需要授权时才进入外层 gate。

## 全局汇合判定

Lite `并行汇合` 必须同时检查后端编码结果和 `frontend-stage-result`。

前端侧至少检查：

- `scopePartitionStatus`
- `sharedContractStatus`
- `sharedContractVersion`
- `sharedDriftFindings`
- `contractStatus`
- `review.status`
- `verification.buildable / reachable / usable`
- `mock.queryMode`
- `contracts.tenantContext`
- `contracts.backendApiReadiness`
- `contracts.productionReplacementTrigger`
- `contracts.pendingReplacementItems`
- `routing.routeOpenMode / routing.tabTitle / routing.queryStateKey`
- `handoffStatus`
- `acceptanceSource`
- `blockers`
- `featureRoot`
- `frontendDesignRoot`
- `evidencePath`
- `frontendDesignPath`
- `contractCheckPath`
- `taskBreakdownPath`
- `taskStatusPath`
- `verificationReportPath`
- `artifactIndexPath`
- `handoffPath`
- `productionReplacementChecklistPath`

路径字段缺失时，必须有 `null + reason`。`demo-slice`、页面交付、需要状态回写的 `regular-change` 或存在 Feature Root 时，缺少稳定路径且无原因，视为前端阶段结果不完整，必须回到 `frontend-auto-agent` 补齐结果合同。
汇合前应按 `front-hzero-enterprise-process-control` 的 schema checklist 逐项核对 `frontend-stage-result`、`task-status.md` 和并发一致性；该模板只作为运行时字段检查，不是业务交付产物。

`production-ready` 只允许在以下条件全部满足时出现：

- `contractStatus=ready`
- `reviewResult=pass`
- `verification.buildable=true`
- `verification.reachable=true`
- `verification.usable=true`
- `handoffStatus=production-ready`
- `blockers` 为空
- 涉及租户级 API、附件、导入导出或 LOV/lookup 时，`tenantContext.status=confirmed` 或 `not-applicable + reason`
- HZERO+Choerodon / DataSet / Table / Form 枚举型 props 已有 `enumImportMapStatus=ready / not-applicable + reason`，且 `enumProvenance` 可追溯
- mock/demo、临时契约和生产替换项均已闭合或 `not-applicable + reason`

`conditional` 或 `frontendExecutionMode=demo-slice` 不得被 Lite 包装为生产闭环。`demo-slice` 只能通过 `deliveryTarget=mock-demo`、`buildable/reachable/usable`、未验证项和 replacement 边界汇合；即使 Review、build 和 mock request 静态验证都通过，也必须保留 production replacement / cleanup 边界，不能写 `production-ready`。需要用户接受的非默认条件性交付必须有 `acceptanceSource`；仅缺目标工程依赖时写 `environment-prerequisite-notice`、`verification.environmentNotice` 和前端服务提示；默认 mock demo 仅缺外部页面运行态证据时只写未验证项和 `manualVerificationRequired`，不得额外暂停确认。非 canonical 交付状态不得汇合或转换。

并行汇合输出必须显式分组：`运行态未验证`、`生产替换提示`、`集成准备状态`。`reachable=unknown`、`usable=unknown`、`manualVerificationRequired=true` 是 verification facts；真实 API、route/menu/permission/title/i18n、LOV/lookup 和导入导出缺口是 advisory facts；后端 readiness 只决定记录 `waiting-backend-integration / ready-for-independent-integration`，不决定当前前端调度。除非缺口影响当前 Mock demo 并满足 blocked 条件，不得把三组 facts 全部平铺进 `blockers`。

若后端编码结果出现 `contracts.backendApiReadiness.status=closed + implementationStatus=completed + runtimeAvailability=verified`，Lite 只记录 `ready-for-independent-integration`；当前前端仍完成 `mock.queryMode=mock-request` 的 Mock demo，不恢复 `frontend-auto-agent`、不执行 production replacement / cleanup slice。CTS 代码完成但运行可达性 unknown/not-run 时记录 `implementation-complete-runtime-unverified + waiting-backend-integration`。两种情况都可继续 Mock demo 汇合和后端/通用资产生成；真实 API 首次试连统一由独立联调测试按 Mock-first、backend signal、env-only 顺序执行。

若后端编码结果仍为 `contracts.backendApiReadiness.status=partial/missing/not-applicable`，且前端为默认 Mock demo、Review/validator/build 已满足本轮范围但缺外部 runtime acceptance 或真实 API 集成，Lite 应保持 `handoffStatus=conditional`、`deliveryTarget=mock-demo`、`mock.integrationState=mock-demo-completed/waiting-backend-integration` 和 `done=false`，并把下一步写为用户手工 Mock 验收、独立联调测试或等待后端服务；不得把该状态改写为前端代码失败、`verification-failed` 或 `blocked`。

## Agent 引用要求

- `hzero-auto-agent-lite`：引用本文件判断全局并行启动、禁止并行、并行汇合和降级交付。
- `frontend-auto-agent`：引用本文件判断前端内部并行、共享文件锁、integration task、状态回写和暂停回退。
- `frontend-task-agent`：引用本文件生成 `parallel-slices`、`shared-file-locks` 和 `integrationTaskId`。
- Review / Verify / Handoff 阶段：引用本文件检查并发结果是否可以继续汇合或需要回退。
并发执行的耗时遥测必须由 strict runtime trace 结果计算，不得仅凭 Task 文档自报。输出至少包含 planned/observed Implementation session 数、可采集时的 average queue wait、actual overlap rate、critical slice、gate bypass count 和 invalid Artifact duration。时间戳不完整时写 `timingCompleteness=partial`；这些指标是 report-only，不改变 `requiredOwningAgentDispatchCount`，也不得作为合并 slice 或串行 fallback 的理由。

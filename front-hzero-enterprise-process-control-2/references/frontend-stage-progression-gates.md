# Frontend Stage Progression Gates

本文件承载各阶段进入下一阶段时的详细可判定条件。`frontend-auto-agent` 保留状态机、owner、backfill/repair 和用户停止条件；只有推进到具体 stage boundary 时读取对应小节。

阶段门禁统一按 `frontend-context-handoff-control.md#Evidence Layers And User Wait Boundary` 分类。Decision Evidence 决定能否无猜测执行；Execution Proof 继续保持机器硬门禁，但缺失只能回脚本/owning Agent 自动补齐；Audit Telemetry 只告警；Runtime Acceptance 在用户未明确要求 runnable/production-ready/完整验收时默认 conditional。不得用证据数量、文档章节完整度或 telemetry 缺失替代这四类判定。

## Design Handoff -> Task
- 必须有外层 `frontend-design-agent` 或等价 handoff，状态为 confirmed / auto-confirmed-for-demo，且 question gates 已 resolved。
- 页面交付必须有 `frontend-design.md`、`contract-check.md` 和当前交付模式所需的 Target Placement、可执行 UI/data/route/mock Decision Evidence 与 validationHandoff。Design Coverage 只要求本轮 changed scope 可映射，不以长 Ledger 行数或完整生产矩阵作为普通 demo/regular-change 门禁。
- 默认 mock demo 必须是 HZERO dev-server middleware/requestable mock contract；legacy `_smock/smock/.smockrc` 不能进入 Task。
- 缺工程事实只返回 targeted evidence backfill；缺业务/交互合同先回 Design/Contract Check，只有存在多个真实语义选项时 question。可由 owner capsule、标准坐标或已确认合同唯一推导的字段同次自动补齐。

## Task -> Implementation
- `frontend-task-agent` 必须真实返回 canonical task-breakdown/task-status 和 owning-agent trace。
- readiness、mapping、execution、dispatch、closeout 五类 gate 必须通过。
- `task-ready-result.json.firstDispatchClosure` 必须在首次派发前一次闭合 `fileMapping / mockEndpointMapping / contractFidelityPlan / validatorPlan / writeScope / dispatchPlanPreparation` 六项；适用项只能是 `passed`，不适用项必须是 `not-applicable + reason`。不得把 mock endpoint、合同保真证据计划、validator target 或 evidence write scope 延迟到 Implementation 后补账。
- File Mapping、Design Coverage Mapping、Target Placement、dependencies、parallel slices、shared locks、execution groups、acceptanceRef、changedFiles plan 和 required validators 必须可判定。
- Task Ready proof 必须绑定当前 task-ready-result、task-breakdown、task-status、design-canonical-state 和 design-coverage-ledger hash，并包含 `taskStatusHash`。任一源变化后旧 proof 立即 stale，必须由 Task owner 重跑 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_task_ready_result.py`，再生成当前 dispatch validation/lease；不得消费历史 passed 结果。
- Task-driven Implementation 必须先通过 dispatch validation 并获得匹配 Todo/group/slice/hash 的 dispatch lease；write scope 独立保持 hard gate。
- dispatch hash、lease、trace 和 Task closeout result 属于 Execution Proof：缺失或不匹配时回 Task owner/脚本自动生成或修复，不得询问用户提供、接受或跳过 proof。
- `TASK_GATE` 不消费 `buildable/reachable/usable`，也不得要求 build、dev server、browser、HTTP/mock smoke 或页面运行态证据。尚未产生目标前端源码时，这三项为 `unknown` 是正常前置事实，不得阻塞 Implementation dispatch。
- 处于 Task Breakdown / TASK_GATE 且尚未进入 Implementation 时，`verification.status` 必须为 `not-run + reason=implementation-not-started`（或未展开 Verification 对象）；不得把未开始构建、运行态或手工验收写成 `verification.status=failed`。Task 自身失败必须归入 readiness/mapping/execution/dispatch/closeout gate 或结构化 blocker。
- 只有 Task-specific gates、dispatch validation、dispatch lease、未闭合 Contract/Design、write scope 或真实 Task artifact/trace 缺口可以阻塞 Task -> Implementation；不得将后续 Verification/Handoff 的 required validator 或 runtime 结果前移为派发前提。
- `direct-no-task` 仅用于目标文件与成功标准明确、无 Feature Root/共享合同/状态回写的小范围 regular-change；demo-slice 不适用。

## Implementation -> Review
- changedFiles 必须来自 File Mapping、direct target files 或 approved repair package；writeScopeAudit 通过。
- 每个 slice / integration task 必须把代码与证据作为一个原子 completion bundle 落盘到 `frontend/evidence/implementation-results/<sliceId-or-taskId>.json`。Implementation Result 除 changedFilesSource、task-status updates proposal、blockers 和适用 validators 外，还必须逐项给出 `contractFidelity / mockRequest / permissionActions / importExport` 的 `passed + evidencePaths` 或 `not-applicable + reason`，并对账 allowedFiles、writeScopeAudit 和全部 touched task。
- primary 必须在进入 Review 前运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_result.py --input <implementation-result.json> --out <implementation-result-validation.json>`。结构或执行证据失败只回当前 slice / integration task 窄补，固定 `repairMode=evidence-backfill + repairBudgetClass=result-contract-backfill + consumesRepairBudget=false + contractDiffDomains=[] + businessChangedFiles=[] + requiresUserDecision=false`；read/skill/reference reload 超预算只生成 cost warning，不得重跑已完成业务实现或覆盖交付状态。
- `PRE_REVIEW_STATIC_GATE` 只运行 Task-required 或 changed-file-triggered V0 validators。`demo-slice/regular-change` 使用 `--gate-profile delivery`，`production-ready/full audit` 使用 `--gate-profile strict`；blocking finding、required validator failed、target 不匹配或无理由 not-run 时不得进入 Review。delivery 下仅 advisory 的 `passed=true + clean=false` 进入 Review/未验证项，不得触发等待或业务阶段重跑。
- validator result、changedFiles source 和 task-status sync 属于 Execution Proof；缺失时在 Implementation owning stage 内补齐，固定 `repairBudgetClass=execution-proof + consumesRepairBudget=false`。只有 validator 失败揭示新的业务/设计取舍或 write scope 授权时才可进入用户门禁；补 proof 的次数本身不得触发授权。
- 可定位静态问题按 `frontend-validator-fix-routing.md` direct-fix/owner-needed；合同或范围缺口走 backfill。

## Review -> Verification
- Review 必须由 `frontend-review-agent` 真实执行并有 report path、scope fingerprint、finding counts 和 trace。
- blocking findings 为 0 才正常进入 Verification；accepted findings 必须进入 conditional/residual risk，不得包装为 clean。
- 自动修复完成后只做 fix-package-recheck；输入未变化不得重复 full scan。

## Verification -> Final Review / Artifact
- 页面交付必须尝试目标范围 V2 build/compile；命令结果和未运行原因必须真实记录。
- buildable/reachable/usable 分开判定；build passed 不推导 runtime passed。
- 默认 demo/runtime evidence 缺失可以 conditional Handoff，不触发普通 Verification 循环。
- telemetry、读取量、耗时和 capsule reuse 只进入成本告警；不得把成本证据缺口升级为 Verification failed、用户等待或业务返工。
- failed validators 或 compile/build 按 repair routing 自动闭合；环境不可用且允许降级时保留 not-run/conditional。
- production-ready、完整验收或高风险任务进入 Final Review；普通 demo/regular-change 可直接 Artifact。

## Final Review -> Artifact
- 只复核 Verification 新事实、accepted findings、replacement 和 Handoff blockers；代码未变化时使用 final-delta。
- blocking findings 为 0 才可进入 production-ready 判定；用户接受风险只能 conditional。

## Artifact -> Done
- Artifact 只消费 canonical facts，按 schema checklist 和 handoff reference 映射 production-ready / conditional / blocked。
- required 内部事实缺失返回同一前端子流程 owning stage；外部 runtime/production-only pending 默认 conditional。
- production-ready 要求生产契约、Review、Verification、write scope、replacement 和 blockers 全部闭合。
- conditional 必须 `done=false` 并携带未验证项、manual checklist、replacement 和 next stage。
- Artifact 返回后，primary 必须先完成 validator evidence close guard，再运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_stage_return.py --stage-result <frontend-stage-result.json> --root <feature-root> --expected-frontend-auto-run-id <expectedFrontendAutoRunId> --out <frontend-stage-return-validation.json>`。Final Stage Return Guard 必须证明 15 个 Core 字段完整、`frontendAutoRunId` 与外部冻结 run id、`stageSummary.handoffCloseout.frozenFrontendAutoRunId` 三者一致、changedFiles/write scope 一致、Review/Verification/runtime/Artifact/preflight 指针可读、runtime 为 `passed/failed/not-run + trace`、Artifact 仅调用一次、source revision hash 有效，且 `stageSummary.stageTimings[]` 来自 primary/owning-agent/deterministic-tool trace。
- Final Stage Return Guard 只允许 `disposition=allow-return` 向 Lite 返回。`internal-repair-required` 必须在同一前端编排会话自动闭合：stageSummary/字段投影/run id 透传由 primary Return Builder 修复；runtime trace/verification 事实回 Verification；dispatch 路径回 Task Gate；write scope 必须重审实际 changedFiles，禁止复制字段伪造审计。只有重审确认 out-of-scope/dirty/conflict、不可降级环境/工具或用户契约问题才是 `external-gate`。不得把前述内部缺口写成 blockers、用户待确认或普通 `conditional / blocked`；Lite 还必须带同一冻结 run id 独立重跑 guard。
- 只有命中 `frontend-validator-fix-routing.md#Terminal Block Whitelist` 的无 runnable target、不可闭合核心契约/安全、write scope/dirty conflict、required 外部权限/环境或真实用户决策时才 blocked；repair budget、timebox、证据或调用缺口本身不得形成 terminal blocker。

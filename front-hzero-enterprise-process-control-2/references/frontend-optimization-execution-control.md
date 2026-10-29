# Frontend Optimization Execution Control

本文把显式 expanded 前端提效工具的“规则建议”转换为可审计执行证据。只有 `optimizationProfile=expanded` 才在 Feature Root 下维护 `frontend/evidence/optimization-execution-manifest.json`；compact 包括普通新子模块 mock/demo，不创建 manifest，也不因缺 optimization evidence 阻塞。每个 expanded 工具只有实际执行并保存结果后才能写 `status=executed`。manifest 使用 `schemaVersion=1.1`，并记录 `executionStage`、`completedAt`；被下游消费的工具还必须记录 `consumedBy` 和 `consumedAt`，禁止在 Handoff 前补跑后倒填为已优化。Explore / Evidence 不生成 scaffold 或 synthetic context pack。

## Scenario-derived Requirements

| Scenario | Required tool |
| --- | --- |
| 已进入 Task Breakdown 或后续阶段且目标 package 已存在 | `generate_frontend_context_pack.py` |
| `createsSubmodule=true` 且目标 package 不存在 | 记录 `scaffoldRequired=true`，由 Design preview 或 Implementation init 显式授权 `generate_hzerojs_submodule_scaffold.py` |
| 已进入 Implementation 或后续阶段 | `run_frontend_static_gate_bundle.py` |
| 已进入 Verification 或后续阶段 | `aggregate_frontend_verification_result.py`，且形成唯一 `finalVerificationRunId` |
| 已进入 Handoff | `render_frontend_short_closeout.py` |

新子模块在 Task Breakdown 前不生成 scaffold。Task 只消费真实工程 evidence、Design / Contract Check 和必要的 context pack；目标 package 不存在时，只记录缺口和 Implementation init 任务。

1. Design 可按 `templates/task-optimization-inputs.json.template` 写 schema 1.1 `frontend/evidence/task-optimization-inputs.json`，用于冻结后续 scaffold/init 参数；`module=packageDir basename`、routePrefix 是无前导 `/` 的完整 feature 父路由（例如 `prm/requisition-management`）、featurePath 为单个 route segment 且只用于页面/locale 标识、mockEnvVar 为 exact `_USE_MOCK` key；主从 profile 显式提供 create/detail/edit titles，不从列表标题猜文案。该文件是后续 init 输入，不是 Task 生成 scaffold 的授权。
2. 已有 package 使用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/generate_frontend_context_pack.py --root <frontend-root> --package-dir <package-dir> --out frontend/evidence/frontend-context-pack.json --expect-ready` 生成真实工程 context pack；Task 可消费其 path/sourceHash。目标 package 不存在时，不使用 `--package-source-dir <generated-scaffold-dir>` 伪造工程包，只在 evidence / task 中记录 `packageStatus=missing`、`scaffoldRequired=true`、`recommendedScaffoldStage=Implementation init`。
3. Task 只消费真实 context pack（如有）、Frontend Design/Contract Check、Target Placement Evidence、owner reference capsule 和 package missing evidence生成任务。所有 profile 生成 schema 1.1 `frontend/evidence/task-ready-result.json`，再运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_task_ready_result.py --input ... --root ... --out frontend/evidence/task-ready-validation.json`；primary 只消费 passed Task Ready validation。compact 写 `optimization.status=not-required + reason`；expanded manifest 固定写 `taskBreakdownPath=tasks/task-breakdown.md`，其 `--gate task` 结果作为 Task Ready 的条件 gate。canonical 路径漂移、引用桩、module/package/mock/route/profile 漂移、route path 分隔符被 kebab 化、featurePath 重复拼接或只改 manifest 不改任务文件都失败。
4. 如果新 package 需要 scaffold，Task 只能把它拆成 Implementation init 或 Design preview 的显式任务，并要求后续阶段记录 `scaffoldDraftStatus=draft/not-runnable-proof`、输入 hash、write-scope audit 和 validator 结果。scaffold draft 不得反填为 Explore evidence，也不得作为 Task 已执行工具证明。
5. Task closeout 只运行 Task Ready validation。只有 `task-ready-validation.dispatchEligibility.implementation=true` 才能生成当前执行组的 `implementation-dispatch-plan.json`。随后运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_dispatch.py --task-breakdown <task-breakdown.md> --task-ready-validation <task-ready-validation.json> --dispatch-plan <dispatch-plan.json> --target-root <target-root> --out <dispatch-validation.json>`；每组实际发令前再运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/authorize_frontend_implementation_dispatch.py --task-breakdown <task-breakdown.md> --task-status <task-status.md> --task-ready-validation <task-ready-validation.json> --dispatch-plan <dispatch-plan.json> --target-root <target-root> --execution-group <group-id> --out <implementation-dispatch-lease-<group-id>.json>`。`targetRoot` 必须是目标前端工程的绝对根，所有 write scope 必须相对该根，重复工程目录名必须被 dispatch validator 拒绝。expanded optimization 仅作提效证据，不替代或阻塞通用 Task Ready；dispatch plan 与 lease 仍分别阻断 Todo 越权、并发写冲突和发令前 hash 漂移。

进入 Implementation 后，manifest 的 `implementationDispatchLeaseRequired=true` 是硬阻断开关。`dispatchLeases[]` 为空、lease 文件不可读、`passed/leaseGranted` 非 true、identity 与当前 `executionGroupId/groupDispatchId/dispatchLeaseId` 不一致，或 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_optimization_execution.py` 报 `optimization_execution_dispatch_lease_missing` 时，当前执行链必须停在 Parallel Dispatch Plan / dispatch lease 修复点；不得继续调用 Implementation，不得把已经发生的单 session 整包实现标成 `conditional`、最终 `blocked`、`serial-fallback` 或 Handoff 风险。运行期并发限制只需在首次 owning Agent 调用前生成 `serial-fallback + serialFallbackReason + affectedSliceIds` dispatch plan 并重新取得 lease，不回调 Task Agent或重写冻结 DAG。

`required` 不由执行者自由降级，而是由 `stagesEntered`、目标 package 是否存在和实际进入的 owning stage 推导。required 工具必须记录真实 `command`、`resultPath`、`resultStatus=passed`、`executionStage` 和 `completedAt`。不适用项必须写 `status=not-required + reason`；缺工具、工具失败或只有计划命令时，不得进入下一阶段或 Handoff ready。

## Validation

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_optimization_execution.py \
  --gate task \
  --manifest <feature-root>/evidence/optimization-execution-manifest.json \
  --root <feature-root> \
  --out <feature-root>/evidence/optimization-execution-task-validation.json
```

Task 在生成任务产物后先执行一次门禁。所有 profile 在 Artifact 发令前先通过通用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py` canonical consistency gate；expanded optimization 再用 `--gate pre-handoff` 核对 optimization 工具结果。两者通过后只调用一次 Artifact，渲染后回写 renderer 结果并用 `--gate final --out <final-validation.json>` 执行最终门禁；pre-Handoff 和 final 均要求 `stagesEntered` 已含 Handoff，final 不得根据残缺 stages 缩小 required tools 后 fail-open。最终 stage-result 在 `stageSummary.handoffCloseout` 引用 canonical preflight result，并在 `stageSummary.optimizationExecution` 引用 expanded manifest、Task validation、并行时的 slice validation、pre-Handoff validation 和 final validation。close guard 的 schema-only 缺口只允许 primary 本地 patch `frontend-stage-result.json`，不得重派 Artifact；其它失败按 owning stage 返回。

并行 slice 采用 group-deduplicated profile：每个 slice 独占写 `slice-gates/<sliceId>.json` 并申报 changedFiles/requiredValidators，primary 在 fan-out 后求并集，对同一 scope fingerprint 只执行一次，再以 `validatorRuns[] + validatorRefs[]` 聚合。详情+明细组自动要求 `integration-contract` 与 `contract-fidelity`；后者固定使用 schemaVersion=1.1，除既有 detail ID、required editable field、payload、保存响应主键到 redirect、状态动作 code guard、按钮权限/承载面、enum/mock、workflow guard 和 attachment carrier 外，还要求空 generatedCandidate、对象 LOV 控件绑定、只读 mutation、动作权限码、Import/ExcelExportPro 权限 prop 和 mock ID runtime type 六项逐项声明并对账，不保留 1.0 兼容分支。slice validator 机械检查 planned slices、scope fingerprint、重复执行、Task acceptance、targeted review、owner capsule 单次加载和 artifact；只有 `progressionDecision=allow-integration` 才能进入 shared integration。该门禁不改变并行切片数量，也不要求 Runtime Acceptance 浏览器执行器。

## Strict Evidence

当前执行链和任何重新进入 Task/Implementation/Verification/Handoff 的 Change 必须使用 schema 1.1 严格门禁。`completedAt/consumedAt` 必须携带 `Z` 或显式 UTC offset；缺 command/result、消费证据、阶段匹配或时序证据时直接失败，不提供历史兼容放行路径。

## Runtime Acceptance Boundary

Runtime Acceptance 是独立验收证据，不是本优化工具清单里的强制工具项。成功标准要求页面真实可达/可用时，按 `frontend-runtime-acceptance-control.md` 写入 `verification.runtimeAcceptance`，并由 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_runtime_acceptance.py` 校验结构和关键断言；本 manifest 只记录真实 context pack、被明确授权的 scaffold draft、static gate bundle、final aggregation 和 Short Closeout renderer 的实际执行。

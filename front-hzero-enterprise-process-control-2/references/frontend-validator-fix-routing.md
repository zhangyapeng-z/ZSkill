# Frontend Validator Fix Routing

## Scope

本文件定义 validator finding 的严重度与修复调度分离规则。所有前端静态 validator、Review finding、Verification failure 和 close guard 失败都必须先区分：

- `severity`：控制交付出口，决定当前结果能否继续 Review / Verify / Handoff / production-ready / DONE。
- `fixRouting`：控制修复入口，决定当前执行者能否直接最小修复，还是必须回 owner stage、并行基线修订、用户确认或 blocked。
- `repairMode`：区分 `evidence-backfill / code-repair / not-applicable`。`fixRouting=owner-needed` 只决定事实 owner，不再隐含一定进入 `repairDispatch`。
- `repairBudgetClass / consumesRepairBudget`：`code-repair / true` 才消耗代码返工预算；`execution-proof`、`result-contract-backfill` 和 `not-applicable` 固定为 `false`。

`blocking` 不等于必须调度专项代码编写 agent。`blocking` 只说明当前状态不能交付；若 finding 是确定性静态小修，仍可走 direct-fix 快速闭环。

## Fix Routing Values

| fixRouting | 含义 | 允许动作 |
| --- | --- | --- |
| `direct-fix` | deterministic static fix；修法唯一或接近唯一，不改变业务语义 | 恢复原 `frontend-implementation-agent` owning context 执行最小修改；原 context 不可恢复时按当前 `repairPlanFingerprint` 派发一个窄 direct-fix Implementation Todo，随后运行 targeted validator / typecheck / grep 复验并记录 closure；同一 fingerprint 不重复，失败后重诊断生成新 fingerprint；不新增主阶段 |
| `owner-needed` | 需要对应阶段或领域 owner 执行，但不需要用户决策 | 回当前前端子流程内 owning stage，例如 Implementation / Review / Verification / 对应专项 owner；不得返回 Lite 新建外层 Todo |
| `design-needed` | 仅并行启动前的 Design closeout 需要补 Frontend Design / Contract Check | 留在 Design owner 内自检和修复，不生成可被 Lite 消费的中间结果 |
| `baseline-invalidated` | `parallelGroupStarted=true` 后证明 frozen Design/FDS/TDS 合同无效 | `reasonClass=parallel-baseline-invalidated`、`targetStage=LITE_PARALLEL_AMENDMENT`；终止旧 run，受权后生成新基线身份 |
| `user-needed` | 需要用户确认业务语义、范围或取舍 | 输出 questionGate / questionOwner，不自行修 |
| `blocked` | 工具、依赖、工程能力、权限或外部条件不可闭合 | 写明 blockedReason、remainingRisk 和可恢复条件 |

## Terminal Block Whitelist

`blocked` 只允许作为交付出口事实，不允许作为内部循环预算、证据格式、调用参数或同一修复方案失败后的默认止损值。最终返回 Lite 的 `terminalBlockClass` 只能是：

- `core-contract-unresolvable`：当前交付目标依赖的核心业务/API/权限/安全合同确实冲突，且标准候选、既有冻结事实和当前授权范围都无法闭合。
- `non-runnable-target`：确认无可运行目标、目标工程形态不受支持且没有本轮可用替代入口。
- `write-scope-or-dirty-conflict`：必须扩大写入范围、处理 dirty/conflict/shared lock，且需要外层授权。
- `external-permission-unavailable`：当前 required 外部权限、账号、环境或工具不可用且交付目标不允许 conditional。
- `user-decision-required`：存在真实业务语义、产品取舍、冻结合同修订或与用户明确目标冲突的降级选择。

`repair budget exhausted`、同一 finding 首次修复未通过、validator invocation defect、canonical/evidence 缺口、owner capsule 漂移、换手深度和阶段 timebox 都不属于 terminal block class。它们必须先留在 `frontend-auto-agent` 内部形成 repair/backfill/runtime checkpoint，并按当前 source revision 继续闭合。

代码修复去重使用 `repairPlanFingerprint=hash(repairAttemptKey + repairDiagnosisRevision + targetFiles + patchIntent + completionCriteria)`。同一 fingerprint 只允许执行一次；窄复查仍失败时，禁止原样重放，但必须更新根因证据并生成递增 `repairDiagnosisRevision` 和新的 fingerprint。只有重新诊断证明命中上述 terminal whitelist 时，才允许结束内部修复链。

## Direct-Fix Criteria

validator finding 只有同时满足以下条件，才能标记 `fixRouting=direct-fix`：

1. 有确定 `ruleId/gateId`、目标文件、行号或稳定定位证据。
2. owner reference 或 validator message 给出标准替换 / 唯一修法。
3. 修复不改变 FDS/TDS/Frontend Design/Task Contract、不新增或删除业务能力、不改变 route/openTab、DataSet/service transport、权限策略、mock/production 边界、导入导出协议、附件/LOV 业务参数。
4. targetFiles 全部位于当前 write scope，且不触碰未持锁 shared file。
5. 可用 targeted validator、typecheck、局部 grep 或等价静态检查复验。

典型 direct-fix：标准 import 坐标错误、enum import 来源错误、`formatterCollections` named import / 旧 `lang` 封装入口 / 非标准 `xxx({ code: [...] })(...)` HOC、固定组件 export shape 错误、本地源码 import 路径深度错误、明确空值 guard、helper payload 结构中 validator 给出唯一替换的字段。

不允许 direct-fix：DataSet transport 参数语义不清、route/openTab/dynamic-tab 行为选择、权限码生成或平台登记策略、导入/导出/附件/LOV 业务参数缺口、mock response shape 需要对账消费端、多页面或 shared contract 联动、任何会改变 production-ready 判断的业务取舍。

## Dispatch Rules

- Review / Verification 发现 `fixRouting=direct-fix` 且目标文件位于当前 write scope 时，可以输出 `sameStageDeltaFastPath=true` 或 `recommendedFixPackage.fixRouting=direct-fix`；主编排必须优先恢复产生该实现的 `frontend-implementation-agent` owning context，只传 delta 修复包和 evidence capsule。原 context 不可恢复时，才派发一次窄 direct-fix Implementation Todo。该修复属于当前 Review/Verification closure，不新增主阶段、不回 Task，也不加载无关 owner reference。
- Review / Verification 自身没有代码写权限时，不直接改代码；但修复包必须保留 `fixRouting=direct-fix`，允许主编排选择 direct executor / current implementation context，而不是强制专项 Implementation agent。
- `fixRouting=owner-needed` 才使用常规 `targetStage=IMPLEMENTATION`、领域 owner 或 `frontend-general-agent -> frontend-implementation-agent` 路径。
- primary、General、Review 和 Verification 都不得因 `direct-fix` 直接修改业务源码；它们只负责选择或恢复 owning context、校验 write scope、收集 closure 和恢复原 Review/Verification。direct-fix owning context 返回空结果、扩大 targetFiles、命中新风险域或改变业务合同后，必须升级为 `owner-needed/design-needed/user-needed/blocked`，不得继续伪装为机械修复。
- `fixRouting=design-needed` 只允许 Design closeout 内部使用；`baseline-invalidated`、`user-needed`、`blocked` 不得放入 `recommendedFixPackage.targetStage=IMPLEMENTATION`，分别使用并行修订 gate、questionGate 或 blockedReason。
- direct-fix 完成后必须记录 `directFixClosure`：`ruleIds`、`targetFiles`、`beforeAfterSummary`、`commands[]`、`validatorResult=passed/failed/not-run + reason`、`remainingRisk`。缺 closure 不得关闭 blocking finding。

## LOV And Contract Fidelity Routing

| rule family | fact owner | fixRouting | repair budget | backfill / closure | required action |
| --- | --- | --- | --- | --- | --- |
| Design closeout 内的 `lov_candidate_*` | Frontend Design candidate manifest | `design-needed` | `repairMode=not-applicable`、`consumesRepairBudget=false` | Design internal closeout | 并行启动前修 `design/lov-candidate-contracts.json` 与 closeout evidence，validator 未通过不得 `readyForTaskDispatch=true` |
| `parallelGroupStarted=true` 后的 `lov_candidate_*`、`contract_fidelity_lov_candidate_manifest_invalid` | frozen candidate manifest / parallel baseline | `baseline-invalidated` | `repairMode=not-applicable`、`consumesRepairBudget=false` | `reasonClass=parallel-baseline-invalidated`、`targetStage=LITE_PARALLEL_AMENDMENT` | 终止旧 run；受权后创建新 Design revision、`designFreezeId`、`parallelGroupId`、`frontendAutoRunId`，不得修 Design 后恢复旧 Task DAG |
| `contract_fidelity_fragment_*`、`contract_fidelity_manifest_invalid/not_object`、缺 canonical fidelity evidence、`implementation_result_*` schema/evidence 缺口 | Implementation slice/group result | `owner-needed` | `repairMode=evidence-backfill`、`repairBudgetClass=result-contract-backfill`、`consumesRepairBudget=false` | `progressionDecision.backfillPackage.reasonClass=result-contract-gap`、`targetStage=IMPLEMENTATION` | 原 slice owning context 只补 completion bundle/fragment，primary 重新 deterministic merge 和 targeted fidelity validator；不创建 `repairDispatch`，不回 Design，不触发用户授权 |
| 除上述 evidence-only 规则外的 `contract_fidelity_*`，包括 `contract_fidelity_lov_candidate_implementation_drift/define_missing/query_missing/fixture_drift` | Implementation code + evidence | `owner-needed` | `repairMode=code-repair`、`repairBudgetClass=code-repair`、`consumesRepairBudget=true` | `recommendedFixPackage.reasonClass=result-contract-gap`、`targetStage=IMPLEMENTATION` | 在原 write/evidence scope 内修实现并窄复验；冻结 LOV manifest 只读；未知规则先根据 business diff 判定，不能默认把纯证据缺口计入代码预算 |

同一轮同时出现无效 frozen LOV manifest 和缺失 fidelity evidence 时，必须保留两个 finding 的独立 owner：前者使旧基线失效，后者作为可复用实现证据记录。不得合并为普通 `frontend-design-gap`，不得定向修 Design 后恢复同一 `frontendAutoRunId`。

## Output Contract

Review / Verification / validator evidence 中的 failure item 应包含：

```text
ruleId:
gateId:
severity: blocking / major / minor / info
fixRouting: direct-fix / owner-needed / design-needed / baseline-invalidated / user-needed / blocked
fixRoutingReason:
repairMode: evidence-backfill / code-repair / not-applicable
repairBudgetClass: execution-proof / result-contract-backfill / code-repair / not-applicable
consumesRepairBudget: true / false
contractDiffDomains: []
businessChangedFiles: []
targetFiles:
completionCriteria:
verificationRerunTargets:
directFixClosure: not-started / closed / not-applicable
```

`severity` 和 `fixRouting` 必须分别出现；不得用 `blocking` 推导 `owner-needed`，也不得用 `direct-fix` 降低 blocking 的交付阻断效果。

`repairMode` 优先于 `fixRouting` 决定是否建立 `repairDispatch`。`evidence-backfill` 即使 owner 为 Implementation，也只能进入 `progressionDecision.backfillPackage`，并固定 `contractDiffDomains=[] + businessChangedFiles=[] + requiresUserDecision=false`。第 2/3/N 个不同 root-cause key 不共享全局预算；同一 code-repair key 的一次自动返工失败后只止损，不因次数创建 `user-needed`。

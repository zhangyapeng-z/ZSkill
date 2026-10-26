# Frontend Context and Handoff Control

用途：控制长上下文、跨 agent 换手和深层嵌套导致的重复阅读、停滞和误判。本文是运行时控制规则，适用于 `frontend-auto-agent`、`frontend-general-agent` 和所有前端阶段 agent。

## 阅读路由
- 跨轮恢复或换手前先读 `Core Rules`。
- 判断是否继续推进、降级、阻塞或提问时读 `Progression Gate`。
- 控制阶段预算、状态快照或二级转交时读 `Phase Timebox`、`Intermediate Status` 和 `General Dispatch Policy`。
- 裁剪阶段输入和限制嵌套时读 `Stage Input Pruning`、`Handoff Depth`。
- 生成阶段输出、复用验证、窄复查或停止条件时读 `Stage Summary Contract`、`Same-stage Delta Fast Path`、`Verification Reuse Fingerprint`、`Cost Telemetry` 和 `Stop Conditions`。

## Core Rules

1. `frontend/index.md` 是前端 feature 的上下文压缩入口。存在该文件时，恢复、继续、换手和阶段重入必须先读 index，再按 `Stage Read Scope` 读取当前阶段必要 canonical sources。
2. 阶段输入必须裁剪。每个 agent 只能读取当前阶段必需材料；额外读取必须有原因：Open Items 指向、状态冲突、缺失证据、用户明确要求或当前阶段读范围要求。
3. Ready evidence 必须复用。若 `frontend/index.md` 指向的 `frontend/evidence/evidence.md` 存在且 `evidenceStatus=ready`、`evidenceReuseStatus=reusable`，目标工程/模块/页面范围未变化，且 Open Items 未要求补工程证据，后续阶段必须继承 evidence 中的 `engineeringExplorationLevel`、`standardBaselineApplied`、`baselineComparisonStatus`、`goldenBaselineStatus`、`baselineConfirmationSource`、`targetPlacementEvidenceStatus`、`enumImportMapStatus`、`componentImportMapStatus`、`evidenceReuseSource`、`evidenceReuseStatus`、`nextExploreAllowed`、`fullExploreForbiddenReason`、`contaminationStatus`、`contaminationSignals` 和 `blockedPatternReuse`；不得重新调度 Explore 或从仓库根重新搜索。只有目标范围变化、index/evidence 冲突、当前阶段必需证据缺失、Open Items 指向工程证据缺口或写入范围不可判定时，才允许 targeted delta explore。
3a. Frontend Design / Contract Check 必须按指纹复用。`frontend/index.md` 或 `frontend/design/frontend-design.md` 应记录 `designInputFingerprint`，来源至少包含 FDS、TDS、MDS/metadata、目标工程关键配置、target placement、route/open interaction、api/permission/field mapping 和默认 mock/demo 决策。恢复或继续时，若指纹未变化、`frontendDesignState=confirmed/auto-confirmed-for-demo`、`contractCheckStatus=pass/conditional` 且 Open Items 没有设计缺口，必须复用 `frontend-design.md` 和 `contract-check.md`，不得重新调度 `frontend-design-agent`。指纹变化、来源文件不可读、target placement/API/permission/field mapping 变化或 design state 冲突时，写 `designReuseStatus=invalidated + reason`，只补受影响设计域。
4. 探索污染必须隔离。`contaminationStatus=mixed / quarantined / unknown` 时，阶段 agent 可以复用定位事实、scripts、routeConfig 路径和 target placement 事实，但不得复用 `blockedPatternReuse` 覆盖的代码结构、Provider、DataSet/service、mock、i18n、permission 或 wrapper 模式。只有 `adoptedPatternItems[]` 明确允许且不冲突 owner reference 的模式可进入 Design/Task/Implementation；其余必须进入 `rejectedPatternItems[]`、风险或 Review 检查项。存在参考子模块、相似子模块、历史模块或最近改动页面时，后续阶段还必须继承 `Reference Module Quality Gate`：`factStatus`、`referenceQuality`、`evidenceQuality`、`qualityBasis`、`contaminationStatus`、`adoptedPatternItems`、`rejectedPatternItems`、`blockedPatternReuse`、`downstreamPolicy` 和 `decision`；`qualityBasis=no-issue-found / scan-only` 不得当作 owner 确认；未评级默认 `unknown-quality / locate-only`，只能用于定位；`legacy-risk / anti-pattern / unknown-quality` 不得进入 `adoptedPatternItems`、不得拆 runnable implementation、不得支撑 `usable=true / production-ready`。`adoptedPatterns / rejectedPatterns` 属于无效旧字段，命中时必须回 Explore/Evidence 重写 canonical contract。项目 wrapper 不作为 Explore 默认探索目标；只有标准路径被真实依赖、版本、编译或源码证据证伪，或用户 / 架构文档明确要求统一 wrapper 时，才允许 targeted exception verification，且不得削弱 owner 标准规则。
5. 默认单层直调。Explore / Evidence / PageSchema / Frontend Design 是进入 `frontend-auto-agent` 前的外层前置阶段或 backfill 目标；`frontend-auto-agent` 只消费其 handoff，不直接调度 `frontend-explore-agent`、`figma-to-frontend-agent` 或 `frontend-design-agent`。Task、实现、审查、验证和 Handoff 默认由 `frontend-auto-agent` 直接调度 owning agent。确定性失败按本文 `Deterministic Failure Routing` 直达 owner；`frontend-general-agent` 只处理路由表仍无法识别 owner，或多个 owner 定向复核后仍冲突的异常协调，并在识别 owner 后返回 auto 直调。`demo-slice`、需要状态回写的 `regular-change`、Feature Root、多文件页面交付或进入 Handoff 时，Task / Implementation / Review / Verification / Artifact 必须有真实 owning agent 调用；General 不得模拟、代写或自声明这些阶段完成。
6. 状态单源化。过程恢复看 `frontend/index.md`；当前任务状态看 `frontend/tasks/task-status.md`；任务定义看 `frontend/tasks/task-breakdown.md`；验证事实看 `frontend/verification/verification-report.md`；最终交付状态看 `frontend/handoff/artifact-index.md` 和 `frontend/handoff/frontend-handoff.md`。
7. 限制换手深度。默认最大换手深度为 1：`frontend-auto-agent -> owning agent`；fallback 最大换手深度为 2：`frontend-auto-agent -> frontend-general-agent -> owning agent`。达到深度后，必须返回 `frontend-auto-agent` 汇总决策，不得继续嵌套调度其它 agent。
8. 阶段摘要替代长历史。每个阶段输出必须包含短摘要：当前阶段、已确认、未确认、阻塞项、状态源、下一步。后续 agent 优先读取该摘要和 index，再按需读取 canonical sources。
9. 推进型门禁优先于继续分析。任何阶段达到搜索/补证/换手/返工上限，或缺少继续推进的关键输入时，必须输出当前结论和下一步，不得继续“再看看”。
10. 前端不再使用额外交付档位。`regular-change` 和 `demo-slice` 直接按阶段规则读取和输出：Task 产出交付物型简版任务，Review 默认 targeted/blocking，Verification 优先 V0 静态/validator 与依赖就绪时的最小 typecheck/build，页面运行态默认只给手动自测清单和前端服务提示，不列启动命令，Handoff 使用 Short Closeout。其中 `demo-slice` 是新模块页面开发内置默认的 requestable mock demo 运行标签，必须同时保留 `frontendExecutionMode=demo-slice`、`runtimeDataPathDecision=requestable-demo-mock`、`queryMode=mock-request`。若任一阶段缺 required gate，仍按 Progression Gate 阻塞、回退或降级。`demo-slice` 允许 Task 规划 `parallel-slices` 并由 Implementation 按多个 slice 子任务执行，但共享 route/menu/i18n/service/mockPluginIntegration/runtime/config 及 test entry 必须串行 integration 收口；最终不得输出 `production-ready`。
11. 成本控制进入既有对象，不新增零散顶层字段。owner skill/reference 复用写入 `stageSummary.ownerReferenceCapsule`，阶段证据压缩写入 `stageSummary.evidenceCapsule` 或阶段产物的 `evidenceCapsule`，验证复用写入 `verification.reuse`，耗时和工具统计写入 `stageSummary.telemetry` 与 `agentDispatchTrace[].telemetry`；最终返回还必须保留 `stageSummary.stageTimings[]`，每项记录 `stage / wallClockMs / source`，其中 source 只能是 `primary-trace / owning-agent-trace / deterministic-tool`。不得用 agent 累计时长替代阶段墙钟。
12. evidence capsule 是跨阶段输出预算合同：只传结论、路径和关键证据，不传长日志。结构为 `conclusion`、`evidencePaths[]`、`keyLines[]`（最多 20 行）、`omittedLongOutputReason`、`fullOutputPath`；完整日志、长报告、长 diff 只能放在 canonical artifact 或日志路径中。
13. owner reference capsule 用于避免重复注入 skill/reference。结构为 `featureRoot`、`ownerReferences[]`，每项包含 `ownerSkill`、`sourcePaths[]`、`loadedReferenceHash`、`gateIds[]`、`riskDomains[]`、`applicableRulesSummary`、`reuseStatus`、`invalidationReason`。同一 feature 内 hash、gateIds 和风险域未变化时复用摘要；新增风险域、sourcePaths 或 gateIds 时只补载增量 owner reference。若 `reuseStatus=reused`，后续 agent 只能读取 capsule 和 source path，不得再次粘贴完整 skill/reference 正文；确需重读完整 reference 时必须写 `invalidationReason`，并在 telemetry 中记录 `ownerReferenceReloadReason`。
13a. Design 是首个 owner reference capsule 的生成 owner，Task 是首个强制 consumer。Design 只输出 skill 名称表而没有 hash/gateIds/riskDomains/applicableRulesSummary 时，不能记为 capsule ready；Task 不得把“继承专项 skill”解释成逐个重新加载。若 Task 实际加载的专项 reference 已被 ready capsule 覆盖且无 `ownerReferenceReloadReason`，必须在 telemetry 标记 `duplicateReferenceInjection=true`，并把该运行计为成本门禁未达标。
13b. 同一前端 agent session 的资源加载状态独立于跨阶段 capsule。任一前端 agent 在恢复、续跑或重入**同一 agent session**时，先检查当前上下文、当前 Todo、`frontend/index.md`、阶段摘要和已接收 capsule；若同名 Skill 已成功加载，且同一 reference 已完整读取，且上下文未被压缩、未出现读取失败、用户未明确要求刷新，则不得重复调用 `skill`，也不得重复读取同一 reference 或已覆盖行范围。此时只消费当前上下文和 capsule，不增加 `skillLoadCount`、`skillReferenceReadCount` 或 `ownerReferenceReloadCount`。上下文压缩、读取失败、明确刷新、或 `ownerSkill + sourcePaths + loadedReferenceHash + gateIds + riskDomains` 发生变化时，才可读取缺失/变化部分；后者必须写 `reuseStatus=invalidated + ownerReferenceReloadReason`。不得因为“重新进入 session”“保险确认”或阶段重入重载完整 Skill/reference。不同 agent session 之间不得假定彼此的工具加载状态可见，必须通过 `ownerReferenceCapsule` 传递可复用规则摘要。
14. Handoff fact-only 收口。repair recheck/rerun 闭合并写回当前 stage result 后，primary 先运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_handoff_preflight.py --repair-closure-stage-result <frontend-stage-result.json> --out frontend/evidence/repair-closure-canonical-state.json`；四类 owner source 只复制该结果的 run id、repair status 和 hash，禁止独立计算。四类 owner 必须在生成/更新自身 source 的同一次写入中原子回写唯一 canonical state：JSON 与 `canonicalState` 同文件落盘，Markdown 与唯一 `frontend-canonical-state` block 同文件落盘；脚本化 writer 必须使用同目录临时文件 + replace，禁止先写正文后另起业务阶段补 block。helper 是现有 closeout 内部 checkpoint，不新增 Agent/阶段；open/invalid 只回 closure 或状态 owner，不得重跑未失效的 Review、validator、typecheck 或 build。preflight 若只报告 canonical block 数量、JSON 序列化、字段落点或同事实 hash 未同步，owner 只执行 `canonical-state-sync` 原子重写并重跑 preflight，不重做 Review/Verification/Implementation。primary 再生成 schema 1.1 `frontend/evidence/handoff-canonical-preflight-request.json`，其中只保留 frontend-index、task-status、Review report、verification-result 四个路径、helper 输出和目标 Handoff 状态；由同一脚本的 `--preflight` 模式读取真实 source canonical state，派生内容 hash、observed/sync/post-fix 状态和 source revision hash，输出 `frontend/evidence/handoff-canonical-preflight.json`。只有 `statusDerivationMode=canonical-source + passed=true + artifactDispatchEligible=true` 才允许调用一次 Artifact。Artifact 只汇总 preflight 已冻结的 canonical facts，不主动补源码审查、补长日志分析或重跑验证。默认输出 Short Closeout：`handoffProfile=short`、`artifactIndexProfile=minimal`、`replacementProfile=triggered-only`，只包含 changedFiles、Review、Verification、未验证项、blockers、命中 replacement 主项、核心 `frontend-stage-result` 和 nextStageRecommendation。
14a. Handoff 不得补造 owning stage。若 Task / Implementation / Review / Verification 任一 required 阶段缺少真实 owning-agent 调用、非空结构化结果、canonical artifact 或结构化 blocker，Artifact 只能返回 `progressionDecision.action=return-to-owning-stage`、`progressionDecision.reason=missing-owning-agent-evidence` 和对应 `nextStageRecommendation`。特别是 `frontend-task-agent` 空返回或未生成 `tasks/task-breakdown.md` / `tasks/task-status.md` 时，不能由 primary、Artifact 或 Handoff 反向补一份任务文档后继续收口；必须回 Task Breakdown 重新派发或止损。
14b. `frontend-auto-agent` 自身不得空返回。企业前端编排作为 Lite 的前端子流程出口，普通 partial、blocked、预算止损或下层结果 untrusted 必须在内部继续闭合，直至形成 terminal 或外层白名单 gate；真实 task/session/transport 中断时输出结构化 runtime interruption。Lite 观察到空结果、无中断证据的 timeout 或缺 Core 字段时判为 invalid return 并阻止汇合/DONE。独立 `frontend-stage-return` 明确 `disposition=internal-repair-required` 时，Lite 按 `issueFingerprint + repairOwners` 恢复原会话，保持同一 run id，不重派已完成 owning agent 或 Artifact；不同 fingerprint 可继续增量闭合，同一 fingerprint 原样重复则重建 owner input，不得升级为业务 blocker。仅 session/transport 确实不可恢复时结束为 runtime interruption。
15. Premature Handoff Guard：Verification / validator 已返回 `c7nComponentApiValidator`、`mockRequestValidator`、`submoduleConfigValidator` 或 stage-result close guard `failed` 时，不得进入最终 Handoff 汇总；canonical preflight 必须在 Artifact 发令前把 stale source、未闭合 repair、required validator failure 和状态冲突打回对应 owner。防御性地在 Artifact 调用后才发现失败时，立即终止当前 closeout，且同一 closeout 不得 retry Artifact：`fixRouting=direct-fix` 时优先恢复产生该实现的原 `frontend-implementation-agent` owning context，原 context 不可恢复时只派发一次窄 direct-fix Todo；只有 `fixRouting=owner-needed + targetStage=IMPLEMENTATION` 才进入常规 Implementation rework；并行启动前的 `design-needed` 留在 Design closeout，并行启动后的 frozen contract failure 改为 `baseline-invalidated`，`user-needed / blocked` 分别进入 question gate 或 blocked。修复后只重跑失效 validator、repair closure 和 canonical preflight，复用未失效的 Review / Verification 证据；preflight 重新通过后才能开启新的 Handoff closeout。页面运行态 `reachable/usable=unknown` 不触发本 guard，仍按 conditional Handoff 未验证项处理。
16. Parallel Runtime Dispatch Guard：Task Breakdown 存在 parallel group 时，Artifact 前必须同时具备 passed Implementation dispatch validation、每组 `passed=true + leaseGranted=true` 的 Implementation Dispatch Lease，以及真实 root session 的 strict runtime trace validation。Dispatch Lease 是自动机器放行凭证，不是人工授权。lease 必须绑定 `groupDispatchId + dispatchPlanHash`，每条调用 trace 必须携带匹配的 `dispatchLeaseId` 且时间不早于 `dispatchLeaseIssuedAt`；调用后的 task-status 回写不与 lease 发放时 status hash 比较。任何 planned slice 缺独立 Implementation session、required/observed count 不一致、Task Gate 被绕过、前置 shared 输出未获得 lease、stage-result 只自报 trace 或 runtime validator 未读取真实 session，都属于 invalid early return；不得进入最终 blocked/conditional Handoff。

## Progression Gate

每个阶段在读取输入后、调度前、阶段输出前都必须做一次推进判断。判断结果写入 `progressionDecision`，并与 `stageSummary.next` 保持一致。

| 状态 | 动作 | 输出要求 |
| --- | --- | --- |
| 信息足够 | 进入下一阶段或执行当前 owning agent | 写明 next stage、读取的 canonical sources 和进入依据 |
| 信息不足但可降级 | 输出降级结果 + reason | 写明 `conditional` / `blocked` / `partial` 及影响；非 canonical 交付状态直接拒绝；无可运行目标写 `blockedReason=non-runnable-target` |
| Decision Evidence 不足且影响契约 | `parallelGroupStarted=false` 时留在 Design closeout；`parallelGroupStarted=true` 时冻结设计事实缺失统一返回 `parallel-baseline-invalidated`，纯 Task 映射缺口留在 Task Breakdown | 写明缺失契约、影响范围和最小证据；并行后不得回 Contract Check / Frontend Design，只有存在业务取舍才提问 |
| 搜索或补证超过上限 | 停止探索/补证，输出当前结论 | 写明已确认、候选、未知项、evidence gap 和自动/降级下一步；不得因证据数量不足本身进入用户等待 |
| 需要用户选择 | 仅命中下述 User Wait Boundary 时调用 question 或返回主流程确认 | 写明最小必要问题、可选项和默认不继续自转 |
| 目标文件或写入范围不明确 | 回 Task Breakdown / 用户确认；若仅缺工程证据，写 `deltaExploreReason=write-scope-unclear` 并做 targeted evidence backfill | 不得边猜边改 |
| 验证目标不明确 | 输出候选命令和 manual checklist，停止执行验证 | 不得猜默认项目、默认页面或默认命令 |

`progressionDecision` 建议结构：

```text
progressionDecision:
  status: enough / degradable / blocked / budget-exceeded / needs-user / target-unclear / verification-unclear
  action: continue / degrade / block / ask / return-to-auto / return-to-design / return-to-task / return-to-explore
  reason:
  confirmed:
  missing:
  next:
```

不得把 `progressionDecision` 写成长篇分析；它是推进结论，不是推理记录。

## Evidence Layers And User Wait Boundary

所有前端阶段必须先给缺口分类，再决定阻塞、自动补齐、告警或降级：

| layer | 内容 | 缺失处理 | 是否询问用户 |
| --- | --- | --- | --- |
| `Decision Evidence` | 当前交付模式所需的业务语义、API/字段合同、权限、route/open interaction、Target Placement、目标文件/write scope、required acceptance | 会迫使实现猜测时 hard block 受影响 task；能由已确认 Design、owner capsule、标准坐标或工程事实唯一推导时，同次自动补齐；否则 targeted backfill | 只有存在真实业务取舍、多个写入/落点候选或外部授权时可以 |
| `Execution Proof` | source hash、dispatch plan/hash、lease、agent trace、validator result、task/status/canonical sync、repair closure | 仍是稳定链路 hard gate，但必须由脚本或 owning Agent 自动生成/补齐；缺失只回原 owning stage，不得创建用户确认或要求用户提供 proof | 否 |
| `Audit Telemetry` | 耗时、读取量、tool count、capsule reuse rate、queue/parallelism 统计 | report-only warning / `costGovernanceStatus=unverified`；不覆盖 delivery gate，不触发阶段重跑 | 否 |
| `Runtime Acceptance` | route load、真实渲染、response consumer shape、交互和 runtime error | 用户未要求 runnable/production-ready/完整验收时默认 `not-required/not-run + conditional`；要求时转独立 Runtime Acceptance | 只有明确交付目标要求闭合且缺账号、环境、权限或用户手工输入时可以 |

`duplicateReferenceInjection`、伪造/不匹配 hash、lease、trace 或 validator result 属于 Execution Proof 完整性违规，不是普通 telemetry 超预算，继续保持 hard gate；但修复责任仍在当前子流程，不得升级成用户授权问题。

User Wait Boundary 只允许四类：业务语义/产品取舍；FDS/TDS 设计修订授权；写入范围、dirty/conflict 或外部权限授权；当前可降级结果与用户明确的 runnable/production-ready/完整验收目标冲突。缺文档字段、缺枚举/import 示例、缺 telemetry、缺页面运行态证据、缺 hash/lease/trace/validator 结果本身都不是用户等待理由。

## Same-stage Delta Fast Path

同阶段返工、复查或补验证可使用窄模式，但仍必须经过 `frontend-auto-agent -> owning agent` 的真实调用；fallback 时可使用 `frontend-auto-agent -> frontend-general-agent -> owning agent`。快路径只裁剪输入和输出，不取消阶段职责。

允许条件：

- `featureRoot`、当前阶段、task-status、design/contract 版本未变化。
- `changedFiles` 未扩展到新风险域、共享文件或新任务边界。
- 场景属于 repair package recheck、失败 validator 复跑、Verification 命令补跑、Handoff 状态刷新或用户只要求补事实。
- 现有 `sourceReviewPath`、`sourceVerificationReportPath` 或对应阶段 source result 可读，且输入指纹未失效。

输出应使用 delta result：`sourceStage`、`sourceResultPath`、`changedFilesDelta`、`targetFiles`、`closedFindings`、`newFindings`、`verificationDelta`、`reuseFingerprint`、`agentDispatchTrace`、`evidenceCapsule`、`nextStageRecommendation`。不得重新构造完整 Todo、完整任务清单或长历史摘要。

禁止条件：新增 route/DataSet/service/permission/i18n/attachment/import-export、共享文件范围扩大、Contract/Task/Design 变化、缺少 source result、用户要求 full review / 页面运行态专项验证 / production-ready，或任一 owning agent 判定原结果 stale。命中时回到常规阶段模式。

## Repair Dispatch Contract

Review 或 Verification 发现当前实现范围内可修复问题时，不得由 Review/Verify agent 自行声明已修复。必须输出带 `fixRouting` 的修复包，由 `frontend-auto-agent` 判断修复入口：`fixRouting=direct-fix` 可在同一前端子流程由当前拥有写权限的执行者做最小 delta 并 targeted rerun；`fixRouting=owner-needed` 才按 `frontend-auto-agent -> frontend-implementation-agent` 真实链路执行代码修复，fallback 时可经 `frontend-general-agent` 透传。

修复 Todo 最小输入：

```text
repairDispatch:
  frontendAutoRunId:
  sourceStage: Review / Verification / UserFeedback
  sourceResultPath:
  fixRouting: direct-fix / owner-needed
  targetStage: IMPLEMENTATION / not-applicable
  sameStageDeltaFastPath: true / false
  recommendedFixPackage:
    packageId:
    repairAttemptKey:
    repairAttemptCount:
    repairMode: code-repair
    repairBudgetClass: code-repair
    consumesRepairBudget: true
    targetStage: IMPLEMENTATION
    autoFixEligible:
    requiresUserDecision:
    sourceReviewPath:
    sourceVerificationReportPath:
    findingIds:
    failureIds:
    rootCause:
    rootCauseTrace:
    userFeedbackTrace:
    affectedStaticGateScan:
    targetFiles:
    changedFilesDelta:
    completionCriteria:
    verificationRerunTargets:
    reviewRecheckMode: fix-package-recheck / final-delta
    verificationReuseFingerprint:
    contractDiffDomains: []
    businessChangedFiles: []
    stopCondition:
  closure:
    status: closed
    repairAttemptKey:
    frontendAutoRunId:
    recheckStage: REVIEW_RECHECK / VERIFICATION_RERUN
    recheckResult: passed
    recheckSessionOrToolEvidence:
    resolvedFindingIds: []
    resolvedFailureIds: []
    userFeedbackResolved: true / false
  evidenceCapsule:
```

`recommendedFixPackage` 只承载可在当前前端子流程内自动闭合的代码修复，并且必须显式写 `fixRouting`、`repairMode=code-repair`、`repairBudgetClass=code-repair`、`consumesRepairBudget=true`、`contractDiffDomains[]` 和非空 `businessChangedFiles[]`。`fixRouting=direct-fix` 表示 deterministic static fix，可由拥有当前 write scope 的执行者直接最小修复并 targeted rerun；`fixRouting=owner-needed` 才要求 `targetStage=IMPLEMENTATION` 并进入 Implementation owner。纯 schema/evidence/fragment/result contract 缺口即使 owner 是 Implementation，也必须写 `repairMode=evidence-backfill + repairBudgetClass=result-contract-backfill + consumesRepairBudget=false` 并使用 `progressionDecision.backfillPackage`。回 `Task Breakdown`、`Frontend Design`、`Contract Check` 或用户确认的动作同样使用 backfillPackage 或 questionGate，不得放入 `repairDispatch`。

`frontend-general-agent` 只透传该修复包和必要 delta，不重构完整 Todo、不重新展开设计/任务全文。`frontend-implementation-agent` 只消费 `repairMode=code-repair + consumesRepairBudget=true + fixRouting=owner-needed`、`repairAttemptCount=0` 且当前 `repairPlanFingerprint` 未执行过的修复包；修复开始前必须执行修复包 preflight：确认 `rootCause/rootCauseTrace/userFeedbackTrace` 可由 `targetFiles` 闭合、`completionCriteria` 可检查、无需新增契约、不扩大 write scope、不会引入新风险域。preflight 不满足时返回 `internal-repair-required` 并附 `preflightFailureClass`，由 primary 重分类为新诊断、backfill 或 Terminal Block Whitelist，不得直接形成 terminal blocked。`fixRouting=direct-fix` 的执行者执行相同 preflight。修复完成后必须返回 `repairAttempt.selfCheck` 或 `directFixClosure`、`resolvedBlockers`、`changedFiles`、`changedFilesSource=recommendedFixPackage` 和窄复查目标。自动修复包在最终 stage result 中必须有闭合链：`frontendAutoRunId`、repair trace、recheck/rerun trace 和 closure 全部一致。窄复查仍失败时禁止原样重放 fingerprint，但必须保留 `repairAttemptKey`、递增 `repairDiagnosisRevision`、更新根因证据并生成新 fingerprint；只有重新诊断命中 Terminal Block Whitelist 才停止内部返工。不同 key 或不同诊断版本不得累计成用户授权次数。

## Required Validator Auto Repair Matrix

required validator 失败不得默认升级成用户确认。`submoduleConfigValidator`、`mockRequestValidator`、`c7nComponentApiValidator`、`i18nLocaleLedger`、`importExportPermissionsValidator` 和 stage-result close guard 命中 failed / missing / stale 时，primary、Verify 和 Review 必须先按本矩阵判断是否能自动修复；只有不满足自动修复条件时，才输出 blocker、`progressionDecision.backfillPackage` 或 question。本矩阵只判断是否可自动修复，具体调度由 `frontend-validator-fix-routing.md` 决定：`severity=blocking` 仍阻断交付出口，但不等于 `fixRouting=owner-needed`；确定性静态小修优先写 `fixRouting=direct-fix`，只有需要 Implementation owner 才写 `fixRouting=owner-needed + targetStage=IMPLEMENTATION`。

自动修复共同前提：

- 失败项可定位到当前 Feature Root、Task File Mapping、changedFiles、integrationTask 或 approved recommendedFixPackage targetFiles。
- targetFiles 位于当前 write scope，匹配 Target Placement / packageDir / pageRoot，且不触碰未持锁 shared file。
- 修复不改变 FDS/TDS/Frontend Design/Task Contract，不新增 route/DataSet/service/permission/i18n/attachment/import-export 能力，不扩大写入范围。
- validator runtime 可用，或同等人工静态检查规则已在 owner reference 中明确；只是 validator 运行失败、路径不可解析或命令目标错误时，应先修 validator target/command，而不是让用户决定是否继续。
- rootCauseTrace 能写清 symptom、cause、evidencePaths、affectedFiles、targetFilesClosure、riskDomains，并给出 verificationRerunTargets。

| validator | 典型可自动修复 rule / failure | 默认 targetFiles | mechanicalFixClass | completionCriteria |
| --- | --- | --- | --- | --- |
| submoduleConfigValidator | `submodule_route_flat_list_detail_forbidden`，且保持现有 list/create/view/edit URL 不变，只把 sibling route 改为父 route + `routes` 嵌套；`submodule_config_dev_extend_parent_config` / `submodule_config_env_extend_parent_config` 去除环境配置中的实际代码使用；`submodule_config_dev_spreads_main_config` 去除环境配置默认展开主配置 | `config/router.ts`、`config/config.dev.ts`、`config/config.<UMI_ENV>.ts` | `route-shape-mechanical` / `config-env-mechanical` | 目标 validator 窄复跑 passed；URL 常量、返回路径和菜单候选未漂移 |
| mockRequestValidator | exact/static mock mount、模板内本地 SSR guard `window.location.origin`、`process.env.<switchEnvVar> !== 'false'`、servicePrefix 集中入口、`queryMode` 被误用为源码主开关、业务请求入口直接使用 real-only service prefix、明显 service/helper target mismatch | `src/utils/servicePrefix.ts`、相关 service/DataSet/form/action/export URL helper、`dev-mock/**`、父工程 mock plugin 注册文件（仅当 File Mapping / integration task 已授权） | `mock-contract-mechanical` | mock validator 窄复跑 passed；`switchEnvVar` 从 Contract Check / stage-result `mockEnvVar` 读取并通过 `--mock-env-var` 传入；list/form/export 等请求入口仍共用集中 helper |
| c7nComponentApiValidator | `c7n_dataset_props_invalid_import_source`、已冻结 enumStrategy 下的 enum import / 字符串 provenance 补齐、`c7n_table_querybar_missing_filterbar` / `not_filterbar` 且 List Query Contract 已确认有查询区、已有项目 confirmed evidence 时补近邻结构化 `componentApiProvenance`、硬编码中文改为既有 i18n prefix 的 `intl.get(...).d(...)`、validator evidence 字段漏填 | 命中组件、DataSet、常量、locale / manifest 文件 | `static-api-prop` / `format-or-enum-literal` / `copy-text` / `validator-evidence-field` | c7n validator 窄复跑 passed；不引入新组件形态、字段契约或交互决策 |
| i18nLocaleLedger | `hzero_i18n_missing_locale_key_not_in_manifest`，且代码已正确使用静态 `intl.get(fullKey).d(defaultValue)`，只是 HZERO 平台 key 未进入 ledger 或缺状态 | `platform-locale-keys.json`、Compliance Manifest、production replacement / handoff ledger | `copy-text` / `validator-evidence-field` | i18n locale ledger validator 窄复跑 passed，pending/confirmed 计数与证据一致；硬编码中文仍由 C7N validator 修复，不能用 ledger 放过 |
| importExportPermissionsValidator | `hzero_import_*` / `hzero_export_*` 权限位置或 permissionList shape 错误、普通 Button/Upload/download/static link/自建 wrapper 替代标准导入导出入口，且不需要重新选择导入导出模式 | 导入/导出入口组件、权限常量、ImportExportEntryProof / manifest | `static-api-prop` / `permission-placement` / `validator-evidence-field` | import/export permission validator 窄复跑 passed；入口仍为标准组件或 confirmed wrapper，未新增无来源 wrapper |
| stage-result close guard | Artifact 后 `frontend-stage-result.json` 的字段漏填、status 枚举或对象落点错误、Lite 冻结 run id 被内部 session 覆盖，且 preflight 与上游事实均未变化 | 只允许 `frontend-stage-result.json`；run id 只能恢复为调度输入的 frozen value | `validator-evidence-field` / `completion-criteria-self-check` / `frontend-stage-return` | primary 本地 patch 后只重跑 close guard，记录 `schemaOnlyPatch.status=applied + artifactRedispatch=false + repairBudgetClass=execution-proof + consumesRepairBudget=false`；task-status、Review、Verification、index 漏回写必须在 Artifact 前由 preflight 打回 owner。runtime `not-run` trace、dispatch path 或 write-scope projection 缺失分别回 Verification、Task Gate、write-scope re-audit 定向补齐；不得重派 Artifact，也不得把这些内部收口缺口上浮为用户/代码 blocker |

不得自动修复的情况：

- 需要选择 routeOpenMode、菜单路径、权限码、LOV/lookup、附件、导入导出、真实 API、生产参数或页面交互策略。
- 修复要求新增或改造未在 Task File Mapping 中授权的 route/DataSet/service/permission/i18n/attachment/import-export 能力。
- C7N 高风险 props 缺少组件 API provenance，且没有标准组件替代形态或项目 confirmed wrapper 证据。
- targetFiles 不足或命中新风险域时先回 primary 重诊断并生成新 repair plan；只有确实需要扩大写入范围、存在 dirty/conflict/shared lock 或命中 Terminal Block Whitelist 时才停止代码修复。
- 用户明确要求暂停、只分析、不改代码，或当前任务目标就是输出问题清单。

## Verification Reuse Fingerprint

Verification 可复用未失效的命令级结果，统一写入 `verification.reuse`，不得新增顶层字段。

```text
verification.reuse:
  verificationScopeFingerprint: hash(changedFilesHash + command + validatorTarget + packageDir + mockNamespace + envKey)
  changedFilesHash:
  command:
  validatorTarget:
  packageDir:
  mockNamespace:
  envKey:
  sourceVerificationReportPath:
  reuseStatus: reused / new-run / invalidated / not-applicable
  invalidationReason:
```

复用只适用于同一指纹、source report 可读且结果仍覆盖当前 changedFiles 的命令/validator 结果。任何 changedFiles、command、validatorTarget、packageDir、mockNamespace、envKey、依赖就绪状态或相关 gate 输入变化都必须失效。Browser/manual 事实不得复用为 passed；只能复用为 checklist、not-run reason 或历史观察摘要。

## Cost Telemetry

各阶段尽量上报成本指标，但 telemetry 是诊断信息，不作为交付阻断项。数值字段禁止写字符串占位；采集不到时省略缺失数值并在成本报告写 `costGovernanceStatus=unverified`、`costGovernancePassed=false` 和 reason。该结果不得覆盖 `deliveryGatePassed`，不得触发业务阶段重跑或阻断允许的 `conditional` Handoff。

进入 Review 或 Verification 并继续 Handoff 的页面交付或 `regular-change`，在 Artifact 发令前默认运行 `report_frontend_cost_telemetry.py`；`repair-fast-lane` 则在 Verification `flowCutoff=after-verification` 前运行，且不得因此调度 Artifact。环境或产物不可读时写 `not-written + reason`。报告必须区分 `aggregateSampleDurationMs`（累计样本，不是墙钟）、`rootStageWallClockMs`、`traceCriticalPathMs`、`traceActiveDurationMs`、`observedTraceQueueWaitMs`、`traceTimingCompleteness`、`telemetryCompleteness`、`capsuleReuseRate`、`totalSkillReferenceReadCount`、`totalReusedOwnerReferenceCount`、`totalOwnerReferenceReloadCount` 和 `duplicateReferenceInjectionCount`。区间时间缺失时成本结论为 `partial`，不得据此宣称提效；`partial` 或普通 read 超预算不阻断业务交付，`duplicateReferenceInjectionCount>0` 仍按 owner reference evidence gate 阻断证据闭合，不能用 oversize reason 免责。

Implementation completion bundle 的输入与成本预算是当前 slice 的固定诊断合同：`inputCapsule.canonicalSources <= 8`、`ownerReferenceIdentities <= 6`、`allowedSourcePaths <= 16`；`telemetry.readFileCount > 12`、`skillLoadCount > 4`，或 `ownerReferenceReloadCount > 0` 且缺 `ownerReferenceReloadReason` 时生成 cost warning。输入 capsule 超上限表示派发输入未裁剪，completion bundle validation 失败；telemetry 超预算只令 `costGovernancePassed=false`，不得令代码结果失败、不得触发业务阶段重跑。新增风险域允许用 `invalidated + ownerReferenceReloadReason` 增量读取对应 reference。

```text
stageSummary.telemetry:
  startedAt:
  completedAt:
  stageDurationMs:
  toolCallCount:
  readCount:
  outputChars:
  retryCount:
  skillLoadCount:
  skillReferenceReadCount:
  reusedOwnerReferenceCount:
  ownerReferenceReloadCount:
  ownerReferenceReloadReason:
  readOutputChars:
  oversizeReadReason:
  capsuleReuseRate:
  duplicateReferenceInjection:
  reuseHitCount:
  plannedParallelism:
  actualParallelism:
  serialFallbackReason:
  triggeredOwnerReferenceCount:
  loadedOwnerReferenceCount:
  untriggeredOwnerReferenceLoadCount:
  specialtyTriggerResolutionMs:
  designReferenceLoadEfficiency:

agentDispatchTrace[].telemetry:
  dispatchRequestedAt:
  startedAt:
  completedAt:
  agentDurationMs:
  toolCallCount:
  outputChars:
  readOutputChars:
  skillReferenceReadCount:
  reusedOwnerReferenceCount:
  contextPackConsumed:
  contextPackPath:
  contextPackSourceHash:
  fullRootExploreUsed:
  fullRootGlobCount:
  fullRootGrepCount:
  targetedDeltaReason:
  targetedDeltaScope:
```

成本治理中的耗时、读取量和工具次数默认是 report-only / downgrade signal；重复注入或 owner capsule 漂移是 execution-proof gate，失败时必须内部重建证据，不得覆盖业务 validator 结论或形成 Lite blocker：
- 同一 `ownerSkill + sourcePaths + loadedReferenceHash + gateIds + riskDomains` 已有 `reuseStatus=reused` 时，完整 skill/reference 正文不得再次进入下游 Todo、stage result、review/verification/handoff 摘要或普通输出；只传 `ownerReferenceCapsule`。各阶段可独立消费同一 owner 的阶段用途摘要：Task 只取 Acceptance/validator plan，Implementation 只取 SOP/拒收条件，Review 只取静态检查项，Verification 只取验证证据要求；不得因阶段不同默认重载同一全文。
- `skillReferenceReadCount` 只统计本阶段真实读取 skill/reference 源文件的次数，消费 capsule 不计数；`reusedOwnerReferenceCount` 必须等于 capsule 中 `reuseStatus=reused` 的 reference 数量；`ownerReferenceReloadCount` 只统计已标记 `invalidated` 后发生的增量或全文重载。所有 reference 均为 `reused` 时，`skillReferenceReadCount=0` 且 `ownerReferenceReloadCount=0`。`duplicateReferenceInjection=true` 表示已经发生无效重复注入，不能由 `ownerReferenceReloadReason`、`oversizeReadReason` 或普通说明免责；stage-result evidence close guard 暂停当前出口并输出 `reasonClass=execution-proof + repairMode=owner-reference-cache-rebuild + requiresUserDecision=false`。primary 必须从 canonical owner identity 重建 capsule/cache、同步 slice 引用并原地重跑；真实规则变化应写 `reuseStatus=invalidated` 并记录增量加载，而不是标记为 duplicate。
- 单阶段 `readOutputChars` 超过阶段预算时尽量写 `oversizeReadReason`：Task/Task Breakdown `150000`，Implementation `240000`，Review/Final Review `120000`，Verification `180000`，Handoff/Artifact `120000`，未知阶段沿用默认 `200000`。读取体积说明只解释输出预算，不得解释或放行 owner reference 重复加载。缺失或超预算属于 Audit Telemetry warning，不覆盖已完成代码/Review/Verification 事实，不阻断 Handoff；只有 `duplicateReferenceInjection` 或其它 Execution Proof 完整性违规继续 hard fail。
- 若重复读取来自新增风险域、source path 变化、reference hash 变化或 gateIds 变化，写 `reuseStatus=invalidated` 并只补载增量 reference；不得全量重注入所有已复用 reference。
- `recommendedFixPackage`、`fix-package-recheck`、失败 validator 窄复跑、`final-delta` 和仅刷新 Handoff 状态默认继承 source stage 的 `ownerReferenceCapsule`。当 `targetFiles`、`loadedReferenceHash`、`gateIds`、`riskDomains` 和 `sourcePaths` 均未变化时必须保持 `reuseStatus=reused`，不得重新读取完整 skill/reference；只有 affected static gate scan 发现新风险域或上述 identity 字段变化时，才允许 `invalidated + ownerReferenceReloadReason` 并只补载增量 reference。
- 并行组进入 fan-out 前由 primary 完整加载 owner references 一次，生成带 `capsuleId + capsuleHash` 的 `ownerReferenceCache`；`fullReferenceLoadCount` 必须为 `1`，`reusedBySlices` 必须覆盖 planned slices。各 slice 的 `ownerReferenceReuse` 必须引用同一 capsuleId，`status=reused` 时 `skillReferenceReadCount=0 + fullReferenceReloadCount=0`。新增风险域或 reference hash 变化时只加载增量并写 invalidation reason，不得让每个 slice 重读全文。任一 cache 覆盖不完整、capsule 不一致或重复加载时，`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_slice_quality_gates.py` 必须暂停 integration 并输出 owner-reference internal repair，固定 `preserveBusinessValidatorResults=true`；primary 重建 cache、同步引用后只重跑该 execution-proof gate，不得重跑或改写已经 passed 的业务 validator，也不得把该缺口返回 Lite。

## Phase Timebox

| 阶段 | 默认预算 | 达到上限后的动作 |
| --- | --- | --- |
| Explore | quick/medium/thorough 搜索预算，以 `frontend-explore-agent` 表格为准；未指定时默认 medium；同一 `scopeFingerprint` 只允许一次 medium/thorough full Explore；已有 ready evidence 时默认预算为 0，只允许复用或针对 Decision Evidence 缺口执行一次批量 targeted delta；每个 `targetedDeltaRequests[]` 项保留唯一 `deltaKey + targetedDeltaScope` | 停止搜索，输出 evidence gap、Top-K 候选和自动/降级下一步；ready evidence 范围一致时输出 `preDesignEvidenceDecision=reuse-ready`；多个真实搜索/写入目标时返回 `needs-user` 给 Lite，不由 Explore 提问 |
| Frontend Design / Contract Check | 最多 1 轮批量补证据；Design 必须一次返回完整 `targetedDeltaRequests[]`，Lite 一次派发，Explore 按 deltaKey 一次回填；仍缺关键契约时不继续扩展搜索 | 标记 `missing/conflict/generatedCandidate/needs-user/blocked`，回 Contract Check / 用户确认，不得再次进入 Explore |
| Task Breakdown | Task 自有映射/状态输入在同次调用自动补齐；缺 frozen Design、Contract Check 或 UI Contract 时不拆 runnable task | Task 发生在并行启动前，固定返回 `design-closeout-internal-repair + targetStage=FRONTEND_DESIGN + requiresUserDecision=false`；不得生成 `parallel-baseline-invalidated` |
| Task Breakdown | 生成 `task-breakdown.md` / `task-status.md`；按三元任务口径控制粒度：`frontendExecutionMode=demo-slice / regular-change`、`taskProfile=compact / expanded / audit`、`taskSizeHint=direct / standard / large`；保留 Target Placement、route/openTab、DataSet/service、PermissionButton、mock、verification、replacement 和并发计划 | 不得为满足固定编号机械扩展任务；任务预算不改变并发计划，不得为了制造并发拆任务，也不得因任务收敛删除 `parallel-slices / execution-groups`。机器 ledger 到 Task 的映射缺口同次自动补齐；frozen ledger 本身缺失/冲突回 Design closeout 内部修复，不按 Markdown 标题判定，不触发用户授权新基线 |
| Task Breakdown | `taskProfile=compact` 使用 `templates/task-breakdown.compact.md` 与 `templates/task-status.compact.md`：优先按 shared-contract、page-slice、mock-data、integration-closeout、validator/verification 五类合并任务，只列 changedFilesPlan、acceptanceRef、validatorPlan 和 replacement，不复制完整设计/审计矩阵 | 能用 compact mode 闭合时不得展开全量 production-complete 任务模板；compact 顶层 section 超过 validator 预算时只提示压缩；缺 required gate 才拆 backfill / blocker |
| Implementation | 每个 slice 完成后先执行 validator-first / pre-review static gate：submodule config、mock-request、C7N/component API、stage-result close guard 按命中场景运行或记录 not-run reason | required validator failed / missing / target mismatch 时不得进入 Review；按 `frontend-validator-fix-routing.md` 走 direct-fix、owner-needed 回 Implementation，或回 Task Breakdown 修正 validator plan |
| Implementation | 不做开放式探索；目标文件、写入范围或关键契约不足时立即阻塞 | Task 映射缺口内部回 Task Breakdown；冻结契约不足返回 `parallel-baseline-invalidated`；write scope/dirty conflict 走外层白名单 gate，不边想边改或回 Contract Check |
| Review | 首次或范围变化使用 `full-scan` 覆盖可见 blocker；返工后默认 `fix-package-recheck`；已有未失效 Review 报告时复用；缺审查对象时 findings-first 输出阻塞；不全仓漫游找代码；`targeted-blocking` 超过 15 分钟时冻结范围 | 输出缺少审查上下文和继续需要；复查只覆盖修复包和受影响 diff；超预算时写 anomaly、stop action 和 scope frozen；失效时写明 full-scan reason |
| Review | 首次前置 Review 默认 targeted/blocking，覆盖 changedFiles、touched tasks、required acceptance、route/permission、DataSet/service、mock/request、validator 适用项和 Handoff 阻塞状态 | 只在范围扩大、契约变化、新风险域、缺 source review/task 或用户要求时升级 full-scan |
| Verification | 缺验证对象、changedFiles、build 类命令证据或长耗时命令成本确认时停止在候选命令/manual checklist | 不运行猜测命令，不启动页面运行态验证，不列 `start` 类命令 |
| Verification | 依赖就绪时优先 V0 validator、typecheck/tsc、目标范围 build/compile；HZEROJS Umi 子模块最终编译固定使用 `npm run build:ms -- <module>`，不做 yarn、pnpm 或其它 build 命令分支；超 15 分钟或同 scope 第 2 次重试时冻结验证范围 | 页面运行态、HTTP/mock smoke、浏览器和 dev server 不在 Verification 内执行；超预算时只复用未失效命令、输出 failure package 或按环境止损；未有外部专项验收证据时 `reachable/usable=unknown`，交付建议为 `conditional` |
| Handoff preflight | Artifact 发令前由 schema 1.1 脚本读取四类 canonical state，派生 hash/status/post-fix sync 并按 Handoff 状态矩阵核对；不通过时在 Artifact 未调用的前提下回状态 owner | request 不得自报 observed/sync/sourceRevision；不得先调用 Artifact 再发现冲突；不得用 blocked / conditional 掩盖内部状态冲突；preflight 通过后只允许一次 Artifact 调用 |
| Handoff | 输出 Short Closeout，包含 changedFiles、Review、Verification、未验证项、blockers、命中 replacement 主项、核心 `frontend-stage-result` 和 nextStageRecommendation | 默认 `artifactIndexProfile=minimal`、`replacementProfile=triggered-only`；不复制长矩阵、长 findings、长验证日志、完整 artifact 行集、完整 replacement 类别或 production-only 细节；required replacement 仍必须有清单或 blocked/missing |

## Intermediate Status

超过阶段预算、搜索预算、补证预算或换手深度前，必须输出中间状态：

- 已确认事实。
- 仍缺什么。
- 当前能否继续。
- 下一步是继续、降级、阻塞、回退还是请求确认。
- 若停止，说明停止原因和不继续扩展的边界。

## Deterministic Failure Routing

| failureClass | requiredOwner | generalAllowed | fixedAction |
| --- | --- | --- | --- |
| design-owned-input-missing | frontend-design-agent | no | 外层 targeted Design backfill；未启动的 slice 保持未派发 |
| task-artifact-or-schema-invalid | frontend-task-agent | no | 直调 Task owner 窄修失效产物，不重跑完整 Task；`repairBudgetClass=execution-proof + consumesRepairBudget=false` |
| task-ready-invalid | frontend-task-agent | no | 携带 validation resultPath 直调 Task owner 窄修 |
| optimization-profile-invalid | frontend-auto-agent | no | 发令前归一化 profile；expanded 缺 Design 输入时走 design-owned-input-missing |
| dispatch-plan-or-lease-invalid | frontend-auto-agent | no | primary 重建当前组 plan/lease；冻结 DAG 本身无效时才回 Task owner；`repairBudgetClass=execution-proof + consumesRepairBudget=false` |
| task-agent-empty-return | frontend-task-agent | no | direct owning call 最多窄重派一次；仍空时形成 `returnTarget=frontend-auto-agent + requiresUserDecision=false` 的 internal checkpoint，重建 owner 输入或按新证据重新路由。只有 task session/transport 确实不可恢复或重新诊断命中 Terminal Block Whitelist 才能外层退出 |
| owner-unresolved-after-routing-table | frontend-general-agent | yes | Task owner 明确后返回 auto 直调；其它异常 Todo 可转交一次 owner |
| cross-owner-conflict-after-targeted-recheck | frontend-general-agent | yes | 汇总已完成的 owner 复核证据，返回唯一 owner 或 `internal-repair-required`；primary 必须在同一 run 重建 owner 输入、backfill 或按 Terminal Block Whitelist 分类，不得把冲突本身提前包装成外层 blocker |

规则：前六类属于确定性 Execution Proof / owner 合同，不得因为 validator 名称、schema 漂移、profile 不一致、Design 输入缺失、Task 空返回或 dispatch 失败调用 General。`createsSubmodule=true` 不自动要求 expanded；compact 通过统一 Task Ready validation 进入 dispatch，expanded 才消费 optimization execution evidence。General 不持有 Task dispatch 权限，也不负责正常并行 fan-out、serial fallback 或逐组 lease。

## General Dispatch Policy

`frontend-auto-agent` 可直接调度 Task 之后的阶段 owning agent；用户明确发起的独立 build/start/HMR/remoteEntry/构建产物诊断直接调度 `hzero-build-frontend-agent` 并在诊断结果后结束。Explore / Evidence / PageSchema / Frontend Design 缺口必须返回外层 backfill。`frontend-general-agent` 仅作为阶段 owning agent 的条件 fallback：

| 场景 | 调度目标 | 条件 |
| --- | --- | --- |
| Explore / 工程证据补齐 | 外层 backfill 到 `frontend-explore-agent` | 只补目标工程、模块、页面目录、相似页面、路由/权限/i18n/DataSet/service/命令证据；不做设计、实现、验证或审查 |
| Figma / PageSchema / Frontend Design / Contract Check | 外层 backfill 到 `figma-to-frontend-agent` / `frontend-design-agent` | 作为设计前置证据或设计阶段处理；确认后再由 `frontend-auto-agent` 从 Task Breakdown 接续 |
| Task / Implementation / Review / Verification / Handoff | 对应阶段 owning agent | primary 已生成当前 Todo、前端执行模式、契约状态和成功标准，owner 明确且不需要协调 |
| 路由表仍无法识别 owner，或多个 owner 定向复核后仍冲突 | `frontend-general-agent` | Task 返回 auto 直调；其它异常 Todo 可转交一次 owner；不得处理前六类确定性失败 |

`frontend-general-agent` 只在异常协调后返回明确 owner；正常阶段由 `frontend-auto-agent` 直调：

- Task Breakdown：`frontend-task-agent`，禁止 General 转发
- Implementation：`frontend-implementation-agent`
- Review / Final Review：`frontend-review-agent`
- Verification：`frontend-verify-agent`
- Handoff：`frontend-artifact-agent`

`frontend-auto-agent` 默认直接调度上述阶段 owning agent；若使用 general fallback 且 general 返回运行时不可见、上下文不足或深度冲突，primary 只能在当前子流程回退、按外层 gate 提问，或对允许降级的外部事实记录 `conditional`。无论直调还是 fallback，若 `agentDispatchTrace.actualAgentCall=false`、`status=not-invoked/simulated/general-owned`，或缺少真实 `sessionOrToolEvidence`，该阶段不得被视为完成；必须在同一前端子流程回对应 owning stage 完成真实调用，不得以最终 `blocked / conditional` 返回 Lite。只有 owning agent 确实不可调用且形成不可闭合外层 gate 时才可最终 `blocked`。

## Stage Input Pruning

各阶段必须遵循 `templates/frontend-index.md#Stage Read Scope`。典型规则：

- Implementation 默认读：`frontend/index.md`、task-breakdown、task-status、设计摘要、目标文件/相似实现；不主动读 Handoff。每个 slice / integration task 的 Todo 必须携带同一 `inputCapsule`，默认最多 8 个 canonical sources、6 个 owner reference identities 和 16 个 allowed source paths；超出时由 primary 在发令前裁剪，不把完整阶段历史或重复 skill/reference 正文注入 Todo。
- Review 默认读：`frontend/index.md`、changedFiles/diff、task-status、设计/任务验收；返工复查时额外读 `sourceReviewPath` 和 `recommendedFixPackage`；不主动全量读 FDS/MDS/FSS。
- Verification 默认读：`frontend/index.md`、changedFiles、task-status、验证目标和候选命令证据；不主动读 Handoff。
- Handoff 默认读：`frontend/index.md`、task-status、review、verification、artifact-index、production replacement checklist 和已压缩 evidence capsule；不主动读全量源码、长 diff、长验证日志或完整历史对话。
- 当 `frontend/evidence/frontend-context-pack.json` 或 `evidence.engineeringEvidencePack` 为 `packStatus=ready` 且 `reuseStatus=reused` 时，Task/Implementation/Review/Verification 优先读取 context pack 和 canonical paths；不得为确认 package、route、request、mock、script 基线重新读取完整 FDS/TDS/设计长文或从仓库根 full Explore。context pack 只能压缩真实目标工程或已存在 package 证据；Explore / Evidence 阶段不得基于 synthetic scaffold 生成 context pack，不得把 `frontend/evidence/generated/**` 写成真实工程证据。
- Task-driven 首次 Implementation 必须把 ready context pack 的 path/sourceHash 写入调用输入和 trace telemetry。`fullRootGlobCount/fullRootGrepCount > 0` 或 `fullRootExploreUsed=true` 时必须有同次 `targetedDeltaReason + targetedDeltaScope`；否则属于 Context Pack 未实际降低探索成本，Handoff close guard 拒绝。

## Optimization Tooling

P0/P1/P2 提效工具必须写入 SDD workspace，不直接覆盖目标工程：
- P0 工程证据包：已有 package 使用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/generate_frontend_context_pack.py --root <frontend-root> --package-dir <package-dir> --out frontend/evidence/frontend-context-pack.json --expect-ready`；Explore / Evidence 只允许生成真实工程 context pack。新 package 不存在时，Explore 只记录 `packageStatus=missing`、`targetPlacementStatus`、相邻 package baseline 和 `scaffoldRequired`，不生成 evidence scaffold，不使用 `--package-source-dir` 伪造工程 evidence。若后续 Design preview 或 Implementation init 明确需要 scaffold draft，必须由对应阶段按写入范围和任务授权生成，并标记为 draft / not-runnable-proof，不能反填为 Explore evidence。
- P0 MDS 生成初稿：`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/generate_hzero_frontend_from_mds.py --mds-root <mds-root> --out-dir frontend/generated/<feature> --feature-name <feature> --service-prefix <service-prefix>`；产物只能作为 service/mock/DataSet 草稿，Implementation 需按 targetPlacement 写入目标文件。
- P0 HZEROJS 子模块 scaffold：`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/generate_hzerojs_submodule_scaffold.py --out-dir frontend/evidence/generated/<module>-scaffold --inputs frontend/evidence/task-optimization-inputs.json`；只接受 Design 冻结的 schema 1.1 结构化输入，一次生成 package/tsconfig/config/router/mock/servicePrefix/最小页面壳和 manifest，不接受散装 module/package/mock/route CLI 字段覆盖。mock namespace 与 env key 分别来自 Contract Check，不由 package 名互推。该工具不属于 Explore / Evidence 职责；产物是 SDD workspace 内的 draft，必须由明确的 Design preview 或 Implementation init 授权消费，并由 Implementation 按 confirmed write scope 应用到目标工程，补业务页面、父工程注册、locale ledger、validator 和运行态证据；不得把生成成功写成 runnable/usable 或真实工程 evidence。
- P1 静态门禁聚合：`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/run_frontend_static_gate_bundle.py --root <frontend-root-or-package> --validator c7n --validator stage-result --stage-result <frontend-stage-result.json> --gate-profile <delivery|strict>`；`demo-slice/regular-change` 取 `delivery`，`production-ready/full audit` 取 `strict`，并按实际命中增补 submodule/mock/integration 参数。主从页 integration 必须同时传 `--manifest <integration-contract-smoke.json> --require-master-detail`。聚合器只有在子命令同时返回退出码 `2` 与结构化 `status=not-run + reason` 时才记为 not-run；delivery 下可继续 conditional，strict 下仍失败。裸退出码 `2`、参数错误或非 JSON 异常必须失败。
- P1 验证 JSON 聚合：`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/aggregate_frontend_verification_result.py --stage-result <frontend-stage-result.json> --validator-result <static-gate-result.json> --runtime-acceptance <runtime-acceptance.json> --out frontend/verification/verification-result.json`；runtime acceptance 不适用时省略对应参数。Handoff 优先读该 JSON；修复后只重跑 fingerprint invalidated 命令，再生成唯一 `finalVerificationRunId`，不做无输入变化的“通过版复验”。
- P1 Short Closeout 渲染：所有 profile 先执行通用 canonical preflight；`optimizationProfile=expanded` 再叠加 optimization validator `--gate pre-handoff`。两者均通过后执行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/render_frontend_short_closeout.py --stage-result <frontend-stage-result.json> --verification-result frontend/verification/verification-result.json --pre-handoff-validation frontend/evidence/optimization-execution-pre-handoff-validation.json --out-dir frontend/handoff`；compact profile 可由 Artifact 直接消费通用 preflight。渲染器只映射已有事实，不补 Review/Verification、不运行命令、不把 runtime 缺口升级为 ready。
- P2 成本报告：`${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/report_frontend_cost_telemetry.py --stage-result <frontend-stage-result.json> --out-json frontend/diagnostics/cost-telemetry.json --out-md frontend/diagnostics/cost-telemetry.md`；用于阶段耗时/read/工具调用复盘。`aggregateSampleDurationMs` 只用于累计 agent 成本，不得写成墙钟；优先用 `rootStageWallClockMs` 评估当前收口阶段、用 `traceCriticalPathMs` 评估有时序证据的子 agent 关键路径、用 `traceActiveDurationMs` 与 `observedTraceQueueWaitMs` 判断并发和调度损耗。
- P0 Implementation 原子完成包：每个 slice / integration task 运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_implementation_result.py --input <implementation-result.json> --out <implementation-result-validation.json>`；只在结构/执行证据失败时回当前 owner 窄补，cost warning 进入 telemetry，不产生后置合同补账 session。
- P0 Final Stage Return Guard：Artifact 单次调用完成且 validator evidence close guard 通过后，运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_stage_return.py --stage-result <frontend-stage-result.json> --root <feature-root> --expected-frontend-auto-run-id <expectedFrontendAutoRunId> --out <frontend-stage-return-validation.json>`；只允许 primary 修白名单 schema-only 字段并重跑本 guard，`artifactRedispatch=false`。Lite 使用同一外部冻结 run id 对最终文件独立重跑；只有 `passed=true + disposition=allow-return + returnAllowed=true` 才可汇合，失败不得包装成普通 conditional。

## Handoff Depth

每次转交应携带 `handoffDepth`：

| handoffDepth | 含义 | 允许动作 |
| --- | --- | --- |
| 0 | `frontend-auto-agent` 当前决策 | 可返回外层 Explore / PageSchema / Design backfill，或调度执行期 owning agent / `frontend-general-agent` 执行当前 Todo |
| 1 | owning agent 或 general 正在处理当前 Todo | 可完成当前阶段，或由 general 转交一个 owning agent |
| 2 | 已经发生二级转交 | 必须返回 `frontend-auto-agent`；不得继续调度第三层 agent |

深度达到 2 后仍缺信息时，必须输出 `frontend-run-checkpoint`，包含 `returnTarget=frontend-auto-agent`、`requiresUserDecision=false`、已消费证据、缺失信息和建议恢复 owner；不得继续嵌套探索，也不得仅因 depth 输出 terminal `blocked / partial`。primary 在同一 `frontendAutoRunId` 内恢复 owning context；只有 owning agent/session/transport 经重试确认不可恢复时，才按真实 runtime interruption 或外部权限 gate 返回。

## Stage Summary Contract

每个阶段结果应包含以下短摘要，供后续恢复替代长对话：

```text
stageSummary:
  currentStage:
  confirmed:
  missingOrConflict:
  blockers:
  canonicalSourcesRead:
	  stateSourceUpdated:
	  next:
	  handoffDepth:
	  ownerReferenceCapsule:
	  evidenceCapsule:
	  telemetry:
	  stageTimings:
	    - stage:
	      wallClockMs:
	      source: primary-trace / owning-agent-trace / deterministic-tool
```

不得把完整设计、完整 findings、完整验证日志或长 diff 塞进 `stageSummary`；这些内容应留在 canonical source。

## Stop Conditions

出现以下情况必须停止当前嵌套并返回主编排：

- 当前阶段需要读取 Stage Read Scope 之外的大量材料才能继续。
- index 与 canonical source 冲突，且当前 agent 不是对应 owner stage。
- 缺少任务状态源、验证对象、审查对象或写入范围。
- 换手深度已达到 2。
- 继续当前 Mock demo 需要用户确认、偏离内置 Mock 链路、非标准工程形态、写入范围冲突处理或影响当前 runnable 路径的契约确认。生产契约、production-ready 或拒绝默认 Mock 的诉求只记录后续独立集成与稳定化 advisory。
- 已达到 Phase Timebox 或 Progression Gate 判定为 `budget-exceeded / blocked / needs-user / target-unclear / verification-unclear`。此时只返回 `frontend-auto-agent` 当前主编排：budget/target/verification 不确定性必须形成同一 run 的 checkpoint、backfill 或重诊断；`blocked/needs-user` 必须再按 Terminal Block Whitelist 或明确 question gate 分类，不得由嵌套停止直接上浮到 Lite。

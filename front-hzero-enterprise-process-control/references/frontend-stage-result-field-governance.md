# Frontend Stage Result Field Governance

用途：治理 `frontend-stage-result` 字段的新增、分层、consumer 责任和豁免边界，避免 `schema-checklist.md` 持续膨胀成“所有字段都要被所有 consumer 直接消费”的总表。

## 阅读路由
- 需要判断新字段是否应该进入 `frontend-stage-result` 时读 `Field Admission`。
- 需要判断字段属于核心汇合字段还是条件/信息字段时读 `Field Classes`。
- 需要判断 Handoff 或用户可见产物是否应输出全量字段时读 `Field Output Profiles`。
- 需要判断用户可见产物里的英文 key 是否需要中文展示时读 `Field Display Labels`。
- 需要判断 `frontend-auto-agent`、Lite、artifact 是否必须显式消费时读 `Consumer Responsibility`。
- 需要判断字段合同是否完整时读 `Field Contract Closure`。

## Field Admission

新字段进入 `frontend-stage-result` 必须至少满足以下三项：

- 会影响阶段推进、回退、汇合或最终交付状态。
- 能形成机械检查，而不是纯自然语言背景说明。
- 有明确 owner，知道由哪个阶段或哪个 skill 产出并维护。
- 能说明为什么不能放进已有对象字段：`evidence`、`designState`、`validators`、`review`、`mock`、`contracts`、`routing`、`uiContracts`、`flowControl`、`artifacts`、`productionCompliance` 或 `blockers`。

以下内容默认不应进入：

- 单一组件 API 解释。
- 单个场景实现细节，但最终不会改变汇合结果。
- 只用于某个专项 skill 内部推理、不会进入跨阶段状态机的局部备注。
- 只属于单一阶段或单一专项 skill 的字段；默认进入对象字段、manifest、replacement checklist 或专项 artifact，不新增顶层字段。

顶层字段预算：

- `field_count > 100`：warning。
- `conditional > 60`：warning。
- `core > 15`：warning。
- 新增顶层字段必须在 PR / governance record 中说明无法折叠进既有对象的原因。

## Field Classes

`frontend-stage-result` 字段分三类：

### Core Merge Fields

用于 `frontend-auto-agent`、`hzero-auto-agent-lite`、`frontend-artifact-agent` 的推进或汇合决策。核心字段必须同时具备：

- `schema-checklist.md`
- stage contract 校验脚本
- 至少一个 consumer agent

Core 固定为 15 个字段：

- `frontendExecutionMode`
- `contractStatus`
- `done`
- `featureRoot`
- `changedFiles`
- `writeScopeAudit`
- `review`
- `verification`
- `productionCompliance`
- `blockers`
- `handoffStatus`
- `progressionDecision`
- `nextStageRecommendation`
- `artifacts`
- `flowControl`

trace、question、mock、replacement、backend readiness 和专项合同均为条件字段；路径统一由 `artifacts`、`review.reviewReportPath` 或 `featureRoot` 承载，普通汇合通过 Core 中的对象摘要和 artifact path 消费。

### Conditional Contract Fields

只在命中特定 gate、页面模式或专项场景时 required。它们必须在 owning stage、checklist、manifest 或专项 reference 中有明确规则，但不要求所有 merge consumer 逐项直读。新产物必须使用对象字段；执行期脚本可以兼容读取历史顶层形态，但新旧值冲突时必须拒绝汇合。

典型字段：

- `questionGate` / `questionGateQueue`
- `agentDispatchTrace`
- `stageSummary`
- `evidence`
- `designState`
- `validators`
- `mock`
- `contracts`
- `routing`
- `uiContracts`
- `repairDispatch`

### Informational Or Trace Fields

主要用于阶段内收尾、设计追溯、恢复上下文或解释原因。它们可以不被所有汇合 consumer 直接使用，但必须能通过上游 gate 或 blockers 间接影响结果。

典型字段：

- `evidence.*`
- `designState.*`
- `review.acceptedReviewFindings`
- `artifacts.*`

字段闭合条件：

| 字段组 | 最小闭合条件 | owner / 细则 |
| --- | --- | --- |
| `evidence.*` | delta explore、baseline、similar page、golden baseline 的状态能映射到 schema checklist、Review finding、questionGate 或 blockers | `templates/evidence.md`、`baseline-comparison-rubric.md` |
| `agentDispatchTrace` | 已进入阶段有真实 owning agent 调用证据；并发实现有 slice/group 维度 trace；`dispatchVia=direct-owning-agent/frontend-general-agent` 表示直调或 fallback；非真实调用只能作为阻塞或回退证据 | `frontend-auto-agent`、`frontend-general-agent`、agent dispatch trace validator |
| `flowControl.frontendAutoRunId / repairDispatch` | Lite 首次调度生成 run id；只有 `repairMode=code-repair + repairBudgetClass=code-repair + consumesRepairBudget=true` 可进入 repairDispatch。自动修复包、IMPLEMENTATION_REWORK、REVIEW_RECHECK / VERIFICATION_RERUN 和 closure 必须保持同一 run id、repairAttemptKey 与递增 sequence，final stage result 不得携带未闭合自动修复包；不同 key 独立计数 | `frontend-auto-agent`、`hzero-auto-agent-lite`、`frontend-context-handoff-control.md`、validator evidence script |
| `review.*` | Review 复用、窄复查、finding 数和 acceptance source 可追溯到独立 review artifact | `frontend-review-agent`、`templates/review-report.md` |
| `validators.*` | validator 状态、command、target、issueCount、sourceAgent 通过 validator evidence script；旧顶层 validator 字段为 invalid | `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_validator_evidence.py`、`frontend-validator-rule-index.md` |
| `mock.parentMockPluginSourceEvidence / mock.parentMockPluginSourceVerification` | 父工程托管 mock-request 有源码级接线证据或明确 not-applicable；不能由 task-status 或自然语言摘要替代 | `front-hzero-mock-request`、`hzerojs-submodule-runtime-gate.md` |
| `verification.reuse` | Verification 指纹复用只进入 `verification` 对象，最小闭合为 fingerprint inputs、source report、reuseStatus 和 invalidationReason；不得新增 `verificationScopeFingerprint` 顶层字段 | `frontend-context-handoff-control.md`、`frontend-verify-agent`、`templates/verification-report.md` |
| `stageSummary.ownerReferenceCapsule / stageSummary.evidenceCapsule / stageSummary.telemetry` | 阶段成本治理只作为摘要、证据预算和诊断指标；完整 skill、reference 正文、长日志、长 diff 留在 canonical artifact；owner reference hash/gate/riskDomain 未变化时复用 capsule，重复完整注入必须写 reload/oversize reason；缺 reason 属于 `telemetry-quality-failed` / evidence close guard 问题，不直接覆盖 `delivery-status` | `frontend-context-handoff-control.md`、`frontend-general-agent` |
| `agentDispatchTrace[].telemetry` | agentDurationMs、toolCallCount、outputChars、readOutputChars、skillReferenceReadCount、reusedOwnerReferenceCount 等只用于定位调度成本；数值采集不到时省略并在成本报告写 `costGovernanceStatus=unverified + reason`，不影响 delivery gate | `frontend-general-agent`、agent dispatch trace validator |

Validator anchors：`agentDispatchTrace` 必须保留 `actualAgentCall=true / actualAgentCall=false / not-invoked / simulated / general-owned` 状态锚点；Review 条件字段包含 `reviewedByAgent / reviewScopeFingerprint / reviewFindingsCount / acceptedReviewFindings`；demo slice 合同锚点为 `frontendExecutionMode=demo-slice`、`runtimeDataPathDecision=requestable-demo-mock`、`mock.queryMode=mock-request`；validator forbidden status 锚点包含 `pass-static / partial / manual-pass / static-pass`。这些锚点在资产维护阶段由 `check:frontend-assets` 的 dispatch trace 校验守护；运行时最终汇合由 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_validator_evidence.py` 消费 validator evidence，具体阶段 SOP 仍归对应 owner。

已迁移的顶层镜像只允许历史产物兼容读取，不得由新产物继续输出；canonical 路径为：`flowControl.frontendEntryMode`、`mock.queryMode`、`mock.integrationState`、`contracts.backendApiReadiness`、`productionCompliance.manifest`、`contracts.productionReplacementTrigger`、`progressionDecision.blockedReason`。兼容读取发现新旧值冲突时必须拒绝汇合。

## Field Output Profiles

`schema-checklist.md` 是字段合同清单，不是用户可见 Handoff 或交付摘要的全量输出模板。产物输出必须使用 profile，避免把未命中字段批量写成 null：

| Profile | 默认使用方 | 输出规则 |
| --- | --- | --- |
| `core-only` | `frontend-artifact-agent` 默认 Handoff、Lite 汇合摘要、demo-slice 用户可见结果 | 只输出 Core Merge Fields；条件字段通过 `conditionalFieldsPresent`、`omittedConditionalFieldsReason` 和对应 canonical artifact 指针说明 |
| `conditional-expanded` | 命中特定 gate、场景、validator、mock-request、production replacement、并发回退或用户需要定位缺口时 | 在 core 外只展开本次命中的 Conditional Contract Fields；未命中字段不输出 null 占位 |
| `full-debug` | schema audit、validator repair、跨轮恢复缺字段定位或用户显式要求“完整字段” | 可以按 `schema-checklist.md` 展开完整字段合同，并为缺失字段写 `null + reason` |

输出约束：

- 核心字段缺失、不可用或用户禁止生成时，必须写字段名和 `null + reason`，因为 merge consumer 不能重新猜测。
- 条件字段只有在 gate 命中后才必须写值、`null + reason` 或 `not-applicable + reason`；未命中时不得为了凑表批量输出空值。
- 已由 `productionCompliance.manifest`、`contracts`、`productionReplacementChecklist`、`blockers` 或专项 artifact 承载的细节，不新增同义顶层字段；Handoff 只输出摘要和 artifact 指针。
- `frontendRoot` 由 `featureRoot + /frontend` 推导；`frontendIndex`、`frontendDesign`、`taskBreakdown`、`taskStatus`、`complianceManifest` 和 `productionReplacementChecklist` 的路径只写入 `artifacts`；Review 摘要和路径只写入 `review.status / review.reviewReportPath`。
- Verification fingerprint、same-stage delta、owner reference capsule、evidence capsule 和 telemetry 均不得扩展为新的 stage-result 顶层字段；必须落在 `verification.reuse`、`stageSummary.*`、`agentDispatchTrace[].telemetry` 或阶段 canonical artifact 内。
- 用户可见 Short Closeout 不输出完整字段矩阵、完整 checklist 或未触达页面区域；完整合同检查保留在 schema audit、validator 和内部产物。

## Field Display Labels

字段 key 是跨 agent、validator、schema checklist 和历史产物的稳定机器合同，默认保持英文 camelCase / kebab-case，不翻译、不新增中文别名字段。

用户可见 Handoff、人工确认摘要、Manifest 顶部状态和简短交付结论可以使用中文显示名，但必须保留英文 key，推荐格式：

```text
可构建性（buildable）：unknown + evidence
数据请求模式（queryMode）：mock-request
交付状态（handoffStatus）：conditional
```

显示名规则：

- 中文显示名只用于人读标签，不作为 `frontend-stage-result`、validator evidence、JSON、schema checklist 或脚本输入字段。
- 枚举值、状态锚点、gateId、ruleId、agent 名、skill 名、artifact path 和命令参数保持原英文值，不翻译。
- 用户可见表格可把表头写成 `中文显示名（englishKey）`；行内 gate / field key 仍使用原英文，避免 Review、Verify、Handoff 跨引用失配。
- `full-debug`、schema audit、validator repair 和跨轮缺字段定位必须优先输出原始英文 key；如需增强可读性，只能追加中文说明列。
- 不得同时输出 `buildable` 和 `可构建性` 两个同义字段；若需要中文说明，用 `可构建性（buildable）` 作为同一标签。

## Consumer Responsibility

### frontend-auto-agent

必须直接消费核心汇合字段和 question / replacement / compliance / write-scope 结果。命中父工程托管 `queryMode=mock-request` 时，还必须直接消费 `parentMockPluginSourceEvidence / parentMockPluginSourceVerification`。

可以豁免：

- Design closeout 追溯字段
- 专项 contract carrier 字段
- 已折叠进 compliance manifest 或 replacement checklist 的运行时细节

消费边界：

| 语义 | 输出位置 | consumer 行为 |
| --- | --- | --- |
| 页面区域覆盖、字段契约、组件 provenance、查询表格、详情/主从区域、动作入口、权限、i18n、LOV/lookup、附件、导入导出、mock/demo、生产替换 gate | `productionCompliance.*` / `productionCompliance.manifest.*` | 消费 gate 结果，不新增同义顶层字段 |
| 静态扫描范围和 ruleId | `validators.affectedStaticGateScan`、Review、Verification、blockers | 作为间接汇合证据，不要求逐条直读 `rulesChecked[]` |
| 前端入口模式 | `flowControl.frontendEntryMode` + `stageSummary` + `progressionDecision` | 只说明本次前端执行子流程由用户直接进入还是 Lite 集成进入；Design 始终由外层 `frontend-design-agent` / 等价 handoff 拥有，不在 `frontend-auto-agent` 内部执行；不表示交付档位，也不替代 `frontendExecutionMode` |
| 前端执行模式 | `frontendExecutionMode` + `stageSummary` + `progressionDecision` | 不新增额外交付档位字段；全局 SDD 等级写入 `changeLevel` |
| demo-slice | core fields + mock/validator/review/verification/artifact 结果 | 默认汇合为 `conditional`，并用 `deliveryTarget=mock-demo` 与 buildable/reachable/usable 表达验证事实；只有当前演示路径、安全或核心契约存在无法在同一前端子流程闭合的问题时才为 `blocked`；不得升级 `production-ready` |

### hzero-auto-agent-lite

必须直接消费 Lite 汇合、并行回退、question gate、backend readiness、replacement、verification、handoff 相关核心字段。

不应直接消费：

- Design 关单循环细节
- 具体场景 contract carrier
- 仅在前端子流程内部有效的实现 wiring 细节

### frontend-artifact-agent

必须直接消费最终交付结论、replacement、verification、write-scope、review 和 blockers 相关核心字段。

不应直接消费：

- 设计阶段细粒度追溯字段
- 已在 Handoff 资产中沉淀的场景 contract 内部细节

## Exemption Rule

字段允许被某个 consumer 豁免，但必须满足：

- 字段不是 core merge field。
- 豁免原因可一句话说明。
- 同一语义已经由其它核心字段、manifest、replacement 或 blockers 吸收。

豁免必须在 stage contract 校验脚本中显式登记，不能依赖隐式漏检。

## Field Contract Closure

字段进入或退出 `frontend-stage-result` 合同前必须能回答：

1. 是否真的需要进入 `frontend-stage-result`。
2. 它属于 core / conditional / informational 哪一类。
3. `schema-checklist.md` 是否已有必填条件和值域。
4. stage contract 校验脚本是否已有 core field 集合或豁免边界。
5. 相关 consumer agent 是否已有显式消费或明确豁免。
6. 旧字段、旧状态或旧 gate 是否残留。

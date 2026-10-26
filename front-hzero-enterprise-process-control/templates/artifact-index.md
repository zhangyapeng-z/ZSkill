# Artifact Index Template

建议路径：`sdd-workspace/changes/{change-id}/frontend/handoff/artifact-index.md`

路径规则：`sdd-workspace/changes/{change-id}/frontend/` 必须位于当前 SDD 项目根目录下，不得放在目标前端工程内部或目标前端工程平级外部目录。

默认作为 Short Closeout 的索引入口：只记录 canonical artifact 路径、状态、关键证据指针、关键缺口和 follow-up；不得复制设计正文、任务全文、完整 Review findings、完整验证日志、production-only checklist 或未触达页面区域。完整明细留在对应 artifact，Handoff 只引用路径。

`artifactIndexProfile`：

- `minimal`：默认 profile。只列核心汇合产物和本轮命中 gate 的 artifact，不为未命中的 artifact 批量生成 `missing/not-applicable` 行。
- `full`：仅用于 production-ready、完整验收、schema audit、validator repair、full-debug 或用户显式要求。可展开完整 artifact 行集和条件字段附录。

## Feature
- 功能名：
- Feature Root：
- Frontend Root：
- Target Frontend Project：
- 当前阶段：
- 交付状态：production-ready / conditional / blocked
- buildable：true / false / unknown
- reachable：true / false / unknown
- usable：true / false / unknown
- queryMode：mock-request / production-transport / partial / blocked / unknown
- similarPageEvidenceQualityStatus：ready / partial / missing / not-applicable
- productionComplianceState：production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable
- complianceManifestStatus：ready / partial / missing / blocked / failed / not-applicable
- mockApiRequestVerified：true / false / not-applicable
- stateTransitionVerified：true / false / not-run / not-applicable
- runtimeStoreConsistency：pass / failed / not-run / not-applicable
- stateTransitionGuard：ui-action-handler / ui-action-only / handler-only / missing / not-applicable
- 是否 runnable：production runnable / mock-demo runnable / 未证明 runnable / non-runnable
- done：true / false

## Artifacts
| artifactType | path | status | ownerStage | evidence | followUp |
| --- | --- | --- | --- | --- | --- |
| artifact-index-profile | `minimal` / `full` | ready | Handoff | profile 选择原因；minimal 时只列核心与命中项，full 时展开全量行集 |  |
| evidence | `sdd-workspace/changes/{change-id}/frontend/evidence/evidence.md` / `null + not-persisted reason` | missing | Explore / Evidence |  |  |
| similar-page-evidence-quality | embedded in `sdd-workspace/changes/{change-id}/frontend/evidence/evidence.md#Similar Page Evidence Quality` / not-applicable + reason | missing | Explore / Evidence / Frontend Design / Task Breakdown / Review | 相似页面、历史模块、项目 wrapper 的 evidenceQuality、adoptedPatternItems、rejectedPatternItems |  |
| component-import-map | embedded in `sdd-workspace/changes/{change-id}/frontend/design/contract-check.md#Component Import / API Provenance Contract` 或 `frontend-design.md#Component Import / API Provenance` / not-applicable + reason | missing | Frontend Design / Contract Check / Task Breakdown | JSX 组件、权限按钮、Choerodon Pro 组件、renderer/helper、附件、导入导出和项目 wrapper 的 importPath/exportShape/apiEvidence；普通 Button 也必须有来源；标准 symbol 必须可追溯到 `frontend-standard-import-coordinates.md` |  |
| choerodon-enum-import-map | embedded in `sdd-workspace/changes/{change-id}/frontend/evidence/evidence.md#Choerodon Enum Import Map` / not-applicable + reason | missing | Explore / Evidence | 仅本轮新增或修改 Choerodon/DataSet/Table/Form/组件枚举型 API props 时 required；不得把 reference import 当项目 confirmed |  |
| frontend-index | `sdd-workspace/changes/{change-id}/frontend/index.md` / `null + not-persisted reason` | missing | Explore / Evidence / Frontend Design / Task Breakdown / Implementation / Review / Verification / Handoff | 跨阶段换手入口，只记录 canonical sources 和状态摘要 |  |
| contract-check | `sdd-workspace/changes/{change-id}/frontend/design/contract-check.md` | missing | Frontend Design |  |  |
| compliance-manifest | `sdd-workspace/changes/{change-id}/frontend/design/frontend-compliance-manifest.md` / `null + not-applicable reason` | missing | Frontend Design / Task Breakdown / Implementation / Review / Verification / Handoff | serviceRequest、字段使用矩阵（含 storedField/renderedField/displayField/labelSource）、主从契约、状态动作、按钮语义、权限/i18n、LOV 绑定、组件类型、附件、导入导出、操作列和静态门禁 |  |
| design | `sdd-workspace/changes/{change-id}/frontend/design/frontend-design.md` | missing | Frontend Design |  |  |
| ui-contract | 并入 `sdd-workspace/changes/{change-id}/frontend/design/frontend-design.md` / 独立 `ui-contract.md` / not-applicable + reason | embedded | Frontend Design | UI Readback Table、QueryFields Schema、List Columns、Detail/Modal/Drawer/Button/Interaction Contract |  |
| task-breakdown | `sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md` | missing | Task Breakdown |  |  |
| task-status | `sdd-workspace/changes/{change-id}/frontend/tasks/task-status.md` | missing | Task Breakdown / Implementation / Review / Verification |  |  |
| implementation | changed files list | missing | Implementation |  |  |
| verification | `sdd-workspace/changes/{change-id}/frontend/verification/verification-report.md` | missing | Verification |  |  |
| mock-request-verification | embedded in `sdd-workspace/changes/{change-id}/frontend/verification/verification-report.md#Mock Request Verification` / not-applicable + reason | missing | Verification / Handoff | static mock validator、父工程 mock plugin 源码接线、servicePrefix/helper 对账；HZERO devServer mock API URL/method/query-body、DataSet transport/request adapter、mockApiRequestVerified、stateTransitionVerified、runtimeStoreConsistency 只能来自外部 runtime acceptance 或用户手工证据 |  |
| manual-checklist | `sdd-workspace/changes/{change-id}/frontend/verification/manual-checklist.md` / 并入 verification-report.md | missing | Verification | runtime/manual checklist、manualFindings、uiRegression |  |
| review-report | `sdd-workspace/changes/{change-id}/frontend/review/review-report.md` | missing | Review | 独立 Review 报告，必须记录 reviewedByAgent、reviewMode、reviewScopeFingerprint、reviewFindingsCount 和 dispatch trace |  |
| pre-review | `sdd-workspace/changes/{change-id}/frontend/review/pre-review.md` | missing | Review | Implementation 后、Verification 前的 findings-first 审查 |  |
| final-review | `sdd-workspace/changes/{change-id}/frontend/review/final-review.md` / `not-applicable + reason` | not-applicable | Final Review | Verification 后、Handoff 前的残余风险审查；production-ready、完整验收或高风险必需；普通 demo-slice / 非高风险 regular-change 未要求 production-ready 时不适用 |  |
| production-replacement-checklist | `sdd-workspace/changes/{change-id}/frontend/handoff/production-replacement-checklist.md` / `not-applicable + reason` | missing | Handoff |  |  |
| lessons-learned | `sdd-workspace/changes/{change-id}/frontend/handoff/lessons-learned.md` / `not-persisted + reason` | missing | Handoff | 用户手测问题、根因、fixedBy、资产增强建议 |  |
| handoff | `sdd-workspace/changes/{change-id}/frontend/handoff/frontend-handoff.md` | missing | Handoff |  |  |
| figma-cache | `sdd-workspace/changes/{change-id}/frontend/figma-cache/` | missing | Figma / Evidence |  |  |

## Status Rules
- Artifact index 是最终交付索引，不是长报告。Short Closeout 下使用 `artifactIndexProfile=minimal`，只写核心状态、核心路径、命中 gate 和关键缺口；production-ready / 完整验收 / schema audit / validator repair / full-debug 或用户显式要求时，才可用 `artifactIndexProfile=full` 展开条件字段附录和完整行集。
- `ready` 只用于单项 artifact 已生成且证据充分。
- 已列出的未生成、未验证、未审查或仅对话输出的 artifact 必须写 `missing`、`not-run`、`blocked` 或 `conditional`；用户禁止落盘、小范围 `regular-change` 或纯问答导致合法不落盘时写 `not-persisted + reason`；明确不适用的 artifact 可写 `not-applicable + reason`。`artifactIndexProfile=minimal` 下未命中 gate 的 artifact 可以不列行，但不得省略已命中 gate 的缺口。
- 存在 mock/demo、generatedCandidate、mock-only 编码或临时平台契约时，production replacement checklist 为 required。默认 `replacementProfile=triggered-only` 只要求覆盖本轮命中的替换类别；production-ready、完整验收或 full-debug 时才要求 `replacementProfile=full` 覆盖所有适用类别。缺少命中关键项不得写 overall production-ready。
- 存在 mock/demo 或 `queryMode=mock-request` 时，必须有 `mock-request-verification` artifact；Verification 只要求静态 mock validator、父工程 mock plugin 源码接线和 servicePrefix/helper 对账。缺外部 runtime acceptance 的 Network/HTTP smoke URL/method/query-body、DataSet transport/request adapter/非 DataSet service-action request 证据或 `mockApiRequestVerified!=true` 时，不得写 `reachable=true` 或 `usable=true`。DataSet 页面不得用 transport 调业务 service 充当证据。有状态动作时，只有外部 runtime acceptance 提供 `stateTransitionVerified=true`、`runtimeStoreConsistency=pass` 和 `stateTransitionGuard=ui-action-handler` 时才能写运行态闭合。
- 存在 mock handler `demoGeneratedValue` 或 placeholder 展示值时，Handoff / production replacement checklist 必须记录 `mockValueSourceLedger` 或 `demo-value` 替换项，说明展示值不代表业务事实，且未作为 create/edit 默认业务输入、submit payload 来源或 production-ready 证据。
- 生产契约已闭合且无待替换项时，production replacement checklist 可写 `not-applicable + reason`；无法判断是否存在待替换项时先标记内部 `missing` 并回 Contract Check / Handoff owner 补齐，只有替换范围存在真实契约冲突且需要外层决策时才可最终 `blocked`。
- production-ready / 完整验收 / 高风险 / HZERO+Choerodon 完整页面缺少 final-review 时，不得写 production-ready 或 DONE。
- Review 已声明执行但缺少 `review-report` / `pre-review` / `final-review` 任一 required 独立报告、`reviewedByAgent=frontend-review-agent` 或 `delegatedAgent=frontend-review-agent + actualAgentCall=true` dispatch trace 时，属于 invalid early return，必须在同一前端子流程回 Review 补齐，不得形成最终 Handoff。fallback 模式下还应记录 `frontend-general-agent -> frontend-review-agent`；未要求 Final Review 时写 `not-applicable + reason`。
- HZERO+Choerodon / DataSet / Table / Form 任务涉及枚举型 API props 且缺少 enum import map、enumProvenance 或 not-applicable reason 时，不得形成最终 Handoff。已冻结来源仅漏 Task 投影时在同一前端子流程回 Task Breakdown；冻结合同本身缺失或被工程事实证伪时返回 `parallel-baseline-invalidated`，不得回 Frontend Design。不涉及枚举型 API props 时，必须写 `not-applicable + reason`，不得因缺 enum map 单独阻塞。
- HZERO+Choerodon / 可见页面 / DataSet / Table / Form / 权限按钮 / 附件 / 导入导出 / renderer helper 任务涉及组件或 helper 使用时，必须有 component-import-map 或等价 componentApiProvenance。缺普通 symbol 来源时，已冻结标准坐标仅漏 Task 投影则内部回 Task；冻结坐标无效则返回 `parallel-baseline-invalidated`。不得在 Handoff 回 Frontend Design。固定标准坐标只需追溯坐标表，不需要 wrapper/override/冲突探索证据，也不得输出目标缺导出或 fallback 分支。`CommonImport/Route`、旧 `ExcelExport` 和深层导入只记录 migration finding，不能满足 provenance。仅 production-only 来源待登记时为 `conditional`。
- HZERO+Choerodon / DataSet / 列表查询 / 权限 / i18n / LOV / 附件 / 导入导出 / 操作列 / mock-demo 门禁命中时，必须有 `compliance-manifest` artifact；required manifest 缺失或未继承到已进入阶段时属于 invalid early return，回同一前端子流程补齐。任一生产适用 gate 为 missing/blocked/failed/conflict 时不得写 production-ready；当前演示路径 required gate 实际失败且无法自动闭合时才最终 `blocked`，production-only、optional 或非本轮范围缺口写 `conditional` + replacement / handoff risk。页面按钮或业务动作适用时，机器 Action/Button Contract 仅漏 Task 映射则内部回 Task，冻结合同缺失则返回 `parallel-baseline-invalidated`；实际显示错误且影响当前演示路径时回 Implementation 修复。
- `productionComplianceState=production-compliant` 只能作为汇总状态，不能替代 `compliance-manifest` 的逐项证据；若两者冲突，以 manifest 缺口阻断交付。
- 存在相似页面、历史模块、最近改动页面或项目 wrapper 复用时，必须有 `similar-page-evidence-quality` artifact 或 embedded 证据；未评级、legacy-risk、anti-pattern 或 unknown-quality 被采纳时，不得写 production-ready 或 `usable=true`。
- `conditional` 必须写 `done=false`，并说明当前不是完整闭环交付。非 canonical 交付状态必须按 `invalid-stage-result` 回原 owning stage，不得写入新 artifact 或整体交付状态。
- build 成功不能推导 route 可达或页面可用；`reachable` / `usable` 未验证时，`是否 runnable` 写 `未证明 runnable`。
- Verification partial 时可以写 `conditional` Handoff，但必须列出未验证项、`manualVerificationRequired`、前端服务提示和下一步。仅缺目标工程依赖或默认 mock demo 仅缺外部页面运行态证据时不需要额外 acceptanceSource；不得写 DONE 或 production-ready。
- Figma 状态为 `figma-unverified` / `screenshot-only` / `cache-only` 时，视觉风险必须继承到 Handoff，不得写视觉 confirmed。

## 用户后续确认清单摘要
| 优先级 | 事项 | 用户需要提供 | 影响 | 回到阶段 | 阻塞 production-ready | 阻塞 reachable/usable |
| --- | --- | --- | --- | --- | --- | --- |
| 必须补齐 / 建议补齐 / 可选优化 |  |  | production-ready / reachable / usable / visual-fidelity / verification / maintainability | Evidence / Contract Check / Frontend Design / Task Breakdown / Implementation / Review / Verification / Final Review / Handoff | yes/no | yes/no |

如果没有后续确认项，写 `后续需要用户确认：无`；如果整体交付状态不是 production-ready，必须说明为何无“必须补齐”项。

# Handoff Status Summary Template

建议嵌入 `sdd-workspace/changes/{change-id}/frontend/handoff/frontend-handoff.md` 顶部。

默认使用 Short Closeout：本模板只承载最终状态、核心汇合字段、Review/Verification 摘要、未验证项、blockers、replacement 主项和下一步。默认 `handoffProfile=short`、`artifactIndexProfile=minimal`、`replacementProfile=triggered-only`；完整字段矩阵、完整 Review findings、完整验证日志、production-only checklist、完整 artifact 行集、完整 replacement 类别和未触达页面区域不得复制到用户可见 Handoff；需要时只给 canonical artifact 路径。只有 production-ready / 完整验收 / schema audit / validator repair / full-debug 或用户显式要求时，才展开条件字段附录并切到相应 full profile。

字段显示名规则：用户可见 Handoff 优先使用 `中文显示名（englishKey）`，例如 `可构建性（buildable）`；`frontend-stage-result`、validator evidence、JSON 和 schema audit 仍使用原英文 key。枚举值、状态锚点、gateId、ruleId、agent 名、artifact path 和命令参数保持原英文值，不翻译。

```text
[Handoff Result]
交付状态：[production-ready / conditional / blocked]
交付摘要档位（handoffProfile）：[short / full-debug / production-ready-full]
产物索引档位（artifactIndexProfile）：[minimal / full]
生产替换档位（replacementProfile）：[triggered-only / full / not-applicable]
环境提示（environmentNotice）：[无 / environment-prerequisite-notice + 目标前端工程依赖未安装，本轮跳过依赖型 lint/typecheck/build；已继续完成 V0 静态检查和工程契约对账；下一步：安装依赖后，请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面。]
可构建性（buildable）：[true / false / unknown + evidence]
可访问性（reachable）：[true / false / unknown + evidence]
可用性（usable）：[true / false / unknown + evidence]
手动验证要求（manualVerificationRequired）：[true / false + reason]
前端服务提示（frontendServiceNotice）：[无 / 请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面]
数据请求模式（queryMode）：[mock-request / production-transport / partial / blocked / unknown / not-applicable]
Mock 请求验证（mockApiRequestVerified）：[true / false / not-applicable + evidence]
状态流转验证（stateTransitionVerified）：[true / false / not-run / not-applicable + evidence]
运行时状态一致性（runtimeStoreConsistency）：[pass / failed / not-run / not-applicable + evidence]
状态流转保护（stateTransitionGuard）：[ui-action-handler / ui-action-only / handler-only / missing / not-applicable + evidence]
Agent 调度链路（agentDispatchTrace）：[ready / missing / incomplete + evidence]
Review 报告路径（reviewReportPath）：[`frontend/review/review-report.md` / `frontend/review/pre-review.md` / `frontend/review/final-review.md` / not-run + reason]
Review 执行 Agent（reviewedByAgent）：[frontend-review-agent / not-run + reason]
Review 范围指纹（reviewScopeFingerprint）：[ready / missing / not-applicable + evidence]
是否 runnable：[production runnable / mock-demo runnable / 未证明 runnable / non-runnable]
是否 DONE：[是 / 否]
完成标记（done）：[true / false]
接受来源（acceptanceSource）：[无 / 用户接受非默认条件性交付 / not-applicable / environment-prerequisite-notice]
相似页面证据质量（similarPageEvidenceQualityStatus）：[ready / partial / missing / not-applicable + evidence]
参考模块质量门禁（referenceModuleQualityGate）：[ready / partial / missing / not-applicable + evidenceQuality / contaminationStatus / downstreamPolicy / decision]
生产符合性（productionCompliance）：[production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable + evidence]
合规清单（complianceManifest）：[ready / partial / missing / blocked / failed / not-applicable + manifestPath；包含 detailRegionCoverage / actionEntryMatrix / buttonSemanticMatrix / statusActionMatrix / buttonPermissionContract 等适用 gate]
UI 合同（uiContract）：[ready / missing / not-applicable + reason]
手工清单（manualChecklist）：[ready / not-run / missing / not-applicable + reason]
经验回灌（lessonsLearned）：[ready / missing / not-persisted + reason]
字段输出档位（frontend-stage-result-fieldProfile）：[core-only / conditional-expanded / full-debug]
核心字段状态（frontend-stage-result-core）：[ready / missing / incomplete + core field gaps]
命中条件字段（conditionalFieldsPresent）：[无 / 按 gate 分组列出命中的条件字段]
省略条件字段原因（omittedConditionalFieldsReason）：[not-triggered / folded-into-complianceManifest / folded-into-productionReplacementChecklist / folded-into-blockers / not-applicable]
下一步：[无 / 外层白名单用户确认 / parallel-baseline-invalidated -> LITE_PARALLEL_AMENDMENT / 独立 runtime acceptance / 用户手工验收]
```

## Rules
- Short Closeout 只消费已通过的 schema 1.1 `handoff-canonical-preflight`，且必须有 `statusDerivationMode=canonical-source`；不重读目标前端源码、不解析长 diff、不重跑验证、不发起二次 Review。状态源冲突应在 Artifact 发令前由 preflight 打回 owner；Artifact 内发现 source revision 漂移时返回 `invalid-artifact-dispatch`，不得降级掩盖或在同一 closeout retry。
- 同一 closeout 只允许一次 `frontend-artifact-agent` 调用。Artifact 后仅 `frontend-stage-result.json` schema-only 缺口允许 primary 本地 patch 并重跑 close guard，固定记录 `artifactAgentCallCount=1`、`artifactRetryCount=0`、`artifactRedispatch=false`。
- Short Closeout 下用户可见输出只展示命中项摘要：`artifactIndexProfile=minimal` 不批量列未命中 artifact，`replacementProfile=triggered-only` 不批量列未命中 replacement 类别。缺事实用 `conditional/blocked + nextStageRecommendation` 表达，不通过扩大 Handoff 正文补调查。
- `buildable=true` 不能推导 `reachable=true` 或 `usable=true`。
- 目标前端工程未安装依赖导致验证跳过时，Handoff 必须写 `buildable=unknown + blocked-by-missing-dependencies`、`reachable=unknown`、`usable=unknown`、`manualVerificationRequired=true`、`是否 runnable=未证明 runnable`、`交付状态=conditional`、`done=false`，并在 `environmentNotice` 或“下一步”中提示：`目标前端工程依赖未安装，本轮跳过依赖型 lint/typecheck/build；已继续完成 V0 静态检查和工程契约对账；下一步：安装依赖后，请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面。` 这是用户侧运行态自测提示，不是当前强制验证要求；不得写 `buildable=false`、`non-runnable` 或把包解析失败归因为业务代码缺陷，除非安装依赖后真实复现失败。
- `workspaceResolverStatus=failed-but-build-passed` 时，Handoff 必须保留 `buildable=true`，把 resolver 失败作为 workspace/link 风险列入未验证项；不得覆盖构建结果、不得生成页面业务代码修复包、不得写 DONE 或 production-ready。`failed-missing-dependencies / failed-link-missing` 按环境前置 conditional 处理；`failed-name-mismatch` 或确认 root dependency/workspace/父工程 registry 缺失时，下一步回 scaffold/integration 修复。
- `conditional` 必须写 `是否 DONE：否`、`done=false`；非 canonical 交付状态必须返回 `invalid-stage-result`，不得在 Handoff 中转换。
- Verification partial 时可进入 `conditional` Handoff，但必须记录未验证项、`manualVerificationRequired`、前端服务提示和下一步；仅缺目标工程依赖或默认 mock demo 仅缺外部页面运行态证据时，不额外请求用户确认。页面运行态、browser、截图、HTTP/Network 缺口的下一步是独立 runtime acceptance 或用户手工验收，不是回普通 Verification 启动服务。不得写 DONE 或 production-ready。
- Review / Final Review 已声明执行但缺少独立 Review 报告、`reviewedByAgent=frontend-review-agent` 或 `delegatedAgent=frontend-review-agent + actualAgentCall=true` 的 dispatch trace 时，不得写 `production-ready`、`Handoff ready` 或 DONE。fallback 模式下还应记录 `frontend-general-agent -> frontend-review-agent`。
- `是否 runnable` 不得填任何交付状态。
- mock demo 或 `queryMode=mock-request` 时，`mockApiRequestVerified=true`、外部 Network/HTTP smoke URL/method/query-body、DataSet transport/request adapter/非 DataSet service-action request 证据缺任一项，不得写 `reachable=true` 或 `usable=true`；DataSet 页面不得用 transport 调业务 service 充当证据。
- 有状态动作时，`stateTransitionVerified=true`、`runtimeStoreConsistency=pass` 和 `stateTransitionGuard=ui-action-handler` 缺任一项，不得写 `usable=true`。
- Figma 未 confirmed 时，视觉风险必须进入后续确认清单。
- UI Contract 缺失时，完整页面交付不得写 production-ready。
- HZERO+Choerodon / DataSet / 列表查询 / 详情或主从页 / 权限 / i18n / LOV / 附件 / 导入导出 / 操作列 / mock-demo 门禁命中时，`complianceManifest` 必须存在并说明当前交付范围；缺 manifest 或任一生产适用 gate 为 missing/blocked/failed/conflict 时不得写 production-ready。当前演示路径 required gate 未闭合时不得写 usable=true；production-only、optional 或非本轮范围缺口必须有明确降级原因和 replacement/blocker 记录。
- i18n ledger `passed=true` 只证明业务 key 已登记。`platformLocalePendingKeyCount>0` 或 `productionLocaleReady=false` 时，Handoff 必须输出 `i18nCoverage=partial/missing` 和平台 `/hpfm/prompt` replacement；只有逐 key confirmed 或 confirmed 公共 namespace 完整覆盖时才可写 pass/production-ready。`src/locales/**` / `src/locale/**` / `locales/zh_CN/**` 不得列为本流程正常交付资产；若到 Handoff 才出现，必须写 `i18n-local-locale-gate-bypass` 并停止 Handoff ready。
- 详情/编辑/主从页 required 或当前演示路径区域适用时，`detailRegionCoverage` 必须证明 Header/基本信息 required 字段、Form owner DataSet/record、required Tabs、明细筛选、详情动作和保存后 route 主键均已闭合；缺失时不得写 production-ready，且当前演示路径缺失时不得写 usable=true。
- 页面按钮或业务动作适用时，`actionEntryMatrix` 必须证明动作入口位置已确认，`buttonSemanticMatrix` 必须证明 Header 导航取消/返回与取消单据、作废、撤回、删除等业务状态动作已拆分；缺失、未验证、未确认业务状态动作出现在 Header，或上游已确认的导航取消触发业务状态 API 时不得写 production-ready。若“取消”语义未确认，Handoff 应回退 Design/Task 补矩阵，而不是直接归因为实现缺陷。
- 存在 `authorized: true` demo/候选 route 时，Handoff 必须在“后续需要用户确认”中明确：前端 route 的 `authorized: true/title` 是候选/开发可访问配置；到平台配置菜单权限、菜单标题和平台多语言；demo 中文 `title` 生产前需替换为平台可识别字符串编码，优先 `hzero.common.*`，业务命名空间编码需到 `/hpfm/prompt` 补译文，且不能写 `intl.get('xx')`。只有已确认完全由平台线上菜单标题驱动且 route 未使用 `authorized: true/title` 时，route title 才可 not-applicable。
- `productionCompliance=production-compliant` 不能替代 `complianceManifest=ready`；前者是摘要态，后者是逐项证据载体。
- `assetBaseline`、`generatedCandidate`、`mock/demo`、`figma-unverified`、`questionGateQueue` 和 `productionReplacement` 必须按累积状态汇总，不得串行短路。`follow-asset-baseline` 只解除参考样板缺失风险；它不能替代真实 API readiness、Target Placement、Open Interaction、Import/Export、LOV/lookup、附件、tenantContext、servicePrefix 或 production replacement。任一未解决项存在时，不得写 `production-ready`；任一 mock-request 核心接线或验证门禁未解决时，不得写 reachable=true 或 usable=true。
- 存在相似页面、参考子模块、历史模块、最近改动页面或项目 wrapper 复用时，`similarPageEvidenceQualityStatus` 必须为 ready，且必须有 Reference Module Quality Gate 或等价嵌入证据；legacy-risk、anti-pattern 或 unknown-quality 被采纳，或 `project-compatible + qualityBasis=no-issue-found` 授权关键实现区时，不得写 production-ready 或 usable=true。污染参考必须写入 `rejectedPatternItems` 和 lessons learned，避免下一轮继续照抄。HZEROJS 空项目、参考资产缺失/不可读或无可采纳参考模块时，可写 `similarPageEvidenceQualityStatus=missing`，但必须同时写 `assetBaselineStatus=active`、`assetBaselineSource=hzerojs-asset-baseline`、`assetBaselineDecision=follow-asset-baseline`、`questionGatePreservationStatus=clear`；这只解除相似页面/参考资产缺失风险，不解除任何未解决提问门禁。
- Handoff 默认 `fieldProfile=core-only`，只输出核心汇合字段和状态摘要；命中特定 gate 时改为 `conditional-expanded` 并只列本次命中的条件字段。只有 schema audit、validator repair、跨轮恢复缺字段定位或用户显式要求完整字段时，才用 `full-debug` 展开完整 `schema-checklist.md` 字段合同。
- 条件字段未命中时不得批量输出 `null`；已折叠进 `complianceManifest`、`productionReplacementChecklist` 或 `blockers` 的细节，用 `omittedConditionalFieldsReason` 和 artifact 指针说明。
- 页面运行态验证未运行时，`usable` 不得写 true；manual checklist 至少应以 `not-run + reason` 留痕。
- 用户手测反馈存在时，lessons learned 必须记录或说明未落盘原因。

# Gate Question Templates

用于阶段门禁需要用户确认时，统一 question 内容，减少重复停顿。

通用选项文案规则：question 的用户可见选项标题不得追加 `（推荐）`、`推荐`、`默认推荐` 或等价引导标记。若系统需要表达当前候选、排序依据或风险倾向，只能写在确认摘要、选项描述、`recommendationEvidence` / `candidateEvidence` / `排序依据` 记录中，并必须说明适用前提、选择后果和剩余风险；不得让“推荐”标记代替用户对业务目标的判断。

## Frontend Design Confirm
适用场景：Frontend Design 已文件化，当前适用的 `FD-G*` 已完成自检；命中 HZERO + Choerodon 生产规范时必须包含 `FD-G10`。本模板只用于确实需要用户冻结前端设计契约的场景；默认 `demo-slice` / mock demo / `minimum-codable` 且所有前置阻塞型 question gate 已闭合时，不再弹出 Frontend Design Confirm，Lite / primary 直接记录自动确认并进入 Task Breakdown。`frontend-auto-agent` 是后续执行承接者，不是 Design Confirm 或自动确认后可直接替代 Task Breakdown 的阶段名。

优先边界：企业前端编排固定完成 Mock demo。用户要求 production-ready、拒绝 Mock 或要求真实 API 时，不得因此阻止 Mock 设计自动确认，也不得在 Design 阶段切换运行目标；这些要求只进入后续独立联调测试与稳定化 advisory。下文涉及这些条件的旧式提问分支均受本边界约束，只有缺口同时影响当前 Mock demo 时才触发。

前置条件：`questionGate.required=false` 或所有 `questionGateQueue[]` 均已 resolved。只有会阻塞当前 Mock Task/Implementation 的 `menuGroup/route-menu`、request helper、tenant resolver、pageRoot/pageDir/pageGroup、Open Interaction 或 Mock 接线缺口才阻止自动确认。production-ready/真实 API 专属缺口进入后续独立集成 advisory，不阻塞本轮。标准 mock plugin 和 current-origin prefix 必须自动规划；只有写入范围、dirty/conflict/只读锁或非标准工程形态才进入对应 gate。

独立提问边界：每个 question item 只能确认一个影响当前 Mock demo 的问题域；候选互不依赖时，一个 question 工具调用应批量承载多个独立 item，减少串行等待。工程/package、Target Placement、Route Menu、Open Interaction、导入导出模式、Mock 接线和 Design Confirm 必须保持独立 `gateId` 和独立答案；production replacement/真实 API 不进入当前 question 队列。默认 Mock demo 是内置决策，不作为用户选项；只有当前写入范围冲突、Mock 契约缺失或非标准工程形态才按对应 gate 提问。

自动确认条件：
- 同时满足以下条件时，不调用 question：`frontendExecutionMode=demo-slice` 或 `mockDemoDecisionStatus=default-mock-demo`，`designCompletenessPolicy=minimum-codable` 或 `firstPassDesignStatus=complete-skeleton`，当前 Mock `blockingGateStatus=clear`，`questionGate.required=false`，队列为空/全部 resolved，Target Placement 已确认或不适用。production-ready/真实 API 目标不影响该自动确认。
- 自动确认时 Lite / primary 必须记录 `designConfirmationSource=default-mock-demo-policy`、`designConfirmationStatus=confirmed`、`designConfirmQuestionToolCall=not-applicable`、`frontendDesignState=confirmed`、`autoConfirmReason=mock-demo-minimum-codable-no-open-question-gate`、`nextStageRecommendation=Task Breakdown`。这只冻结当前 mock demo / minimum-codable 实现计划，不把 generatedCandidate、productionReplacement、平台菜单、权限码、真实 API、附件/导入导出生产参数或 browser 可达性升级为生产 confirmed。
- 自动确认后仍必须进入 Task Breakdown；不得直接进入 Implementation，除非小范围 `regular-change` direct 已按主流程合法跳过设计/任务。

强制调用条件：
- 不满足自动确认条件，且 `frontendDesignState=ready-for-design-confirm`、`设计确认状态=待人确认`、`suggestedQuestionTemplate=Frontend Design Confirm`、`nextStageRecommendation=Task Breakdown` 或等价状态出现时，Lite / primary 必须调用 OpenCode `question` 工具执行本模板。
- Frontend Design Confirm 是设计冻结人工确认门禁，不是普通输出模板；不得把下列文本块渲染成“请回复其一 / 请直接回复以下其一”的普通 assistant 消息替代 question 工具。
- `suggestedQuestionTemplate=Frontend Design Confirm` 只能作为模板选择线索；不能替代工具调用，也不能让 Lite 直接进入 `frontend-auto-agent`、Task Breakdown、Implementation、后端编码实现或并行组。
- 若当前运行环境没有 `question` 工具，或工具调用失败，必须输出 `question-unavailable`、保留 `frontendDesignState=ready-for-design-confirm` 和 `designConfirmationStatus=待人确认`，并暂停在当前阶段；不得用普通文本选项收集确认，也不得继续下游。
- 允许 `questionGate.required=false` 表示前置阻塞型契约门禁均已闭合；这不表示 Design Confirm 必须人工完成。满足自动确认条件时，以 `designConfirmationSource=default-mock-demo-policy` 视为已确认；不满足自动确认条件时，只有 `designConfirmationSource=user-question` 且 `designConfirmationStatus=confirmed` 后才视为已完成。

确认摘要必须先给出，不能只问“是否继续”：
- 前端设计文档：`sdd-workspace/changes/{change-id}/frontend/design/frontend-design.md`
- Contract Check：`pass / conditional / missing`，并列出阻塞项数量。
- 前端设计澄清清单：`frontend-clarifications.md` 或 `frontend-design.md` 内嵌澄清小节；列出 `blockingProductionReady=true` 的事项，若无则写 `无 / not-applicable`。
- generatedCandidate 清单：routePath、menuPath、routeTitle（仅 `authorized: true` route）、routeOpenMode、tabTitle、dws/queryStateKey、permissionCode、i18nCode、lovCode、lookupCode 中待确认项。
- Target Placement：展示 `packageDir / businessDomain / pageGroup / pageDir / routePrefix / menuGroup`，并分别标明 `evidenceStatus` 与 `userConfirmStatus`。若 `userConfirmStatus != confirmed`，不得调用本模板；必须先调用独立 `Target Placement Confirm`，确认后再回到 `Frontend Design Confirm`。
- Target Placement 还必须展示 `pageRoot / pageRootSource`。命中 HZEROJS 空项目、参考资产缺失/不可读或无可采纳参考模块时，固定 `pageRoot=src/pages`、`pageRootSource=asset-baseline`；若候选来自 TDS/FDS/生成规则并指向 `src/routes`，必须纠正为 `src/pages`。不能用“确认当前落位”这种笼统选项同时确认 package、pageRoot 和 pageDir。
- 页面打开方式：routeOpenMode（menu-current / hzero-openTab / dynamic-tab / browser-new-tab / direct-url）、父级 Tab key、目标 path、Tab title、dws、query/state 唯一性；未确认时写 `needs-confirmation / missing / generatedCandidate`。HZERO 应用内 Tab 不等于浏览器新标签页；`openTab` 复用父级 `key` 表示当前 Tab，使用详情级 `key` 才表示独立业务页签。
- mock/demo 默认决策状态：default-mock-demo / denied / not-applicable。
- production-ready 要求：要求 / 不要求 / 待确认。
- 验证范围：V0 validator、依赖就绪时的最小 typecheck/build/compile、最终编译命令候选，以及外部 runtime acceptance / 用户手工证据可能覆盖的 dev server、route smoke、browser/manual、Playwright、HMR。默认 Verification 不执行页面运行态，只记录未验证项或外部证据，不作为默认阻塞失败项。
- 下一步：进入 `Task Breakdown`，或回到 Frontend Design / Contract Check。若本轮为代码实现终点裁剪或实现后阶段裁剪，只记录 `flowCutoff=after-implementation`，不改变下一阶段仍为 Task Breakdown。

question：
- 标题：`前端设计确认`
- 问题：`是否确认当前前端设计契约，并允许进入下一阶段？`
- 选项：
  - `确认设计`：冻结当前前端设计、Contract Check 和 handoff metadata，进入 Task Breakdown；记录 confirmationSource。默认 Mock demo 已是 Frontend Design 入口内置路径；该选项不授权 generatedCandidate 直接请求远端真实 API，也不授权跳过任务拆分。只有影响当前 Mock demo 的非标准 Mock 链路偏离、必要契约缺口或写入范围冲突，才必须先完成对应 question gate 或自动 backfill；production-ready、拒绝 Mock 或真实 API 诉求只进入后续独立集成与稳定化 advisory。
  - `补充后再确认`：回到 Frontend Design / Contract Check，补齐待确认项。

记录要求：
- `designConfirmationSource`：用户选择、时间/阶段、对应 frontend-design.md 和 contract-check.md；自动确认时写 `default-mock-demo-policy`，并记录自动确认条件证据。
- `designConfirmationStatus`：confirmed / needs-revision。
- `frontendDesignState`：用户选择确认或满足自动确认条件后写 `confirmed`；用户选择补充后再确认时写 `ready-for-design-confirm` 或回退为 `needs-user`，并记录回退原因。
- `designConfirmQuestionToolCall`：called / unavailable / failed / not-applicable。`called` 且用户选择确认，或 `not-applicable` 且 `designConfirmationSource=default-mock-demo-policy` 时，才允许进入 Task Breakdown。
- `generatedCandidateReview`：记录已向用户展示的候选 route/menu/permission/i18n/lov/servicePrefix/API path、来源和后续确认/登记责任；不得命名为“授权候选编码”，也不得把设计确认理解为候选值已成为 confirmed 契约。未由平台/后端/用户明确确认或未随 `runtimeDataPathDecision` 选定路径闭合的，仍保持 `generatedCandidate` 或 `missing`。
- `designCumulativeFallbackPolicy`：必须记录 `cumulative-no-short-circuit`。确认设计只冻结当前 Contract Check、UI Contract 和 handoff metadata；它不解决 `generatedCandidate`、`assetBaseline`、`figma-unverified/cache-only/screenshot-only`、`mockDemoDecisionStatus`、`productionReplacement` 或 `questionGateQueue` 中尚未 resolved 的事实缺口。
- `targetPlacement.userConfirmStatus`：confirmed / needs-confirmation / missing / conflict / not-applicable；`Frontend Design Confirm` 只能展示既有结果，不能把 `needs-confirmation/missing/conflict` 升级为 confirmed。需要用户确认时必须来自独立 `Target Placement Confirm`。
- `targetPlacement.confirmationSource`：user-question / requirement-doc / FDS / TDS / platform-menu / not-applicable；若为 `user-question`，必须能追溯到独立 `Target Placement Confirm`，不能追溯到 `Frontend Design Confirm`。
- `confirmedOpenInteraction`：展示 explicit-source 用户/设计证据，或 `default-safe-current-tab` 策略解决的详情打开方式及内部 `routeOpenMode/detailViewInteractionMap` 映射。只有 `ambiguous-or-conflict` 才必须先调用独立 `Open Interaction Confirm`；默认策略只能实现当前菜单页签内打开，不得生成独立新标签页或 dynamic Tab。
- 已由独立 domain receipt 关闭的 Target Placement、Route Menu、Open Interaction、Import/Export Mode 或 Missing Contract 只能在 Frontend Design Confirm 摘要中只读展示，禁止再次复制该 domain 的候选选项或重新提问。
- 用户确认 domain 必须保存 Lite / 外层 question owner 返回的 `questionReceipt`：`receiptVersion=1.0`、确定性 `receiptId=<contractFreezeId>:<gateId>:<answerHash>`、questionOwner、toolName/toolCallStatus、contractFreezeId、gateId、answerHash、带时区 answeredAt 和 toolCallIdAvailability。tool call id 未暴露时允许 `not-exposed`，禁止猜测；旧 questionCallId/questionEvidence 不接受。同一 scope 的合法 receipt 是 at-most-once 依据，stale queue 只能同步 projection，不能再次提问。
- 本模板确实被调用时固定使用独立 `gateId=frontend-design-confirm` 并生成自己的 questionReceipt；前置 domain receipt 只作为摘要证据，不能复用为整体冻结确认的 receipt。
- `nextStageRecommendation`：Task Breakdown / Frontend Design / Contract Check。只有 Task Breakdown 通过后，才由 `frontend-auto-agent` 推进 Implementation。

### Route Menu Confirm
统一用于在 Frontend Design 阶段向用户确认无法由规则唯一生成、存在冲突或需要本轮生产闭合的页面访问路径、菜单入口和路由标题。它只确认 route/menu 入口契约，不替代 Target Placement、Open Interaction、权限码、平台菜单登记或默认 mock/demo 决策。若同一轮同时命中 `Route Menu Confirm` 和 `Open Interaction Confirm`，必须在 `questionGateQueue[]` 中保留两个独立 gate；候选互不依赖时由 Lite / 外层 question owner 在一次 question 工具调用中批量提交两个独立 question item，只有后者候选依赖前者答案时才允许串行。不得把访问路径/菜单入口和详情打开方式合并成一个 question 或一个答案。

强制调用条件：
- 新增或改造页面、菜单入口、路由入口、子模块 route、`authorized: true` route、route title、menu path、route prefix、菜单分组或页面访问路径时，Design 必须先按 `generated-code-conventions.md` 生成候选。已有项目父路径时沿用父路径并追加 feature kebab；无父路径但子模块明确时使用 `/<module-kebab>/<feature-kebab>`。列表 + 详情/编辑/新建形态必须拆分 `parentRoutePath`、`listRoutePath` 和 `menuPath`：父级 path 只做分组/稳定 Tab 边界，列表真实入口默认 `/list`，菜单候选默认指向真实列表 path；单页功能才默认 routePath 与 menuPath 一致。routeTitle 使用业务中文名。
- 候选无法唯一生成、存在多个可信父路径/父菜单/菜单分组冲突、目标 package 内业务域不唯一导致 routePrefix/menuGroup 不可判定、用户要求 production-ready 或本轮必须完成正式平台菜单挂载时，才调用本 question。
- FDS/TDS/功能设计/后端 handoff/设计文档/相似页面/routeConfig/平台菜单候选可作为 `recommendationEvidence`。未通过 question 或平台资产确认前，route/menu 不能写 production confirmed；但唯一 generatedCandidate 可进入 mock/demo 和候选实现，并必须进入 Handoff / production replacement。
- 若当前环境无 question 工具或主流程要求统一提问，必须输出 `questionGate.required=true`、`questionGate.template=Route Menu Confirm`、`questionGate.resolved=false` 和 `questionGateQueue[]`，停止在 `needs-user`；不得进入 Design Confirm / Task Breakdown / Implementation。
- 若同时存在未确认的详情打开方式、Tab 行为或 `routeOpenMode`，本 question 只能覆盖 route/menu 字段；另起 `questionGate.template=Open Interaction Confirm` 的独立队列项。当前 question 的问题、选项和覆盖范围不得出现“详情怎么打开 / 当前页 / Drawer / 系统页签 / 浏览器新标签页”等打开方式选择。

question：
- 标题：`路由菜单确认`
- 问题：`请确认当前页面的访问路径和菜单入口是否按以下候选执行？`
- 覆盖范围：列出本次 question 覆盖的页面、parentRoutePath / listRoutePath / createRoutePath / viewRoutePath / editRoutePath（适用时）、menuPath、routeTitle、routePrefix、menuGroup、routeConfigPath 和来源证据。
- 选项：
  - `使用候选路径`：接受当前设计给出的 routePath、menuPath、routeTitle、routePrefix 和菜单分组候选；记录 `routeMenuConfirmationSource=user-question`。该选择只确认访问入口，不确认按钮权限码、平台菜单已登记、Target Placement、详情打开方式或真实 API；描述中必须列出候选来源、适用前提和可调整点。
  - `调整路径后确认`：用户提供新的访问路径、菜单入口、标题或菜单分组；Design 必须回写候选表、Contract Check、Target Placement 关联字段和生产替换项。
  - `暂停补路由菜单`：暂不进入 Task Breakdown / Implementation；补充菜单位置、平台菜单编码、路由前缀或产品确认材料。

记录要求：
- `questionGate.template=Route Menu Confirm`。
- `routeMenuConfirmationSource`：user-question / generatedCandidate-rule / platform-menu / routeConfig / not-applicable。
- `routePathStatus / menuPathStatus / routeTitleStatus`：confirmed / generatedCandidate / needs-confirmation / missing / conflict / not-applicable。
- `routePathSource / menuPathSource / routeTitleSource`：user-question / generatedCandidate-rule / platform-menu / routeConfig / FDS / TDS / design-doc；只有 user-question、platform-menu 或明确 routeConfig/platform asset 可写 production confirmed，generatedCandidate-rule 只能写 generatedCandidate。
- `routeMenuConfirmedScope`：本次确认覆盖的页面、parentRoutePath / listRoutePath / 子页面 routePath（适用时）、menuPath、routeTitle、routePrefix、menuGroup。
- `platformMenuRegistrationStatus`：confirmed / generatedCandidate / missing / not-applicable；本 question 不自动确认平台菜单已登记。
- `openInteractionConfirmationStatus` 不得由本 question 写入 confirmed；详情打开方式必须由独立 `Open Interaction Confirm` 或明确 Drawer/抽屉证据关闭。
- 本 question 被触发且未 resolved 前阻塞 Design Confirm / Task Breakdown / Implementation / Verification / Handoff。未触发本 question 且候选唯一时，不阻塞 mock/demo 或候选实现；不得把 generatedCandidate 误报为平台菜单已登记或 production-ready。

### Button Semantic Confirm
统一用于确认同名按钮或含糊按钮文案的业务语义，尤其是“取消 / 返回 / 关闭”在 Header、业务状态动作、明细表按钮、行操作或弹层 footer 中同时出现时。

适用场景：
- FDS/TDS/Figma/PageSchema/用户输入只写“取消”，但未说明是返回列表、关闭页签/弹层、放弃本地编辑，还是取消单据/作废/撤回等业务状态动作。
- 同一文案出现在多个 UI 区域，Design 无法确认是否应拆成不同 `buttonId / handler / permission / statusActionRef`。
- Action Entry Matrix 出现 `chosenEntryLocation=not-confirmed`、`entryStatus=needs-confirmation/missing/conflict`，或 Button Semantic Matrix 出现 `semanticKind=unknown`、`navigationTarget=unknown`、`businessMutation=unknown`、`designStatus=needs-confirmation/missing/conflict`，且该项会影响 production-ready、Task Breakdown 或 Implementation。

question：
- 标题：`按钮语义确认`
- 问题：`以下“取消/返回/关闭”等按钮分别表示什么动作？`
- 选项：
  - `导航返回/关闭`：仅跳转列表、返回上一页、关闭页签/弹层或清理本地 UI 状态；记录 `semanticKind=navigation`、`businessMutation=none` 和 `navigationTarget`。
  - `业务状态动作`：表示取消单据、作废、撤回、删除等会改变业务状态的动作；必须记录 `semanticKind=business-state-action`、`statusActionRef`、权限和状态守卫。
  - `两者都需要`：拆成两个不同 `buttonId`，分别落到 Header 导航按钮和业务状态动作区/行操作/弹层 footer；Task Breakdown 必须拆任务和验收。

记录要求：
- `questionGate.template=Button Semantic Confirm`，`reason=button-semantic-unclear`。
- 更新 Action Entry Matrix：`actionId / label / actionExistsSource / chosenEntryLocation / uiArea / pageModes / entryStatus / implementationPolicy / confirmationSource`。
- 更新 Button Semantic Matrix：`buttonId / label / sourceText / copyPolicy / copyOverrideSource / uiArea / semanticKind / navigationTarget / businessMutation / statusActionRef / designStatus / confirmationSource`。
- 未 resolved 前阻塞 Task / Implementation / Verify / Handoff；若用户只接受 demo/mock 降级，可继续生成候选演示，但不得写 `production-compliant` 或 `production-ready`。

### Detail Surface Conflict Confirm
统一用于“基础信息固定展示”与“基础信息作为页签”存在实质冲突时确认详情承载面。它只处理页面内的信息架构，不替代 Frontend Design Confirm，也不顺带确认字段、按钮、接口或详情打开方式。

适用场景：
- FDS/TDS/PRD 的主语义要求“固定表头 + 业务页签”，但 FDS 的组件定义、Figma/PageSchema、用户既有要求或项目 confirmed baseline 又明确把基础信息设计为一个 Tab。
- 两类证据优先级相当，无法通过 `layoutAuthority / businessAuthority` 唯一消解，或选择会改变验收截图、页面冻结口径、首屏必见信息或 production-ready 承诺。
- 仅出现“页签包括基础信息”“基础信息页签”等概括性措辞，但全文仍能稳定读出“固定表头 + 业务页签”的两层结构时，不触发本 question；记录 `uiBusinessConflicts`，使用 `conflictResolution=auto-fixed-header` 自动收口。

question：
- 标题：`详情信息布局确认`
- 问题：`基础信息在页面中的展示位置存在冲突，请确认采用哪种布局？`
- 选项：
  - `固定基础信息 + 业务页签`：基础信息在页面上方持续可见，采购、运营、物流、单位、附件、审批记录等分类信息放在下方页签；适合“固定表头 + 业务页签”的原始语义。
  - `基础信息也作为页签`：基础信息作为第一个页签，与其它分类并列；切换到其它页签后基础信息不再持续可见。选择后必须把本次 question 结果记录为 `surfaceExceptionSource`。
  - `沿用设计稿/项目页面`：仅在已有可定位的 Figma/PageSchema 或项目 confirmed baseline，且其布局结论唯一时展示；描述中必须给出证据路径和最终映射，不能只写“参考相似页面”。

记录要求：
- `questionGate.template=Detail Surface Conflict Confirm`，`reason=detail-surface-conflict`，并作为独立项进入 `designConfirmationBundle.questionDomains[]` 和 `questionGateQueue[]`。
- 记录 `layoutAuthority / businessAuthority / uiBusinessConflicts / surfaceDecision / conflictResolution / surfaceExceptionSource / requiredVisibleByDefault`，并同步更新 Detail Contract 的 `expectedSurface / forbiddenSurface / negativeAcceptance`。
- 选择固定基础信息时，`surfaceDecision=fixed-basic-with-business-tabs`、`conflictResolution=question`、`surfaceExceptionSource=not-applicable`，基本信息 `expectedSurface=Content > BasicInfoSection/Form`、`forbiddenSurface=Tabs.TabPane`。
- 选择基础信息页签时，`surfaceDecision=basic-as-tab`、`conflictResolution=question`、`surfaceExceptionSource=user-question:<questionGateId>`，并明确首屏默认页签和切换后的可见性。
- 选择沿用设计稿/项目页面时，`surfaceExceptionSource` 必须定位到 Figma node/PageSchema 路径或项目 confirmed baseline 文件；若证据不能唯一映射为前两种布局，保持 unresolved，不得让 Implementation 自行决定。
- 当前环境有 question 工具时必须调用工具，不得用普通 assistant 文本列选项代替；工具不可用或调用失败时记录 `question-unavailable` 并停在 `needs-user`。未 resolved 前阻塞 Design Confirm / Task Breakdown / Implementation / Verification / Handoff。

### Open Interaction Confirm
统一用于向用户确认“页面入口或详情点击后怎么打开”，是该问题域唯一有效的 question 模板。面向用户时不解释 `routeOpenMode` 和 `detailViewInteractionMap` 的区别；用户只选择一种打开方式，系统内部再派生技术字段。若同一轮同时命中 `Route Menu Confirm` 和 `Open Interaction Confirm`，本模板必须作为独立 question 单独调用；不得把 routePath、menuPath、routeTitle、routePrefix 或 menuGroup 的确认合并到本 question。

适用场景：
- 列表、搜索结果或候选池中点击“查看 / 详情 / 姓名 / 编号”后，未确认是在当前菜单页签内、系统页签、独立页签还是浏览器新标签页打开。
- 详情页、编辑页或记录级页面本身作为 route 打开时，未确认是复用当前页、系统页签、每条记录独立系统页签还是浏览器新标签页打开。
- 需求文档、功能设计、FDS、TDS、Figma/PageSchema 或用户输入写明“点击跳转至新建页面 / 点击跳转至编辑页面 / 跳转至对应数据的编辑页面 / 跳转到详情页面”等“跳转至……页面”语义时，只能证明目标是 route page / 页面跳转，不是 Drawer、Modal、抽屉或弹窗；若仍需确认 Tab 行为，本 question 只展示当前菜单页签、系统页签、记录级独立系统页签或浏览器新标签页相关选项，并使用 `route-page` 作用域。
- `routeOpenMode`、`detailViewInteractionMap`、`parentTabKey`、`targetDetailPath`、`tabTitle`、`routeMode` 或 `dws/queryStateKey` 只来自 FDS/TDS/功能设计/后端 handoff/前端设计文档/相似页面/工程 evidence/routeConfig/generatedCandidate 时，必须触发本 question；默认 `demo-slice` / mock demo / `minimum-codable` 只能按内置规则把 `当前菜单页签内打开` 生成到候选列表，记录 `routeOpenMode=menu-current generatedCandidate/needs-confirmation` 与 `detailViewInteractionMap=current-tab-page unresolved/needs-confirmation`，不得写 `auto-confirmed-for-demo` 或把本 gate 从 question 队列移除。上述资料不能把 `routeOpenMode=hzero-openTab/dynamic-tab/menu-current/browser-new-tab` 写成 confirmed；其中 `ambiguous-new-tab` 变体不得读取参考子模块、相似页面、工程 evidence、routeConfig、`openTab` 调用或 `mode: 'dynamic'` 来生成、裁剪、排序或改写路由/页签选项。唯一例外是同类参考模块对当前全部入口存在可采纳的 Drawer 证据时，可追加一个固定文案的 `抽屉打开` 候选，仍需用户确认。
- 需求文档、功能设计、FDS、TDS、Figma/PageSchema 或用户输入只写“新标签页 / 新开标签 / 打开新页签”，但未明确是 HZERO 系统页签、每条记录独立系统页签还是浏览器新标签页时，必须触发本 question。该表述只能证明不是 Drawer / Modal / 当前详情内嵌，不能自动确认 `hzero-openTab`、`dynamic-tab` 或 `browser-new-tab`。
- 设计想生成 current-tab、`openTab` 独立系统页签、dynamic Tab、browser-new-tab 或其它详情交互前，必须先用本 question或明确设计证据确认交互形态；默认 demo current-tab 只作为候选，不触发自动确认。
- 设计未明确出现 `Drawer / 抽屉 / 侧边详情 / Modal / 弹窗 / 对话框 / 弹层` 时，Open Interaction question 的候选项不得包含 Drawer、抽屉、Modal、弹窗、对话框或弹层；不得为了“多给用户选择”把未出现的弹层形态加入选项。若用户只是要求编辑页、详情页、记录页或普通 route 打开，只能展示路由/页签/浏览器级候选。
- 若需求文档、功能设计、FDS、TDS、Figma/PageSchema 或用户输入已明确指定“Drawer / 抽屉 / 侧边详情”，该入口不触发 question；直接记录 `detailViewInteraction=drawer`、`questionGate.required=false`、`reason=explicit-drawer-design` 和证据来源，并继续写入 Drawer Contract。
- 若需求文档、功能设计、FDS、TDS、Figma/PageSchema 或用户输入已明确指定“Modal / 弹窗 / 对话框 / 弹层”，该入口不触发 question；直接记录 `detailViewInteraction=modal`、`questionGate.required=false`、`reason=explicit-modal-design` 和证据来源，并继续写入 Modal Contract。
- 若 route/menu 候选也需要用户确认，必须先把 `Route Menu Confirm` 和本 gate 作为两个独立的 `questionGateQueue[]` 项保存；当前 question 只能询问打开方式，不能夹带“是否使用候选路径 / 是否调整菜单入口 / 是否确认菜单分组”等访问入口问题。

内部作用域规则：
- `detail-entry` 是默认作用域：确认某个查看详情入口。用户选择写入 `detailViewInteractionMap`；若选择当前页 / 系统页签 / 每条记录独立系统页签 / 浏览器新标签页，还要同步派生 `routeOpenMode`、`parentTabKey`、`targetDetailPath`、`routeMode` 等字段。
- `route-page` 只作为内部作用域：当需要确认详情页、编辑页或记录级 route 本身的 Tab/浏览器打开方式时使用。用户问题仍按“详情怎么打开”表达，不展示 `route-page` 术语；结果只写入 `routeOpenMode` 及相关 route 字段。
- `route-page` 作用域命中“跳转至……页面”时，用户可见问题可写“这个页面入口点击后怎么打开？”，不得写“是否抽屉/弹窗打开”；路由/页签类选项默认全部展示：`当前菜单页签内打开`、`新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页`。若当前目标缺记录 id、业务单据 id、业务标题或同 route 多实例依据，`每条记录新开独立系统页签` 的描述必须说明适用前提和待补字段，选择后先记录 `generatedCandidate/needs-confirmation`，不得直接写 confirmed。
- Drawer / Modal 是明确设计来源下的详情交互形态，不是 `routeOpenMode`。没有明确弹层来源时不得作为用户可见选项；Open Interaction 不得同时生成 Drawer 和 Modal 两个弹层候选，也不得单独生成 `Modal 弹窗` 用户选项。明确 Drawer / 抽屉 / 侧边详情来源或冲突回问确需提供弹层候选时，只允许出现一个 `抽屉打开` 类选项，选择后写 `detailViewInteraction=drawer` 和 Drawer Contract，不写 `routeOpenMode`。明确 Modal / 弹窗 / 对话框 / 弹层来源时不通过本 question 提供选项，直接写 `detailViewInteraction=modal` 和 Modal Contract；若与 route-page 或 Drawer 来源冲突，先记录冲突并回到设计澄清，不得把冲突展开成 `Drawer 抽屉` / `Modal 弹窗` 两个选项让用户二选一。
- 有参考子模块、相似页面、工程 evidence、routeConfig、`openTab` 调用或 `mode: 'dynamic'` 时，这些证据默认只能作为内部 `candidateEvidence/recommendationEvidence`、route helper、path、key/title 或验证方式候选；不得改变内置路由/页签选项、不得把参考文案替换为技术标题。若同类参考模块在相同 triggerAction / targetDetail 上明确使用 Drawer，且 reference quality 不是 `anti-pattern/unknown-quality`，允许额外追加唯一一个 `抽屉打开` 候选；必须记录 `overlayEvidence=reference-drawer`、`referenceEvidenceInfluence=drawer-option-only`、参考文件路径、适用入口和 `drawerOptionChangesFds=true`。参考模块中的 Modal/弹窗仍不得生成用户选项。
- `每条记录新开独立系统页签` 作为默认路由/页签类选项展示；没有记录上下文、记录唯一 key、业务标题、`dws/queryStateKey` 或同 route 多实例依据时，不得隐藏该选项，但必须在选项描述和记录要求中标明缺口，选择后保持 `generatedCandidate/needs-confirmation`，待补齐后才可进入 confirmed 实现。
- 输入只写“新标签页”时，`questionVariant=ambiguous-new-tab`：问题文案应改为“FDS 要求新标签页打开，请确认这里的新标签页指哪种？”；默认 `recommendationEvidence=internal-rule-only`。该变体不限制为固定三个预设项，必须默认展示 `新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页` 来区分三种“新标签页”语义；若 UI 允许展示 4 个预设项且流程允许变更 FDS，可同时展示 `当前菜单页签内打开（变更 FDS）`。内部排序只可按内置模板和当前入口是否已有记录级唯一 key / 业务标题 / 同 route 多实例依据调整；参考模块不得影响这些内置选项。参考模块存在可采纳且覆盖本 question 全部入口的 Drawer 证据时，可在上述集合之外追加一个 `抽屉打开`，描述必须说明来源于参考模块且选择后会变更 FDS 的“新标签页”要求；若 Drawer 证据只覆盖部分入口，必须按适用入口拆组，不得给整组套用。若同一 question 批量覆盖列表上的新建、编辑、详情入口，必须在覆盖范围中分别列出 create/edit/detail，并说明 `每条记录新开独立系统页签` 对新建入口通常不适用，选择后新建入口只能按新建 route 的系统页签策略记录，不得借记录级 dynamic key；编辑/详情缺记录唯一 key、业务标题或 dws/queryStateKey 时只能记录 `generatedCandidate/needs-confirmation`。任何情况下都不得追加单独 `Modal 弹窗` 选项。`openTab` 只能作为内部导航工具或实现 API 记录，不得作为“新标签页”的用户可见解释；同样调用 `openTab` 时，复用父级 `key` 是当前页/当前系统页签，使用详情级或记录级 `key` 才可能是独立系统页签。
- 多个未确认入口能归为同一组时，应先按相同行为、相同目标详情和无冲突证据分组批量确认；只有入口之间存在证据冲突、目标详情不同、列表上下文保留要求不同、Tab 唯一性要求不同或用户要求逐项区分时，才拆成多组 question。

`questionToolPayload` 传递合同：
- `frontend-design-agent` 是 Open Interaction 用户可见问题的唯一生成 owner。返回 `needs-user` 时，必须在对应 `questionGateQueue[]` 项中携带完整 `questionToolPayload`，至少包含 `template=Open Interaction Confirm`、`questionVariant`、`optionSetSource`、`referenceEvidenceInfluence`、`question`、`options[].label`、`options[].description`、`coveredEntries` 和 `allowFdsChange`；不得只返回 `routeOpenMode` 候选或让外层编排重新生成选项。
- `questionVariant=ambiguous-new-tab` 时固定写 `optionSetSource=builtin-open-interaction-template`；无参考 Drawer 候选时写 `referenceEvidenceInfluence=none`。仅当同类参考模块的可采纳 Drawer 证据覆盖 `coveredEntries` 全部入口时，允许写 `referenceEvidenceInfluence=drawer-option-only`、`overlayEvidence=reference-drawer`、`referenceDrawerEvidence.sourcePath/quality/triggerAction/targetDetail/appliesToEntries` 和 `drawerOptionChangesFds=true`，并追加固定 `抽屉打开` 候选。其它参考证据仍只能保留在 `implementationEvidence`。
- 外层 `frontend-auto-agent`、Lite / primary 只能逐字段原样转发已通过 preflight 的 `questionToolPayload`，不得摘要、翻译、合并、裁剪、重排或自行根据参考模块补充选项。payload 缺失、字段不全、出现技术标题、缺少固定候选、`referenceEvidenceInfluence` 不是 `none/drawer-option-only`，或 Drawer 证据不能覆盖当前入口时，标记 `openInteractionPayloadValidation=failed`，回 `frontend-design-agent` 做 targeted question payload backfill；不得调用 question，也不得自行修写后继续。
- `ambiguous-new-tab` preflight 的最小合法集合为 `新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页`；`allowFdsChange=true` 时再包含 `当前菜单页签内打开（变更 FDS）`。明确记录 `overlayEvidence=drawer-conflict` 或合法 `reference-drawer` 时可再出现唯一一个 `抽屉打开`；任何情况下不得出现 `弹窗/抽屉`、`Modal 弹窗` 或 `弹窗打开`。`输入自己的答案` 属于 question 客户端能力，不写入 payload 业务选项。
- `ambiguous-new-tab` payload 在运行时必须完成同字段的内存 preflight，并记录 `openInteractionPayloadValidation=passed`、`validationMode=in-memory-contract` 和校验摘要。资产维护阶段由 `check:frontend-assets` 覆盖 fixture 级机械校验；运行时不得依赖资产治理脚本。未通过不得发起 question。

用户可见选项文案：
- 实际向用户提问时，选项标题和描述必须优先复用下面的中文行为文案；标题保持短、稳定、面向业务用户，不得追加“推荐”标记。描述要尽可能详细，至少说明：用户选择后的页面行为、是否新增 HZERO 系统页签或浏览器标签页、适用场景、关键限制或不适用场景、后续会写入的内部技术映射/验证点；若某个选项存在特殊要求、前置条件、字段缺口、适用例外、生产替换或后续确认要求，必须直接写进该选项的用户可见描述，不得只写在内部记录、Contract Check 或 Handoff。不得只写“按候选实现”“新开页签”“使用 dynamic-tab”“通过 openTab 打开标签页”等短句。不得把 `routeOpenMode`、`current-tab-page`、`hzero-openTab`、`dynamic-tab`、`browser-new-tab`、`HZERO openTab`、`dynamic tab`、`系统动态页签`、`当前页内切换`、`应用内 Tab`、`动态 Tab` 等技术枚举值或实现术语直接作为选项标题，也不得用 `HZERO 页签` 这种未说明“新开/复用/每条记录独立”的半技术标题替代用户可见描述。技术枚举只写入记录要求、Contract Check、Handoff 和 `frontend-stage-result`。可验证锚点为 `owner=frontend-design-agent`、`evidence=questionGate.template=Open Interaction Confirm + questionVariant + optionTitles + optionDescriptions + routeOpenModeStatus + specialRequirementsInDescriptions`、`status=question-ready | needs-rewrite | blocked-by-unresolved-open-interaction`、`reason=ambiguous-new-tab | technical-term-leak | missing-option-description | hidden-special-requirement`；若命中 `needs-rewrite/blocked-by-unresolved-open-interaction`，回退动作是重写用户可见选项文案或暂停在 Open Interaction Confirm，不得进入 Task Breakdown / Implementation。
- `当前菜单页签内打开`：点击后仍在当前 HZERO 系统页签 / 当前菜单页中，系统页签数量不增加；列表、新建、查看、编辑在同一父 route 下切换。适合编辑页或详情页是完整页面，但不需要同时打开多个记录的场景。技术映射为 `detailViewInteraction=current-tab-page`、`routeOpenMode=menu-current`、`openTabMode=parent-key`；实现固定使用 `import { openTab } from 'utils/menuTab';`，并让 `key` 复用父级菜单 path / 父级 route，例如 `openTab({ key: '/test/demo-parent', path: '/test/demo-parent/detail/edit/{id}' })`。这里的 `openTab` 是页签容器导航工具，不表示新开系统页签。新生成路由必须使用内置页面模式模板：列表 `/list`、新建 `/create`、详情 `/detail/view/:id`、编辑 `/detail/edit/:id`；不得把编辑页描述或设计为 `/<feature>/edit/:id`、`/detail/create`、`?editFlag=true`、`?mode=edit` 或同类 query 身份。详情 route 使用 `mode: 'route'` 或省略默认 route，不能配置成 `dynamic`。
- `当前页打开详情`：仅在 `detail-entry` 作用域可作为 `当前菜单页签内打开` 的业务化标题使用；描述和技术映射完全继承 `当前菜单页签内打开`，仍必须使用 `/detail/view/:id` 或 `/detail/edit/:id` 等内置 route 模板。
- `抽屉打开`：Open Interaction 中唯一允许出现的弹层类用户选项。设计冲突回问，或同类参考模块在相同入口/目标上存在可采纳且覆盖当前 question 全部入口的 Drawer 证据时可以展示；参考证据只增加该候选，不自动确认 Drawer。点击后在当前列表页侧边打开详情，列表页本身不离开，筛选、分页和滚动上下文可以保留。若 FDS 原要求“新标签页”，描述必须明确选择抽屉会变更该要求。技术映射为 `detailViewInteraction=drawer`，不写 `routeOpenMode`；对应 Drawer Contract。若设计未指定宽度，详情 Drawer / 高密度只读详情优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并记录 readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`；只有设计/Figma/PageSchema/项目 confirmed baseline/用户明确要求更大时才能使用 medium/large/百分比宽度。
- `Modal 弹窗` 不得作为 Open Interaction 的用户可见选项。明确 Modal / 弹窗 / 对话框 / 弹层来源时，直接记录 `detailViewInteraction=modal`、`questionGate.required=false` 和 Modal Contract；来源与 route-page / Drawer 冲突时进入设计澄清，不得把普通编辑页降级成弹窗表单，也不得新增一个单独“弹窗打开”选项。
- `新开一个系统页签`：点击后在 HZERO 系统页签栏中新开或激活一个业务详情页签；这不是浏览器新标签页。它通常表示一个可复用的业务详情页签，例如重复打开同类详情时复用同一详情页签或按业务 key 控制复用。技术映射为 `detailViewInteraction=hzero-openTab`、`routeOpenMode=hzero-openTab`；必须确认 tabTitle、详情 Tab key 和查询状态传递方式，且详情级 key 不得误写成父级 key。若标题要显示记录身份，应使用用户可读业务编号/名称字段；不能把技术主键、加密 id 或 route param id 默认作为用户可见标题。
- `每条记录新开独立系统页签`：点击不同记录会在 HZERO 系统页签栏中分别打开多个详情页签，例如 A 记录、B 记录各一个。它强调多实例并存，适合并行查看或对比多个记录。技术映射为 `detailViewInteraction=dynamic-tab`、`routeOpenMode=dynamic-tab`、`routeMode=dynamic`；`openTab.key` 与 `path` 使用带记录 id 的具体详情路径。若同一 pathname 不同 search 也要分别打开，必须确认 `dws=true` 或 queryStateKey。`openTab.title` 可以显示业务编号/名称来帮助识别多实例页签，但该 display field 必须来自 API/List record/详情回读合同；不能用 `id/headerId/*Id` 技术字段替代业务标题。
- `浏览器新标签页`：点击后打开浏览器自己的新标签页或新窗口。仅用于外链、跨系统地址，或用户明确要求浏览器级打开的场景。技术映射为 `detailViewInteraction=browser-new-tab`、`routeOpenMode=browser-new-tab`；必须验证完整 URL 构造，内部 HZERO route 默认不得选它。

question：
- 标题：`页面打开方式`
- 问题：`这个页面入口点击后怎么打开？`
- 覆盖范围：列出本次 question 覆盖的 `routePath / listRegion / triggerAction / targetDetail`；若批量确认多个详情入口，必须列出分组和应用范围。不得把 `route-page/detail-entry` 术语展示给用户。
- 选项：路由/页签类默认展示 `当前菜单页签内打开`、`新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页`；不得因为当前缺少记录 id、业务单据 id 或同 route 多实例证据而隐藏 `每条记录新开独立系统页签`，但描述必须说明补齐记录唯一 key、业务标题、`dws/queryStateKey` 后才能 confirmed。设计冲突回问，或同类参考模块存在可采纳且覆盖当前 question 全部入口的 Drawer 证据时，可追加唯一一个 `抽屉打开` 选项；参考证据只增加该选项，不影响内置选项。任何情况下不得追加单独 `Modal 弹窗` / `弹窗打开` 选项。若内部作用域是 `detail-entry`，可把 `当前菜单页签内打开` 的标题显示为 `当前页打开详情`；若是编辑页、详情页或记录级 route 本身，必须使用 `当前菜单页签内打开`，不得用含糊的 `当前页打开`。默认展示顺序不是推荐标记，必须通过描述说明各选项适用场景；任何特殊要求、缺口或不适用条件都必须写在对应选项描述中。
- `ambiguous-new-tab` 变体选项：不得按固定数量裁剪选项。默认展示 `新开一个系统页签`、`每条记录新开独立系统页签` 和 `浏览器新标签页`；若 UI 允许展示 4 个预设项且流程允许变更 FDS，可同时展示 `当前菜单页签内打开（变更 FDS）`。排序可根据记录级多实例证据调整，但不得在标题中标记推荐。参考子模块、相似页面、工程 evidence、routeConfig、`openTab` 或 `mode: 'dynamic'` 不得影响内置选项；仅合法 `reference-drawer` 可追加固定 `抽屉打开`，并必须在描述中说明参考来源、适用入口和对 FDS 的变更，部分入口适用时先拆组。不要用“HZERO 页签”“系统页签打开”“系统动态页签”等含技术实现色彩或语义不完整的标题替代用户可见文案，也不要把 `dynamic-tab / hzero-openTab / browser-new-tab` 暴露成选项标题。批量覆盖 create/edit/detail 时，选项描述必须写清选择会应用到哪些入口，且 edit/detail 的记录级独立页签策略不能反推为 create 的记录级动态策略。缺少记录唯一 key、tabTitle 或 dws/queryStateKey 时，仍可展示对应候选并说明缺口，但记录为 `generatedCandidate/needs-confirmation`，不得写 confirmed。若用户选择 `当前菜单页签内打开（变更 FDS）` 或 `抽屉打开`，必须记录这是对 FDS “新标签页”要求的变更确认。任何情况下不得追加 Modal / 弹窗选项。

记录要求：
- `questionGate.template` 必须精确等于 `Open Interaction Confirm`。`Route Open Mode Confirm / Detail View Interaction Confirm` 属于无效旧值；命中时形成 migration finding 并回 Design 重建 question，不得静默归一化或沿用旧回答。
- 本 gate 不得写入 `routeMenuConfirmationSource`，不得把 `routePathStatus / menuPathStatus / routeTitleStatus` 从 generatedCandidate 升级为 confirmed；route/menu 入口确认只能来自独立 `Route Menu Confirm`、平台菜单或 routeConfig 证据。
- `questionGrouping`：记录本次 question 覆盖的入口集合、分组依据、是否批量应用到组内全部入口；禁止只写“全部详情入口”而不列具体入口。
- `routeOpenMode`：menu-current / hzero-openTab / dynamic-tab / browser-new-tab / direct-url / not-applicable。
- `routeOpenModeSource`：user-question / requirement-doc / FDS / TDS / Figma / project-evidence。只有 `user-question` 可把新增/改造详情打开方式写成 confirmed；其它来源只能作为 `recommendationEvidence`，状态必须为 generatedCandidate / needs-confirmation。
- `detailViewInteractionMap`：按 `routePath + listRegion + triggerAction + targetDetail` 逐项记录；每条包含 `detailViewInteraction`、`sourceEvidence`、`questionGate.required/resolved` 和 `reason`。
- `detailViewInteraction`：drawer / current-tab-page / hzero-openTab / dynamic-tab / browser-new-tab / modal / other。
- `interactionConfirmationSource`：user-question / requirement-doc / functional-design / FDS / TDS / Figma / user-input / project-evidence。
- `recommendationEvidence`：SOP default / FDS / TDS / Figma / project-evidence / user-hint。
- 只由 FDS/TDS/用户输入中的“新标签页”触发时，未得到用户选择前必须记录 `routeOpenModeStatus=needs-confirmation/generatedCandidate`、`routeMode=generatedCandidate`、`detailViewInteractionMap=unresolved`、`questionGate.required=true`、`questionGate.template=Open Interaction Confirm`、`questionVariant=ambiguous-new-tab`；不得写 `confirmed`，也不得把 `routeMode=dynamic` 或 `browser-new-tab` 作为已确认事实。
- 任何 Open Interaction 回执都固定使用 `designConfirmationPatchMode=targeted-contract-patch + contractDiffDomains=[route-interaction]`；它会改变打开方式的契约值或权威来源，不是 metadata-only 状态同步。Design 必须在该次回执 closeout 内同步受影响路由/页签字段、Design Handoff Metadata、Contract Check、Coverage Ledger、canonical source hashes 和 Index，并在 canonical validator 通过后才返回。
- 若选择当前菜单页签内打开 / 当前页打开详情：写入 `detailViewInteraction=current-tab-page`、`routeOpenMode=menu-current`、`routeMode=route/omitted-default-route` 和 `navigationApi=builtin-standard: import { openTab } from 'utils/menuTab';`；若目标是详情或编辑 route，还必须写入 routeContext、returnPolicy、filter/page/sort/scroll 恢复策略、`parentTabKey`、`targetDetailPath`，并使用 `/create`、`/detail/view/:id`、`/detail/edit/:id` 内置 route 模板。
- 若选择抽屉打开：写入 Drawer Contract；宽度未指定时记录项目 Drawer 默认尺寸或 confirmed baseline、readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`，并记录关闭后是否刷新列表。仅当有明确 Drawer / 抽屉 / 侧边详情来源或冲突回问时允许出现本选择。
- 明确 Modal / 弹窗 / 对话框 / 弹层来源时不提供用户选择项，直接写入 Modal Contract；宽度未指定时普通表单 Modal 默认 `size=small / width≈520px` 或项目 small 等价值，并记录关闭后是否刷新列表。若需要用户确认，是设计冲突澄清，不是 Open Interaction 的单独 `Modal 弹窗` 选项。
- 若选择新开一个系统页签：写入 `routeOpenMode=hzero-openTab`、`routeMode=route/omitted-default-route`、tabTitle、详情 Tab key 和查询状态传递方式；若存在新建/查看/编辑页面模式，还必须写入内置 `/create`、`/detail/view/:id`、`/detail/edit/:id` 的 `routeContext`，并把 router 模板策略记录为 `submodule-router-open-tab-page-modes.ts.template` 或等价父子 `routes` 结构。不得把页面模式、记录 ID 或 openTab key/path 身份放进 `editFlag/mode/action` query；记录中必须区分 `openTab-parent-key` 与 `openTab-detail-key`，前者属于当前页打开，不属于本选项。
- 若选择每条记录新开独立系统页签：写入 `routeOpenMode=dynamic-tab`、详情级 key 规则、`routeMode=dynamic`、route `mode: 'dynamic'`、tabTitle、dws/queryStateKey、重复打开同一记录时复用还是新开；若存在新建/查看/编辑页面模式，还必须写入内置 `/create`、`/detail/view/:id`、`/detail/edit/:id` 的 `routeContext`，并把 router 模板策略记录为 `submodule-router-dynamic-tab-page-modes.ts.template` 或等价父子 `routes` 结构。
- 若选择浏览器新标签页：必须记录为什么不能使用 Drawer 或 HZERO 系统页签，并验证完整 URL 构造。
- 未 resolved 前不得进入 runnable Task Breakdown / Implementation；不得让 Implementation 自行选择当前菜单页签内打开、当前页打开详情、Drawer、Modal、route、openTab、dynamic Tab 或浏览器级新标签页。涉及 `window.open` / `target="_blank"` 必须来自已确认设计。当前菜单页签内打开只是 Design question 的可选项之一，不是开发阶段的默认实现兜底。

旧模板拒绝规则：
- `Route Open Mode Confirm` 和 `Detail View Interaction Confirm` 不能作为 template、alias 或已解决 question 继续消费；必须由 Design 使用 `Open Interaction Confirm` 重新生成对应作用域的问题。

### Target Placement Confirm
适用场景：前端工程或 `packages/<module>` 已定位，但功能应落到哪个包内业务域、页面目录、路由前缀或菜单分组尚未确认。确认 `packageDir` 不等于确认 `pageDir / businessDomain / routePrefix`。

强制调用条件：
- 目标包下存在多个业务目录、多个 route prefix、多个菜单分组或多个相似页面候选，例如同一包内同时存在 `Setting`、`PreEntry`、`Talent` 等业务域。
- 用户只给出父工程或 package 路径，但未说明当前功能应落到已有业务域、新增业务域还是父工程集成入口。
- Explore 只能得到包内候选目录或 route prefix，且候选来自 similarPage、命名相似、最近改动或生成规则。
- 历史 feature 已有 changedFiles，但缺 `Target Placement Contract` 中的 `businessDomain / pageDir / routePrefix / routeConfigPath`。
- 主流程或子 Agent prompt 仅写了“目标模块/微包”“探索发现候选落位”“已有文件位于某微包”，但没有用户确认、需求/FDS/TDS 明确指定或平台菜单配置确认。
- 命中 HZEROJS 空项目、参考资产缺失/不可读或无可采纳参考模块，且候选 `pageDir` 指向 `src/routes/**`。TDS/FDS/后端 handoff 中的文件清单或生成候选只能作为 invalid hint，不能把 `src/routes` 置为 confirmed，也不再向用户询问是否偏离空项目基线；Design 必须固定回填为 `pageRoot=src/pages`、`pageRootSource=asset-baseline`。
- 无参考基线下，问题文案不得写成“是否接受 `packages/<module>/src/routes/<Feature>` 作为包内页面落位基线”。`src/routes` 不是 asset baseline，也不是新生成页面的可选落点。必须把默认落点表述为 `packages/<module>/src/pages/<PageName>`。

question：
- 标题：`功能落点`
- 问题：`当前功能应落到哪个业务子模块 / 页面目录 / 路由分组？`
- 选项：
  - `使用资产基线`：当项目为空或缺少可采纳参考模块时，固定使用 `packages/<module>/src/pages/<PageName>` 作为页面根；记录 `pageRoot=src/pages`、`pageRootSource=asset-baseline`、`assetBaselineSource=hzerojs-asset-baseline`。这只确认工程形态，不确认 LOV、附件、权限、真实 API 或后端 readiness。
  - `沿用最匹配目录`：仅当存在项目证据或相邻模块证据时使用工程证据中最高置信的已有业务目录和 route prefix；必须展示候选路径、候选路由和证据来源，用户确认后才可写入。无参考基线下不得把 TDS/FDS 候选 `src/routes/**` 作为本选项的候选依据。
  - `新建业务目录`：在已确认 package 下新建独立业务目录和 route prefix；必须同步确认目录名、路由前缀、菜单分组和 i18n/权限 namespace。
  - `回到设计补充`：暂不进入实现，补充菜单位置、业务域归属、路由前缀或产品/平台确认材料。

记录要求：
- `targetPlacement.businessDomain`：例如 `Talent / PreEntry / Setting`，或 `new:<name>`。
- `targetPlacement.pageRoot`：页面根目录；新生成页面固定 `src/pages`。`src/routes` 只允许用于改造已存在且证据明确的存量页面，不作为新生成页面选项。
- `targetPlacement.pageRootSource`：asset-baseline / project-evidence / adjacent-module / existing-file / user-confirmed；`src/routes` 不允许使用 asset-baseline，也不允许仅由 user-confirmed 作为新生成页面来源。
- `targetPlacement.pageGroup`：页面目录分组，例如 `src/pages/hhronbrd/Talent`。
- `targetPlacement.routePrefix`：功能主 route prefix，例如 `/hhr/onboard/talent`。
- `targetPlacement.menuGroup`：菜单分组或 `missing/generatedCandidate/not-applicable`。
- `targetPlacement.packageInternalAmbiguity`：none / multiple-business-domains / multiple-route-prefixes / multiple-candidates / missing-evidence。
- `targetPlacement.confirmationSource`：user-question / requirement-doc / FDS / TDS / platform-menu / not-applicable。
- `targetPlacement.evidenceStatus`：ready / partial / missing / conflict / not-applicable。
- `targetPlacement.userConfirmStatus`：confirmed / needs-confirmation / missing / conflict / not-applicable。
- `targetPlacement.status`：只有 `userConfirmStatus=confirmed` 时才能写 `confirmed`；仅有工程证据时写 `generatedCandidate / needs-confirmation`。
- 确认文本必须包含精确 `pageRoot` 和 `pageDir`。`confirmedAnswer=确认当前落位 / 沿用当前落位 / 确认目标包` 但没有写明 `src/pages` 时，只能确认 `packageDir`，不能确认包内页面根；若设计仍要进入 runnable Task，必须重新触发 Target Placement Confirm。
- `confirmationSource=TDS / FDS / backend-handoff / user-question` 不能单独支撑新生成页面 `pageRoot=src/routes`。缺参考基线时即使 TDS 写了 `src/routes/<Feature>`，也必须纠正为 `src/pages`。
- 若上游已错误输出“`src/routes` 作为包内页面落位基线”，必须在 Lite / Frontend Design 汇总中纠正为 `invalid-baseline-label`，把默认候选改回 `pageRoot=src/pages`、`pageRootSource=asset-baseline`；不得要求用户接受该错误基线才能继续。
- 未 resolved 前，`questionGate.template=Target Placement Confirm`，`reason=target-placement-unclear`，阻塞 Task / Implementation / Verify / Handoff。

### Native HTTP Confirm
适用场景：需求文档、技术设计或用户输入明确提到原生 `axios`、`fetch`、`XMLHttpRequest`、外部直连、第三方域名或绕过 HZERO request，但 serviceRequestContract 尚未确认。目标项目既有原生 HTTP 代码只能作为实现参考，不能单独触发确认或授权。

不适用：需求文档没有提原生 HTTP 或外部直连时，不问用户，默认使用 HZERO/project request helper。

question：
- 标题：`请求方式`
- 问题：`当前资料提到原生 HTTP / 外部直连。是否确认本页面允许绕过 HZERO request？`
- 选项：
  - `使用 HZERO request`：按项目 request helper、getEnvConfig 和服务前缀实现；nativeHttp.allowed=no。
  - `允许原生 HTTP`：必须记录原因、外部域名/API_HOST 策略、token/header/error/tenant/CSRF 处理和验证方式；nativeHttp.allowed=yes。
  - `回到契约补充`：补充接口或运行时配置资料后再判断。

记录要求：
- `serviceRequestContract.nativeHttp.confirmationSource`：user-question / requirement-doc。
- `serviceRequestContract.baseUrlStrategy`：request-adds-api-host / explicit-api-host-required / external-origin。
- `risk`：绕过 HZERO request 后的 token、错误处理、租户、跨域和验证风险。

### Mock Plugin Registration Confirm
适用场景：已进入或计划进入 `queryMode=mock-request`，且目标落点明确不是标准 HZERO/Umi 父工程托管形态，或用户显式要求偏离内置 mock plugin 注册链路。标准父工程托管 `packages/<module>` 不使用本 question。

默认策略：
- 父工程托管 `packages/<module>` 的 mock-request 注册是内置工程接线，不向用户确认。
- 默认直接规划父工程 `config/config.ts` 顶层 `plugins` 写入 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')`；若项目已有父工程聚合 plugin 且明确可复用，默认用 `require.resolve('./dev-mock-plugin')` 复用聚合 plugin。
- `package-start` / 子包独立启动按默认支持处理，必须同步规划 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`，即子模块 `config/config.ts` 通过 `extendParentConfig` 继承父工程同一 plugin；子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得重复注册该 plugin，不要先深度探索或要求用户确认是否支持 package-start。
- 以上文件必须进入 Design / Task 的 File Mapping、integration task 和 verification，不得只写“待确认”。

自动 backfill 条件：
- `parentMockPluginRegistrationEvidence=missing / invalid-packages-config / unknown`，且目标是标准 HZERO/Umi 父工程托管子模块。
- `parentRootMockPluginRegistration` 缺失，或 mock 接线只写了子模块自身 plugin、`packages-config` package 条目 `plugins` 字段，或只确认了 `.hzerorc` / `config/packages-config.js` 子模块包注册。
- 子模块 `config/config.ts` 未通过 `extendParentConfig` 继承父工程同一 mock plugin，或 `config/config.dev.ts` 重复注册 `../dev-mock/<module>-dev-mock-plugin`。
- 用户只确认了“接入 packages/<module> / 父工程包注册 / mock-request demo”，但未单独确认父工程 `config/config.ts` 顶层 `plugins` 的 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')` 或父工程聚合 plugin 的 `require.resolve('./dev-mock-plugin')` 写入方式；这属于自动补接线信号，不是提问触发条件。

需要提问条件：
- 目标明确不是标准 HZERO/Umi 父工程托管子模块，且无法套用内置父工程 `config/config.ts` 顶层 plugin 注册。
- 用户显式要求偏离父工程 `config/config.ts` 顶层 plugin 注册或子模块 `config/config.ts` 继承父 plugin。
- 父工程配置不在已确认写入范围，或需要扩大写入范围；此时优先使用 Write Scope Confirm。
- dirty/conflict、只读/锁定文件或外部改动影响当前注册。
- 项目证据显示该工程不是标准 HZERO/Umi 目标，无法按内置规则生成。

不适用：
- 独立非父工程项目无 parent config，且已有项目等价根 devServer plugin 入口；记录 `parentMockPluginRegistrationEvidence=not-applicable + reason`。
- `queryMode` 不是 `mock-request`，或本轮不是可运行数据页面且完全无 runtime request。

question：
- 标题：`Mock插件注册`
- 问题：`当前 mock demo 需要把子模块 mock plugin 接入父工程 dev server。请选择注册方式。`
- 选项：
  - `父工程直接注册`：在父工程 `config/config.ts` 顶层 `plugins` 写入 `require.resolve('../packages/<package>/dev-mock/<module>-dev-mock-plugin')`，同时确认子模块 `config/config.ts` 通过 `extendParentConfig` 继承父 plugin；除非用户或目标工程文档明确禁止 package-start，否则 package-start 继承证据不得标记为不适用。
  - `父工程聚合注册`：在父工程新增或复用聚合 plugin，由父工程 `config/config.ts` 顶层 `plugins` 写入 `require.resolve('./dev-mock-plugin')` 注册聚合 plugin，再由聚合 plugin 引用子模块 mock handler；适合多个子模块共享父工程 mock 接入口。
  - `暂停补注册方案`：本轮不进入 runnable mock 实现；回到 Frontend Design / Contract Check / Task Breakdown 补工程证据或注册方案。

记录要求：
- `questionGate.template=Mock Plugin Registration Confirm`。
- `parentRootMockPluginRegistrationConfirmationSource=user-question`。
- `parentRootMockPluginRegistration`：parent config/config.ts plugins -> submodule plugin / parent config/config.ts plugins -> aggregator / blocked。
- `parentMockPluginRegistrationEvidence`：standard-generated / parent config/config.ts top-level plugins confirmed / parent aggregator standard-generated / parent aggregator confirmed / invalid-packages-config。
- `packageStartMockPluginSource`：parent-config-inherited-by-extendParentConfig / missing / not-applicable，并写明子模块 `config/config.ts` 继承证据。
- `mockPluginTemplateCompliance`：submodule-dev-mock-plugin-template / parent-aggregator-template / unknown。
- `mockPrefixOriginPolicy`：current-dev-server-origin / unknown；本 question 只确认 plugin 注册，不替代 request origin 验证。
- 本 question 未 resolved 前，阻塞 Design Confirm / Task Breakdown / runnable Implementation；不得用 “父工程包注册已确认” 或 `packages-config` package 条目替代。

### Import Component Mode Confirm
适用场景：Frontend Design 识别到导入能力，且标准导入入口无法自动承接或存在组件模式风险。普通 demo-slice / `minimum-codable + default-mock-demo` 默认使用 HZERO 标准导入入口自动承接，不触发本 question。

强制调用条件：
- 用户、需求、FDS/TDS、后端 handoff 或主流程明确要求 production-complete / production-ready，且导入能力需要作为生产闭合能力交付。
- 目标项目或目标模块存在 confirmed current import wrapper 或 custom 外壳，并且需要在标准导入入口与当前版项目封装之间做模式选择。
- 用户、FDS/TDS 或项目证据拒绝标准导入入口、要求自定义外壳，或与标准 `Import` 抽屉入口冲突。
- 参数结构、入口路径或 wrapper/exportShape 冲突导致无法形成可实例化标准候选，且会影响组件模式选择。
- 命中本 question 时，Frontend Design 只生成并预检完整 `questionGateQueue[].questionToolPayload`，由 Lite / 外层 question owner 原样调用并回传 `questionReceipt`；Design 不得直接调用 question，也不得只输出 `suggestedQuestionTemplate` 后继续。外层 question 工具不可用或调用失败时记录 `question-unavailable`，并停止在 `needs-user`，不得进入 Task / Implementation。

不适用：
- 用户或需求已明确本轮不包含导入能力时，不触发本 question；在 Contract Check 中把导入写为 `not-applicable + reason`。
- `minimum-codable + default-mock-demo` 或普通 demo-slice 可用 HZERO 标准导入入口自动承接时，不触发本 question；记录 `importComponentMode=drawer-component`、`importComponentModeSource=designAutoResolution`、`designAutoResolution=standard-import-export-direct`、`entryWrapperPolicy=standard-component-direct`。缺少 templateCode/importCode、prefixPath/action/uploadEndpoint、tenantContext、权限或运行验证证据时，用 generatedCandidate / mockOnly 承接并写入 Contract Check / Verification / Handoff，不因此提问组件模式。
- 当前无法确认任何可实例化标准入口所需的 component/importPath、templateCode/importCode、prefixPath/action/uploadEndpoint 时，不用“暂不实现导入”让用户选择；应先走 Missing Contract / 补导入契约。若仍进入代码生成，只能生成 `Import` 的 generatedCandidate 入口，并把缺口写入 Contract Check、Verification、Handoff 和生产替换项。

question：
- 标题：`导入模式`
- 问题：`当前页面包含导入能力。请选择通用导入组件的入口模式。`
- 动态选项规则：
  - 选项只能来自已确认可执行的入口类型。未在目标前端项目或目标模块中探索到相似页面、封装组件源码、类型声明或可复用 wrapper 合同前，不得展示“项目既有导入封装 / 项目 wrapper / 自定义封装”类选项，也不得把它写入候选说明。
  - 若探索到 confirmed import wrapper，才可追加 `项目既有导入封装` 选项；该选项必须展示 evidence path、wrapper importPath、props 合同、权限策略、请求构造和不削弱 `front-hzero-import-export` owner 规则的证据。
  - 未探索到 current wrapper 时只展示 `新版抽屉`；wrapper 缺失不是阻塞项，按 HZERO 标准 `Import` 坐标继续设计。
- 选项：
  - `新版抽屉`：使用新版通用导入组件，以当前页面内抽屉或弹层方式完成模板下载、上传、结果反馈和错误明细查看；适合新生成页面和生产化页面，能保留当前查询上下文，关闭后可直接刷新当前列表。设计需记录组件 import / wrapper 证据、templateCode/importCode、prefixPath/action/uploadEndpoint、drawer 生命周期、关闭后刷新列表和验证清单。
  - `项目既有导入封装`（仅当 `confirmed import wrapper` 证据存在时展示）：技术映射 `importComponentMode=drawer-component`、`entryWrapperPolicy=project-wrapper`。使用目标项目或目标模块已有且适用于当前业务的导入 wrapper；必须记录封装组件路径、props 合同、内部标准组件或路由页能力、权限控制、模板/上传请求构造、租户策略和 legacy 风险。没有 confirmed wrapper 证据时，本选项不得出现在 question 中。

记录要求：
- `importComponentMode`：`drawer-component` / `project-wrapper` / `missing` / `not-applicable`。
- `missing` / `not-applicable` 是 Contract Check 或前置判定状态，不是本 question 的用户可选项；`missing` 必须转 Missing Contract / 补导入契约，`not-applicable` 表示本轮不包含导入能力。
- `importComponentModeSource`：`user-question` / `designAutoResolution`；requirement-doc / project-evidence / generatedCandidate 只能写入 recommendationEvidence。
- `recommendationEvidence`：requirement-doc / project-evidence / generatedCandidate / SOP default。
- `entryWrapperPolicy`：默认 `standard-component-direct`。`新版抽屉` 表示使用 `Import` 自身的抽屉/弹层生命周期，或使用 confirmed current wrapper；不得再塞进自建 `Modal` / `Drawer` / `children` 外壳。只有用户明确要求、需求/FDS/TDS/Figma 明确指定或项目已有 current wrapper 证据时，才允许 `project-wrapper` / `custom-modal-confirmed`，并必须记录 `entryWrapperEvidence`。
- `importComponentContract`：
  - 新版抽屉：component / importPath / wrapperEvidence / drawerOpenAction / status。
- `importFlowContract`：
  - component / importPath / wrapperEvidence。
  - templateCode / importCode。
  - prefixPath / action / uploadEndpoint。
  - requestParams / paramPlacement：query / path / body / formData / customData / search / state。
  - templateDownload：endpoint / static file / platform template / not-applicable。
  - tenantContext / permissionCode。
  - resultHandling：sync / async / polling / task center / not-applicable。
  - errorDetailDownload：endpoint / fileId / message list / not-applicable。
  - closeRefreshPolicy / backPath。
  - `status`：confirmed / generatedCandidate / partial / missing / conflict / not-applicable。
- `questionGate.template=Import Component Mode Confirm`，未 resolved 前阻塞 Task / Implementation。
- 只确认入口模式但缺 templateCode/importCode/prefixPath/action/uploadEndpoint 等业务参数时，必须补导入契约或标记 generatedCandidate / missing，但不得因此把入口模式标为 blocked 或把导入按钮实现为空壳。若进入代码生成，入口仍必须是 `Import`，缺失参数用 mock/generatedCandidate 候选值先形成可实例化组件，并把来源未确认写入 Contract Check / verification / handoff。只缺结果反馈、错误明细、关闭刷新、运行时权限或后端可用性验证时，可进入标准入口实现，并把缺口写入 verification / handoff。

### Export Component Mode Confirm
适用场景：Frontend Design 识别到导出能力，且标准导出入口无法自动承接或存在组件模式风险。普通 demo-slice / `minimum-codable + default-mock-demo` 默认使用 HZERO 标准导出入口自动承接，不触发本 question。

强制调用条件：
- 用户、需求、FDS/TDS、后端 handoff 或主流程明确要求 production-complete / production-ready，且导出能力需要作为生产闭合能力交付。
- 目标项目或目标模块存在 confirmed current export wrapper 或 custom 外壳，并且需要在 `ExcelExportPro` 与当前版项目封装之间做模式选择。
- 用户、FDS/TDS 或项目证据拒绝标准导出入口、要求自定义外壳，或与标准 `ExcelExportPro` 入口冲突。
- 参数结构、导出请求协议或 wrapper/exportShape 冲突导致无法形成可实例化标准候选，且会影响组件模式选择。
- 命中本 question 时，Frontend Design 只生成并预检完整 `questionGateQueue[].questionToolPayload`，由 Lite / 外层 question owner 原样调用并回传 `questionReceipt`；Design 不得直接调用 question，也不得只输出 `suggestedQuestionTemplate` 后继续。外层 question 工具不可用或调用失败时记录 `question-unavailable`，并停止在 `needs-user`，不得进入 Task / Implementation。

不适用：
- 用户或需求已明确本轮不包含导出能力时，不触发本 question；在 Contract Check 中把导出写为 `not-applicable + reason`。
- `minimum-codable + default-mock-demo` 或普通 demo-slice 可用 HZERO 标准导出入口自动承接时，不触发本 question；记录 `exportComponentMode=pro-component`、`exportComponentModeSource=designAutoResolution`、`designAutoResolution=standard-import-export-direct`、`entryWrapperPolicy=standard-component-direct`。缺少 requestUrl/exportRequest、endpoint/templateCode、tenantContext、权限、query/export 参数或运行验证证据时，用 generatedCandidate / mockOnly 承接并写入 Contract Check / Verification / Handoff，不因此提问组件模式。
- 当前无法确认标准导出组件/importPath 与可调用 endpoint/导出模板等事实时，不用“暂不实现导出”让用户选择；应先走 Missing Contract / 补导出契约。若仍进入代码生成，只能生成 `ExcelExportPro` / confirmed current wrapper 的 generatedCandidate 入口，并把缺口写入 Contract Check、Verification、Handoff 和生产替换项。

question：
- 标题：`导出模式`
- 问题：`当前页面包含导出能力，但导出组件模式尚未确认。请选择导出入口的实现方式。`
- 动态选项规则：
  - 选项只能来自已确认可执行的入口类型。未在目标前端项目或目标模块中探索到相似页面、封装组件源码、类型声明或可复用 wrapper 合同前，不得展示 `项目既有导出封装`、`项目 wrapper` 或等价封装选项，也不得把它写入候选说明。
  - `项目既有导出封装` 只有在 confirmed export wrapper 证据存在时才展示；证据必须至少覆盖相邻页面用法或封装源码、wrapper importPath、props 合同、权限策略、requestBuilder / queryParams 策略、文件名和租户策略。
  - 未探索到 current wrapper 时只展示 `新版导出组件`；wrapper 缺失不是阻塞项，按 HZERO 标准 `ExcelExportPro` 坐标继续设计。
- 选项：
  - `新版导出组件`：技术映射 `exportComponentMode=pro-component`。使用 `ExcelExportPro` 或 confirmed current wrapper。导出参数必须来自当前查询条件、租户上下文、业务筛选条件和已确认导出接口契约；需要同步确认权限码、endpoint/method/params、文件名规则、是否支持勾选行导出、是否包含当前筛选条件。
  - `项目既有导出封装`（仅当 `confirmed current export wrapper` 证据存在时展示）：技术映射 `exportComponentMode=project-wrapper`。wrapper 必须证明内部使用 `ExcelExportPro` 并保留权限、参数、文件名、租户和国际化合同；内部仍使用旧 `ExcelExport` 时不得展示本选项，只能生成迁移 finding。

记录要求：
- `exportComponentMode`：`pro-component` / `project-wrapper` / `missing` / `blocked` / `not-applicable`。
- `missing` / `blocked` / `not-applicable` 是 Contract Check 或前置判定状态，不是本 question 的用户可选项；`missing/blocked` 必须转 Missing Contract / 补导出契约，`not-applicable` 表示本轮不包含导出能力。
- `exportComponentModeSource`：`user-question` / `designAutoResolution`；requirement-doc / project-evidence / generatedCandidate 只能写入 recommendationEvidence。
- `recommendationEvidence`：requirement-doc / project-evidence / generatedCandidate / SOP default。
- `entryWrapperPolicy`：默认 `standard-component-direct`。`新版导出组件` 表示直接使用 `ExcelExportPro` 或 confirmed current wrapper 的入口与组件内置弹层能力；不得再塞进自建 `Modal` / `Drawer` / `children` 外壳。只有用户明确要求、需求/FDS/TDS/Figma 明确指定或项目已有 current wrapper 证据时，才允许 `project-wrapper` / `custom-modal-confirmed`，并必须记录 `entryWrapperEvidence`。
- `exportComponentContract`：
  - 新版导出：component / importPath / wrapperEvidence / queryFormItemExtra / modalProps / defaultFileType / exportAsync / status。
  - 项目既有导出封装：component / importPath / wrapperEvidence / internalComponent(pro/legacy/unknown) / propsContract / permissionPolicy / requestBuilder / fileNamePolicy / tenantContextPolicy / legacyRisk / status。
  - 旧版导出：component / importPath / wrapperEvidence / queryFormItem / defaultConfig / defaultSelectAll / exportAsync / status。
- `exportRequestContract`：
  - `columnQueryRequest`：url / method / query / path / body / customData / templateCode / status。
  - `exportRequest`：url / method / query / path / body / customData / templateCode / status。
  - `queryParamsTypePolicy`：same / split by `type=query|export` / custom / not-applicable。
  - `paramPlacement`：query / path / body / customData。
  - `queryColumnProps` / `allBody` / `fakePost`。
  - `extraConditions` / `fileConfig` / `selectedColumns` / `defaultFileType` / `exportAsync`。
  - `status`：confirmed / generatedCandidate / partial / missing / conflict / not-applicable。
- `questionGate.template=Export Component Mode Confirm`，未 resolved 前阻塞 Task / Implementation。
- 只确认组件版本但缺可调用 endpoint/导出模板等业务参数时，必须补导出契约或标记 generatedCandidate / missing，但不得因此把入口模式标为 blocked 或把导出按钮实现为只传列表查询参数的下载入口。若进入代码生成，入口仍必须是 `ExcelExportPro` / confirmed current wrapper，缺失参数用 mock/generatedCandidate 候选值先形成可实例化组件。只缺两阶段参数细节、异步结果、文件格式、运行时权限或后端可用性验证时，可进入标准入口实现，并把缺口写入 verification / handoff。

## Missing Contract Confirm
适用场景：字段、接口、路由菜单、权限、LOV/lookup、附件、导入导出或验证目标缺失。

优先边界：本模板只处理阻塞当前 Mock demo 的契约缺口。production-ready 或真实 API 目标本身不触发本 question；前端设计继续默认 Mock，真实 API 首次试连交给独立 `hzero-local-integration-test`。生产专属缺口只输出 advisory，不要求用户在此选择替换方式。

强制调用条件：
- Contract Check / Frontend Design 发现当前 Mock demo 必需契约为 `missing / conflict`，且无法按内置候选或标准 Mock 接线补齐。
- 新增或改造可运行前端页面固定走 `mock request demo`。标准 Mock 接线必须自动 backfill，不因缺历史证据或用户要求真实 API/production-ready触发本 question；只有接线与目标工程冲突或不可写时才提问。
- 有参考子模块、相似页面、可复用 DataSet/service 写法、Mock 插件注册样例时，这些 evidence 只能作为后续 Mock API Contract 输入。无参考模块、参考资产缺失/不可读、启用 `hzerojs-asset-baseline` 或 asset baseline 时同样默认进入 mock request demo；baseline/generatedCandidate 不能确认生产契约或真实远端请求。
- FSS/API/Swagger 只证明 documented，不证明服务可用。可运行页面始终进入 Mock demo 并记录独立集成 advisory；不得以文档完整或用户要求真实 API为由进入 `production-transport`。
- 前端设计发生在后端部署/联调前时，始终进入 requestable Mock demo；后端 readiness 和生产缺口只写 advisory，不触发真实契约 question。
- `generatedCandidate` 不是用户交付路径选项。候选 route/menu/permission/i18n/lov/servicePrefix/API path 只能作为所选路径的候选值；不得因为用户允许候选编码或设计生成了候选 servicePrefix/API path，就直接判定 `queryMode=production-transport`、`mockDemoDecisionStatus=not-applicable` 或请求远端 `API_HOST`。
- 设计阶段确认不能替代真实 API 接入；production-ready/真实 API 目标进入后续独立集成，不触发当前 `Missing Contract Confirm`。
- 系统自动采用可请求 Mock demo；用户真实 API/production-ready目标不改变该路径。Mock 工程接线缺失时自动 backfill；只有写入范围、dirty/conflict/只读锁或非标准工程冲突才进入 gate。
- `mockDemoDecisionStatus=default-mock-demo` 是可运行数据页面固定状态；`unknown / denied` 只用于历史输入迁移。
- `mockDemoDecisionStatus=not-applicable` 只能用于非可运行页面或完全不涉及 DataSet/service/API/transport，并必须写 reason。

禁止只在普通输出中写“待确认”“请补充资料”后继续进入 runnable code；当前环境有 question 工具且存在未解决 question gate 时，必须调用 question。若 question 工具不可用，必须输出 `question-unavailable`，并停止在 `needs-user`。本条不适用于已满足默认 mock demo 自动确认条件的路径；自动确认必须记录 `designConfirmationSource=default-mock-demo-policy`，不得自行选择真实 API 或 production-ready。
禁止把“只做静态骨架 / 只做非 runnable 方案 / 空页面占位”作为用户可选择的继续路径。无真实 API 时默认走可请求 mock demo；若连可请求 mock 数据契约或 mock 工程接线也无法形成，正确动作是暂停并补齐契约或工程接线证据，不得把低价值结构占位包装成设计确认、Task Breakdown 或 Implementation 入口。
禁止生成“本轮运行契约目标 / 请选择先 Mock Demo 还是生产就绪”这类 question。默认 mock demo 是系统 fallback，不是用户选择项；只读分析只在用户明确要求“先分析/先看一下/不改代码”时作为流程范围状态记录，不得混入运行契约目标选项。

question：
- 标题：`补契约`
- 问题：`当前 Mock demo 的必要契约或工程接线仍有缺口。请选择处理方式。`
- 选项排序规则：本 question 不询问是否采用 Mock demo或切真实 API；只根据当前 Mock 缺口展示补契约或暂停。
- 选项：
  - `补真实契约`：用户提供当前 Mock demo 仍需要的 PRD、接口形态、菜单权限、附件/导入导出协议或路径；不授权真实 API 试连。
  - `暂停补契约`：不进入 Task Breakdown / Implementation / Verify / Handoff；只记录 Contract Check 缺口、填写提示和下一步资料清单。
- 选项标题必须严格使用以上两项；描述必须写清选择后的流程后果、可进入或阻塞的阶段、生产就绪边界和需要用户补充的资料类型，不得只写“继续实现 / 使用候选 / 先 mock”。不得改写为 `按候选实现`、`按 generatedCandidate/partial 实现`、`先 Mock Demo`、`仅 mock demo`、`只做分析` 或其它会把默认 fallback、只读范围、`generatedCandidate/partial` 包装成用户交付路径的文案。候选编码只能作为所选路径下的实现边界和 replacement 项，不能成为单独选项。

记录要求：
- `contractGapConfirmationSource`：user-question / question-unavailable / requirement-doc。
- `mockDemoDecisionStatus`：default-mock-demo / denied / not-applicable。
- `selectedPath`：real-contract / pause-for-contract；未触发本 question 且按默认 mock demo 自动推进时，可在阶段结果记录 `selectedPath=not-asked-default-mock-demo`。
- `runtimeDataPathDecision`：real-contract / requestable-demo-mock / pause-for-contract / not-applicable + reason。
- `queryModeAfterDecision`：production-transport / mock-request / blocked / partial。
- `remoteBackendRequestAuthorization`：企业前端编排固定 `not-applicable + independent-integration-stage`；不得由本 question 写 confirmed。
- `allowedFrontendExecutionMode`：production-ready-blocked / demo-slice / contract-blocked。
- `productionReplacementRequired`：yes / no / not-applicable + reason。
- `questionGate`：
  - `required`: true before confirmation, false or resolved after confirmation.
  - `template`: Missing Contract Confirm.
  - `reason`: contract-missing / mock-demo-authorization-unknown / production-contract-partial / other.
  - `blockingStages`: TASK / IMPLEMENTATION / VERIFY / ARTIFACT / DONE as applicable.
  - `allowedNext`: user-question / contract-check / frontend-design / demo-slice.
  - `resolved`: true only after user-question or explicit requirement-doc confirmation.
  - `resolutionSource`: user-question / requirement-doc / not-applicable / null.

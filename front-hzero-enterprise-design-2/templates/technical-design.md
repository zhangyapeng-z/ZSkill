# 前端技术设计文档模板
<!-- frontend-design-canonical-ref: {"stateId":"<stateId>","statePath":"design/design-canonical-state.json","contractFreezeId":"<contractFreezeId>","projection":"<ready-for-task|needs-user|blocked>"} -->
适用：页面交付 / demo-slice / mock-demo / production-ready 前端交付统一使用本模板。复杂度差异不得通过 lite/full 模板分流解决；必须在本模板内补齐适用契约，不适用项写 `not-applicable + reason`，缺失、冲突或待确认项写入澄清或阻塞项。小范围 `regular-change` direct 可不生成前端设计文档，但必须在主流程或实现结果中记录跳过原因、目标文件、成功标准和验证方式。

## 适用章节矩阵

| 场景 | 必填 | 可简化 | 禁止省略 |
| --- | --- | --- | --- |
| 小范围 `regular-change` direct | 可不生成本文；必须在主流程或实现结果中记录目标文件、成功标准、验证方式和跳过原因 | Contract Check、UI Contract 可写 `not-applicable + reason` | 不得新增或改变 API、字段、权限、路由菜单、LOV/lookup、附件、导入导出、tenantContext、production-ready 判断 |
| 页面交付 `regular-change` | 文档状态、设计输入、Feature Workspace、Contract Check 结论、Design Coverage Ledger、Frontend Design Handoff Metadata、目录结构、数据层设计、UI Contract、页面区域 checklist、候选编码、validationHandoff、确认摘要 | 导入、导出、附件、mock/demo、Figma、子模块落点按需求写 `not-applicable + reason` | route/menu/permission/i18n 状态、routeOpenMode、Target Placement、serviceRequestContract、关键字段和接口状态 |
| 高风险 / 多模块 / 严格门禁 | 本模板全量适用；需要补齐 Design Coverage Ledger、Target Placement、Backend Asset Coverage、serviceRequestContract、tenantContext、ID runtime、UI Contract、导入导出附件、validationHandoff 和风险项 | 无关能力可逐项 `not-applicable + reason` | 关键生产契约、写入边界、子模块注册、routeContext/editMode、validationHandoff |
| mock-demo / demo-slice | Contract Check、Mock API Contract、Design Coverage Ledger、UI Contract、候选编码、Production Replacement Draft、validationHandoff | production API 可为 partial/missing，但必须进入替换草稿 | 不得把 mock/local 成功路径写成 production-ready；不得把 generatedCandidate 写成 confirmed |
| production-ready | Contract Check 关键项 confirmed 或 `not-applicable + reason`；Review/Verify/Handoff 继承本设计要求 | 无 | partial/generatedCandidate/missing/conflict 不得升级为生产闭合；API URL/method、bucket、templateCode 不得凭命名生成 confirmed 生产事实，导入导出标准组件的 mock/generatedCandidate 参数候选必须标明未确认 |

## 文档状态
- 设计结论：设计文档已形成 / 设计输入不足
- 当前标准链路阶段：Frontend Design
- 模板类型：standard
- 是否可进入 Task Breakdown：是 / 否；原因：
- 是否可进入 Implementation：是 / 否；原因：
- 设计确认状态：draft / 待人确认 / 已确认 / auto-confirmed-for-demo / blocked-by-contract
- frontendDesignState / designCompletenessPolicy / firstPassDesignStatus / targetedEvidenceBackfillUsed / designConfirmationSource：见下方状态机与 First-pass Completeness Policy
- designInputPreflightStatus：pass / partial / failed + reason
- standardPageProfile：HZEROJS_SUBMODULE_MASTER_DETAIL_MOCK_REQUEST / custom / not-applicable
- designAutoResolution：standard-profile-defaults / standard-import-export-direct / standard-import-direct / standard-export-direct / none + reason

## Frontend Design State Machine
本节是阶段推进的人类可读 projection。唯一机器事实源是 `design/design-canonical-state.json`；本文不得独立覆盖其状态。

| state | 进入条件 | 允许下一步 | 禁止动作 |
| --- | --- | --- | --- |
| draft | 已进入 Frontend Design，但 Contract Check、Design Coverage Ledger、UI Contract、Target Placement 或设计闭合清单尚未完成 | 继续补设计 / Contract Check / Evidence | Design Confirm / Task Breakdown / Implementation |
| needs-user | 存在需用户或上游确认的 `questionGate`、`questionGateQueue`、generatedCandidate、targetPlacement 或 UI/契约歧义 | 用户确认 / Lite 统一确认 / 回 Contract Check | 自行升级 confirmed / runnable Implementation |
| blocked-by-contract | 缺少功能文档、接口列表、关键 API、字段、权限、routeOpenMode、detailViewInteractionMap、tenantContext、serviceRequestContract、Target Placement 或生产必需契约 | 补契约 / 回 Frontend Design；仅工程证据缺口使用 targeted evidence backfill | production-ready / Task Breakdown / Implementation |
| ready-for-design-confirm | `frontend-design.md`、`contract-check.md`、适用的澄清和合规产物已文件化，FD-G1~FD-G10 Refine Loop 无剩余阻塞；若满足默认 mock demo / minimum-codable 自动确认条件，可由 Lite / primary 直接转 `confirmed` | Design Confirm / auto-confirm-for-demo / Task Breakdown | 直接 Implementation |
| confirmed | Lite 或 primary 已记录 `designConfirmationSource=user-question/default-mock-demo-policy`，用户确认具备合法 questionReceipt，且无未解决阻塞门禁 | Task Breakdown | 跳过 Task Breakdown 直接编码，除非小范围 `regular-change` direct 合法例外 |

- currentState：同 frontendDesignState（draft / needs-user / blocked-by-contract / ready-for-design-confirm / confirmed）
- previousState：
- transitionReason：
- questionGateState：required=false / resolved=true / unresolved / not-applicable + reason
- progressionDecision：`wait-user` 仅用于 `designState=needs-user + required pending question gate`；`blocked` 仅用于 `designState=blocked + blockers[] 非空`；`allow-task-dispatch` 仅用于 `designState=ready-for-task + readyForTaskDispatch=true + required question gate 全闭合 + canonical validator passed`。`ready-for-design-confirm / auto-confirmed-for-demo / confirmed` 只是 `frontendDesignState` 人类可读 projection，不得作为机器推进值。
- nextAllowedStage：Frontend Design / Contract Check / Design Confirm / auto-confirm-for-demo / Task Breakdown / blocked

## First-pass Completeness Policy
本节决定初次设计不全时如何推进。Design 的目标是首轮形成可编码骨架和完整缺口分类，不是把所有事项都升级为 confirmed。

- firstPassDesignStatus：complete-skeleton / needs-targeted-backfill / blocked
- targetedEvidenceBackfillScope / targetedEvidenceBackfillAttemptCount：none 或 target-placement / project-directory / similar-page / scripts / component-import / package-route-mock-entry；0 / 1
- mandatorySelfCheckStatus：pass / failed + reason
- sourceInventoryStatus：pass / missing + source
- coverageConservationStatus：pass / failed + missingLedgerIds
- blockingGateStatus：clear / blocked + reason
- refineBudgetPolicy：single closeout for minimum-codable; additional refine only for production-complete / high-risk / explicit-full-closure

| gapClass | 典型事项 | Design 处理 | 下游承接 |
| --- | --- | --- | --- |
| blocking | 前端工程/落点不明、Target Placement 冲突、影响当前 Mock demo 的关键业务契约冲突、Mock 接线无法形成、写入范围不可判定 | `frontendDesignState=needs-user/blocked-by-contract`，不得进入 Task Breakdown | 用户确认 / Contract backfill |
| generatedCandidate | route/menu、权限码、i18n key、LOV/lookup code、附件 bucket/template、导入导出参数、servicePrefix 候选 | 写候选值、来源规则、replacementRequired 和验证门禁；不得写 confirmed | Task 可拆 runnable demo/mock 或候选实现；Handoff 保留 replacement |
| verification | dev server、browser、账号、测试数据、Network 可达性、运行态性能 | 写入 Verification checklist；不阻塞 Design | Verify 只记录 not-run / external-evidence / conditional；不启动服务或浏览器 |
| not-applicable | 本轮明确不涉及的能力 | 写 source reason | 不进入任务 |

规则：`minimum-codable` 可进入 Task Breakdown 的前提是 blocking 类为空、Design Coverage Ledger 已覆盖 required 项并给出 taskMappingPolicy、候选/验证类缺口都有下游承接，且 `mandatorySelfCheckStatus=pass`。`production-complete` 必须把关键生产契约 confirmed 或 `not-applicable + reason`；`blocked` 只能返回确认或补契约。轮次预算不能替代自检，任何 required 项未进 ledger 或未分类都不得放行。

## Design Cumulative Fallback Matrix
本节记录设计阶段所有降级/继续状态。它们是累积状态，不是串行阶段、互斥选择或短路条件；任何一项存在都必须继续检查其它项，不能把一个状态当成另一个状态的 resolved/confirmed 证据。

- designCumulativeFallbackPolicy：cumulative-no-short-circuit
- fallbackStates：assetBaseline / generatedCandidate / defaultMockDemo / figmaFallback / needs-user / blocked-by-contract / productionReplacement / questionGateQueue
- fallbackShortCircuitCheck：pass / failed + reason

| fallbackState | 可承接内容 | 不能关闭的事项 | 下游策略 |
| --- | --- | --- | --- |
| assetBaseline | HZEROJS 空项目、参考资产缺失/不可读或无可采纳参考模块时的标准形态、目录和组件基线 | 业务事实、Target Placement、Open Interaction、导入导出模式、LOV/lookup、附件 bucket、templateCode、tenantContext、servicePrefix、backend readiness | 继续 Contract Check，并把未解决项写入 `questionGateQueue[]` |
| generatedCandidate | route/menu/permission/i18n/lov/servicePrefix/API path 等可按规则生成的候选值 | `confirmed` 契约、生产请求授权、可达性、LOV/权限/菜单登记 | 保留候选来源和确认人；route/menu 可按规则生成候选并进入 mock/demo，production confirmed 必须来自用户、平台菜单资产或明确 routeConfig/platform evidence，未确认项不得进入 production-ready |
| defaultMockDemo | Frontend Design 入口默认的可请求 mock/demo 路径 | 生产 API、后端 readiness、Figma 视觉、目标落点、交互形态、导入导出/附件/LOV/tenantContext 的生产事实 | 只允许 demo/mock；必须保留 replacement、verification 和 handoff 风险 |
| figma-unverified / screenshot-only / cache-only | 视觉证据降级和视觉风险留痕 | 业务契约、接口、权限、状态流转、LOV/lookup、附件、导入导出、运行态请求 | 可继续非视觉阻塞项；视觉 confirmed 前不得声明 layout confirmed |
| needs-user | 聚合需用户或上游确认的问题 | 任一事实缺口或阶段门禁 | 写入 `questionGate`/`questionGateQueue`；未 resolved 不进入 runnable Task / Implementation |
| blocked-by-contract | 契约不足、冲突或生产必需事实缺失 | Design Confirm、production-ready、runnable Task / Implementation | 只能补契约、回设计或拆 backfill-only 任务 |
| productionReplacement | mock/demo、临时契约、generatedCandidate 或待替换项的生产替换债务 | 生产闭合、验证通过或交付验收 | 继承到 Task / Verify / Handoff，不得当作通过依据 |
| questionGateQueue | 多门禁完整队列和提问顺序 | 其它未列门禁、首个 gate 以外的门禁 | 任一 unresolved 都阻塞对应下游阶段 |

## Design Coverage Ledger
机器事实源固定为同目录 `design-coverage-ledger.json`；本节是其人类可读 projection，标题、编号和排版不参与业务门禁。设计闭合清单可以解释需求，后续阶段必须消费机器台账进行机械对账，不得从 Markdown 标题另起一套覆盖口径。

| ledgerId | sourceRef | requirement | requirementType | uiRegion | pageMode | contractRefs | expectedCodeSurface | expectedSurface | forbiddenSurface | requiredVisibleByDefault | acceptance | negativeAcceptance | verificationMethod | required | status | taskMappingPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DCL-001 | FDS/TDS/Figma/user/evidence path#line |  | field / action / query / table-column / detail-section / layout-container / line-filter / table-toolbar / route-behavior / save-redirect / permission / i18n / mock / replacement / other | page-header / header-form / basic-info / list-query / list-toolbar / table / row-action / detail-tabs / line-filter / line-table / table-toolbar / modal-footer / route / service / other | create / edit / copy / detail / list / approval / readonly / mixed / not-applicable | Field Usage Matrix / Action Entry Matrix / Button Semantic Matrix / List Query Contract / Detail Contract / Detail Collection Contract / Route Context / Status Action Matrix / serviceRequestContract / productionReplacement | file/component/DataSet/service/route/mock/handoff target | Content / Header children / Table.buttons / Tabs.TabPane / Modal.open / not-applicable | forbidden parent/container/surface or not-applicable | yes / no / not-applicable + source |  |  | static-review / browser-manual / network / command / not-applicable | yes / no | confirmed / generatedCandidate / missing / conflict / blocked / not-applicable | must-map-to-task / backfill-only / replacement-only / no-code + reason |

规则：
- `required=yes` 的台账行必须有 `acceptance` 和 `negativeAcceptance`；没有拒收条件的 required 行不得进入 Task Breakdown。
- 详情/主从页至少要覆盖：Header 表单字段、字段可编辑/只读策略、审计/后端生成字段展示策略、页面按钮和状态动作、撤回/提交/取消/作废/删除等动作入口、明细 Tab、明细筛选区、明细工具栏、明细行操作、保存后路由/URL/Tab 行为；FDS/TDS/Figma/用户确认出现 `组件类型：标签页`、`标签内组件`、`显示在某标签内`、Drawer、Modal、折叠面板或其它容器承载语义时，必须按来源容器名生成 `requirementType=layout-container` 行，并把来源子组件再生成对应业务行。
- 列表页至少要覆盖：查询区字段、顶部 fuzzy search、页面工具栏、表格列、行操作列、分页/刷新/重置行为。
- `status=not-applicable` 必须写 source reason；不能用“不做”省略来自 FDS/TDS 的 required 能力。
- Task Breakdown 必须逐行继承本台账并填写 task 映射；Review 必须按本台账输出覆盖矩阵。

## Design Understanding Deviation Check
用于捕获设计理解偏差，尤其是 Figma 与 FDS/TDS/API 冲突、后端 TDS UI hint 被误当 confirmed、相似页面坏范式被复用、Figma 可见文案被误当业务契约、用户“新标签页/子模块”等歧义被过度推断。

- designUnderstandingDeviationCheck：

| item | suspectedDeviation | conflictingSources | decision | questionGate | downstreamImpact |
| --- | --- | --- | --- | --- | --- |
|  | none / possible / confirmed | FDS / TDS / API / Figma / PageSchema / Evidence / user / similarPage | follow-layout / follow-business / generatedCandidate / needs-question / blocked / rejected | template / resolved / reason | Design Confirm / Task Breakdown / Implementation / Verification / Handoff |

规则：
- 无偏差时写 `none + checked sources`，不得省略本节。
- 仅来自后端 TDS 的 UI 布局、组件选型、字段顺序或弹层形态，最高只能写 `generatedCandidate / partial`。
- Figma/PageSchema 只确认布局和视觉呈现；业务能力、接口、权限、状态流转、LOV/lookup、附件、导入导出和生产请求契约必须回到 FDS/TDS/API/用户确认。
- 相似页面证据为 `legacy-risk / anti-pattern / unknown-quality` 时，只能进入 `rejectedPatternItems` 或 needs-question，不得作为 confirmed 设计依据。
- 偏差影响业务能力、生产契约或详情打开方式时，必须触发 `questionGate` 或写 `blocked-by-contract`。

## 设计输入
- 功能文档来源：
- 接口列表来源：
- 页面或交互资料来源：
- 后端资产来源：
- Figma/PageSchema 路径：
- 输入缺口：

## Feature Workspace
- featureName：
- featureSlug：
- featureRoot：`sdd-workspace/changes/{change-id}/`
- frontendRoot：`sdd-workspace/changes/{change-id}/frontend/`
- frontendIndexPath：`sdd-workspace/changes/{change-id}/frontend/index.md`
- frontendDesignRoot：`sdd-workspace/changes/{change-id}/frontend/design/`
- frontendDesignPath：`sdd-workspace/changes/{change-id}/frontend/design/frontend-design.md`
- contractCheckPath：`sdd-workspace/changes/{change-id}/frontend/design/contract-check.md`
- frontendClarificationsPath：`sdd-workspace/changes/{change-id}/frontend/design/frontend-clarifications.md` / `embedded` / `null + not-applicable reason`（仅存在需独立跟踪的 blocking/missing/conflict/needs-confirmation 项时独立生成）
- uiContractPath：并入 `frontend-design.md` / `sdd-workspace/changes/{change-id}/frontend/design/ui-contract.md`（复杂页面或内容过大时独立生成）
- productionReplacementDraft：`contract-check.md#Production Replacement Draft` / `sdd-workspace/changes/{change-id}/frontend/design/production-replacement-draft.md` / `not-applicable + reason`
- frontendEvidencePath：`sdd-workspace/changes/{change-id}/frontend/evidence/evidence.md` / `null + reason`
- engineeringExploration：engineeringExplorationRequired yes / no / null；engineeringExplorationLevel E1 minimal / E2 standard / E3 submodule / not-applicable
- engineeringEvidenceReuse：engineeringEvidenceSourcePath `frontend/evidence/evidence.md` / embedded-in-design / frontend-evidence-packet / missing + reason；engineeringEvidenceCoverage target-placement / directory-plan / route-menu-permission / component-import-map / enum-map / validator-commands / similar-page-quality / mock-request-path / partial + missingItems；engineeringExplorationReusePolicy task-reuse-only / targeted-delta-allowed / blocked-by-missing-evidence / not-applicable；targetedDeltaExploreScope none / target-placement / validator-command / mock-request-path / component-import-map / enum-map / similar-page-quality / file-mapping / changed-files-plan
- baselineComparisonStatus：not-needed / ready / partial / blocked / needs-confirmation
- targetPlacementStatus / targetPlacementEvidenceStatus / targetPlacementUserConfirmStatus：confirmed / generatedCandidate / ready / partial / missing / conflict / needs-confirmation / not-applicable
- enumImportMapStatus / componentImportMapStatus / componentApiProvenanceStatus / typescriptRenderContractStatus：ready / partial / missing / conflict / not-applicable
- figmaFetchStatus / figmaFallbackMode：success / partial / rate-limited-429 / permission-denied / node-not-found / failed / cache-only / screenshot-only / figma-unverified / not-applicable
- uiSourcePriorityStatus：ready / missing / conflict / not-applicable
- frontendFutureArtifacts：figma-cache 由 Evidence 阶段生成；tasks / verification / review / handoff 由后续执行或交付阶段生成。本设计只引用目标路径，不创建这些产物。

## 设计产物策略
- Frontend Design 阶段默认只生成 `frontend-design.md` 和 `contract-check.md`。
- 页面交付、demo-slice 或需要跨阶段换手时，应生成或更新 `frontend/index.md`，只记录 canonical sources、当前阶段、状态摘要和开放事项。
- `frontend-clarifications.md` 只在存在需独立跟踪的阻塞、缺失、冲突或人工确认队列时生成；轻量确认可内嵌，没有待确认项时在本文澄清小节写 `无 / not-applicable`。
- UI Contract 默认作为本文章节，不额外生成 `ui-contract.md`；只有复杂页面、多人协作或设计文档过长时才拆出独立文件。
- 设计阶段 production replacement 只保留 draft 语义，优先写入 `contract-check.md`；不得在 `frontend/design/` 目录生成最终语义的 `production-replacement-checklist.md`。
- `frontend/tasks`、`frontend/verification`、`frontend/review`、`frontend/handoff` 和最终 production replacement checklist 是执行/交付资产，不属于 Frontend Design 默认产物；对应模板归属 `front-hzero-enterprise-process-control`。
## Contract Check
完整契约事实源写入 `contract-check.md`，使用 `templates/contract-check.md`。本文只保留设计摘要和阻塞结论；除非用户要求单文件交付，否则不要复制 Contract Check 的完整表格。
- contractCheckPath：
- contractCheckStatus：pass / conditional / missing / conflict
- backendAssetCoverageSummary：FDS / TDS / MDS / FSS / API / DTO / route-menu / permission / LOV / attachment / import-export 的覆盖结论；完整表见 `contract-check.md#Backend Asset Coverage`。
- backendTdsFrontendHintsSummary：后端 TDS 前端段落只作为 hint / partial / generatedCandidate；完整吸纳表见 `contract-check.md#Backend TDS Frontend Hints`。
- apiContractStatus / backendApiReadiness / runtimeReachability：documented / closed / reachable / partial / missing / conflict / unknown / not-run / not-applicable；FSS/API/external-assets 只证明 documented，未验证 readiness 写 reason=unverified。
- blockingContractGaps：
- generatedCandidatesRequiringConfirmation：
- mockDemoDecisionStatus：default-mock-demo / denied / not-applicable
- assetBaselineStatus / assetBaselineSource / assetBaselineDecision：active / blocked + reason / hzerojs-asset-baseline / follow-asset-baseline / not-applicable
- questionGatePreservationStatus：required / clear / blocked
- designCumulativeFallbackPolicy / fallbackStates / fallbackShortCircuitCheck：cumulative-no-short-circuit / states list / pass 或 failed + reason
- uiContractDowngradeAllowed：no / not-applicable
- mockOnlyDataTransport：allowed-only-when-authorized / blocked / not-applicable
- productionReplacementDraft：embedded in contract-check / separate draft / not-applicable + reason
### Contract Status Summary
| 契约项 | 状态 | 来源 | 影响 | 下一步 |
| --- | --- | --- | --- | --- |
| 字段 / 请求响应 / fieldMapping | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | DataSet/Form/Table/payload |  |
| API URL/method / serviceRequestContract | confirmed / partial / missing / conflict / not-applicable |  | service/transport/API_HOST/nativeHttp |  |
| apiContractStatus / backendApiReadiness / runtimeReachability | documented/partial/missing/conflict / closed/partial/missing/conflict / reachable/unknown/not-run |  | queryMode、真实请求授权、验证计划；未验证 readiness 写 reason=unverified |  |
| tenantContext / frontendIdRuntimeContract | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | tenant path/ID-like 字段/Lov/rowKey |  |
| targetPlacement / route / menu / routeOpenMode / routeContext | confirmed / partial / generatedCandidate / needs-confirmation / missing / conflict / not-applicable |  | 真实代码落点/页面入口/编辑态 | route/menu 可按 `generated-code-conventions.md` 生成候选；production confirmed 必须来自用户、平台菜单资产或明确 routeConfig/platform evidence；候选可进入 mock/demo 和 replacement；新生成 route config 不得要求任何 `redirect` route |
| detailViewInteractionMap / routeOpenMode | confirmed / generatedCandidate / needs-confirmation / unresolved / missing / conflict / not-applicable |  | 每个详情入口打开方式和 Tab 行为；routeOpenMode confirmed 必须来自 Open Interaction Confirm 的 user-question，或明确 Drawer/抽屉证据；只来自 FDS/TDS/设计文档/工程证据/generatedCandidate 时不得进入 Task / Implementation |  |
| permission / i18n / LOV/lookup | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | 权限适用性、required 权限按钮/多语言/值集 |  |
| UI / fieldEditability / fieldVisibility / emptyDerivedFieldUx / actionEntry / drawer-modal | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | 页面布局/字段状态/字段显隐/空态派生字段/动作入口/弹层形态 |  |
| componentImportMap / componentApiProvenance / enumProvenance / typescriptRenderContract | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | JSX 组件、权限按钮、Choerodon Pro 组件、renderer/helper、组件静态 API、枚举型 props、Table columns/buttons 类型可编译策略 |  |
| attachment / import / export | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | 文件能力/导入导出入口与协议 |  |
导入/导出只在本表保留状态摘要。完整 `importComponentMode`、`importFlowContract`、`exportComponentMode` 和 `exportRequestContract` 写入 `contract-check.md`，并先继承企业模板内置导入导出 Design Gate；命中能力时记录 `specialtyTriggers[]=import-export`，只有满足专项加载条件时才读取 `front-hzero-import-export` owner reference。FDS/TDS/API/模板资产要求导入或导出时，设计阶段默认候选为 HZERO 新版标准组件；`minimum-codable + default-mock-demo` 可用 `designAutoResolution=standard-import-export-direct` 自动承接，不再触发组件模式 question。只有 production-complete、目标项目 confirmed wrapper/custom 外壳冲突、用户拒绝标准入口或参数结构无法形成候选时，才触发 `Import Component Mode Confirm` / `Export Component Mode Confirm`。参数或契约事实不完整时仍按 HZERO 标准组件或项目 confirmed wrapper 规划代码形态，使用 mock/generatedCandidate 候选常量承接，并在 Contract Check / Verification / Handoff 标明来源未确认；运行期权限、Network、后端部署或两阶段细节未完全验证时，进入 verification/handoff，而不是设计成 disabled/no-op、普通按钮或提示入口。
## Specialty Load Decisions
先根据 `specialtyTriggers[]` 写出专项加载决策，再读取完整专项 reference。复杂页面可以加载多个专项 owner，但每一项都必须独立证明其会改变当前 Design 阶段的 Contract Check；不得仅为了记录 trigger、风险域或摘要而读取完整专项内容。
| ownerSkill | trigger | loadRequired | reason | evidence | contractCheckImpact | selectedSourcePaths | gateIds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `front-hzero-*` |  | true / false | true: production-complete / production-ready / template-default-insufficient / conflict / blocked / multiple-candidate / user-requested-specialty / design-contract-changing-rule；false: template-default-sufficient / trigger-only / not-applicable | FDS/TDS/API/evidence/Contract Check 路径 + 章节或 gate | 明确写受影响的 Contract Check 字段、状态、blocking 结论或 gate；不能只写“补充规则” | 仅 `loadRequired=true` 时填写；false 必须为空 | 仅 `loadRequired=true` 时填写；false 必须为空 |
`loadRequired=false` 不得写入 `ownerReferenceCapsule.ownerReferences[]`；`loadRequired=true` 的 evidence 必须证明模板默认无法闭合、存在冲突/阻塞/多候选、用户明确要求，或专项规则本身会改变 Contract Check，“命中特性”或“页面复杂”不是充分理由。`selectedSourcePaths`、`loadedReferenceHash`、`gateIds` 和 `loadDecision.reason` 必须可追溯；核心 `front-hzero-enterprise-design` / `front-hzero-enterprise-process-control` 不适用专项加载决策。
## Frontend Design Handoff Metadata
| field | value / summary | status / source |
| --- | --- | --- |
| targetProject / targetModule / pageType |  |  |
| routePath / menuPath / routeTitle / routeRedirectPolicy | route title、route/menu confirmation、route redirect 禁止策略和平台多语言后续项摘要 | `routeRedirectPolicy` 必须为 forbidden/not-applicable；命中父路由 redirect 到 `/list`、父级 `redirect + routes`、同父级 path redirect 子路由或叶子 redirect 时写 blocked/conflict |
| routeOpenMode / detailViewInteractionMap / navigationApi | 每个详情入口打开方式、questionGrouping、parentTabKey、targetDetailPath、tabIdentityPolicy、tabTitle、routeMode、dws、queryStateKey 摘要 |  |
| routeContext | routePattern / idSource / isCreateSource / editableDerivation / pageModeDerivation / editableAuthority / saveRedirectPolicy |  |
| permissionCodes / fieldMappingStatus / apiList |  |  |
| serviceRequestContract / runtimeDataEntryContract / tenantContext | 完整字段见 `contract-check.md` 及对应 references |  |
| importExportContract / attachmentContract | 完整字段见 `contract-check.md`；专项 owner 只在已加载时补充细则 |  |
| targetPlacement | placementType、packageDir、businessDomain、pageGroup、routePrefix、parent registration、evidence/userConfirm/status 摘要 |  |
| backendDependencyMap / directoryPlan / codingRules / validationHandoff | riskDomains、acceptanceSignals、candidateVerificationEntries、unresolvedVerificationInputs、downstreamOwners | Design 只记录候选入口和风险域，不定义最终命令、validator 顺序或单测策略 |
| uiSourcePriority / figmaEvidence | layoutAuthority、businessAuthority、conflictPolicy、figma fallback 和 visualRisk |  |
| specialtyLoadDecisions / ownerReferenceCapsule | 每个专项的 trigger、是否加载、加载原因、证据、Contract Check 影响、引用路径、hash、gateIds 和复用状态 | 已加载的非核心专项 owner 必须有 `loadDecision={reason,evidence,contractCheckImpact}`；未加载专项不得出现在 capsule |
## Target Placement Contract
适用：新增/改造页面、路由、菜单、`packages/<module>` 子模块、微前端子包或用户提到“子模块/独立子模块/微前端/packages 模块”时必填；纯设计资产或非代码讨论写 `not-applicable + reason`。
| 字段 | 值 | 状态 | 来源 / 证据 | 影响 |
| --- | --- | --- | --- | --- |
| placementType | new-package / existing-package / parent-src-page / integration-only / unknown | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable | user / FDS / TDS / evidence / generatedCandidate | 决定业务代码写入根 |
| placementIntentSource | user-explicit / user-implicit / FDS / TDS / evidence / generatedCandidate |  |  | 判断是否需要 question |
| targetProject |  |  |  | 目标前端工程根 |
| packageName |  |  |  | `packages/<module>` 包名或 not-applicable |
| packageDir | `packages/<module>` / not-applicable |  |  | 子模块业务代码根 |
| businessDomain |  | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  | package 内业务域；确认 packageDir 不等于确认业务域 |
| pageGroup |  | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  | package 内页面目录分组 |
| pageDir |  |  |  | 页面/组件/DataSet/service/style 业务文件根 |
| routePrefix |  | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  | 当前功能主 route prefix |
| menuGroup |  | confirmed / generatedCandidate / missing / not-applicable |  | 菜单分组或平台菜单归属 |
| packageInternalAmbiguity | none / multiple-business-domains / multiple-route-prefixes / multiple-candidates / missing-evidence / not-applicable |  |  | package 内功能级落点是否仍有歧义 |
| submoduleRouteSystem | umi-submodule / hzero-cli-submodule / parent-src-route / unknown / not-applicable |  |  | 默认 umi-submodule；hzero-cli 仅用户明确指定或工程证据确认 |
| submoduleRouteEntryMode | single-router-ts / split-routes-dir / not-applicable / missing |  |  | 仅一个路由文件用 `config/router.ts`；多路由文件或项目拆分模式用 `config/routes/**` |
| umiConfigPath | `packages/<module>/config/config.ts` / not-applicable |  |  | Umi 子模块主配置 + registerRegex 接线；不得内联完整 route array |
| umiDevConfigPath | `packages/<module>/config/config.dev.ts` / not-applicable |  |  | Umi 子模块独立 start/package-start 开发态配置；mock-request 命中时不得注册 `../dev-mock/<module>-dev-mock-plugin` |
| packageTemplate | project-template / baseline-template / user-template / missing / not-applicable |  |  | 新子模块 package.json 来源；baseline 为 `submodule-package.json.template` |
| packageRequiredScripts | start/build/build:ms/transpile/build:app present / missing / not-applicable |  |  | 新 Umi 业务子模块硬必选 scripts；`transpile` 只作为发布/转译模板能力，Verification 不直接执行；`prettier`、`test`、`test:coverage` 可按模板保留 |
| packageFilesPolicy / packageBuildArtifactPolicy | files: project-trimmed / baseline-template / missing / invalid / not-applicable; artifact: clean-after-build / artifact-found-cleaned / artifact-found-untracked / invalid / not-applicable |  |  | `files` 可保留模板发布清单 `lib`；`build:ms` 后检查 `packages/<module>/lib` 等副产物，不得写入源码交付或 Handoff 资产 |
| packageDependencyFieldsSource | adjacent-package / parent-template / workspace-evidence / user-template / none / not-applicable |  |  | `dependencies`、`peerDependencies`、`devDependencies`、`resolutions`、`volta`、`private`、`main` 等字段来源；无证据不生成 |
| tsconfigTemplate | project-template / baseline-template / user-template / missing / not-applicable |  |  | 新子模块 tsconfig.json 来源；baseline 为 `submodule-tsconfig.json.template`，生成时直接复制模板 JSON，不自行增删字段，默认不写 `compilerOptions.paths`，paths alias 继承父工程 |
| mockPluginPath | `packages/<module>/dev-mock/<module>-dev-mock-plugin.js` / aggregator / not-applicable / missing |  |  | mock-request 命中时必须规划并由父工程注册或聚合注册 |
| mockDirectoryPolicy | `packages/<module>/dev-mock` / not-applicable / missing |  |  | mock handler/plugin/data/store 统一放在与 `config` 平级的 `dev-mock` 目录；不存在时新建 |
| mockDataSplitPolicy | inline-small-seed / split-data-store / not-applicable |  |  | 1-2 条简单 seed 可内联；多接口、状态流转或头行明细数据拆到 dev-mock data/store 文件 |
| mockTemplatePlaceholders | replaced / generatedCandidate / not-applicable / missing |  |  | mock-request 命中时必须规划 `__MODULE_KEY__`、`__MODULE_CAMEL__` 替换，并确认 handler 直接导出 middleware 函数、plugin 使用 `api.addBeforeMiddlewares(() => [middleware])` |
| routeConfigPath |  |  |  | 子模块或父工程路由配置 |
| parentRegistrationPath |  |  |  | 父工程注册文件，例如 `config/packages-config.js` |
| parentRegistrationEntryPolicy | minimal-name-only / schema-confirmed-extra-fields / missing / conflict / not-applicable |  |  | 默认 `{ name: '<module>' }`；额外字段必须有 active schema / 项目基线 / 用户确认来源 |
| parentRegistrationExtraFieldSource | active-schema / project-baseline / platform-required / user-confirmed / none / not-applicable |  |  | `initLoad/registerRegex/plugins/priority/routes` 等额外字段来源；无来源不得生成 |
| registerRegex |  |  |  | 必须收敛到已确认 route prefix |
| parentSrcWritePolicy | registration-only / forbidden / allowed-with-reason / not-applicable |  |  | 父工程 `src/**` 写入边界 |
| forbiddenBusinessPaths | 例如 `src/pages/**` |  |  | Implementation / Review 拦截 |
| evidenceStatus | ready / partial / missing / conflict / not-applicable |  | engineering-evidence / similarPage / routeConfig / platform-menu / generatedCandidate | 工程证据是否足以形成候选 |
| userConfirmStatus | confirmed / needs-confirmation / missing / conflict / not-applicable |  | user-question / requirement-doc / FDS / TDS / platform-menu / not-applicable | 是否已由用户或上游权威输入确认落点 |
| confirmationSource | user-question / requirement-doc / FDS / TDS / platform-menu / none / not-applicable |  |  | 决定是否允许进入 Implementation |

规则：
- 这里的字段表是权威记录面；子模块解释、`packages/<module>` 与父工程 `src/pages/**` 的边界、`userConfirmStatus` / `evidenceStatus` 分离、Umi/hzero-cli 子模块判断、`config/config.dev.ts`、`registerRegex`、`pageRoot=src/pages` 默认值、`src/routes` 例外条件、mock plugin 注册方案和 asset-baseline 约束，统一以 `references/hzerojs-submodule-development.md`、`references/hzerojs-asset-baseline.md`、`front-hzero-enterprise-process-control` 的 HZEROJS 子模块运行期门禁 为准。
- 设计阶段在这里的最低要求只有三条：一是上述字段必须按事实落盘；二是 `userConfirmStatus != confirmed`、`packageInternalAmbiguity != none/not-applicable`、`placementType=unknown/missing/conflict/needs-confirmation` 或关键子模块基线字段缺失时，必须触发 `Target Placement Confirm` / 阻塞；三是设计不得把工程候选、历史目录、routeConfig 或最短可运行路径升级成 confirmed 落点。

## 目录结构和编码规则
- 真实工程结构来源：
- 工程类型：
- 父应用路径：
- 微包路径：
- targetPlacement：见 `Target Placement Contract`
- 路由配置入口：
- 页面目录：
- 页面入口文件：
- DataSet/service/model 文件：
- 样式文件：先填写 Style Necessity Contract 结论；默认 `no-new-style`，只有组件 props / HZERO Header+Content / 项目已有 class 不足且来源明确时才允许 `modify-existing-style/new-local-style`：
- i18n 文件或 namespace：

## 数据层设计
- 字段来源：
- 接口来源：
- service/model 或 DataSet transport：DataSet transport 必须标明 `transportMode=request-config-direct`；service action 只用于非 DataSet 生命周期动作或明确 `owner=service-action` 的场景
- Runtime Data Entry：页面按钮、DataSet submit/create/update/destroy、service function、mock handler 是否一一映射；Header/Line 保存粒度和 payload builder；DataSet transport 不得委托业务 service：
- fields / queryFields / queryDataSet：
- Frontend ID Runtime Contract：ID-like 字段的 declared type、runtime type、normalizationPolicy、encryptedIdPolicy、exceptions（按 `references/frontend-id-runtime-contract.md`；DB/API `Long/BIGINT/number` 不等于前端 runtime number）
- DataSet-first 约束：查询关系必须由 DataSet 的 `queryFields/queryDataSet/transport.read` 建模；Table 不得承接 `queryDataSet/onQuery/onReset` 业务查询职责，除非有目标项目组件封装证据：
- Mock API Contract：前端 mock 标准实现统一为 HZERO 本地 devServer middleware 暴露的 HTTP mock API；业务页面、DataSet 和 service 必须通过正常 HTTP 请求访问该 mock API；缺少 HZERO / Webpack / Umi devServer 扩展点时不得启动 runnable mock。默认按 Explore/Evidence 已确认的工程事实、本模板和 Contract Check 字段直接落盘并记录 `specialtyTriggers[]=mock-request`；历史 mock 机制不参与默认选型。只有满足专项加载条件时才引用 `front-hzero-mock-request` 的 Design Contract。
- Mock API Fields：只记录 `mockApiMode`、devServer 扩展证据、mock mount、handler/plugin 文件、parent registration evidence、template compliance、self check、origin policy、page response shape、runtime store、delivery ceiling；完整字段见 `contract-check.md#Mock API Contract`。
- 分页/排序/筛选协议：
- 提交 payload：
- 返回结构：
- 状态枚举和值集：

## 组件和交互设计
- 页面设计来源：
- UI 来源优先级：Figma/PageSchema confirmed 优先约束页面布局、区块顺序、字段显示顺序、按钮位置和弹层形态；FDS/TDS/API/用户确认优先约束业务能力、字段语义、接口、权限、route/menu 和生产契约：
- 关键交互：
- HZERO 页面容器：
- F 型布局：Header / ListHeader / ListContent / List / ListItem / ContentCard / EmptyPage / TabsAdsorptionContainer 适用性，`_LOCATED_DATA_` 选中项定位、列表折叠宽度、保存后刷新定位和滚动吸附策略：
- Choerodon DataSet/Form/Table/Lov/Attachment：
- routeContext / editMode：`getRouteContext(location, params)` 或项目 wrapper；`id/isCreate/editFlag/pageMode` 来源；内置 `/create` 默认新建编辑态；`/detail/create` 属于违规路径，发现后迁移到 `/create`；保存后跳转策略：
- field usage / visibility / editability / empty UX：字段存在、展示、编辑和 submitPolicy 必须拆开；完整矩阵见 `contract-check.md`。
- componentApiProvenance / enumProvenance / typescriptRenderContract：记录组件、静态 API、renderer/helper、enum-like props 和类型来源；完整字段见 `contract-check.md` / schema checklist。
- Choerodon Enum / Type Contract：若本轮新增或修改 DataSet/Table/Form/Button/Lov/Attachment、renderer/helper 或 enum-like props，必须引用 `contract-check.md#Choerodon Enum / Type Contract` 的 strategy、import/type source、stringFallbackPolicy 和 `validationRiskHandoff`。空基线或无健康参考时默认 enum-first；弱类型相邻页面只能作为 legacy risk，不得把 `enumImportMapStatus` 写成 not-applicable。
- table / row actions / import / export / attachment：只写设计摘要、来源、trigger、风险域和阻塞项；细则只在对应专项 owner 已加载时写入 ownerReferenceCapsule，其余交给 compliance manifest 与下游阶段继承。
- 异常、空态、loading：

## UI Contract
必须按 `front-hzero-enterprise-design` 的 UI Contract guardrails 和 `templates/ui-contract.md` 形成编码前 UI 回读。Implementation 只能实现 UI Contract 中 confirmed 或明确允许的 generatedCandidate 项。
Figma/PageSchema 与 FDS/TDS/API/工程证据并存时，必须分别记录 `layoutAuthority` 和 `businessAuthority`。UI 显示布局以 Figma/PageSchema confirmed 为优先证据；业务契约以 FDS/TDS/API/用户确认为优先证据。冲突时写 `conflictResolution`，不得静默合并。

本节只写摘要和关键结论；详细表格优先写入 `templates/ui-contract.md` 的对应结构。单文件交付时可内嵌必要表格，但不要重复 `contract-check.md` 中的字段/API/request schema。

- uiContractPath：embedded / `frontend/design/ui-contract.md` / not-applicable + reason
- uiReadbackStatus：confirmed / partial / generatedCandidate / missing / conflict / not-applicable
- queryFieldsStatus：
- listColumnsStatus：
- routeContextEditModeStatus：
- fieldUsageMatrixStatus：
- fieldEditabilityStatus：
- fieldVisibilityStatus：
- emptyDerivedFieldUxStatus：
- actionEntryMatrixStatus：
- buttonContractStatus：
- buttonSemanticMatrixStatus：
- componentApiProvenanceStatus：
- typescriptRenderContractStatus：
- componentEnumProvenanceStatus：
- drawerModalContractStatus：
- fLayoutContractStatus：
- uiBusinessConflicts：
- blockedUiItems：

> 操作列“更多”不属于 Drawer / Modal Contract。它必须使用 `c7nOperatorRender` / `operatorRender` helper overflow、项目操作菜单、Dropdown/Popover/Menu 等轻量浮层；只有详情、表单、导入组件等被 UI Contract 明确为业务弹层的动作才允许使用 Drawer。

## 页面区域 checklist
| pageRegion | required items | source | status | taskImpact |
| --- | --- | --- | --- | --- |
| list | 查询区、fuzzy search、页面工具栏、表格列、行操作列、权限拆分 | FDS/TDS/Figma/UI Contract | confirmed / partial / missing / not-applicable |  |
| f-layout | Header/ListContent/ListItem/ContentCard、定位、保存刷新、滚动吸附 | F 型布局合同 / 项目证据 | confirmed / partial / missing / not-applicable |  |
| detail-master-line | Header 按钮、基本信息 Form、审计字段、附件、明细筛选、明细工具栏、行操作、编辑态刷新 | Detail Contract / Action Entry / Button Semantic / Field matrices | confirmed / partial / missing / not-applicable |  |

规则：区域细节只在当前页面命中时展开到 Design Coverage Ledger、Contract Check 或 UI Contract；本节只保留覆盖状态和下游任务影响。

## Status Action Matrix
| action | statusField | statusEnumMap | sourceStatus | visibleWhen | enabledWhen | actionGuard | serviceAction | mockHandler | successTargetState | refreshTarget | permissionAction | designStatus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| submit / withdraw / void / delete / other |  | code / meaning / color / source | FDS / TDS / API / MDS / status-flow / user-confirmation |  |  |  |  |  |  |  |  | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 业务状态枚举必须以 `statusField + statusEnumMap` 记录 code、显示文案、颜色/标签策略和来源；不得把设计状态值改成旧模型近义值，例如 `NEW` 改 `DRAFT`、`IN_APPROVAL` 改 `SUBMITTED`，除非有集中 adapter 或 legacy runtime 来源。
- 按钮可见、按钮禁用、handler 二次校验、mock/API handler 当前态校验和成功后刷新目标必须同源；缺少状态矩阵时，相关状态动作不得进入 production-ready implementation。

## Action Entry Matrix
| actionId | label | actionExistsSource | sourceSectionPath | sourceRegion | sourceRegionReason | statusActionRef | allowedEntryLocations | chosenEntryLocation | uiArea | pageModes | entryStatus | overrideSource | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| save / submit / cancel-navigation / cancel-business / withdraw / void / delete / other |  | FDS / TDS / API / status-flow / Figma / project evidence / user-confirmation | fds.md#heading / tds.md#heading / figma node / evidence path | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | why this region maps to chosenEntryLocation | not-applicable / status-action-id | detail-header / page-toolbar / row-action / table-toolbar / modal-footer / hidden | detail-header / page-toolbar / row-action / table-toolbar / modal-footer / hidden / not-confirmed | page-header / business-state-actions / row-action / table-toolbar / modal-footer / other | create / edit / detail / list / approval / readonly | confirmed / generatedCandidate / needs-confirmation / missing / conflict / not-applicable | not-applicable / UI Contract / user-confirmation / Figma / project-baseline | implement / block-and-confirm / keep-hidden / demo-only-with-risk / not-applicable |

规则：
- “业务动作存在”不等于“页面 Header 必须展示按钮”。FDS/TDS/API/status-flow 只能证明动作存在，入口位置必须由页面按钮区、Figma/PageSchema、UI Contract、项目 confirmed baseline 或用户确认单独证明。
- `entryStatus=generatedCandidate/needs-confirmation/missing/conflict` 的业务状态动作不得进入 `detail-header/page-header`；只能隐藏、阻塞确认或记录 replacement 风险。
- 导航取消、返回、关闭与取消单据/作废/撤回等业务状态动作必须使用不同 `actionId`，不得用同一“取消”按钮承接两种语义。
- 列表/表格/明细表章节下的“列表头按钮区 / 明细表列表头按钮区”默认归类为 `table-toolbar`，并由 `Table.buttons` 或项目 confirmed table toolbar wrapper 消费。只有 `overrideSource` 明确来自 UI Contract / 用户确认 / Figma / PageSchema 时，才允许归类到页面 Header。

## Button Semantic Matrix
| buttonId | label | sourceText | copyPolicy | copyOverrideSource | sourceSectionPath | sourceRegion | sourceRegionReason | location | uiArea | semanticKind | navigationTarget | businessMutation | statusActionRef | permissionRequirement | destructive | confirmPolicy | asyncAction | requestOwner | loadingPolicy | repeatClickGuard | finallyReleasePolicy | designStatus | overrideSource | taskAcceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| not-applicable |  | FDS/TDS/Figma/用户确认原文 | exact-source / override-with-source / generatedCandidate | FDS/TDS/Figma/用户确认/项目基线路径或 not-applicable | fds.md#heading / tds.md#heading / figma node / evidence path | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | why this region maps to this UI surface | page-header / page-toolbar / table-toolbar / row-action / modal-footer / other | page-header / business-state-actions / table-toolbar / row-action / modal-footer / other | navigation / business-state-action / data-edit / table-operation / import-export / attachment / unknown | list / previous / close-tab / close-modal / route / not-applicable / unknown | none / creates / updates / deletes / status-change / import-export / upload / unknown | not-applicable / status-action-id | required / not-applicable / unknown | yes / no / not-applicable | Popconfirm / Modal.confirm / project-wrapper / not-required / blocked | yes / no / not-applicable | DataSet / service / mock-request / request-adapter / not-applicable | row-level / batch-level / action-level / page-level / not-applicable | disabled / handler-guard / both / not-applicable | try-finally / promise-finally / wrapper-guaranteed / not-applicable | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable | not-applicable / UI Contract / user-confirmation / Figma / project-baseline | Contract Acceptance / UI Acceptance / Verification Acceptance |

规则：
- 前端设计必须从 FDS/TDS、UI Contract、Figma/PageSchema、工程证据或用户确认中抽取按钮原文，并按 `buttonId + uiArea + semanticKind` 拆分；不得只按文案合并。默认 `copyPolicy=exact-source`，把“新建”改为“新增行”、把“提交审批”改为“提交”等近义改写必须有 `copyOverrideSource`。
- 破坏性动作必须在设计阶段标出 `destructive/confirmPolicy`；异步接口动作必须标出 `asyncAction/requestOwner/loadingPolicy/repeatClickGuard/finallyReleasePolicy`，并进入 Task 的 Contract / UI / Verification Acceptance。缺失时不得进入 production implementation。
- 页面 Header、页面工具栏、Table buttons、Table toolbar、行操作列和弹层 footer 必须分区记录；`page-toolbar` 的任务验收指向 `Header` children 且负向排除 `Table.buttons`。语义不明时写 `semanticKind=unknown` 并阻塞 production runnable。

## 设计阶段候选编码
| 类型 | value | source | status | confirmOwner | usage |
| --- | --- | --- | --- | --- | --- |
| routePath |  | user-question / generatedCandidate-rule / FDS / TDS / design-doc / routeConfig / platform-menu | confirmed / generatedCandidate / needs-confirmation / missing / conflict | routeMenuConfirmationSource | 页面访问；规则候选可进入 mock/demo，production confirmed 需用户或平台/routeConfig 证据 |
| menuPath |  | user-question / generatedCandidate-rule / FDS / TDS / design-doc / routeConfig / platform-menu | confirmed / generatedCandidate / needs-confirmation / missing / conflict | routeMenuConfirmationSource | 菜单入口；默认与 routePath 一致，正式平台挂载进入 replacement |
| routeTitle |  | user-question / generatedCandidate-rule / FDS / TDS / design-doc / routeConfig / platform-menu | confirmed / generatedCandidate / needs-confirmation / missing / not-applicable | routeMenuConfirmationSource | `authorized: true` route 的前端 title；中文标题可生成候选，生产需平台菜单标题和平台多语言 |
| routeOpenMode | menu-current / hzero-openTab / dynamic-tab / browser-new-tab / direct-url | user-question / explicit-drawer-design / FDS / TDS / design-doc / project-evidence / generatedCandidate | confirmed / generatedCandidate / needs-confirmation / missing / conflict | openInteractionConfirmationSource | 页面打开方式；confirmed 必须来自 Open Interaction Confirm 或明确 Drawer 证据 |
| detailViewInteractionMap | routePath + listRegion + triggerAction + targetDetail => current-tab-page / drawer / hzero-openTab / dynamic-tab / browser-new-tab / modal / other | user-question / explicit-drawer-design / FDS / TDS / design-doc / project-evidence / generatedCandidate | confirmed / unresolved / missing / conflict / not-applicable | openInteractionConfirmationSource | 每个列表详情入口的打开方式；unresolved 阻塞 Task / Implementation |
| parentTabKey |  |  | confirmed / generatedCandidate / missing / not-applicable |  | 当前 Tab 页跳转复用的父级 HZERO Tab key |
| targetDetailPath |  |  | confirmed / generatedCandidate / missing / not-applicable |  | 当前 Tab 页跳转实际渲染的详情 route path |
| navigationApi | openTab / project-wrapper / history / browser / not-applicable |  | confirmed / generatedCandidate / missing / conflict / not-applicable |  | 页面导航 API；current-tab-page 不得只靠 history.push |
| tabIdentityPolicy | current-parent-key / route-path-exact / reusable-fixed-path / not-applicable |  | confirmed / generatedCandidate / missing / conflict / not-applicable |  | `dynamic-tab` 必须为 `route-path-exact`：从同一个 `targetPath` 派生 `key` 与 `path`，并记录 `keyPathRelation=key===path`、`recordIdSource`、`pageModeSource`；不得只用记录 ID、标题或虚拟后缀作为 key。`current-tab-page` 为 `current-parent-key`，固定详情复用为 `reusable-fixed-path` |
| tabTitle |  |  | confirmed / generatedCandidate / missing / not-applicable |  | HZERO 应用内 Tab 或浏览器 Tab 标题；必须记录 `tabTitlePolicy/staticRouteTitle/runtimeTitleSource/displayField/technicalIdField/fallbackTitle/titleUpdateTiming`，区分 route 静态 `title` 与运行时 `openTab.title` |
| routeMode | route / omitted-default-route / dynamic / not-applicable |  | confirmed / generatedCandidate / missing / not-applicable |  | HZERO route `mode`；当前 Tab 详情为 route/default，动态 Tab 为 dynamic |
| dws / queryStateKey |  |  | confirmed / generatedCandidate / missing / not-applicable |  | 同一路由多 Tab 唯一性 |
| permissionCode |  |  | confirmed / generatedCandidate / missing / conflict |  | 权限按钮 |
| i18nCode |  |  | confirmed / generatedCandidate / missing / conflict |  | 多语言 |
| lovCode/lookupCode |  |  | confirmed / generatedCandidate / missing / conflict / not-applicable |  | 值集/LOV |

## transitionalCopy 清单
| 文案/说明 | 承载位置 | 是否进入代码 | 是否用户可见 | 生产前处理方式 | 备注 |
| --- | --- | --- | --- | --- | --- |
|  | handoff / replacement checklist / verification report / dev log / page UI(需产品确认) | yes/no | no/yes-with-product-approval | 删除 / 隐藏 / 替换为正式 i18n notification |  |

> 默认不得把 `mock/demo`、`generatedCandidate`、`待替换`、`未接生产接口`、`request helper 待确认`、`SecurityToken 待确认`、`Figma 未确认` 等内部临时说明渲染到页面 UI。页面需要演示环境提示时，应使用产品确认的正式业务文案和 i18n key。

## validationHandoff
- intent：
- riskDomains：
- acceptanceSignals：
- candidateVerificationEntries：仅记录 evidence 已知或模板可推导的候选入口；不得写成最终命令或通过标准。
- unresolvedVerificationInputs：
- downstreamOwners：Task / Implementation / Review / Verify / Artifact / specialty owner when loaded。
- 未验证风险：

## 风险和待确认项
- questionGate：
- questionGateQueue：
- closeoutLoopResult：designCompletenessPolicy / loopCount / maxLoop / targetedEvidenceBackfillUsed / failedGates / classifiedGaps(blocking/generatedCandidate/verification/notApplicable) / fixApplied / recheckResult / remainingBlockers / fuseTriggered / fuseReason / nextAllowedStage
- 导入模式确认：Import Component Mode Confirm / auto-resolved-standard / resolved / unresolved / not-applicable；选择来源：
- 导出模式确认：Export Component Mode Confirm / auto-resolved-standard / resolved / unresolved / not-applicable；选择来源：

## 前端设计确认摘要
- 设计文档路径：
- Contract Check 结论：
- frontendDesignState：
- designCompletenessPolicy：见 `First-pass Completeness Policy`
- closeoutLoopResult：designCompletenessPolicy / loopCount / maxLoop / targetedEvidenceBackfillUsed / failedGates / classifiedGaps(blocking/generatedCandidate/verification/notApplicable) / fixApplied / recheckResult / remainingBlockers / fuseTriggered / fuseReason / nextAllowedStage
- designUnderstandingDeviationCheck：none / possible / confirmed + checked sources / unresolved conflicts
- blocking clarifications：
- generatedCandidate 待确认：
- UI 来源优先级：layoutAuthority / businessAuthority / uiBusinessConflicts
- 页面打开方式待确认：routeOpenMode / tabTitle / dws / queryStateKey
- 导入/导出模式待确认：importComponentMode / exportComponentMode / questionGateQueue
- mock/demo 默认决策状态：
- Action Entry Matrix 状态：pass / partial / missing / conflict / needs-confirmation / not-applicable；入口未确认项：
- Button Semantic Matrix 状态：pass / partial / missing / conflict / needs-confirmation / not-applicable；语义未确认项：
- production-ready 要求：
- validationHandoff：riskDomains / acceptanceSignals / candidateVerificationEntries / unresolvedVerificationInputs / downstreamOwners
- 构建候选入口：HZEROJS Umi 子模块必须且只能记录 `npm run build:ms -- <module>`；`--` 为 npm 参数分隔符，`<module>` 为当前子模块名。不得改写为 yarn、pnpm 或其它 build 命令；根 scripts 缺少 `build:ms` 时记录 `missing-required-build-ms-script` 并回工程接线补齐。执行时机和通过标准由 Task/Verify 决定：
- 确认后下一步：Task Breakdown。`frontend-auto-agent` 是后续执行承接者，不是可替代 Task Breakdown 的阶段名；若本轮裁剪到代码生成完成，仍应先进入 Task Breakdown，再进入 Implementation 并停止在代码生成完成。
## Task Breakdown 衔接
- Task Breakdown 目标路径：`sdd-workspace/changes/{change-id}/frontend/tasks/task-breakdown.md`（模板见 `front-hzero-enterprise-process-control` 的 Task Breakdown 模板）
- 主干依赖链：
- 可并行支线：
- 进入 Task Breakdown 条件：Design Confirm 已通过，Contract Check 允许进入 Task Breakdown，`questionGate/questionGateQueue` 无阻塞未解决项，目标落点和运行态数据链路达到任务拆分所需状态。若只允许拆补契约/确认任务，必须写 `taskScope=backfill-only`，不得拆 runnable implementation。
- Task Breakdown 是否必需：Feature Root、新增/改造页面、多文件、demo-slice、HZERO+Choerodon、共享 route/menu/i18n/API/权限/DataSet 或需要状态回写时必须为 `required`；不得因代码实现终点裁剪或实现后阶段裁剪写成可选或 not-generated。
- 允许不生成任务拆分的例外：仅小范围 `regular-change` direct，且必须写明目标文件、成功标准、无 Feature Root、无共享契约、无状态回写要求和 decisionSource=`direct-no-task`。
- 任务验收拆分要求：Task Breakdown 必须继承“页面区域 checklist”、Action Entry Matrix 和 Button Semantic Matrix，并把按钮、筛选区、行操作列、权限、DataSet-first、编辑态刷新策略拆入 `Contract Acceptance`、`UI Acceptance`、`Verification Acceptance` 三段验收。动作入口未确认、按钮文案相同但 `uiArea` 或 `semanticKind` 不同的，必须拆任务、拆 handler、拆验收；入口或语义未确认项只能拆补契约或确认任务，不得进入 production implementation。

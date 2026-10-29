# Contract Check Template
<!-- frontend-design-canonical-ref: {"stateId":"<stateId>","statePath":"design/design-canonical-state.json","contractFreezeId":"<contractFreezeId>","projection":"<ready-for-task|needs-user|blocked>"} -->
Owner Stage: Frontend Design / Contract Check  
Default Path: `sdd-workspace/changes/{change-id}/frontend/design/contract-check.md`
Required When: 页面交付 / demo-slice / mock-demo / production-ready 前端交付需要进入 Task Breakdown 或 Implementation。  
Not Required When: 小范围 `regular-change` direct 且主流程已记录目标文件、成功标准、验证方式和跳过原因。  
Source Of Truth: 本文件是契约明细事实源；Task progression 只读取 `design/design-canonical-state.json`。
Downstream Consumers: `frontend-design.md`、Task Breakdown、Implementation、Review、Verification、Handoff、Lite 汇合。
## Contract Check Status
- contractCheckResult：ready / partial / blocked / demo-only / missing-input
- productionReadiness：production-ready / blocked-by-contract / demo-ready / not-applicable
- mockDemoDecisionStatus：default-mock-demo / denied / not-applicable
- generatedCandidatePolicy：allowed-for-demo / requires-confirmation / not-applicable
- lovCandidateContract：status=validated/not-applicable/failed；path=`frontend/design/lov-candidate-contracts.json`/not-applicable；contractFreezeId=stable-id/not-applicable；validatorResult=`frontend/evidence/design-gates/lov-candidate-contract.json`/not-applicable；manifestSha256/resultSha256=`sha256:<64hex>`/not-applicable。禁止 `validated-pending`。
- apiContractStatus：documented / partial / missing / conflict / not-applicable
- backendApiReadiness：closed / partial / missing / conflict / not-applicable；未验证写 missing 或 partial，并在 reason/source 中标记 unverified
- runtimeReachability：reachable / failed / unknown / not-run / not-applicable
- runtimeDataPathDecision：real-contract / requestable-demo-mock / pause-for-contract / unknown / not-applicable + reason
- remoteBackendRequestAuthorization：confirmed / denied / unknown / not-applicable + reason
- fieldVisibilityMatrixStatus：pass / partial / missing / conflict / not-applicable
- fieldEditabilityMatrixStatus：pass / partial / missing / conflict / not-applicable
- emptyDerivedFieldUxStatus：pass / partial / missing / conflict / not-applicable
- listQueryContractStatus：pass / partial / missing / conflict / blocked / not-applicable
- fuzzyQueryContractStatus：required-confirmed / required-missing / unsupported-with-evidence / not-applicable / conflict；unsupported-with-evidence 只能与 listQueryContractStatus=partial/blocked/conflict 配套，不得单独支撑 pass
- actionEntryMatrixStatus：pass / partial / missing / conflict / needs-confirmation / not-applicable
- buttonSemanticMatrixStatus：pass / partial / missing / conflict / needs-confirmation / not-applicable
- designInputPreflightStatus：pass / partial / failed + reason
- standardPageProfile：HZEROJS_SUBMODULE_MASTER_DETAIL_MOCK_REQUEST / custom / not-applicable
- designAutoResolution：standard-profile-defaults / standard-import-export-direct / standard-import-direct / standard-export-direct / none + reason
- fieldMatrixDerivationStatus：generated-from-MDS-API / mixed / manual / missing / not-applicable
- productionReplacementDraftProfile：standard-mock-demo / production-complete / custom / not-applicable
- lastUpdated：
- sourceSummary：
规则：
- 新增/改造可运行前端数据页面进入 Frontend Design 时，只要存在运行态数据请求，固定记录 `mockDemoDecisionStatus=default-mock-demo`、`runtimeDataPathDecision=requestable-demo-mock`、`queryMode=mock-request`、`mockApiMode=hzero-dev-server-middleware` 和 `contractGapConfirmationSource=default-mock-demo-policy`，并完整规划 handler/plugin/父工程注册/继承/current-origin prefix。用户要求 production-ready 或真实 API 不触发切换型 Missing Contract Confirm，只追加后续独立集成和生产门禁 advisory；只有缺口影响当前 Mock demo、写入范围冲突或目标不是标准 HZERO/Umi 托管形态时才进入对应 gate。
- `mockDemoDecisionStatus=not-applicable` 只能用于非可运行前端页面或完全不涉及 DataSet/service/API/transport，并必须写 reason 和 `contractGapConfirmationSource`。
- 可运行页面只要存在 DataSet/service/transport/action request，且 `serviceRequestContract / tenantContext / responseShape / queryMode` 未全部 confirmed，仍可按默认 mock demo 继续 Contract Check，但必须把缺口写入 Mock API Contract、production replacement 或 questionGate；不得用 generatedCandidate servicePrefix/API path 直接升级为 `production-transport`。
- `generatedCandidatePolicy` 不是用户交付路径。候选编码可随 real-contract 或 mock-demo 路径进入候选实现，但不能替代 `runtimeDataPathDecision`，也不能自动确认远端 `API_HOST` 请求。
- 默认 mock/demo 的主数据 LOV 缺平台编码或 object/bind 参数时，不进入 Missing Contract Confirm。Design 自动生成 `lov-candidate-contracts.json`，记录 `questionGate.required=false`、`status=not-required`、`resolutionSource=default-mock-candidate-policy`；consumer 固定写成 `{"controlId":"<control-id>","objectField":"<与合同顶层 objectField 完全一致>"}`，缺任一字段均为 Design closeout failure。Contract Check 只引用 path/freezeId/validator result，不复制候选对象形成第二事实源；不得留给 Task、Implementation 或 Review 补齐。旧复合状态 `generatedCandidate/mockOnly`、伪造 question call 和 `blocked + resolved` 双状态均不允许。
- FSS、`external-assets/api-list.json`、`external-assets/apis/*.json`、Swagger/OpenAPI 或后端接口清单只能把 `apiContractStatus` 置为 `documented/partial`；不能单独把 `backendApiReadiness` 置为 `closed`，不能把 `runtimeReachability` 置为 `reachable`，也不能把 `queryMode` 置为 `production-transport`。目标为可运行页面时始终写默认 Mock demo；真实 API 要求和 readiness 仅进入后续独立集成 advisory。
## Design Input Preflight
本节用于减少前端设计续跑。先判断是否可用标准 profile 和默认承接，再展开完整合同矩阵；缺失项必须归入 generatedCandidate / replacement / questionGate，不能让 Implementation 猜。
| item | status | source | autoResolution | blockingRule |
| --- | --- | --- | --- | --- |
| standardPageProfile | HZEROJS_SUBMODULE_MASTER_DETAIL_MOCK_REQUEST / custom / not-applicable | FDS/TDS/MDS/evidence/user | standard-profile-defaults / none | custom 需写 reason |
| targetPlacement | confirmed / generatedCandidate / needs-confirmation / conflict | Target Placement Evidence / user | generatedCandidate if unique | conflict blocks |
| queryMode/mockRequest | mock-request / production-transport / blocked | default-mock-demo / backend readiness | mock-request standard | blocked if user denies mock and real API not closed |
| routeOpenMode/detailViewInteractionMap | confirmed / unresolved / not-applicable | user / explicit Drawer / FDS/TDS explicit | none when unresolved | unresolved enters Open Interaction question |
| import/export mode | standard-direct / project-wrapper / custom / unresolved / not-applicable | standard component / project wrapper / user | standard-import-export-direct for minimum-codable mock-demo | question only for production/custom/conflict |
| fieldMatrixSource | generated-from-MDS-API / mixed / manual / missing | MDS/API/FDS | generated skeleton | missing blocks runnable design |
## Specialty Load Decision Cross-Reference
完整的 `specialtyLoadDecisions[]` 和已加载 owner reference 审计信息写入 `frontend-design.md#Specialty Load Decisions` / Handoff Metadata；本文件只记录其实际改变的 Contract Check 字段、状态或 gate。
| ownerSkill | loadDecision reason / evidence | affected Contract Check field or gate | status impact |
| --- | --- | --- | --- |
| `front-hzero-*` | 仅已加载专项；指向 `frontend-design.md` 的对应 decision |  | confirmed / generatedCandidate / missing / conflict / blocked / not-applicable |
不得因为“命中特性”单独加载专项 reference；只有专项规则会改变本表的状态、字段或 gate，或模板默认无法闭合/存在冲突阻塞等已记录原因时才加载。
## Backend Asset Coverage
按 `references/contract-asset-discovery.md` 输出。未执行兜底搜索时必须写明原因。

| 类别 | 标准路径读取 | 兜底搜索 / 外部来源 | 状态 | 缺口或冲突 | 处理结论 |
| --- | --- | --- | --- | --- | --- |
| FDS | `sdd-workspace/changes/{change-id}/fds.md` |  | confirmed / missing / conflict |  |  |
| TDS | `sdd-workspace/changes/{change-id}/tds.md` |  | confirmed / partial / missing / conflict | 后端 TDS 前端段落默认 hint/partial |  |
| MDS | `sdd-workspace/changes/{change-id}/mds/**` |  | confirmed / partial / missing |  |  |
| FSS | `sdd-workspace/changes/{change-id}/fss/**` |  | confirmed / partial / missing |  |  |
| API / DTO |  | Swagger/OpenAPI / DTO/schema / backend handoff / source evidence | confirmed / partial / missing / conflict |  |  |
| apiContractStatus |  | FSS / external-assets API / Swagger / backend source | documented / partial / missing / conflict / not-applicable | documented 不代表真实接口可达 |  |
| backendApiReadiness |  | Backend API Readiness / real API verification / dev gateway evidence | closed / partial / missing / conflict / not-applicable | 文档证据不足以 closed；未验证写 reason=unverified |  |
| runtimeReachability |  | Network / HTTP smoke / browser verification / not-run | reachable / failed / unknown / not-run / not-applicable | 未验证不得写 reachable |  |
| serviceRequestContract |  | HZERO baseline request/getResponse + API_HOST strategy / envSource / servicePrefix / nativeHttp confirmation | confirmed / partial / missing / conflict / not-applicable | 标准 `request` / `getResponse` 无冲突时自动闭合；逐 API response handling 仍须有 backend evidence |  |
| tenantContext |  | request helper / hzero-front utils / backend path variable / resolverProvenance / source evidence | confirmed / partial / missing / conflict / not-applicable |  |  |
| route/menu/permission |  | user-question / generatedCandidate-rule / platform export / TDS / FSS / source evidence | confirmed / generatedCandidate / missing / conflict | route/menu production confirmed 必须来自用户、平台菜单资产或明确 routeConfig/platform evidence；规则生成值只能为 generatedCandidate；新生成 route config 不得使用 `redirect` | 前端生成 route 可带 `authorized: true` 和中文 title 作为候选/开发可访问配置；正式菜单权限和菜单标题仍需平台配置；`authorized: true` route 必须记录 routeTitle / 平台多语言后续项；若设计或任务要求父路由 redirect 到 `/list`、父级 `redirect + routes`、同父级 path redirect 子路由或叶子 redirect，状态写 blocked/conflict |
| LOV/lookup/value set |  | MDS / FSS / platform export / source evidence | confirmed / generatedCandidate / missing / conflict |  |  |
| attachment/import/export |  | MDS / FSS / backend handoff / source evidence | confirmed / partial / missing / not-applicable |  |  |

## Backend TDS Frontend Hints
后端 TDS 中的前端相关内容只作为候选/约束输入；除 API/DTO 等后端契约本身外，不得单独确认 UI Contract。
| hintArea | hintContent | source | absorbedAs | defaultStatus | frontendRecheckRequired | confirmationSourceNeeded |
| --- | --- | --- | --- | --- | --- | --- |
| api / field / status-flow / permission / route-menu / lov-lookup / attachment / import-export / ui-layout / component / interaction / other |  | `tds.md#...` | backend-contract / cross-end-constraint / ui-candidate / platform-candidate | confirmed / partial / generatedCandidate / conflict / not-applicable | yes/no | FDS / user / Figma / evidence / UI Contract / platform export / API doc |

## Contract Status Matrix
| 契约项 | 状态 | 来源 | 影响 | 下一步 |
| --- | --- | --- | --- | --- |
| 字段清单 | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | DataSet/Form/Table |  |
| 接口 URL/method | confirmed / partial / missing / conflict / not-applicable |  | service/transport |  |
| serviceRequestContract / standard request handling | confirmed / partial / missing / conflict / not-applicable |  | `request`、`getResponse`、API_HOST、servicePrefix、native HTTP 例外；标准 HZERO 无冲突时不问用户 import/helper 路径 |  |
| responseHandlingContract | confirmed / partial / missing / conflict / not-applicable | backendApiReadiness per API / API contract | `hzero-get-response`、DataSet-native、`dataKey/totalKey`、data envelope 或 project adapter；不得由页面猜测 |  |
| 请求/响应字段 | confirmed / partial / missing / conflict / not-applicable |  | 字段映射/提交 payload |  |
| frontendIdRuntimeContract | confirmed / partial / missing / conflict / not-applicable |  | ID-like 字段、route/path ID、Lov value、rowKey、DataSet primaryKey、`@Encrypt` 字段 | 按 `references/frontend-id-runtime-contract.md` 判定 |
| tenantContext / organizationId | confirmed / partial / missing / conflict / not-applicable |  | API path、request helper、附件/导入导出 |  |
| targetPlacement / 子模块落点 | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  | 真实代码目录、父工程注册、父工程 src 写入边界 |  |
| packageInternalPlacement / 包内业务落点 | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable |  | businessDomain、pageGroup、pageDir、routePrefix、menuGroup；packageDir 不能替代这些字段 |  |
| targetPlacementEvidenceStatus | ready / partial / missing / conflict / not-applicable |  | 工程证据、相似页面、routeConfig、平台菜单候选 | 只代表候选证据，不代表用户确认 |
| targetPlacementUserConfirmStatus | confirmed / needs-confirmation / missing / conflict / not-applicable |  | user-question / requirement-doc / FDS / TDS / platform-menu | 非 confirmed 时阻塞 Task / Implementation |
| route path / 菜单 path | confirmed / generatedCandidate / needs-confirmation / missing / conflict / not-applicable | user-question / generatedCandidate-rule / FDS / TDS / design-doc / routeConfig / platform-menu | 路由和页面入口 | 新增/改造页面先按规则生成候选；候选唯一时可进入 mock/demo，production confirmed 需用户或平台/routeConfig 证据；冲突或生产挂载要求时才触发 Route Menu Confirm |
| routeRedirectPolicy | forbidden / not-applicable / blocked / conflict | Design rule / routeConfig / Task / Handoff | route redirect 禁止策略 | 新生成 HZEROJS 子模块 route config 不得使用任何 `redirect` route；菜单仍指向父级 path 时，记录菜单/openTab/navigation 直接进入真实列表 path，不得记录父路由 redirect 到 `/list` |
| routeOpenMode / Tab 行为 | confirmed / generatedCandidate / needs-confirmation / missing / conflict / not-applicable | user-question / explicit-current-tab-design / explicit-drawer-design / FDS / TDS / design-doc / project-evidence / generatedCandidate | 页面打开方式、openTab、dynamic Tab、direct URL | confirmed 必须来自 Open Interaction Confirm 的 user-question，或明确 current-tab / Drawer / 抽屉等设计证据。默认 `demo-slice` / `minimum-codable` 可按内置规则写 `menu-current generatedCandidate + needs-confirmation` 作为 Open Interaction 候选，但不能进入 mock/demo runnable 实现；FDS/TDS/设计文档/工程 evidence 只能作为 recommendationEvidence。`dynamic-tab` 必须记录 `tabIdentityPolicy=route-path-exact`、`keyPathRelation=key===path`、`recordIdSource`、`pageModeSource` 与 route-matched concrete path；不得用纯记录 ID、标题或 route 不存在的后缀作 key |
| tabTitle / 页签标题 | confirmed / generatedCandidate / missing / conflict / not-applicable | user-question / FDS / TDS / design-doc / API / routeConfig / project-evidence / generatedCandidate | HZERO 系统页签或浏览器标题展示 | 必须区分 route 静态 `title` 与运行时 `openTab.title`；详情/编辑/标记等记录级入口若页签标题要承载记录身份，优先使用用户可读业务编号/名称字段，例如 `requisitionNumber`，不得把 `requisitionHeaderId`、数据库主键、加密 id 或纯技术 id 当作用户可见标题，除非 FDS/用户/项目基线明确要求显示该编号字段；缺业务显示字段时使用 route 静态中文标题并记录 fallback/replacement。dynamic-tab 的运行时标题必须从本次点击记录或已确认详情回读的同一业务显示字段生成，并在 `titleFormat` 中区分详情/编辑，例如“申请编号 - 详情/编辑”；不得让 key 来自记录 ID、标题却来自旧 record、泛化 route title 或另一条记录 |
| routeMode / dws | route / omitted-default-route / dynamic / missing / not-applicable |  | 当前 Tab 详情应为 route/default；每条记录独立动态 Tab 必须为 dynamic；同 pathname 不同 search 独立 Tab 需 dws=true |  |
| detailViewInteractionMap | confirmed / unresolved / missing / conflict / not-applicable | user-question / explicit-current-tab-design / explicit-drawer-design / FDS / TDS / design-doc / project-evidence / generatedCandidate | 每个 route page / list entry 的查看详情打开方式；Drawer 明确证据可直接 confirmed，不弹 question；默认 `demo-slice` / `minimum-codable` 无冲突时可写 `current-tab-page generatedCandidate` 作为候选，但仍必须 unresolved 并按 questionGrouping 进入 Open Interaction Confirm；required unresolved 阻塞 Task / Implementation |  |
| routeContext / editMode | confirmed / generatedCandidate / missing / conflict / not-applicable |  | id/isCreate/editFlag/pageMode、query 解析和编辑态权威来源 |  |
| Field Usage Matrix | pass / partial / missing / conflict / not-applicable |  | canonicalField / runtimeFieldPolicy / adapterAliasPolicy / forbiddenRuntimeAliases / storedField / renderedField / displayField / labelSource / component / renderer / submit/actionGuard 用途 | `*Meaning/*Name/displayField/renderer/Output` 展示字段必须有 label 来源；空子模块默认 canonical-only |
| field visibility matrix | pass / partial / missing / conflict / not-applicable |  | 字段存在来源与 create/edit/detail/list/query 展示时机拆分 | 缺失时不得进入 runnable Implementation |
| field editability matrix | pass / partial / missing / conflict / not-applicable |  | 字段在各 pageMode 的 editable/readonly/disabled/hidden 和组件策略 | 缺失时不得进入 runnable Implementation |
| empty/derived field UX rules | pass / partial / missing / conflict / not-applicable |  | 编号、合计、比例、无明细、审计字段等空态/派生/保存后生成规则 | 缺失时不得渲染只读空字段 |
| List Query Contract | pass / partial / missing / conflict / blocked / not-applicable | FDS/TDS/Figma/UI Contract/工程证据/用户确认 | `queryAreaPolicy`、Table queryBar、QueryDS/queryFields、fuzzyQuery、queryFieldsLimit、查询/重置/刷新行为 | `queryAreaPolicy` 为 `required-filter` 或 `required-fuzzy` 时必须闭合 Table filterBar 查询形态 + QueryDS/queryFields + enumProvenance；`none-by-design` 必须有 `sourceRef/reason` 且不得强制生成查询区；FDS/TDS/Figma/用户确认出现“搜索框 / 关键字搜索 / 模糊查询 / 顶部快速搜索”时，只有 `fuzzyQueryContractStatus=required-confirmed` 才能使本项为 pass；`unsupported-with-evidence` 必须保留 partial/blocked/conflict 和替代交互/降级说明；缺 `fuzzyQueryFields`、实现计划允许 `fuzzyQuery=false`，或计划写入 `queryBarProps.fuzzyQueryField/fuzzyQueryFields` 时不得进入 runnable Implementation |
| action entry matrix | pass / partial / missing / conflict / needs-confirmation / not-applicable |  | 动作存在来源与 detail-header/row-action/toolbar/hidden 入口位置拆分 | 缺失或 needs-confirmation 时不得把业务动作放入 Header |
| 权限适用性/编码 | confirmed / generatedCandidate / missing / conflict / not-applicable |  | required / not-applicable / unknown；PermissionButton/操作列 |  |
| Button Semantic Matrix | pass / partial / missing / conflict / needs-confirmation / not-applicable |  | Header 导航、业务状态动作、Table toolbar、行操作列、弹层 footer；sourceText/copyPolicy/copyOverrideSource；取消/返回/关闭语义 | 页面按钮或业务状态动作适用时必须闭合；默认 exact-source，文案改写需 copyOverrideSource；语义未确认时回 Design/Task 补矩阵或 question |
| i18n namespace/key | confirmed / generatedCandidate / missing / conflict / not-applicable |  | 多语言 |  |
| LOV/lookup/value set | confirmed / generatedCandidate / missing / conflict / not-applicable |  | Lov/Select/状态展示 |  |
| componentImportMap / componentApiProvenance | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | JSX 组件、权限按钮、Choerodon Pro 组件、renderer/helper、组件静态 API、项目 wrapper | 普通 Button 也必须记录 import 来源和权限适用性 reason；缺来源不得进入 runnable Implementation |
| enumImportMap / enumProvenance | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | DataSet/Table/Form/Button/Lov/Attachment/Modal enum-like props | 组件 props 必须 enum；DataSet 配置类按项目 enum/string 策略；不得把 reference import 当项目 confirmed |
| typescriptRenderContract | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | Table columns、renderer 参数、buttons 数组、ColumnProps/ColumnRenderProps/Buttons 来源 | tsc 可编译写法；不得用 broad `as any`、裸字符串 enum 或 `condition && <Component>` 数组项绕过 |
| 上传/附件协议 | confirmed / partial / missing / conflict / blocked / not-applicable |  | attachmentComponentMode、Attachment Contract；默认 Attachment / project-wrapper，Upload 需确认降级原因 |  |
| 导入协议 | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | Import / upload / result handling |  |
| 导出协议 | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | ExcelExportPro / column query / export request |  |
| Mock API Contract | confirmed / partial / missing / conflict / not-applicable |  | HZERO devServer middleware / mock API mount / runtime store / delivery ceiling |  |

## Field Usage Matrix
字段存在、存储字段、展示字段和页面真正渲染字段必须拆开。尤其是 `authorizationStatus -> authorizationStatusMeaning -> TagRender`、`applicantId -> applicantName`、`supplierId -> supplierName` 等 code/id + meaning/name 场景，不能只确认字段存在。

| field | canonicalField | runtimeFieldPolicy | adapterAliasPolicy | forbiddenRuntimeAliases | storedField | renderedField | displayField | label | labelSource | component | renderer | form/table/query/action/payload usage | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| authorizationStatus / applicantId / other | authorizationStatus / applicantId | canonical-only / not-applicable | none | [] | authorizationStatus / applicantId | authorizationStatusMeaning / applicantName | authorizationStatusMeaning / applicantName | 审批状态 / 申请人 | current-field / stored-field / explicit-props / i18n-key / missing | Output / Tag / Lov / TableColumn / other | TagRender / project-renderer / none | form-display / table-display / actionGuard-code / submit-code / query / not-applicable | confirmed / partial / missing / conflict / not-applicable |

判定规则以 `frontend-ui-contract-guardrails.md`、`frontend-ui-runtime-gates.md` 和 generated-code static gate 为准；本表只记录当前 feature 字段证据和状态。

## Choerodon Enum / Type Contract
新增或改造 HZERO + Choerodon、DataSet、Pro Table/Form/Button/Lov/Attachment、renderer/helper 或 enum-like props 时必填；不涉及这些对象时写 `not-applicable + reason`。本节是 Implementation 前置合同，不能留到 Review 首次发现。

| contractItem | target | strategy | importPath / typeSource | provenanceStatus | sourceEvidence | implementationRule | taskAcceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| enumImportMap | FieldType / DataSetSelection / DataToJSON / SelectionMode / TableQueryBarType / TableEditMode / ColumnLock / ColumnAlign / LabelLayout / ButtonColor / FuncType / other | project-enum-confirmed / asset-baseline-enum / dataSet-confirmed-string / needs-decision / blocked / not-applicable |  | confirmed / generatedCandidate / missing / conflict / not-applicable |  | 缺项目 enum 证据时默认 asset fallback 只能 generatedCandidate；组件 props 必须 enum-first；Table `selectionMode` 用 `SelectionMode.*`，不得误用 `DataSetSelection.*`；mixed/missing 不得进入 runnable Implementation |  |
| stringStylePolicy | DataSet.fields.type / DataSet.selection / DataSet.dataToJSON / component props | dataSet-confirmed-string / forbidden / not-applicable |  | confirmed / missing / not-applicable |  | `confirmed-string` 仅可用于 DataSet 配置类枚举且必须来自同一目标工程健康样例；弱类型或组件 props 字符串必须进入 `rejectedPatternItems`，不得作为策略值或新增实现形态 |  |
| typescriptRenderContract | Table columns / renderer / buttons / table toolbar buttons / PermissionButton / DataSet options | typed-columns / typed-renderer / typed-buttons / local-options-dataset / blocked / not-applicable | ColumnProps / ColumnRenderProps / RenderProps / Buttons / project wrapper type / asset reference | confirmed / generatedCandidate / missing / conflict / not-applicable |  | 禁止 broad `as any/as unknown`、`columns as any`、无类型 renderer 参数、`buttons={[condition && <Component />]` 和 raw array options；本地 options 内层 DataSet 默认 `new DataSet({ data, selection: false, paging: false })`，外层普通列表 DataSet 仍优先 `autoQuery=true` |  |
| validationRiskHandoff | c7n-component-api / enum-provenance / typescript-render / other | risk-domain-present / not-applicable | candidateTargets only；exact validatorCommand 由 Task/Verify owner 生成 | planned-hint / not-applicable |  | Design 只传递风险域和候选 target；required validator、command、target 和失败回退由 Task / Verify / Review owner 决定 |  |

规则：
- `enumImportMapStatus=not-applicable` 只允许本轮完全不新增/修改 enum-like props，并必须写 reason。
- `confirmed-string` 只允许用于 DataSet 配置类枚举，并且需要局部、结构化、可追溯：至少包含 `enumProvenance`、`enumTarget`、`enumSource`、`enumReason`，且只覆盖对应 target；不得用文件级宽泛注释放行。Table/Form/Button/Lov/Attachment/Modal/Drawer/Dropdown 等组件 props 即使命中健康字符串证据，也必须改为 enum 形态或项目 confirmed 等价 enum 导出。
- 弱类型存量字符串写法只能形成 `rejectedPatternItems` / migration finding；不能写入 `stringStylePolicy`，新增代码必须使用 confirmed enum，或由 Design/Task 选择健康的 DataSet confirmed-string 策略。
- 本节任一 required 项为 `missing/conflict/blocked/needs-decision` 时，`Can Enter Implementation` 必须为 no，或只能拆 backfill/确认任务。

## HZERO Page Skeleton / Scroll Boundary Contract
新增或改造 HZERO 页面、详情页、头行主从页、Tab 明细页或使用 `Header` / `Content` 时必填；不涉及 HZERO Page 容器时写 `not-applicable + reason`。本节必须在 Design 阶段闭合，不能留给 Implementation 自行选择。

| item | target | designDecision | provenanceStatus | sourceEvidence | implementationRule | negativeAcceptance |
| --- | --- | --- | --- | --- | --- | --- |
| pageRoot | page entry JSX | Fragment sibling `Header + Content` / PageHeaderWrapper confirmed / project wrapper confirmed / blocked / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable | UI Contract / project HZERO Page layout / confirmed golden-baseline | `Header` 与 `Content` 作为 Fragment 下相邻根节点 | 不得用业务 `<div className="*-page/*-detail">`、`section`、`main` 或 Provider 包住整组 `Header + Content` |
| pageProvider | page entry JSX | no-provider / confirmed-provider / blocked / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable | UI Contract / confirmed golden-baseline / explicit requirement | 默认不引入 `UrlHistoryProvider`、`HistoryProvider`、`ConfigProvider` 或自定义 Provider 包裹页面骨架 | 无来源 Provider 包住 `Header + Content` |
| businessContainer | Content children | inside-Content / Content className confirmed / wrapperClassName confirmed / blocked / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable | UI layout / project evidence / style necessity contract | 业务 className、section 背景、底部 padding 和滚动样式放在 `Content` 内部 | 业务容器包住 `Header + Content` |
| scrollBoundary | Content / page content | page-content-scroll / confirmed-container / blocked / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable | UI Contract / manual checklist | 长内容可滚到最后区块；详情/头行页明细表默认自然撑开 | 滚动容器不明、固定层遮挡、动态 `autoHeight maxHeight` 无稳定高度 |

规则：
- 本节任一适用项为 `missing/conflict/blocked` 时，`Can Enter Implementation` 必须为 no，或只能拆 backfill/确认任务。
- `pageRoot` 不能只写“Header + Content”自然语言；必须写明 Fragment sibling roots 与负向验收。
- 业务 wrapper 如果确需存在，必须在本节说明其位于 `Content` 内部；不能作为整页骨架外层。

## Detail Region Surface Contract
新增或改造详情页、头行主从页、Tab 明细页时必填；不涉及详情区域时写 `not-applicable + reason`。本节只记录区域承载面，避免 Implementation / Review 修复阶段自行移动或包裹区域。

| region | expectedSurface | forbiddenSurface | requiredVisibleByDefault | source | status | negativeAcceptance |
| --- | --- | --- | --- | --- | --- | --- |
| header-fields / basic-info | Content / Content > BasicInfoSection / Form owner record | Tabs.TabPane / Table.buttons / Header children | yes / no + source | Detail Contract / FDS / Figma / UI Contract / user-confirmation | confirmed / generatedCandidate / missing / conflict / not-applicable | 不得新增 `basic/basicInfo` TabPane 或把基本信息 Form 放入 Tabs，除非来源明确允许 |
| detail-tabs / line-section | Content > DetailTabs > Tabs.TabPane(lines) / Content > LineSection | Header / page-toolbar / basic-info Form | yes / no + source | Detail Contract / FDS / Figma / UI Contract / user-confirmation | confirmed / generatedCandidate / missing / conflict / not-applicable | 不得用裸 Table 替代 required Tab；不得把明细工具栏上提 Header |

规则：
- 缺特殊来源时，基本信息 Form 默认 `expectedSurface=Content`、`forbiddenSurface=Tabs.TabPane`、`requiredVisibleByDefault=yes`；明细 Tabs 默认 `tabsScope=line-sections-only`。
- 任一 required 区域 `missing/conflict/blocked` 时，不得进入 runnable Implementation；只能拆 UI Contract / Task backfill 或用户确认。

## Field Visibility Matrix
字段存在来源与展示策略必须拆开。字段出现在 FDS/TDS/API/DTO/详情字段清单中，不等于 create/edit/detail/list/query 均展示。

| field | label | fieldExistsSource | create | edit | detail | list | query | displayTiming | hiddenReason | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| requisitionNumber / totalAmount / budgetRate / creationDate / lineList / other |  | FDS / TDS / API / DTO / Figma / engineering evidence | visible / hidden / readonly-placeholder / not-applicable | visible / hidden / readonly-placeholder / not-applicable | visible / hidden / not-applicable | visible / hidden / not-applicable | visible / hidden / not-applicable | before-save / after-save / after-line-change / backend-return / no-detail-hide / always |  | FDS/TDS/API/Figma/工程证据/user-confirmation | confirmed / generatedCandidate / missing / conflict / not-applicable |

判定规则：`requisitionNumber`、`totalAmount`、`budgetRate`、`creationDate/lastUpdateDate/createdBy/lastUpdatedBy/objectVersionNumber` 等字段必须逐字段明确 create 态的 `visible / hidden / readonly-placeholder`、displayTiming、hiddenReason 和来源，不能只写“字段属于详情页”或按字段类别推导默认隐藏；已有主键 detail/readonly 态是否显示同样按 UI Contract 的字段矩阵决定。

## Field Editability Matrix
| field | label | pageMode | editability | component | readonly/disabled/hidden reason | defaultValueSource | submitPolicy | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | create / edit / copy / detail / approval / readonly / mixed | editable / readonly / disabled / hidden | TextField / Select / NumberField / DatePicker / Lov / Attachment / Output / project component |  | FDS/TDS/API default / backend-generated / user-context / copy-source / none | include / exclude / display-only / not-applicable | FDS/TDS/Figma/工程证据 | confirmed / generatedCandidate / missing / conflict / not-applicable |

判定规则：create/edit/copy 可编辑字段不得被详情 `Output` 模板误锁；readonly/disabled/hidden 必须有来源，缺来源时不得让 Implementation 自行降级。

## Empty / Derived Field UX Rules
| field | label | fieldClass | generationTiming | derivedFrom | createUx | editUx | detailUx | emptyText / placeholder | occupyLayoutWhenEmpty | submitPolicy | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| requisitionNumber / totalAmount / budgetRate / lineList / creationDate / other |  | backend-generated / frontend-derived / backend-calculated / aggregate / audit-generated / optional-detail / other | before-save / after-save / after-line-change / backend-return / user-input / not-applicable | line amount / budget amount / backend rule / none | hidden / readonly-placeholder / visible-empty / not-applicable | hidden / readonly-placeholder / readonly-value / editable / not-applicable | hidden / readonly-value / empty-state / not-applicable | 保存后自动生成 / 暂无明细 / not-applicable | yes / no / source-required | include / exclude / display-only / not-applicable | FDS/TDS/API/Figma/user-confirmation | confirmed / generatedCandidate / missing / conflict / not-applicable |

判定规则：禁止“只读空字段”直接上页面；只能隐藏、显示确认文案或使用明确空态组件。后端生成、后端计算、保存后回填、前端派生但后端为准的字段，必须写 generationTiming、derivedFrom 和 submitPolicy；无明细时隐藏区块还是显示空态，必须在本表确认，不能由 Implementation 猜。

## Action Entry Matrix
业务动作存在与按钮入口位置必须拆开。状态流/API/FDS/TDS 中存在动作，不等于详情 Header、列表行操作或工具栏必须出现按钮。

| actionId | label | actionExistsSource | sourceSectionPath | sourceRegion | sourceRegionReason | statusActionRef | allowedEntryLocations | chosenEntryLocation | uiArea | pageModes | entryStatus | source | overrideSource | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| save / submit / cancel-navigation / cancel-business / withdraw / void / delete / other |  | FDS / TDS / API / status-flow / Figma / project evidence / user-confirmation | fds.md#heading / tds.md#heading / figma node / evidence path | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | why this region maps to chosenEntryLocation | not-applicable / Status Action Matrix actionId | detail-header / page-toolbar / row-action / table-toolbar / line-row / modal-footer / hidden | detail-header / page-toolbar / row-action / table-toolbar / line-row / modal-footer / hidden / not-confirmed | page-header / business-state-actions / row-action / table-toolbar / modal-footer / other | create / edit / detail / list / approval / readonly | confirmed / generatedCandidate / needs-confirmation / missing / conflict / not-applicable |  | not-applicable / UI Contract / user-confirmation / Figma / project-baseline | implement / block-and-confirm / keep-hidden / demo-only-with-risk / not-applicable |

判定规则：
- 详情 Header 只允许 `entryStatus=confirmed` 且 `chosenEntryLocation=detail-header/page-header` 的按钮进入实现。`cancel-navigation` 与 `cancel-business` 必须拆行；FDS 页面按钮区只写“取消/返回”时默认是导航动作，不能绑定取消单据 API。
- `cancel-business`、`withdraw`、`void`、`delete` 等业务状态动作若只有状态流/API 来源，入口位置写 `needs-confirmation` 或 `hidden/not-confirmed`，并进入 Blocking Clarifications 或保持隐藏。项目同类页面常见按钮只能作为 `generatedCandidate`，不能单独把入口位置置为 confirmed。
- 列表或明细表章节下的“列表头按钮区 / 明细表列表头按钮区”默认 `chosenEntryLocation=table-toolbar`。若改为 `page-toolbar` 或 Header，必须写 `overrideSource=UI Contract / user-confirmation / Figma / PageSchema`；仅因文案包含“头”字不得归类为页面 Header。

## Component Import / API Provenance Contract
- required：yes / no
- componentImportMapStatus：ready / partial / missing / not-applicable
- componentApiProvenanceStatus：confirmed / partial / generatedCandidate / missing / conflict / not-applicable
- projectComponentStyle：confirmed-imports / generated-candidate / mixed-needs-decision / missing / not-applicable

| symbol | usage | importSource | importPath | exportShape | apiEvidence | permissionRequirement | status | replacementRequired | modalLifecycleContract | closeApiSource | closeApiEvidence | customHeaderFooterPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Button / ButtonPermission / Table / Form / Tabs.TabPane / Modal.open / TagRender / c7nOperatorRender / Import / ExcelExportPro / Attachment | JSX / namespace / static-method / helper-function / project-wrapper | builtin-standard / project-evidence / adjacent-module / package-doc / generatedCandidate / current-file / missing / not-applicable |  | named / default / namespace / static-member / current-file / unknown |  | required / not-applicable / unknown | confirmed / generatedCandidate / missing / conflict / not-applicable | true / false | required / confirmed / blocked / not-applicable | return-proxy / children-modal-prop / header-closeBtn / static-close / project-wrapper / blocked / not-applicable |  | default-close-only / custom-header-with-confirmed-close / custom-footer-with-confirmed-close / blocked / not-applicable |

判定规则：
- 所有将进入代码的 JSX tag、组件变量、`Component.SubComponent`、命名空间/静态方法和 renderer/helper 函数都必须出现在本表；普通 `<Button>` 也必须有 import 来源和 `permissionRequirement` 结论。`builtin-standard/project-evidence/adjacent-module` 可支撑 confirmed；`package-doc/generatedCandidate` 只能支撑 generatedCandidate，不能单独支撑 production-ready。
- `builtin-standard` 表示已加载 `front-hzero-enterprise-process-control` 的标准 import 坐标 reference 或 owner reference 明确固化的内置标准坐标、固定 helper 或标准 UI 入口，目标工程证据只用于发现 wrapper/override、兼容性或冲突；缺少目标工程 import 样例不得把该行降级为 `partial/missing/generatedCandidate`。
- 标准组件、固定 helper、Page alias、i18n、权限按钮、renderer、导入导出、常用 Choerodon 类型和 HZERO 通用组件必须优先消费 `frontend-standard-import-coordinates.md`。表内 `builtin-standard` 行按内置规则直接 confirmed，importPath 必须填写该标准坐标；存量 `CommonImport` / `ExcelExport` 只记录为迁移 finding。
- `status=missing/conflict`、`importPath=missing/unknown` 或 `permissionRequirement=unknown` 且涉及业务动作时，Contract Check 结论不得为 ready；必须进入 Blocking Clarifications / Task backfill。目标工程证据否定标准坐标或与项目 wrapper 冲突时，状态写 `conflict/blocked` 并回 Evidence/Design；不得用本地 `HeaderImportAction`、`HeaderExportAction`、`ImportExportActions`、`*ImportAdapter`、`*ExportAdapter`、`*ImportWrapper`、`*ExportWrapper` 作为 importPath 缺失的替代。
- Implementation 不得把“手动补 import”当作契约闭合；补 import 后仍需把来源回写到本表、UI Contract 和 Task Acceptance。`Modal.open` / Drawer / 业务弹层出现自定义 header/footer/children、关闭按钮、保存后关闭、记录级导航或 update 行为时，`modalLifecycleContract` 必须为 `required/confirmed` 并写清 `closeApiSource` 与 `closeApiEvidence`；缺证据时只能使用组件内置关闭入口、已确认 `header closeBtn` / `children.modal` / 返回 proxy，或进入 Task backfill。

## Style Necessity Contract
页面布局契约不等于样式文件契约。前端设计必须先判断“组件默认布局 / 组件 props / 项目已有 class”是否足够，再决定是否需要样式文件。

| target | layoutNeed | componentFirstDecision | styleFilePolicy | styleScope | source | status | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| page / content / section / form / table / modal / drawer / line-table / other | page-skeleton / spacing / scroll-boundary / background / fixed-height / responsive / visual-state / none | component-props-sufficient / existing-project-class-sufficient / style-required / unknown | no-new-style / reuse-existing-style / modify-existing-style / new-local-style / block-and-confirm | none / Content-inner-only / section-only / table-container-only / modal-body-only / other | Figma / UI Contract / project baseline / runtime gate / user-confirmation / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable | no-style-task / reuse-only / implement-local-style / block-and-confirm |

判定规则：
- 只有 `componentFirstDecision=style-required` 且 `styleFilePolicy=modify-existing-style/new-local-style` 有来源时，Task Breakdown 才能拆样式实现任务；`component-props-sufficient` 或 `existing-project-class-sufficient` 时，样式任务必须为 `no-style-task/reuse-only`，不得新建 `style.less`。
- `unknown/missing/conflict` 不得进入 runnable Implementation，必须回 UI Contract 补充样式必要性判断；样式只能解决组件无法覆盖的局部布局/滚动/间距问题，不得用自定义样式复刻组件库外观、包裹整组 `Header + Content` 或改变无来源视觉层级。

## Frontend Callable API Contract
- requestMode：
- requestHelper：symbol / importPath / evidence
- baseUrlStrategy：request-adds-api-host / explicit-base-url / external-absolute-url / missing
- envSource：
- resourcePath：/v1/{organizationId}/... / missing / not-applicable
- servicePrefix：confirmed prefix / generatedCandidate / missing / not-applicable
- servicePrefixSourcePriority：common-config / similar-service / backend-service-code / user-confirmed / missing / not-applicable
- servicePrefixHelperFile：existing-common-config / packages/<module>/src/utils/servicePrefix.ts / not-applicable / missing
- switchEnvVar：<MODULE>_USE_MOCK / not-applicable / missing
- mockDefaultPolicy：default-mock-explicit-false-to-production / production-only / not-applicable
- realApiCandidateBranch：generated / not-generated / not-applicable；status=confirmed / partial / generatedCandidate / missing；reason：
- actionServiceSwitchPolicy：shared-service-functions / separate-mock-only / blocked / not-applicable；save/delete/submit/withdraw/void/copy 等动作是否共用 payload builder、状态 guard、response adapter：
- responseHandlingContract：逐 API 写 `hzero-get-response / dataset-native / dataset-data-key-total-key / data-envelope / project-adapter / not-applicable`、证据和 consumer；非 DataSet action 的 `hzero-get-response` 是 HZERO baseline，DataSet read 不强制使用它：
- nativeHttp：allowed / prohibited / needs-confirmation；confirmationSource / reason
- pagination / sorting / filtering：
- responseShape：
- errorShape：
- securityToken / headers：
- status：confirmed / partial / missing / conflict / not-applicable

判定规则：
- API/MDS 中的 `/v1/{organizationId}/...` 只能确认 `resourcePath`，不能自动确认 `servicePrefix`。
- servicePrefix 优先来自项目公共配置或 env helper；没有公共配置时再读相似 service；只有服务编码时只能生成候选，例如 `HSPD -> /hspd`。
- 不得假设存在 `packages/*-common`；无公共配置时允许在业务包内生成本地 `src/utils/servicePrefix.ts`，但候选前缀必须进入 production replacement。
- mock/demo 默认走当前 dev server origin + `/_mock/<module>`；`/_mock/<module>` 只作为 middleware mount，不能作为交给 HZERO request 的裸 service prefix；只有 `<MODULE>_USE_MOCK=false` 精确字符串才切真实 `/<servicePrefix>`。
- 可切换双链路已具备相同 API 路径、payload、响应消费和 action service 时，必须记录 `initialSwitchMode=env-switch-only`、`switchEnvVar` 和 `productionEnvValue=false`。保留 `dev-mock/**` 源码；首次集成试连不删除 mock handler/plugin/store，也不修改应用源码。
- mock/真实响应消费、字段或 adapter 是否一致在本阶段只写入 advisory，等待独立联调测试的实际 Network/页面结果；不得预先选择 `env-switch-plus-adapter` 或创建替换任务。local-filter、inline mock 或页面内存成功路径属于当前 Mock demo 质量缺陷，应按既有门禁修复，不能留到首次真实试连时 cleanup。
- mock/demo 可同步生成真实 API 候选分支，但必须保持默认 mock；真实分支状态为 partial/generatedCandidate 时进入 Production Replacement Draft，不得声明 production-ready。若缺 URL/method/payload/response 或 tenantContext 基础事实，`realApiCandidateBranch=not-generated` 并写 missing，不得编造 endpoint。
- `queryMode=production-transport` 只能在真实前端可调用契约闭合，且 `runtimeDataPathDecision=real-contract`、`remoteBackendRequestAuthorization=confirmed` 后写入。仅有 `apiContractStatus=documented` 时应写 `queryMode=partial/unknown/blocked`，或在默认 mock demo 决策下写 `mock-request`。

## Runtime Data Entry Contract
- runtimeDataEntryStatus：confirmed / partial / missing / conflict / not-applicable
- ownerPolicy：dataset-transport / service-action / confirmed-hybrid-wrapper / blocked
- driftPolicy：no-duplicate-entry / shared-helper-only / blocked-on-drift

| scope | action | owner | pageTrigger | dataSetTransport | serviceFunction | endpoint/method | payloadBuilder | responseAdapter | mockHandler | runtimeStore | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| header / line / master-detail / status-action | read / save / submit / delete / withdraw / void / copy | DataSet transport / service action / confirmed hybrid wrapper / blocked | button handler / DataSet submit / page effect | HeaderDS.submit / LineDS.submit / read/create/update/destroy / none | service function name / none |  | shared pure helper / DataSet dataToJSON / service-action mapper / missing | shared adapter / DataSet keys / missing | same route / same store / missing | same store / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable |

判定规则：
- DataSet 管理的 read/create/update/destroy/submit 请求默认由 DataSet `transport` 直接承接，`transport` 返回 DataSet 可消费的 request config，不 import 或调用业务 service；页面 service action 只用于提交、撤回、作废、复制、导出等非 DataSet 生命周期动作，或 Design 明确声明 `runtimeDataEntry.owner=service-action` 的场景。
- `confirmed-hybrid-wrapper` 只表示 DataSet transport 与页面 service action 共享纯 helper / request adapter，不表示 DataSet transport 委托业务 service。DataSet `transport.submit/create/update/destroy` 与页面 service 手工保存不能并列成为两个权威入口；若两者同时存在，必须证明其中一个退出运行入口，并共享 endpoint、payloadBuilder、responseAdapter、mockHandler 和 runtimeStore。
- 主从页面必须逐项写 header/line 保存粒度和字段映射。HeaderDS submit、LineDS submit、页面 service save、mock route 不能各自拼一套 payload；缺少本表时，Implementation 不得自行选择 `ds.submit()` 或 service 手工保存，只能返回 Design / Task Breakdown 补契约。

## Tenant Context Contract
- required：yes / no
- source：
- resolverProvenance：symbol / importPath / definedInCurrentChange / evidence
- rolePolicy：tenant / site / mixed / not-applicable
- userOrganizationUsage：allowed / prohibited / not-applicable；reason
- injection：path / query / body / request-helper / not-applicable
- status：confirmed / partial / missing / conflict / not-applicable

## Frontend ID Runtime Contract
- ID-like fields：
- declaredType：
- runtimeType：string / string[] / number-exception / not-applicable
- normalizationPolicy：
- encryptedIdPolicy：
- exceptions：
- status：confirmed / partial / missing / conflict / not-applicable

## Target Placement Contract Summary
- placementType：new-package / existing-package / parent-src-page / integration-only / unknown / not-applicable
- targetProject：
- packageDir：
- businessDomain：
- pageRoot：src/pages / src/routes / custom / missing / conflict / not-applicable
- pageRootSource：asset-baseline / project-evidence / adjacent-module / existing-file / user-confirmed / generatedCandidate / missing / not-applicable
- pageGroup：
- pageDir：
- pageRootDecision：default-pages / existing-routes-exception / invalid-routes-candidate / custom-confirmed / not-applicable
- pageRootExceptionProof：none / evidence-paths-present / missing
- pageRootEvidencePaths：[]
- pageRootDecisionResult：pass / failed / blocked / not-applicable
- routePrefix：
- menuGroup：
- packageInternalAmbiguity：none / multiple-business-domains / multiple-route-prefixes / multiple-candidates / missing-evidence / not-applicable
- parentRegistrationPath：
- parentRegistrationEntryPolicy：minimal-name-only / schema-confirmed-extra-fields / missing / conflict / not-applicable
- parentRegistrationExtraFieldSource：active-schema / project-baseline / platform-required / user-confirmed / none / not-applicable
- parentSrcWritePolicy：
- forbiddenBusinessPaths：
- evidenceStatus：ready / partial / missing / conflict / not-applicable
- userConfirmStatus：confirmed / needs-confirmation / missing / conflict / not-applicable
- confirmationSource：user-question / requirement-doc / FDS / TDS / platform-menu / none / not-applicable
- status：confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable

判定规则：
- `status=confirmed` 必须同时满足 `userConfirmStatus=confirmed`，且确认来源为用户明确确认、需求/FDS/TDS 明确指定或平台菜单配置确认。工程搜索证据、相似页面、历史目录、routeConfig 或主流程探索摘要只能闭合 `evidenceStatus`，不能单独闭合 `userConfirmStatus`。
- 若 `packageDir` 来自主流程输入的“目标模块/微包”或 Explore 候选，但未记录上述确认来源，`targetPlacement / 子模块落点` 与 `packageInternalPlacement / 包内业务落点` 必须写 `generatedCandidate / needs-confirmation`，并在 Blocking Clarifications 中新增 `Target Placement Confirm`。
- 进入 Task Breakdown / runnable Implementation 前，`userConfirmStatus` 必须为 `confirmed`；否则 `Contract Check Conclusion` 的 runnable Implementation 结论为 `no`。
- 新建/生成 HZEROJS 子模块页面默认且固定为 `pageRoot=src/pages`、`pageRootSource=asset-baseline`、`pageRootDecision=default-pages`。无可采纳参考模块、参考资产缺失/不可读、或仅有 FDS/TDS/后端 handoff/生成规则/用户笼统确认时，候选 `pageDir=packages/<module>/src/routes/**` 必须写为 `pageRootDecision=invalid-routes-candidate`、`pageRootDecisionResult=failed`，并自动纠正为 `packages/<module>/src/pages/**`；不得把该候选冻结为 confirmed/ready。
- `pageRoot=src/routes` 只允许用于改造已存在的存量页面。Contract Check 必须同时记录 `pageRootSource=existing-file/project-evidence/adjacent-module`、`pageRootDecision=existing-routes-exception`、`pageRootExceptionProof=evidence-paths-present` 和具体 `pageRootEvidencePaths`；缺任一项时 `pageRootDecisionResult=blocked`，只能进入 Target Placement Backfill，不得进入 runnable Task Breakdown 或 Implementation。
- 父工程 `packages-config` / `hzeroMicro.packages` 新增子模块时，默认条目为 `{ name: '<module>' }`。`initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段缺少 active schema / 项目 confirmed baseline / 平台强制要求 / 用户确认来源时，`parentRegistrationEntryPolicy` 不得为 pass；`registerRegex` 默认由子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex` 闭合。

## Import / Export / Attachment Contracts
### Master Detail Contract
- status：confirmed / generatedCandidate / partial / missing / conflict / blocked / not-applicable
- pageShape：header-line / header-line-tabs / list-detail-lines / line-only / not-applicable
- headerPrimaryKey：
- linePrimaryKey：
- headerLineForeignKey：
- lineDataMode：embedded-local-lines / line-query-transport / mixed / missing / not-applicable
- lineQueryDataSet：required / optional / forbidden / missing / not-applicable
- lineReadSource：detail-response / line-query-api / mixed / missing / not-applicable
- lineReadRefreshPolicy：header-refresh / line-query-refresh / mixed / missing / not-applicable
- saveGranularity：header-cascade-lines / header-only / line-separate / mixed / blocked / not-applicable
- lineDeleteMode：local-remove-before-save / replace-all-on-save / service-delete / mixed / missing / not-applicable
- persistedLineDeletePolicy：confirmed / generatedCandidate / missing / conflict / not-applicable
- unsavedLineDeletePolicy：confirmed / generatedCandidate / missing / conflict / not-applicable
- dataToJSONStrategy：dirty / all / selected / custom / missing / not-applicable
- handPayloadPolicy：dataset-submit / shared-payload-builder / generatedCandidate-normalizer / blocked / not-applicable

规则：
- 头行/主从页面适用时，`lineDataMode`、`lineDeleteMode`、`saveGranularity`、`lineReadSource` 和 `handPayloadPolicy` 必填；缺失时不得把 `lineQueryDS.ts`、`loadData + normalizeLines` 或 `lineDS.delete()` 视为可直接实现的默认方案。
- `lineQueryDataSet=required` 时，Task/Implementation 不得只生成 `lineQueryDS.ts` 文件而不接入明细表 `queryDataSet/transport`。
- `lineDeleteMode=service-delete` 时必须有独立删除 action；`replace-all-on-save` 时必须写明 persisted line 删除由整体保存覆盖实现；`local-remove-before-save` 只适用于未落库行或设计明确允许的 demo-only 行为。
- `generatedCandidate-normalizer` 只能用于 mock/demo 或临时契约，必须进入 replacement；宣称 production-compliant / production-ready 时应收敛为 `dataset-submit` 或 `shared-payload-builder`。

### Import Flow Contract
- status / requirement / importComponentMode / source / questionGate / minimumStandardEntryStatus
- entryWrapperPolicy / entryWrapperEvidence / component / importPath / importSource / wrapperEvidence
- templateCode / importCode / prefixPath / action / uploadEndpoint / requestParams / paramPlacement / templateDownload / resultHandling / errorDetailDownload / closeRefreshPolicy / backPath
- parentIdPolicy / unresolvedParentBehavior / tenantContext / permissionCode

### Export Request Contract
- status / requirement / exportComponentMode / source / questionGate / minimumStandardEntryStatus
- entryWrapperPolicy / entryWrapperEvidence / component / importPath / importSource / wrapperEvidence
- columnQueryRequest / exportRequest / queryParamsTypePolicy / queryColumnProps / allBody / fakePost / extraConditions / selectedColumns / fileConfig / defaultFileType / exportAsync / templateCode
- parentIdPolicy / unresolvedParentBehavior / invalidPlaceholderPathPolicy

### Attachment Contract
- status / requirement / attachmentComponentMode / component / importPath / exportShape / importUsage / wrapperEvidence / fallbackReason
- attachmentField / valueStructure / attachmentUuidPolicy / bucketName / bucketDirectory / storageCode / template / contractValueStatus / generatedCandidateCarrier / forbiddenUsage
- uploadAction / requestParams / uploadImmediately / previewProtocol / downloadProtocol / downloadAllProtocol / removeProtocol / removeConfirm / removeImmediately / historyProtocol / orderProtocol / sortable / chunkProtocol / tenantContext / permissionCode / runtimeValidation

Import / Export / Attachment 默认按本模板字段和 production compliance gate 落盘，并记录对应 specialty trigger；只有专项 owner reference 已加载时，才引用 `front-hzero-import-export` 或 `front-hzero-attachment` 细则。

### HZERO Common Component Contract
- status：confirmed / partial / missing / conflict / blocked / not-applicable
- component：ChunkUploader / NewRichTextEditor / RichTextViewer / project-wrapper / missing / not-applicable
- importPath / wrapperEvidence：
- hzeroFrontVersion：confirmed / generatedCandidate / missing / not-applicable
- bindingMode：upload-button / controlled / dataset-field / viewer / project-wrapper / not-applicable
- valueShape：Delta / Delta.ops / string-candidate / attachmentUUID / url / not-applicable / missing
- uploadProtocol：action / method / prefixPatch / uploadMode / bucketName / directory / storageCode / paramsData / fileSize / chunkSize / attachmentUUID / privateBucket / accept
- richTextProtocol：FieldType.object / FieldType.intl / toolbar / removeButtons / readOnly / showValidation / intl / viewerDeltaOps
- attachmentConfig：importPath / exportShape / targetProp / wrapperApi / not-applicable
- runtimeValidation：render / interaction / upload / callback / edit / validation / readonly / intl / preview / error

## Mock API Contract
| fieldGroup | required fields |
| --- | --- |
| decision | queryMode / mockDemoDecisionStatus / mockApiMode / productionBuildImpact / deliveryCeiling / status |
| devServer | devServerExtensionPoint / devServerExtensionEvidence / middlewareRegistration / startupEntry / serviceMiddlewarePathConsistency |
| request path | requestWrapperMockConflict / requestBypassPrefix / requestBypassRemediation / businessApiPath / mockApiMount |
| files and registration | mockHandlerFile / mockPluginFile / parentRootMockPluginRegistration / parentMockPluginRegistrationEvidence / packageStartMockPluginSource / invalidMockPluginRegistrationSites / mockPluginTemplateCompliance / mockPluginSelfCheck / mockPrefixOriginPolicy |
| data | pageResponseShape / mockRuntimeStoreRequired / affectedStateActions / dependencyPolicy / mockResponseValuePolicy / mockValueSourceLedger |

Mock request 默认按 Explore/Evidence 已确认的目标工程、父子模块落点、写入范围、HZERO/Umi 托管形态和 request/servicePrefix 证据，加本模板字段组直接形成 Contract Check，并记录 `specialtyTriggers[]=mock-request`。历史 `_smock/smock/sproxy/.smockrc/*.mock.js` 不作为默认字段来源，也不因未探索而阻塞默认 mock demo；只有满足专项加载条件并已读取 owner reference 时，才以 `front-hzero-mock-request` 的 Design Contract 补充判定细则。

## Production Replacement Draft
适用：存在 mock/demo、generatedCandidate、临时平台契约或 production-ready 缺口时必填；纯生产契约已闭合时写 `not-applicable + reason`。

| replacementItem | currentState | requiredProductionState | owner | blockingProductionReady | next |
| --- | --- | --- | --- | --- | --- |
| API / field-shape / permission / route-menu / route-title / i18n / lov-lookup / bucket / templateCode / import-export / attachment / mock-runtime-path / tenantContext / serviceRequestContract / responseHandlingContract |  |  | frontend / backend / platform / user | yes/no | `dev-mock` source can remain; only production runtime-connected mock is a cleanup item |

## Blocking Clarifications
| id | category | question | options / needed input | blockingStage | defaultIfUnresolved |
| --- | --- | --- | --- | --- | --- |
|  | missing-contract / conflict / generated-candidate / mock-demo / production-ready / target-placement / route-menu / tenant / request / id-runtime |  |  | Task Breakdown / Implementation / Verification / Handoff | blocked / demo-only / not-applicable |

## Contract Check Conclusion
- 是否可进入 Frontend Design 完成态：yes / no；reason
- 是否可进入 Task Breakdown：yes / no；reason
- 是否可进入 runnable Implementation：yes / no；reason
- 是否允许 mock/demo：yes / no / needs-user-confirmation / not-applicable
- production-ready 阻塞项：
- generatedCandidate 待确认项：
- questionGate：
- questionGateQueue：
- next：Frontend Design / Design Confirm / Missing Contract Confirm / Task Breakdown / blocked

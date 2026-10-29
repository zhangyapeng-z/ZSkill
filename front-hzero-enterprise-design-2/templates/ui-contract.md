# UI Contract

Feature：<feature>
建议路径：`sdd-workspace/changes/{change-id}/frontend/design/ui-contract.md` 或并入 `frontend-design.md`
状态：draft / confirmed / blocked

## Source Rules

- FDS、用户确认、Figma/PageSchema、Frontend Evidence 和目标工程模式可以共同支撑 UI confirmed。
- UI 显示布局权威顺序：用户明确确认 > Figma/PageSchema confirmed > 目标工程同类页面基线 > FDS UI 描述 > 后端 TDS 前端提示。适用范围：页面布局、区块顺序、视觉层级、按钮区域、列表/表单/详情/弹层形态、字段显示顺序、密度和响应式视觉约束。
- 业务契约权威顺序：用户明确确认 > FDS/TDS/API/DTO/权限/平台协议 > 目标工程业务证据 > Figma 可见文案。适用范围：业务能力、字段语义、接口、状态流转、权限、route/menu、LOV/lookup、附件/导入导出协议和生产请求契约。
- Figma/PageSchema 可以约束 UI 如何显示，但不能删除 FDS/TDS 已确认的业务能力；FDS/TDS 可以约束数据和业务，但不能在无前端复核时覆盖 Figma confirmed 的布局。
- Figma 与 FDS/TDS/API/工程证据冲突时必须记录 `uiBusinessConflicts`、`layoutAuthority`、`businessAuthority`、`conflictResolution`；不得静默合并或让 Implementation 自行取舍。
- TDS 中的前端相关内容若来自后端 TDS，只能作为 `backend-provided-hint / ui-candidate`；唯一来源为后端 TDS 时，UI 状态只能是 `partial / generatedCandidate / missing / conflict`，不得写 confirmed。
- 后端 TDS 可提供 API、字段、状态流转、权限和按钮条件等约束；页面布局、组件选型、字段顺序、查询条、Drawer/Modal 和样式必须由前端设计复核。
- FDS 原文中的结构词必须守恒进入 UI Contract：`组件类型：标签页/折叠面板/弹窗/抽屉/分区/左右布局`、`标签内组件`、`显示在某标签内`、`列表头按钮区/明细表列表头按钮区` 等都必须保留 `sourceRef/sourceComponentType/sourceContainer/childComponent`。不得把“标签页承载表格”降级成只有“明细 Table”的组件描述；若后续设计确认改为非 Tab，必须写 `overrideSource` 和 `negativeAcceptance`。

## UI Readback Table
| 页面/区域 | UI 要求 | 来源（FDS/TDS/TBS/Figma/工程证据） | layoutAuthority | businessAuthority | conflictResolution | sourceRole | 状态 | 实现位置 | 验证方式 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 列表/筛选/按钮/详情/抽屉 |  |  | user-confirmed / figma-pageschema / project-baseline / fds-ui / backend-tds-hint / missing / not-applicable | user-confirmed / fds-tds-api / project-business-evidence / figma-visible-copy / missing / not-applicable | none / figma-layout-business-covered / business-contract-overrides-visual-copy / needs-question / blocked / not-applicable | primary-design / backend-provided-hint / engineering-evidence / figma / user-confirmed | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |  | Review / runtime-manual / Network |

## List Contract
| 项 | 规则 |
| --- | --- |
| queryAreaPolicy | required-filter / required-fuzzy / none-by-design / project-wrapper-confirmed / missing / blocked；设计明确无筛选时必须写 `none-by-design + sourceRef + reason` |
| Table 模式 | Choerodon Pro Table + filterBar 查询形态 / 项目等价封装；非 filterBar 必须有 mode、sourceRef、reason；`queryBar` 代码形态必须按 enumProvenance 使用 enum |
| fuzzyQueryRequired | true / false；只记录需求是否要求顶部搜索框、关键字或模糊查询，来源为 FDS/TDS/Figma/用户确认 |
| fuzzyQuery | required / confirmed / unsupported-with-evidence / not-applicable + reason；记录实现策略和支持状态。若 FDS/TDS/Figma/用户确认出现“搜索框 / 关键字搜索 / 模糊查询 / 顶部快速搜索”，必须至少写 required，且 Implementation 不得配置 `fuzzyQuery=false` 或 `queryBarProps.fuzzyQueryField/fuzzyQueryFields` |
| fuzzyQueryFields | required 时填写参与模糊搜索的 QueryDS/queryFields 字段，例如 `name, positionApplied`；这是 UI Contract 字段映射，不是 `queryBarProps` 组件参数；不适用写 `not-applicable + reason` |
| fuzzyQueryPlaceholder | required 时填写用户可见 placeholder 或项目默认来源；实现可进入 `queryBarProps.fuzzyQueryPlaceholder` |
| queryFieldsLimit |  |
| 默认展示查询字段 |  |
| 更多筛选字段 |  |
| 操作列 | 最后一列 + 右锁定（按 enumProvenance 使用 `ColumnLock.right` 或项目 confirmed 等价 enum 导出） + width |
| 操作列更多入口 | confirmed helper overflow / Dropdown / Popover / Menu；不得使用 Drawer |
| 查询行为 | 查询回第一页；刷新保留当前页；重置清空并回第一页 |

规则：
- `queryAreaPolicy=none-by-design` 时，设计来源优先于默认 filterBar；Implementation 不得自行补无来源查询区、QueryDS/queryFields 或顶部搜索框。Review/Verify 只核对无筛选设计是否有 `sourceRef/reason`，不因缺 Table filterBar 查询形态判失败。
- `filterBar` 只表示查询条形态，不等于顶部 fuzzy search 已实现。若来源要求搜索框或模糊查询，必须同时确认 `fuzzyQueryFields`，并把 `queryBarProps.fuzzyQuery=true` 或项目等价写法作为实现验收；不得把合同字段写成 `queryBarProps.fuzzyQueryField` / `queryBarProps.fuzzyQueryFields`。
- 表格固定列默认只对行操作列提出右锁定要求；普通业务列只有在 Figma/PageSchema、UI Contract、用户确认或项目 confirmed baseline 明确要求固定时，才可写入对应固定列 seed。
- 只有项目证据证明当前 Table/queryBar 封装不支持 fuzzy query，或用户/设计明确取消快速搜索时，才能写 `not-applicable`；原因和替代交互必须可追溯。
- `fuzzyQueryRequired=true` 但 `fuzzyQuery=unsupported-with-evidence` 时，不代表已放行；必须同时写替代交互、阻塞项或降级状态，并在 Contract Check 中把 `listQueryContractStatus` 标为 `partial / blocked / conflict`，不得写 `pass`。

### QueryFields Schema
| field | label | component | multiple | clearable | defaultValue | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-yet-confirmed | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | missing |

## Route Context / Edit Mode Contract
| routePattern | idSource | isCreateSource | editableDerivation | pageModeDerivation | queryParser | editableAuthority | dataSetEditFlagUsage | saveRedirectPolicy | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | path params / useParams / not-applicable | `/create` / path params / not-applicable | path pageMode + user-action + status-guard / not-applicable | create / edit / copy / view / detail / approval / readonly / mixed from path | URLSearchParams / project wrapper | routeContext + UI Contract + business status guard | display/submit only / not-applicable | keep path pageMode / switch to view path / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本节只记录 Route Context / Edit Mode 合同字段；判定细则、禁止 hash 推导、`/create` 默认新建语义、`/detail/create` 违规迁移边界和 ID runtime 约束统一以 `references/frontend-ui-contract-guardrails.md`、`references/route-context-edit-mode.md`、`references/frontend-id-runtime-contract.md` 为准。
- 缺 `routePattern/idSource/isCreateSource/editableDerivation/pageModeDerivation/editableAuthority` 或与 UI/业务状态守卫冲突时，不得把本节标为 ready/confirmed。
- 新生成详情/编辑/新建页面的 `idSource/isCreateSource/pageModeDerivation` 必须来自 path；UI 可编辑态派生为语义化 `editable`，不得生成或读取 route/query `editFlag` 作为页面模式、Tab 唯一性或 UI 编辑态来源。API/DataSet 若确有同名业务字段，只能按 `dataSetEditFlagUsage` 用于显示或提交。

## Frontend ID Runtime Contract
| item | rule / evidence |
| --- | --- |
| status | confirmed / partial / generatedCandidate / missing / conflict / not-applicable |
| declaredTypeSource | TDS / MDS API / DTO / DB schema / source evidence |
| runtimeType | ID-like 字段默认 `string`；ID 数组默认 `string[]` |
| matchingFields | `id` / `*Id` / `*Ids` / path/query ID / Lov value / rowKey / DataSet primaryKey / `@Encrypt` 字段 |
| normalizationPolicy | mock/API adapter 入口统一 `String(id)`；数组 `ids.map(String)` |
| encryptedIdPolicy | 是否发现 `@Encrypt` / 主键加密 / 外键加密；发现时禁止 number runtime |
| exceptions | `lineNum`、金额、数量、比例、分页、展示文本、编码字段、`objectVersionNumber` 等不按业务 ID 处理 |

## Field Visibility Matrix
| field | label | fieldExistsSource | create | edit | detail | list | query | displayTiming | hiddenReason | source | verification | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| requisitionNumber / totalAmount / budgetRate / creationDate / lineList / other |  | FDS / TDS / API / DTO / Figma / engineering evidence | visible / hidden / readonly-placeholder / not-applicable | visible / hidden / readonly-placeholder / not-applicable | visible / hidden / not-applicable | visible / hidden / not-applicable | visible / hidden / not-applicable | before-save / after-save / after-line-change / backend-return / no-detail-hide / always |  | FDS/TDS/API/Figma/工程证据/user-confirmation | runtime-manual / static / payload / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本节只记录字段显隐事实；字段存在来源与 pageMode 展示策略拆分、编号/合计/比例的 create 态规则、审计字段展示时机、submitPolicy 和空 `Output` 禁止项统一以 `references/frontend-ui-contract-guardrails.md` 为准。

## Field Editability Matrix
| field | label | pageMode | editability | component | readonly/disabled/hidden reason | defaultValueSource | submitPolicy | source | verification | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | create / edit / copy / detail / approval / readonly / mixed | editable / readonly / disabled / hidden | TextField / Select / NumberField / DatePicker / Lov / Attachment / Output / project component |  | FDS/TDS/API default / backend-generated / user-context / copy-source / none | include / exclude / display-only / not-applicable | FDS/TDS/Figma/工程证据 | input / required validation / readonly check / payload check / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本节只记录字段编辑态和组件结论；主数据/枚举/附件默认组件候选、detail `Form + Output`、editable 字段不得落成 `Output`、以及缺来源不能自行降级的细则统一以 `references/frontend-ui-contract-guardrails.md` 为准。

## Empty / Derived Field UX Rules
| field | label | fieldClass | generationTiming | derivedFrom | createUx | editUx | detailUx | emptyText / placeholder | occupyLayoutWhenEmpty | submitPolicy | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| requisitionNumber / totalAmount / budgetRate / lineList / creationDate / other |  | backend-generated / frontend-derived / backend-calculated / aggregate / audit-generated / optional-detail / other | before-save / after-save / after-line-change / backend-return / user-input / not-applicable | line amount / budget amount / backend rule / none | hidden / readonly-placeholder / visible-empty / not-applicable | hidden / readonly-placeholder / readonly-value / editable / not-applicable | hidden / readonly-value / empty-state / not-applicable | 保存后自动生成 / 暂无明细 / not-applicable | yes / no / source-required | include / exclude / display-only / not-applicable | FDS/TDS/API/Figma/user-confirmation | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本节只记录空态/派生字段 UX 决策；禁止只读空字段、后端生成/前端派生字段的 timing 约束、无明细/无附件区块处理统一以 `references/frontend-ui-contract-guardrails.md` 为准。

## Field Usage Matrix
| field | canonicalField | runtimeFieldPolicy | adapterAliasPolicy | forbiddenRuntimeAliases | storedField | renderedField | displayField | label | labelSource | ownerDataSetOrRecord | component | renderer | source | DataSet fields/queryFields | list table column | detail form field | line table column | actionGuard | submit payload | displayOnly | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-yet-confirmed | canonical-only / not-applicable | none | [] | not-yet-confirmed | not-yet-confirmed | not-applicable |  | current-field / stored-field / explicit-props / i18n-key / missing / not-applicable | headerDs / detailDs / lineDs / queryDs / record / not-applicable / missing | Output / Tag / TextField / Lov / Select / TableColumn / other | none / TagRender / project-renderer / custom | not-yet-confirmed | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | missing |

规则：
- 本节只记录字段使用映射；运行时字段统一使用设计/API 的 `canonicalField`，`runtimeFieldPolicy=canonical-only`、`adapterAliasPolicy=none`。历史字段迁移不进入页面生成合同，必须由独立数据迁移或 API 契约变更处理。
- 同一业务对象的列表列、详情 Form、明细表、payload builder、mock/API response 必须使用同一 `canonicalField`；不得让列表和详情各自使用近义字段名。详情/编辑/新建 Form 字段必须记录 `ownerDataSetOrRecord`，缺失时下游不得实现可运行 Form。
- `storedField/renderedField/displayField/labelSource` 闭合、状态 code/meaning 分工、displayOnly payload 边界和 `*Meaning/*Name` 展示字段 label 规则统一以 `references/frontend-ui-contract-guardrails.md` 为准。

## Status Action Matrix
| action | statusField | statusEnumMap | source status | visible condition | enabled condition | function guard | service action | mock handler | success status | refresh target | permission action | failure handling | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| submit / withdraw / void / delete / copy / create-related / workflow | authorizationStatus / status / not-applicable | `NEW=新建; IN_APPROVAL=审批中` / source-required |  |  |  |  |  |  |  | list / detail / lineTable / none |  | notification / backend error / stay current page | missing |

规则：
- 提交、撤回、作废、删除、复制、创建下游单据、审批/工作流等动作必须进入矩阵。
- 业务状态枚举全集必须进入 `statusEnumMap`，包括 code、显示文案和颜色/标签策略来源；实现不得把设计状态值改成近义旧值，例如 `NEW` 改 `DRAFT`、`IN_APPROVAL` 改 `SUBMITTED`，除非有 API adapter 或 legacy runtime 来源。
- UI 显隐/禁用和 action 函数入口二次校验必须一致；不得只在按钮层判断。
- 来源写“显示/隐藏/仅显示”时进入 `visibleWhen`；来源写“启用/禁用/置灰/可点击”时进入 `enabledWhen`。不得把 FDS 的“仅某状态启用”翻成其它状态隐藏，除非来源明确写隐藏。
- 列表和详情的同一动作应共享状态机来源；若差异化，必须写明原因。
- 缺 `service action / mock handler / refresh target` 时，不得把状态动作视为 runnable 设计完成。

## Action Entry Matrix
| actionId | label | actionExistsSource | sourceSectionPath | sourceRegion | sourceRegionReason | statusActionRef | allowedEntryLocations | chosenEntryLocation | uiArea | pageModes | entryStatus | source | overrideSource | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| save / submit / cancel-navigation / cancel-business / withdraw / void / delete / other |  | FDS / TDS / API / status-flow / Figma / project evidence / user-confirmation | fds.md#heading / tds.md#heading / figma node / evidence path | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | why this region maps to chosenEntryLocation | not-applicable / Status Action Matrix actionId | detail-header / page-toolbar / row-action / table-toolbar / line-row / modal-footer / hidden | detail-header / page-toolbar / row-action / table-toolbar / line-row / modal-footer / hidden / not-confirmed | page-header / business-state-actions / row-action / table-toolbar / modal-footer / other | create / edit / detail / list / approval / readonly | confirmed / generatedCandidate / needs-confirmation / missing / conflict / not-applicable |  | not-applicable / UI Contract / user-confirmation / Figma / project-baseline | implement / block-and-confirm / keep-hidden / demo-only-with-risk / not-applicable |

规则：
- 本节只记录动作入口结论；入口位置确认原则、`cancel-navigation` / `cancel-business` 拆分、Header 禁放条件和状态流/API 只能证明动作存在的细则统一以 `references/frontend-ui-contract-guardrails.md` 为准。
- FDS/TDS 同时出现“列表头按钮区”和“列表行按钮区”时，必须拆成两行独立入口；同名“删除/编辑/详情”等不得合并。列表或明细表章节下的“列表头按钮区”默认 `chosenEntryLocation=table-toolbar`，除非 `overrideSource` 明确来自 UI Contract / 用户确认 / Figma / PageSchema 并说明为页面 Header。不能只因 sourceRegion 文案包含“头”字写成 `page-toolbar`。

### List Columns
| order | field | label | widthPolicy | render | source | i18nKey | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | not-yet-confirmed | not-applicable | not-applicable | not-applicable | not-applicable | missing |

规则：
- `widthPolicy` 记录列宽来源与策略，例如 `minWidth:160`、`fixedWidth:120 + sourceRef`、`flexTextColumn`、`projectWrapperAutoFit` 或 `not-applicable`。普通业务列不得只因参考页存在固定宽度就写 `fixedWidth`；只有 Figma/PageSchema、UI Contract、用户确认或项目 confirmed baseline 明确要求固定宽度时才允许。
- 字段较少的列表必须识别至少一个主展示文本列作为自适应承载列，优先使用名称、描述、分类名称等长文本字段；实现验收需确认宽屏下表格不会因所有业务列固定宽度而留下明显空白。状态、日期、金额、操作等稳定窄列可保留固定或最小宽度策略。

## Detail Contract
| 区块顺序 | 区块名 | 字段/数据 | requiredFields | sourceComponentType | sourceContainer | childComponent | 组件 | expectedSurface | forbiddenSurface | requiredVisibleByDefault | visualContainer | ownerDataSetOrRecord | 来源 | surfaceExceptionSource | conflictResolution | negativeAcceptance | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 基本信息 |  | field list from FDS/TDS/API/Figma | 表单 / 分区 / not-applicable | Content / BasicInfoSection / not-applicable | Form fields | Form + Output / Form editable | Content > BasicInfoSection / Content > Form | Tabs.TabPane / Table.buttons / Header children | yes / no + source | continuous-section / Card / project-card / none-by-design | headerDs / detailDs / record / missing | FDS/TDS/Figma/UI Contract/project evidence | not-applicable / explicit sourceRef | auto-fixed-header / question / follow-layout / follow-project | 基本信息不得进入 Tabs.TabPane / source-specific rejection | confirmed / generatedCandidate / missing / conflict / not-applicable |
| 2 | 明细页签/明细区 |  | tab ids + line fields + line query fields | 标签页 / 分区 / not-applicable | <source tab title> TabPane / DetailTabs / LineSection | source child component / line Table / attachment / other | Tabs + Table / Table only with source | Content > DetailTabs > Tabs.TabPane(source tab) / Content > LineSection | Header / page-toolbar / basic-info Form | yes / no + source | continuous-section / Card / project-card / none-by-design | lineDs / lineQueryDs / record / missing | FDS/TDS/Figma/UI Contract/project evidence | not-applicable | follow-source / not-applicable | 不得绕过 required sourceContainer 裸渲染 childComponent | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- Detail Contract 必须逐区块列出 required fields 和 owner DataSet/record。TDS/FDS/API/Figma 声明的头字段、审计/后端返回只读字段、驳回原因/拒绝原因、联系方式、创建/更新人显示字段等，只要在详情/编辑/只读场景 required，就必须出现在 `requiredFields`，并在 Field Usage Matrix 中给出 `visibleIn`、`ownerDataSetOrRecord`、`componentPolicy` 和 `labelSource`。
- `expectedSurface` / `forbiddenSurface` 是轻量结构契约，只约束区域归属和承载面，不要求 Design 固化具体 JSX 父子层级。“固定表头 / 基础信息 / HeaderForm + 业务页签 / 业务 Tab / 明细区”等结构语义默认解释为两层结构：基本信息 Form 在 `Content` 内默认可见，`forbiddenSurface=Tabs.TabPane`；业务页签或业务区域只承载明细集合、附件、审批/记录区和其它从属业务分类，`tabsScope=business-sections-only`。业务名称示例不参与触发判断，必须按来源文档中的结构关系和组件归属判定。同一资料又出现“基础信息页签”等轻微歧义时，记录 `uiBusinessConflicts` 后按固定表头主语义自动收口；只有存在对等或更强的相反证据时才进入 `Detail Surface Conflict Confirm`。若最终确认基本信息进入 Tab，必须填写可定位到明确条款、Figma/PageSchema、项目 confirmed baseline 或用户 question 结果的 `surfaceExceptionSource`，并补齐 `conflictResolution`、`requiredVisibleByDefault`、`expectedSurface` 和 `negativeAcceptance`；只写泛化的 `FDS/TDS` 或“参考相似页面”不算例外证据。表格工具栏上提 Header、页面工具栏下沉 Table 仍必须有对应来源并写清负向验收。
- FDS 写明 `组件类型：标签页`、`标签：<名称>`、`标签内组件：<子组件>` 或“此组件显示在 <标签> 内”时，必须生成独立结构行：`sourceComponentType=标签页`、`sourceContainer=<标签名> TabPane`、`childComponent=<子组件>`、`expectedSurface=Tabs.TabPane(<标签名>)`、`negativeAcceptance=不得绕过 sourceContainer 裸渲染 childComponent`。只有 FDS/Figma/PageSchema/UI Contract/用户确认明确取消页签时，才可写 `Table only with source`。
- 区块顺序、字段分组和区块标题只确认信息架构，不等于确认卡片化视觉。`visualContainer` 未由 FDS/TDS/Figma/PageSchema、项目 confirmed baseline、UI Contract 或用户确认明确为 `Card/project-card` 时，默认写 `continuous-section`：同一 `Content` 下连续表单区、标题和必要间距；不得自动生成白底、边框、圆角、阴影或独立背景。
- 设计要求详情 Tab、明细页签、附件页签或其它区域容器时，必须记录组件为 `Tabs + Table` 或项目 confirmed 等价组件；Implementation 不得直接渲染裸 Table 替代 required Tab。若设计明确不需要 Tab，必须写明 `not-applicable + reason`。
- 明细筛选字段必须进入 `line query fields` / List Query Contract 或 Master Detail Data Contract；required 明细筛选不得被 `queryBar=false/none` 或无 queryDataSet 的裸表格关闭。设计明确明细无筛选时必须写 `lineQueryPolicy=none-by-design + sourceRef + reason`，不得反向生成无来源筛选区。

### Form Composition Contract
| formRegion | composition | pageContainerOwner | formComponentInput | fieldContractOwner | pageModeOwner | validationAndActionOwner | readonlyPolicy | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BasicInfoSection / HeaderForm | page-container-plus-presentational-form / simple-page-co-located-with-reason | DataSet / record lifecycle / refresh | `dataSet` / `mode` / local component props | DataSet `fields` / `dynamicProps` / bind | routeContext + UI Contract + business state guard | page container `validate()` + save/submit/back/navigation | field-level editability first; Form `disabled` only as confirmed global readonly protection | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 头行、主从、多 Tab、复用基础信息区或页面动作较多时，默认 `composition=page-container-plus-presentational-form`：容器创建/注入 DataSet、派生 mode、加载/刷新 record 并负责 validation 和页面动作；Form 组件不重建 DataSet、不解析路由、不发起页面级请求，也不复制 DataSet 中的字段规则。
- `simple-page-co-located-with-reason` 仅适用于无复用、无多区域协调的简单单记录页面；即使同文件实现，也必须保持 DataSet 字段契约、pageMode、页面动作和 Form 布局的职责分离。
- `readonlyPolicy` 必须逐字段继承 Field Editability Matrix。全局 `Form disabled` 不能替代 `dynamicProps/readOnly`、权限锁定或 create/edit/detail 差异；后端生成编号、状态、合计和审计字段的可见性、readonly/hidden 原因和 `submitPolicy` 必须逐字段继承 Field Visibility Matrix / Field Editability Matrix 并有业务来源。当前 mode 无可显示值时，不能以空 `Output` 或 disabled 输入框填充网格。

### Basic Info Form Layout Contract
| formRegion | pageMode | layoutAuthority | containerWidthPolicy | columns | columnsSource | responsiveColumns | labelLayout | labelAlign | labelWidthPolicy | fieldOrderPolicy | field | semanticType | valueLengthRisk | colSpan | valueOverflowPolicy | decisionSource | negativeAcceptance | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BasicInfoSection / HeaderForm | create/edit/detail/copy/approval | Figma/PageSchema / project baseline / user / default-form-layout-by-design-rule / reference-code-fact | default-content-available / confirmed-max-width-centered / project-wrapper | 3 / 2 / 1 | target sourceRef / default-basic-info-3col-by-design-rule / layout-adjustment-reason / narrowed-container / modal-small | default-xs1-sm1-md2-lg3-by-design-rule / explicit breakpoint contract / not-applicable | horizontal / project-default / explicit | project-default / right / left | project-default / 120-default-by-design-rule / adjusted-for-label-or-value-length | source-order / UI Readback order | companyName / contactMobile / address / remark | short-text / contact / date / amount / status / address / remark / long-body / rich-text / unknown | low / medium / high / unknown | 1 / 2 / full-row | no-special / single-line-ellipsis-tooltip / multiline-block / preserve-wrapping | FDS / TDS / Figma / UI Contract / project baseline / default-form-layout-by-design-rule / reference code `sourceRef:line` | 触发默认规则时必须记录基线或 `layoutAdjustmentReason`；固定 max-width、居中、卡片化和字段顺序分别按其自身合同处理 | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- `default-form-layout-by-design-rule` 仅在以下条件同时满足时触发：已确认页面存在基础信息 / HeaderForm；设计输入只给出“基础信息表单 + 联系人表 + 地址表 + 账号表”或“基础信息/头表单 + 明细/业务分区/附件/审批记录”等高层结构，未给出列数、容器宽度、跨列、标签布局或响应式细节；原型/Figma/PageSchema、用户和项目 confirmed baseline 均未覆盖这些细节。本节必须落盘并记录触发判断，不能只在实现摘要中说明；联系人表、地址表、账号表等只是同类示例，不是穷举。
- 表格模板行中的 `companyName / contactMobile / address / remark` 只是字段填写格式示例，不得作为触发条件、固定业务字段或穷举清单；实际字段必须来自 UI Readback / Field Usage Matrix / FDS/TDS/API/Figma。
- 工程参考代码中的 `columns=3`、`labelWidth=120`、`labelLayout=horizontal`、固定 `colSpan=3` 或 create 态字段显隐处理，记录为 `reference-code-fact + sourceRef:line`。其中 create 态显隐只能作为参考事实，不得升级为默认布局规则；布局型事实可作为默认基线的来源证据。
- 默认基线为：页面级 `Content` 使用 `containerWidthPolicy=content-available`；默认响应式为 `xs=1, sm=1, md=2, lg=3`，`lg` 初始采用 `columns=3`、`columnsSource=default-basic-info-3col-by-design-rule`、`labelWidthPolicy=120-default-by-design-rule` 和横向标签。短字段初始 `colSpan=1`，长值 Lov 可优先评估 `colSpan=2`，地址、备注、长说明、富文本、附件等优先评估跨当前整行。该基线可进入 runnable implementation。
- 实现前或实现中可根据可用宽度、字段密度、标签长度、值长度和字段语义，以 `layoutAdjustmentReason` 调整 `columns=3/2/1`、`labelWidth`、`colSpan` 或断点；这类调整不需要补外部设计来源，也不得用“字段少于 6 个”作为自动降列阈值。普通 Modal、窄 Drawer 或可用宽度不足只是常见调整场景，不是唯一条件。审计/后端生成字段的展示时机和跨 mode 策略不属于默认表单布局基线，必须由 Field Visibility Matrix / Field Editability Matrix 决定。
- 固定 `max-width` 或居中必须有来源。若目标页面确认列数会变化，长字段的 `colSpan` 必须随当前列数全跨，不能继续固定 `3`；字段顺序由 UI Readback / Field Order Contract 决定，不得由布局基线自行改变。
- 本合同只确认 Form 网格、label 可见性、跨列和长值展示策略；Card、白底、边框、圆角、阴影、摘要头、统计块、字段分组、字段顺序和字段可见性均由各自合同决定。

### Detail Field Overflow UX Rules
| field | semanticType | valueLengthRisk | valueOverflowPolicy | tooltipOrReveal | multilinePolicy | decisionSource | questionRequired | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| candidateEmail / companyName / positionName / address / remark | short-text / contact / identifier / name / address / long-body / remark / rich-text / unknown | low / medium / high / unknown | no-special / single-line-ellipsis-tooltip / two-line-clamp-tooltip / multiline-block / preserve-wrapping / question-required | Tooltip / title / popover / expanded-block / none | none / 2-line / 3-line / natural-multiline / rich-text-viewer | FDS / TDS / Figma / UI Contract / project baseline / AI-semantic-default / user-confirmation | yes / no | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 不得用增大 Modal / Drawer 宽度作为解决字段过长的唯一手段。宽度和 `columns/colSpan` 负责整体布局，字段值过长必须进入 `valueOverflowPolicy`。
- 表格模板行中的 `candidateEmail / companyName / positionName / address / remark` 只是字段填写格式示例，不得作为触发条件、固定业务字段或穷举清单；实际字段必须来自 UI Readback / Field Usage Matrix / FDS/TDS/API/Figma。
- AI 可按字段语义默认选择展示策略：邮箱、手机号、编号、姓名、公司名、职位名、地址、短标签等默认 `single-line-ellipsis-tooltip`；备注、拒绝/驳回原因、经历描述、富文本、长正文等默认 `multiline-block` 或按设计 `2-line/3-line clamp`；金额、日期、状态、短枚举默认 `no-special`。这些默认必须标记 `decisionSource=AI-semantic-default` 或项目证据来源。
- 只有当 FDS/TDS/Figma/项目基线/用户输入对长值展示有冲突，或策略会改变业务可读性、验收含义、复制/查看完整内容能力时，才触发 question。不得把每个普通长文本字段都交给用户选择；也不得在无证据时把长正文强行单行省略。

### Detail Collection Contract
| section | apiField | declaredShape | itemKey | columns | component | componentSource | nativeFallbackEvidence | fieldNameSource | mockFieldPolicy | renderPolicy | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 履历/明细 | `workExpList` / confirmed API field | array<object> / PageResponse / unknown | confirmed row key / generatedCandidate | `positionName/companyName/startMonth/endMonth/workDescription` + label + source | Choerodon Pro Table | builtin-choerodon-table / blocked | not-applicable-for-table | TDS / MDS API / DTO / response sample | mock must use the exact apiField; aliases forbidden | no text flatten; no `ul/li` join/stringify | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- FDS/TDS/MDS/API/DTO 声明为数组或集合的详情字段，必须进入本表；表格型详情集合命中 `front-hzero-choerodon-ui` owner 规则，组件只能是 Choerodon Pro Table，不允许项目只读表格、手写 wrapper、HZERO 非表格组件或原生 DOM 替代。只有来源明确要求自然语言摘要且该区域不作为表格型集合验收时，才允许单独设计摘要展示，并必须记录 source。
- `apiField` 必须使用后端契约字段名；mock/demo 数据和组件列绑定也必须同名。旧字段、别名或双 shape 命中时标记 `conflict/migrationRequired`，回 API/TDS/MDS 合同修正；不得在新实现中增加兼容 adapter。
- 表格型详情集合不适用通用 native DOM fallback；`nativeFallbackEvidence` 必须写 `not-applicable-for-table`。原生 `<table>`、`ul/li`、`div/grid`、手写 summary table、`SimpleCollectionTable` 或项目薄 wrapper 都不得替代 Choerodon Pro Table。
- `履历/明细`、`workExpList` 和 `positionName/companyName/startMonth/endMonth/workDescription` 只是集合合同填写示例，不是触发条件或固定字段。`columns` 必须逐列绑定 MDS/TDS/API 原始 item 字段名；不得把不同集合统一改造成 `title/organizationName/timeRange/description` 等前端自造或兼容 shape。
- 禁止把结构化集合用 `renderPlainList`、`ul/li`、逗号拼接、JSON stringify、多字段模板字符串或手写通用 summary table 作为完成态展示；native fallback 也必须保留字段级列契约和空态，不得吞掉原始字段名。

### Detail Record Navigation Contract
| surface | recordIdentity | navigationScope | triggerSource | requestContract | stateRefreshPolicy | refreshRegions | boundaryBehavior | notApplicableReason | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Modal / Drawer / current-page detail / not-applicable | currentId from route / currentId from detail state / record primaryKey / missing | current-filter-result / all-candidates / fixed-set / not-applicable | UI Contract / FDS / TDS / project baseline / user-confirmation / not-applicable | service action / DataSet read / mock-request nav API / production API / not-applicable | component state / modal update / modal recreate with key / owner DataSet rebinding / route id / blocked / not-applicable | Header + basic Form + sections + Tabs + child tables + attachments / custom list / not-applicable | disable-at-boundary / notification / explicit empty shape / blocked / not-applicable | pagination / carousel / wizard / tab-switch / attachment-preview / image-preview / none | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本合同只用于同一详情表面内切换业务主记录，例如候选人、订单、申请单或单据头；不用于列表分页、轮播、步骤向导、Tab/区块切换、附件/图片预览翻页。
- 适用时必须写清当前记录身份、导航候选范围、请求或 DataSet 入口、边界行为，以及切换后需要同步刷新的区域。Implementation 不得只依赖 `Modal.open` 打开时的 children 闭包或旧 record。

### Detail Section Title Contract
| section | titleText | auxiliaryDisplay | allowedFields | component | source | status |
| --- | --- | --- | --- | --- | --- | --- |
| 基本信息 | 基本信息 | none | not-applicable | plain title | FDS/TDS/Figma/UI Contract/project evidence/user confirmation | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本节只记录区块标题及标题附加展示的允许范围；禁止把状态/编号/金额/数量无来源拼进标题、以及状态字段应保留在 Form 字段位置展示的细则统一以 `references/frontend-ui-contract-guardrails.md` 为准。

### Detail Section Visual Contract
| section | visualContainer | allowedVisuals | source | stylePolicy | status |
| --- | --- | --- | --- | --- | --- |
| 基本信息 / 金额与地址 / 附件 / 明细 | continuous-section / Card / project-card / none-by-design | title + spacing / white-bg / border / radius / shadow / project-class | FDS / TDS / Figma / project confirmed baseline / user-confirmation / default-continuous-section | no-card-style / use-confirmed-card / block-and-confirm | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 详情区块顺序或“section/order”不授权卡片视觉；`Card/project-card` 必须有明确来源。缺来源时 `stylePolicy=no-card-style`，只能保留标题、上下间距和字段布局。

### HZERO Page Skeleton / Scroll Boundary
| item | contract | source | status | verification |
| --- | --- | --- | --- | --- |
| pageRoot | Design-frozen Fragment with sibling `Header` and `Content`; no business wrapper around `Header + Content` | project HZERO Page layout / UI Contract | confirmed / generatedCandidate / missing / conflict / not-applicable | Design FD-G7 + Review static check |
| pageProvider | No `UrlHistoryProvider`, `HistoryProvider`, `ConfigProvider`, custom Provider, or page-level wrapper around `Header + Content` unless UI Contract / confirmed golden-baseline / explicit requirement confirms it | UI Contract / baselineComparison.evidenceQuality / goldenBaselineStatus / baselineConfirmationSource | confirmed / generatedCandidate / missing / conflict / not-applicable | Review static check |
| businessContainer | Business className / section wrapper lives inside `Content`; `Content className/wrapperClassName` only with project evidence | UI layout / project evidence | confirmed / generatedCandidate / missing / conflict / not-applicable | Review + runtime-manual |
| scrollBoundary | Long form, detail sections, line tables and tabs scroll within `.page-content` or confirmed container to final block | UI Contract / manual checklist | confirmed / generatedCandidate / missing / conflict / not-applicable | runtime-manual small viewport |

规则：
- 本节是 Design 阶段必填合同，不是 Implementation 自查补充项；新增或改造 HZERO 页面时必须在进入 Task Breakdown 前冻结。
- `pageRoot` 默认写为 Fragment 下相邻 `Header` 与 `Content`。不得把业务 `<div className="*-page">`、`<div className="*-detail">`、`section`、`main`、`Provider` 或自定义 layout wrapper 设计为包住整组 `Header + Content`。
- 需要业务 className、section 背景、底部 padding 或滚动样式时，`businessContainer` 必须写明它位于 `Content` 内部；只有项目证据确认时才允许使用 `Content className` / `wrapperClassName`。
- 本节 `missing/conflict`，或把业务 wrapper 包整页骨架写成 confirmed 时，`FD-G7` 不通过，不得进入 Task Breakdown / Implementation。

### Baseline Evidence Quality
| evidencePath | evidenceType | evidenceQuality | adoptedPatternItems | rejectedPatternItems | reason |
| --- | --- | --- | --- | --- | --- |
| not-yet-confirmed | similarPage / routeConfig / projectEvidence / userInput | golden-baseline / project-compatible / asset-baseline / legacy-risk / anti-pattern / unknown-quality | none | none | missing；golden-baseline 必须有 goldenBaselineStatus=confirmed 和合法 baselineConfirmationSource |

## Drawer / Modal Contract
| 项 | 规则 / 证据 |
| --- | --- |
| 组件选型 | 普通 Modal / Drawer / Overlay / not-applicable；来源必须是需求/Figma/UI Contract/工程证据/用户确认 |
| 打开方式 | 业务弹层必须 `Modal.open` / confirmed wrapper；点击事件优先，受控 effect 必须 cleanup；不得 JSX Modal/Drawer 常驻渲染 + visible state |
| Drawer 默认属性 | `drawer: true` 且 `resizable: true`；wrapper 必须记录等价默认证据 |
| size / width | 所有普通业务 Modal / Drawer / Overlay 宽度必须严格来自设计/Figma/PageSchema/项目 confirmed baseline/用户确认。设计未指定宽度时，普通表单 Modal 默认 `size=small`（约 520px 或项目 small 等价值）；详情 Drawer / 高密度只读详情 / 三列及以上 Form 默认优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并必须记录 readabilityRisk 与 `valueOverflowPolicy`。`medium`、`large`、`70%`、`80%`、`980px` 等宽框只允许在有明确来源时使用 |
| size / width prop placement | 尺寸必须写在项目 confirmed 的 Modal/Drawer 配置入口（如 `size` / `width` / wrapper `drawerWidth`、`modalSize` 等）并记录 API 证据；仅写 `style.width`、内容容器宽度或 CSS 宽度不算弹层宽度契约闭合 |
| 挂载生命周期 | visible=false 不挂载；关闭 cleanup |
| 背景和层级 | body/content 不透明；mask/z-index 验证 |
| 形态强制 | 明确 Modal 不得实现 Drawer；明确 Drawer 不得实现普通 Modal |

> 操作列“更多”菜单不纳入 Drawer / Modal Contract。更多入口是行操作溢出浮层，必须按操作列合同实现；不得默认打开抽屉。

## Button Contract
| buttonId | 按钮文案 | sourceText | copyPolicy | copyOverrideSource | sourceSectionPath | sourceRegion | sourceRegionReason | 位置 | uiArea | semanticKind | action | navigationTarget | businessMutation | statusActionRef | permissionRequirement | 权限码 | type | visibleWhen | enabledWhen | disabledReasonSource | disabledTooltipPolicy | selectionReactivePolicy | destructive | confirmPolicy | asyncAction | requestOwner | loadingPolicy | repeatClickGuard | finallyReleasePolicy | 来源 | overrideSource |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable |  | exact-source / product-copy-override / generatedCandidate / not-applicable | FDS / TDS / Figma / user-confirmation / project-baseline / missing / not-applicable | fds.md#heading / tds.md#heading / figma node / evidence path | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | why this region maps to this UI surface | Header / toolbar / row-action / detail-header / table-toolbar / line-row / import / export / attachment | page-header / page-toolbar / table-toolbar / row-action / modal-footer / other | navigation / business-state-action / data-edit / table-operation / import-export / attachment / other | not-applicable | not-applicable | none / creates / updates / deletes / status-change / import-export / upload | not-applicable | required / not-applicable / unknown | not-applicable | not-applicable | visible / hidden / condition-source / not-applicable | enabled / disabled / condition-source / not-applicable | source text / helper / missing / not-applicable | Tooltip / title / project-wrapper / not-required / missing / not-applicable | DataSet select-events / React state / project-wrapper / not-required / missing | yes / no / not-applicable | Popconfirm / Modal.confirm / project-wrapper / not-required / blocked | yes / no / not-applicable | DataSet / service / mock-request / request-adapter / not-applicable | row-level / batch-level / action-level / page-level / not-applicable | disabled / handler-guard / both / not-applicable | try-finally / promise-finally / wrapper-guaranteed / not-applicable | not-applicable | not-applicable / UI Contract / user-confirmation / Figma / project-baseline |

规则：
- Button Contract 只记录按钮事实；按钮唯一性、导航/业务状态语义拆分、权限适用性和区域划分规则统一以 `references/frontend-ui-contract-guardrails.md` 为准。
- 删除、批量删除、撤回、取消单据、作废等破坏性动作必须写 `destructive=yes` 和 `confirmPolicy`；调用接口、DataSet、service 或 mock request 的动作必须写 `asyncAction=yes`、`requestOwner`、`loadingPolicy`、`repeatClickGuard` 和 `finallyReleasePolicy`。非异步/非破坏性动作写 `not-applicable + reason`。
- 默认 `copyPolicy=exact-source`，按钮文案必须与 `sourceText` 保持一致。把“新建”改成“新增行”、把“提交审批”改成“提交”等近义改写，必须有 `copyOverrideSource`；否则不得进入 runnable implementation 或 production-compliant。
- 页面工具栏按钮与表格工具栏按钮必须按 `uiArea` 区分消费组件：`page-toolbar` 默认由页面 `Header` children 消费，负向验收是不得进入 `Table.buttons`；`table-toolbar` 默认由对应 `Table.buttons` 消费。主从明细中的按钮只有来源区域明确为明细表列表头按钮区，或 UI Contract / Figma / 用户确认明确映射到对应 Table 时，才能记录为 `table-toolbar`。除非本表或项目证据明确允许，表格工具栏按钮不得上提到页面 Header，也不得在 Table 上方另建独立按钮容器；页面工具栏按钮也不得下沉到 `Table.buttons`。只看到“明细表”不自动触发本规则；必须有表格工具栏按钮来源。
- 批量动作按钮若依赖 Choerodon DataSet / Table 选中行，`selectionReactivePolicy` 必须写明由 `select/unSelect/selectAll/unSelectAll/load/reset` 事件、React state 或项目 confirmed wrapper 驱动重新计算按钮态；直接在 render 中读取 `dataSet.selected.length` 且没有刷新桥接时写 missing。

## Button Semantic Matrix
| buttonId | label | sourceText | copyPolicy | copyOverrideSource | sourceSectionPath | sourceRegion | sourceRegionReason | location | uiArea | semanticKind | navigationTarget | businessMutation | statusActionRef | permissionRequirement | visibleWhen | enabledWhen | disabledReasonSource | disabledTooltipPolicy | designStatus | overrideSource | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable |  | exact-source / product-copy-override / generatedCandidate / not-applicable | FDS / TDS / Figma / user-confirmation / project-baseline / missing / not-applicable | fds.md#heading / tds.md#heading / figma node / evidence path | 页面按钮区 / 列表头按钮区 / 列表行按钮区 / 明细表列表头按钮区 / 明细表行按钮区 / modal-footer / other | why this region maps to this UI surface | page-header / page-toolbar / table-toolbar / row-action / modal-footer / other | page-header / business-state-actions / table-toolbar / row-action / modal-footer / other | navigation / business-state-action / data-edit / table-operation / import-export / attachment / unknown | not-applicable | none / creates / updates / deletes / status-change / import-export / upload / unknown | not-applicable | required / not-applicable / unknown | visible / hidden / condition-source / not-applicable | enabled / disabled / condition-source / not-applicable | source text / helper / missing / not-applicable | Tooltip / title / project-wrapper / not-required / missing / not-applicable | confirmed / generatedCandidate / missing / conflict / needs-confirmation / not-applicable | not-applicable / UI Contract / user-confirmation / Figma / project-baseline | implement / block-and-confirm / demo-only-with-risk / not-applicable |

矩阵规则：
- Button Semantic Matrix 只记录按钮语义闭合结论；同名按钮拆分、unknown 语义的阻塞条件和 production-compliant 限制统一以 `references/frontend-ui-contract-guardrails.md` 为准。
- `uiArea=page-toolbar` 的验收证据应指向 `Header` children，并明确不得出现在 `Table.buttons`；`uiArea=table-toolbar` 的验收证据应指向对应 `Table` 的 `buttons` prop 或项目 confirmed 等价封装。典型实现形态分别是先定义 `headerButtons` 再 `<Header title={...}>{headerButtons}</Header>`，以及先定义 `buttons` 数组再 `<Table buttons={buttons} ... />`。

## Component / Enum Provenance
| target | api/prop | value | style | importPath / evidence | status | note |
| --- | --- | --- | --- | --- | --- | --- |
| DataSet / Table / Form / Button / Modal / Lov / Attachment | FieldType / DataSetSelection / SelectionMode / ColumnLock / ColumnAlign / TableQueryBarType / ButtonColor / FuncType / other |  | component-enum / dataSet-enum / dataSet-string / not-applicable |  | confirmed / generatedCandidate / missing / conflict / not-applicable | 组件 props 必须 enum；DataSet 字符串只允许健康 confirmed；Table `selectionMode` 用 `SelectionMode.*`，不要用 `DataSetSelection.*` |

规则：
- 本节只记录 component/enum provenance 事实；enum import 与 string 风格选择、生产 confirmed 条件和混用限制统一以 `references/frontend-ui-contract-guardrails.md` 为准。

## TypeScript Render Contract
| target | typedSurface | requiredTypeSource | implementationShape | forbiddenShape | status | note |
| --- | --- | --- | --- | --- | --- | --- |
| Table columns / line table columns / toolbar buttons / table toolbar buttons / renderer | ColumnProps / ColumnRenderProps / Buttons / ReactNode guard / not-applicable | project import / package d.ts / adjacent module / generatedCandidate / missing | typed-array / typed-renderer-param / conditional-push / type-guard-filter / not-applicable | untyped columns with required `{ record, value }` / `condition && <Component />` in buttons / broad `as any` / missing | confirmed / generatedCandidate / missing / conflict / not-applicable |  |

规则：
- 本节只记录 render typed surface 结论；`ColumnProps/ColumnRenderProps/Buttons` 约束、`condition && <Component />` 禁用和 broad `as any` 禁用统一以 `references/frontend-ui-contract-guardrails.md` 和 `front-hzero-enterprise-process-control` 的生成代码静态质量门禁 为准。

## Style Necessity Contract
样式文件和样式修改必须与布局契约拆开。设计可以确认 HZERO `Header + Content`、Form/Table/Section、滚动边界和间距承载，但不得默认因此新增 `style.less`、`index.less` 或局部 className。详情页区块顺序不等于卡片视觉来源；无明确视觉来源时，Style Necessity Contract 必须写 `componentFirstDecision=component-props-sufficient` 或 `styleFilePolicy=no-new-style`，不得因分区生成白底、边框、圆角、阴影或独立背景。

## Form Layout Contract
需求/FDS/TDS/Figma/UI Contract 或项目 confirmed baseline 未明确 `labelLayout` 时，前端设计默认 `labelLayout=horizontal`，并记录 `labelLayoutSource=default-horizontal-by-design-rule`。`placeholder/none` 只允许用于搜索条件、紧凑筛选区或明确无标签表单。

| target | pageMode | labelLayout | labelLayoutSource | labelAlign | columns | labelWidth | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| headerForm / detailForm / queryForm / other | create / edit / detail / readonly / query | horizontal / vertical / float / placeholder / none | requirement / FDS / TDS / Figma / project-confirmed-baseline / default-horizontal-by-design-rule | left / right / project-default / not-applicable |  |  |  | confirmed / generatedCandidate / missing / conflict / not-applicable |

| target | layoutNeed | componentFirstDecision | styleFilePolicy | styleScope | reason | source | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| page / content / section / form / table / modal / drawer / line-table / other | page-skeleton / spacing / scroll-boundary / background / fixed-height / responsive / visual-state / none | component-props-sufficient / existing-project-class-sufficient / style-required / unknown | no-new-style / reuse-existing-style / modify-existing-style / new-local-style / block-and-confirm | none / Content-inner-only / section-only / table-container-only / modal-body-only / other |  | Figma / UI Contract / project baseline / HZERO runtime gate / user-confirmation / not-applicable | confirmed / generatedCandidate / missing / conflict / not-applicable |

规则：
- 本节只记录样式必要性结论；组件优先、`Header + Content` 包裹禁用、样式作用域和无来源样式阻塞统一以 `references/frontend-ui-contract-guardrails.md` 为准。

### Component Import / API Provenance
| symbol | usage | importSource | importPath | exportShape | apiEvidence | status | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Button / ButtonPermission / Table / Form / Tabs.TabPane / Modal.open / TagRender / c7nOperatorRender / Import / ExcelExportPro / Attachment | JSX / namespace / static-method / helper-function / project-wrapper | builtin-standard / project-evidence / adjacent-module / package-doc / generatedCandidate / current-file / missing / not-applicable |  | named / default / namespace / static-member / current-file / unknown | evidence path, package API, or wrapper contract | confirmed / generatedCandidate / missing / conflict / not-applicable | use-standard-import / use-confirmed-import / use-generatedCandidate-with-verification / block-and-confirm / not-applicable |

规则：
- 本节只记录组件/API provenance 事实；普通 `Button` 也要有来源、非内置 generatedCandidate 不能当 production confirmed、以及缺 provenance 不得 runnable 的细则统一以 `references/frontend-ui-contract-guardrails.md` 为准。
- `importSource=builtin-standard` 只用于已加载 `front-hzero-enterprise-process-control` 的标准 import 坐标 reference 或 owner reference 明确固化的内置标准坐标、固定 helper 或标准组件入口；这类坐标必须写 `status=confirmed`、`implementationPolicy=use-standard-import`。目标工程缺相似页面、缺 import 样例或缺 wrapper 证据时，不得改写为 `generatedCandidate`、`missing`、`use-generatedCandidate-with-verification` 或常见但未确认的项目坐标。
- 导入/导出、Page alias、i18n、权限按钮、renderer/helper、常用 Choerodon 类型、Attachment 和 HZERO 通用组件优先按 `frontend-standard-import-coordinates.md` 填写。标准坐标写 `importSource=builtin-standard`、`status=confirmed`、`implementationPolicy=use-standard-import`；目标工程编译/runtime 未验证只进入 Verification，不得把 importPath 留空或写 `missing/unknown`。
- 存量 `CommonImport` / `ExcelExport` 只进入迁移 finding，不得写入新实现的 Component Import / API Provenance Contract。

## Interaction Contract
| 交互 | 预期 | 来源 | 验证方式 |
| --- | --- | --- | --- |
| 查询 | 回第一页 |  | runtime-manual |
| 刷新 | 保留当前页 |  | runtime-manual |
| 重置 | 清空查询条件并回第一页 |  | runtime-manual |
| 关闭详情/业务弹层 | 列表无遮挡，筛选/分页不丢 |  | runtime-manual |
| 详情主记录切换 | 适用时，同一详情表面内切换业务主记录后 Header、基本信息、区块、Tabs、子表和附件同步更新；不适用时写明原因 | Detail Record Navigation Contract | runtime-manual + Network/DataSet |

## Prohibited Additions
| 项 | 状态 | 说明 |
| --- | --- | --- |
| 无来源摘要头/统计卡片/额外字段 | prohibited | 无 FDS/TDS/TBS 来源不得实现 |

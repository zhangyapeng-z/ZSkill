# Frontend UI Contract Guardrails

本文只描述 Frontend Design 阶段必须产出的 UI Contract。Implementation、Review、Verification、Handoff 的 UI 门禁和手工验收规则在 `front-hzero-enterprise-process-control` 的 UI runtime gates。

## 阅读路由
- 先读 `Design Scope`、`UI Readback Table` 和 `No Source, No UI Element`，判断哪些 UI 事实可以进入 confirmed。
- 需要落设计结构时读 `Required UI Contract Sections`；这里只定义 Design 必须交付哪些 section，不重复运行期拒收清单。
- 需要决定默认值、候选形态或 unresolved 项时读 `Design Defaults`；仍 unresolved 的内容返回 Contract Check / question，不进入 confirmed。
- 需要判断是否可以交接 Task/Implementation 时读 `Output Requirements`。

## Design Scope
- 把 FDS/TDS、Figma/PageSchema、工程证据和用户确认转成可实现、可审查的 UI Contract。
- 明确 `layoutAuthority`、`businessAuthority`、`uiBusinessConflicts` 和 `conflictResolution`。
- 防止无来源字段、按钮、区块、弹层、摘要卡片和内部说明进入 confirmed 设计。

## UI Readback Table

Frontend Design 或 Task Breakdown 进入 Implementation 前，必须形成 `UI Readback Table`。它可以写入 `frontend-design.md`、任务文档或独立 `ui-contract.md`，但不得只停留在对话里。

| 项 | 必填内容 |
| --- | --- |
| 页面/区域 | 列表、筛选、工具栏、操作列、详情 Header、基本信息、详情区块、附件、Modal/Drawer/Overlay、按钮 |
| UI 要求 | 展示字段、组件类型、字段顺序、按钮位置、默认状态、交互动作 |
| 来源 | FDS / TDS / Figma / 工程证据路径和章节 / 用户确认 |
| layoutAuthority | Figma/PageSchema / FDS UI / project evidence / user / missing / not-applicable |
| businessAuthority | FDS/TDS/API / user / project business evidence / missing / not-applicable |
| conflictResolution | follow-layout / follow-business / question / block / not-applicable |
| 状态 | confirmed / generatedCandidate / missing / conflict / not-applicable |
| 实现位置 | 目标组件、DataSet、service、route、样式或验证产物 |
| 验证方式 | Review 静态检查、browser/manual、Network、console、截图或 not-applicable |

## No Source, No UI Element
- 功能文档、FDS/TDS、Figma/PageSchema、目标工程证据和用户确认都没有描述的页面能力、按钮、行操作、Tab、弹层、附件、导入导出、统计卡片、额外字段或分组，不得进入 confirmed 设计。
- 字段是否展示、展示位置、组件类型、布局顺序、按钮区域、交互动作、弹层形态、默认值、编辑态/只读态、状态展示、样式结构和数据处理入口，都必须有来源。Implementation 阶段不得把任何缺来源内容补成“默认优化”。
- 区块标题、页面 Header 标题、标题后缀、摘要头和标题旁状态/金额/数量等辅助展示都属于 UI 元素；没有 FDS/TDS、Figma/PageSchema、UI Contract、项目 confirmed baseline 或用户确认来源时，不得把表单字段挪到标题或 Header 中重复展示。
- Figma/PageSchema 可作为布局、文案、区块、按钮位置和弹层形态来源；不能单独确认业务能力、接口、权限、状态流转、LOV/lookup、附件/导入导出协议或生产请求参数。
- 功能文档有业务能力但 Figma 未画出时，必须标记 `layoutAuthority=fds-ui / missing`，并记录问题或明确不做入口。
- Figma 画出 UI 元素但 FDS/TDS/API 未提供业务契约时，只能作为 `generatedCandidate / partial`，必须进入 Contract Check 或 question。
- 目标工程同类页面的常见按钮或布局只能作为 `project-baseline` 候选；若本功能文档和 Figma 均未提及，默认不实现。
- 目标工程同类页面必须继承 `baselineComparison.evidenceQuality`。`legacy-risk`、`anti-pattern` 或 `unknown-quality` 的相似页面不得把 `UrlHistoryProvider`、自定义 Provider、无来源单组件薄封装、`runtimeAdapters`、`t()` i18n helper、非标准导入/导出入口、local options、`as any` 或无 mock/queryMode 链路升级为 confirmed UI / component pattern。

这里的结论只负责 `confirmed / generatedCandidate / missing / conflict` 判定；运行期怎么拒收 `UrlHistoryProvider`、local-filter、层级穿透、动态高度抖动、组件 API 逃逸等，统一以后续 `frontend-ui-runtime-gates.md` 和静态质量门禁为准。

## 详情承载面判读
- 详情、编辑、新建或审批页面出现“固定表头 / 基础信息 / HeaderForm + 业务页签 / 业务 Tab / 明细区”等结构语义时，Design 默认按两层结构解释：上方基础信息或 HeaderForm 默认可见，下方 Tabs 或业务区域承载一个或多个业务分类、明细集合、附件区、审批/记录区等从属区域。业务名称（如采购、运营、物流、联系人、地址、账号、附件、审批记录）只作为示例，不是触发条件或穷举清单。这个默认不是视觉定稿，只是承载面归属，仍由 UI Contract 记录字段、组件和验证方式。
- 如果同一份 FDS/TDS/PRD 又写“页签包括基础信息”“基础信息页签”等容易产生歧义的说法，Design 必须写入 `uiBusinessConflicts` 或 Detail Contract 备注，说明采用的解释、来源优先级和剩余风险。主语义仍是“固定表头”且没有对等证据时，按默认两层结构自动收口，不弹 question。
- 只有出现对等或更强的相反证据时才触发 `Detail Surface Conflict Confirm` 或阻塞：FDS/Figma/PageSchema 明确把“基础信息”画成或描述成第一个 Tab；用户要求沿用的项目 confirmed baseline 就是 basic Tab；或布局选择会影响用户验收截图、页面冻结口径、production-ready 承诺。question 选项必须使用业务语言说明后果，例如“固定基础信息 + 业务页签”“基础信息也作为页签”；只有确有可追溯的设计稿或项目基线且其布局结论唯一时，才追加“沿用设计稿/项目页面”。不得把内部 `Tabs.TabPane`、`expectedSurface` 等术语作为用户可见选项标题。
- 若最终允许基础信息进入 Tab，Detail Contract 必须写清 `surfaceExceptionSource`、`layoutAuthority`、`conflictResolution=question/follow-layout/follow-project`、`requiredVisibleByDefault` 和负向验收；缺这些来源时，`basic/basicInfo` TabPane 只能作为设计漂移处理，不能进入 confirmed。

## Required UI Contract Sections
- `List Contract`：查询字段、字段组件、模糊查询、默认展示字段、更多筛选、表格列顺序、列宽、操作列、分页、刷新、重置。
- `Route Context / Edit Mode Contract`：routePattern、idSource、isCreateSource、editableDerivation、pageModeDerivation、queryParser、editableAuthority 和 saveRedirectPolicy。
- `Field Visibility Matrix`：字段存在来源与 create/edit/detail/list/query 展示策略拆开记录；字段在 FDS/TDS/API/DTO 或详情字段清单中存在，不等于新建、编辑、列表或查询可见。
- `Field Editability Matrix`：create/edit/copy/detail/approval/readonly/mixed 下每个字段的 editable/readonly/disabled/hidden 状态、原因来源、组件类型、默认值策略、submitPolicy 和验证方式。
- `Empty / Derived Field UX Rules`：编号、合计、比例、审计、保存后生成、无明细/无附件等字段或区块的生成时机、展示时机、空态文案、是否占位和 submitPolicy。禁止把只读空字段直接渲染到页面。
- `Detail Contract`：详情区块顺序、区块标题文案、标题附加信息是否允许、字段分组、只读字段组件、数组字段展示方式、附件入口、敏感字段、按钮 enabled/disabled 条件、HZERO Header/Content 页面骨架、长内容滚动边界、明细表高度策略，以及关键区域的 `expectedSurface / forbiddenSurface / requiredVisibleByDefault`。surface 字段只表达区域归属和承载面，不要求 Design 固化具体 JSX；缺特殊来源时，基本信息 Form 默认在 `Content` 内默认可见，`forbiddenSurface=Tabs.TabPane`，明细 Tab 默认只承载明细/附件等子区域。区块顺序、字段分组和标题只确认信息架构，不自动确认 Card、白底、边框、圆角、阴影、独立背景或其它强视觉容器；这些视觉形态必须来自 FDS/TDS/Figma/PageSchema、项目 confirmed baseline、UI Contract 或用户确认，并在 Detail Section Visual Contract / Style Necessity Contract 中记录。缺视觉来源时默认同一 `Content` 下连续表单区 + 标题 + 必要间距。区块标题默认只展示确认文案，不附加状态、编号、金额或统计值；若需要突出状态，必须在 UI Contract 明确展示位置和组件。Field Visibility Matrix / Field Editability Matrix 已要求 `Tag/Output` 的状态字段应作为表单字段展示，不能被 Implementation 自行拼接到 section title 或 Header 标题后。HZERO 页面默认使用 Fragment 根结构，`Header` 与 `Content` 相邻；业务样式容器、section 背景和底部 padding 放在 `Content` 内部，不得设计业务 wrapper 包住整组 `Header + Content`。当 `Content` 或页面容器承担主滚动时，详情/头行页底部明细 Table 默认自然撑开，不设计 `autoHeight maxHeight` / `TableAutoHeightType.maxHeight` / 依赖视口剩余空间的动态 max-height；该配置只作为单一列表页、固定查询区 + 主表格页候选。若明细表必须内部滚动，必须在 UI Contract 写明稳定容器高度或明确 `height` 来源，并把“滚到底部不抖动”列入验证。不得默认引入 `UrlHistoryProvider`、`HistoryProvider`、`ConfigProvider`、自定义 Context Provider 或页面级 wrapper；只有 UI Contract、项目 confirmed golden-baseline 或明确功能需求确认其必要性时才允许。
- `Form Composition Contract`：详情、编辑、新建、复制、审批或头行页面必须记录页面容器、Form 展示组件、owner DataSet/record、pageMode、字段契约、validation/action 和 readonly 策略的归属。头行、主从、多 Tab 或复用基础信息区默认 `page-container-plus-presentational-form`：页面容器拥有 DataSet、mode、record lifecycle、校验和页面动作，Form 组件只接收 `dataSet`、`mode` 和局部组件参数。DataSet `fields/dynamicProps` 是字段 metadata、bind 和动态可编辑性的唯一入口；Form 不得重建 DataSet、解析 route、复制字段规则或维护竞争性字段 local state。简单单记录页面可以 `simple-page-co-located-with-reason`，但不能混淆这些职责。
- `Basic Info Form Layout Contract`：仅当已确认页面存在基础信息 / HeaderForm、设计输入只给出高层结构而缺列数/容器宽度/跨列/标签/响应式细节、且原型/Figma/PageSchema、用户和项目 confirmed baseline 均未覆盖时，触发 `default-form-layout-by-design-rule`。“联系人表、地址表、账号表”等仅为同类示例，不是穷举。本合同记录 `formRegion`、`layoutAuthority`、`containerWidthPolicy`、`columns`、`columnsSource`、`responsiveColumns`、`labelLayout`、`labelAlign`、`labelWidthPolicy`、`layoutAdjustmentReason`、逐字段 `colSpan`、`valueLengthRisk`、`valueOverflowPolicy` 和负向验收。默认基线为 `containerWidthPolicy=content-available`、`xs=1, sm=1, md=2, lg=3`、`lg=3` 列、`labelWidth=120`、横向标签、短字段初始单列、长值 Lov 可优先评估两列、长正文优先跨当前整行；可根据可用宽度、字段密度、标签/值长度和字段语义记录 `layoutAdjustmentReason` 后调整为 `3/2/1` 列、调整 labelWidth、跨度或断点，无需补外部设计来源。审计/后端生成字段的 create/edit/detail 可见性、readonly/hidden 原因和 `submitPolicy` 必须由 Field Visibility Matrix / Field Editability Matrix 逐字段决定，不属于布局默认。普通 Modal、窄 Drawer 或可用宽度不足是常见调整场景，不设字段数自动阈值。固定 `max-width` 或居中不是通用默认，只能由设计、项目 wrapper 或 confirmed baseline 授权。目标页面确认列数变化时，整行字段的 `colSpan` 必须随当前列数变化；字段顺序、卡片化、额外分组和字段可见性不由本布局规则决定。
- `Detail Record Navigation Contract`：同一详情 Modal / Drawer / 当前页详情内切换业务主记录时必须记录。触发条件是业务主对象身份变化，例如候选人、订单、申请单、单据头；分页、轮播、步骤向导、Tab/区块切换、附件/图片预览翻页不适用。合同必须写清当前记录身份、导航候选范围、请求入口、状态刷新策略、刷新区域和边界行为。
- `Modal / Drawer / Overlay Contract`：组件选型证据、打开方式、生命周期、宽度、Portal/挂载容器、背景、遮罩层级和关闭后状态。所有业务 Modal / Drawer / Overlay 在未确认宽度时，普通表单 Modal 默认 `size=small / width≈520px 或项目 small 等价值`；详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先记录项目 Drawer 默认尺寸或 confirmed baseline、readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`，不强制 small；`medium≈720px`、`large≈80%`、`980px` 或任何百分比宽度只能来自 FDS/TDS、Figma/PageSchema、项目 confirmed baseline 或用户确认，不得生成 `60%~80%` 这类无来源候选。
- `Button Contract`：按钮文案、sourceText、copyPolicy、copyOverrideSource、位置、动作、权限适用性、权限码、类型、enabled/disabled 条件、禁用原因和来源。权限适用性必须先判定为 required / not-applicable / unknown，不能仅凭按钮文案强制生成权限码。required 权限按钮必须通过 `front-hzero-permission-button`，不得设计为普通 Button fallback、永久 disabled 或 no-op；`not-applicable` 或未确认 required 的按钮不得为了视觉统一、间距、对齐或“看起来像权限按钮”而改成 `ButtonPermission`。导入/导出 required 动作还必须具备 `ImportExportEntryProof`，入口为 HZERO 标准组件或项目 confirmed wrapper。按钮区域必须同时记录 FDS 原始区域和消费组件，字段至少包括 `sourceSectionPath / sourceRegion / sourceRegionReason / overrideSource`：页面工具栏按钮默认由 HZERO `Header` 的 children 消费，且负向验收为不得进入 `Table.buttons`；任何表格工具栏按钮，包括列表/表格组件章节下的“列表头按钮区”、表格上方按钮区和明细表工具栏按钮，默认由对应 Choerodon Pro `Table` 的 `buttons` prop 或项目等价封装消费。触发条件包括来源明确为“表格工具栏 / 明细表工具栏 / table toolbar”，或 FDS/TDS 结构位于“列表 / 某业务列表 / 明细表 / 表格组件”下并写“列表头按钮区 / 行列表头按钮区 / 明细表列表头按钮区”；不得只因包含“头”字就转译为页面 Header。不得把表格工具栏按钮设计成 Table 外单独自建按钮区域，除非 `overrideSource` 明确来自 UI Contract、Figma/PageSchema、用户确认或项目 confirmed baseline。按钮视觉合同只约束组件来源、样式类型、spacing/alignment 来源和验证方式，不改变权限适用性结论。
- `Action Entry Matrix`：每个业务动作必须拆分 `actionExistsSource`、`sourceSectionPath`、FDS 原始按钮区 `sourceRegion`、归类原因 `sourceRegionReason`、覆盖来源 `overrideSource` 和 `chosenEntryLocation`。动作存在于 FDS/TDS/API/status-flow 不等于能放到详情 Header；`detail-header/page-header/row-action/table-toolbar/hidden` 必须单独确认。FDS 同时出现“列表头按钮区”和“列表行按钮区”时，必须分别生成 `table-toolbar` 和 `row-action` 入口；同名“删除/编辑/查看”等不能合并成一个能力证明。列表/表格/明细表章节下的“列表头按钮区”若没有 `overrideSource`，不得生成 `page-toolbar` 或 Header 入口。`entryStatus=generatedCandidate/needs-confirmation/missing/conflict` 的业务状态动作不得进入 Header 实现。
- `Button Semantic Matrix`：每个按钮必须按 `buttonId / label / sourceText / copyPolicy / copyOverrideSource / sourceSectionPath / sourceRegion / sourceRegionReason / location / uiArea / semanticKind / navigationTarget / businessMutation / statusActionRef / visibleWhen / enabledWhen / disabledReasonSource / disabledTooltipPolicy / designStatus / overrideSource` 记录语义闭合。页面 Header / 页面级按钮区、业务状态动作、Table `buttons`、行操作列和弹层 footer 必须分区记录；同名“取消/返回/关闭”不能只按文案合并。`uiArea=page-toolbar` 的按钮应落到页面 `Header` children，例如先定义 `headerButtons` 再 `<Header title={...}>{headerButtons}</Header>`，不得因为页面存在 Table 或按钮视觉上靠近表格就放入 `Table.buttons`；`uiArea=table-toolbar` 的按钮应落到对应 Table 的 `buttons` prop，例如 `const buttons = []; buttons.push(...)` 后 `<Table buttons={buttons} ... />`。来源写“显示/隐藏/仅显示”时映射到 `visibleWhen`；来源写“启用/禁用/置灰/可点击”时映射到 `enabledWhen`，不得把“仅某状态启用”转译成“其它状态隐藏”，除非 FDS/Figma/UI Contract 明确写隐藏。业务禁用态必须记录用户可理解的 `disabledReasonSource`；行操作或工具栏按钮在置灰后仍可 hover 的场景默认记录 `disabledTooltipPolicy=Tooltip/title/project-wrapper`，无提示来源时写 missing 并进入 Verification。已确认导航语义的按钮必须是 `semanticKind=navigation`、`businessMutation=none`；取消单据、撤回审批、作废、删除等必须是独立 `business-state-action` 并引用 Status Action Matrix。若上游只写“取消”且语义不清，Design 必须写 `semanticKind=unknown`、`designStatus=needs-confirmation/missing`，并触发补矩阵或 question，不得让 Implementation 猜。
- `Component / Enum Provenance`：Table、DataSet、Form、PermissionButton、Modal、Attachment、i18n、导入导出组件、customizedCode、componentApiProvenance 和 enumProvenance。HZERO + Choerodon 页面只要会新增或修改 `type/selection/dataToJSON/queryBar/editMode/lock/align/labelLayout/color/funcType` 等 enum-like props，就必须写出 enumProvenance 和 enumStrategy；不得把本轮“不确定 import”写成 `not-applicable`。`project-string-confirmed` 只允许用于 DataSet 配置类枚举，并且必须来自同一目标工程稳定、健康的字符串风格证据；Table/Form/Button/Lov/Attachment/Modal/Drawer/Dropdown 等组件 props 必须使用 enum 形态或项目 confirmed 等价 enum 导出。相邻页面若存在 `as any`、无类型 columns/renderer、混用 enum/string 或其它 legacy-risk，不得支撑新增页面继续复制弱类型字符串风格。无项目证据时默认走 asset/fallback enum 候选并记录 generatedCandidate/replacement，不交给 Implementation 猜。不得为单一项目组件新增无来源薄封装、`runtimeAdapters`、`buttonProps`、`t()` 等来隐藏 provenance；若项目已有封装，必须证明其为 confirmed golden-baseline 或 project-compatible。
- `Interaction Contract`：查询回第一页、刷新保留当前页、重置清空条件并回第一页、关闭详情/业务弹层不丢列表筛选/分页；适用时覆盖详情主记录切换后 Header、基本信息、详情区块、Tabs、子表和附件同步更新。

字段与文案保真规则：
- Field Usage Matrix 必须记录 `canonicalField`、`runtimeFieldPolicy`、`adapterAliasPolicy` 和 `forbiddenRuntimeAliases`。空子模块、无参考页面或 asset baseline 场景默认 `runtimeFieldPolicy=canonical-only`；旧字段别名只能作为 service/request adapter 的兼容输入输出，不得进入页面、DataSet、Table、Form、actionGuard 或 submit payload。
- Button Contract / Button Semantic Matrix 默认 `copyPolicy=exact-source`。字段 label、按钮、状态文案、确认/通知、区块标题等正式用户可见文案必须来自 FDS/TDS/Figma/UI Contract/用户确认；近义改写必须写 `copyOverrideSource`。i18n key 覆盖不能替代 sourceText 保真。
- Status Action Matrix 必须记录状态枚举全集和显示文案映射，例如 `NEW=新建`、`IN_APPROVAL=审批中`。实现不得把状态 code 或 meaning 改成旧模型近义值，除非有集中 adapter/legacy runtime 来源。

规则：
- 这些 section 是 Design 的最小闭合面。Task/Implementation/Review 只消费这些 section 的字段和状态，不要求 Design 在这里复写 browser checklist、静态扫描词或 Review 反模式大全。
- 命中页面按钮、业务状态动作、主从、附件、导入导出、权限按钮、renderer/helper、Choerodon enum-like props 时，Design 必须把对应 section/status 写出来；涉及 enum-like props 时 `enumImportMapStatus=not-applicable` 只能用于本轮完全不新增/修改这些 props，并必须写 reason。具体实现与拒收细则交给下游 owner reference。

## Design Defaults
- 列表页默认使用项目已确认的 Table/DataSet 查询范式；无项目证据时只写 generatedCandidate，不写 confirmed。
- 操作列必须设计为最后一列；固定右侧默认按 enumProvenance 使用 `ColumnLock.right` 或项目 confirmed 等价 enum 导出，除非项目证据要求其它 enum 写法。仅有 legacy-risk 相邻页面使用 `lock: 'right'` 不足以确认新增页面字符串策略。
- 操作列“更多”是轻量溢出菜单，不归入 Drawer / Modal Contract。
- 操作列显示必须跟随可见动作清单。只读详情、不可编辑状态或权限隐藏导致当前行没有任何可见动作时，默认隐藏整列；保留空操作列必须有 UI Contract、Figma 或用户确认来源。
- 新建、编辑、复制、详情页必须声明 pageMode、fieldVisibility、fieldEditability 和 empty/derived field UX rules；新建路由固定 `/create` 并默认 create/editable；`/detail/create` 属于违规路径，发现后迁移到 `/create`，不得被项目基线或用户确认放行。
- `requisitionNumber`、`totalAmount`、`budgetRate` 等编号、合计、比例、派生字段在 create 态必须逐字段明确 `visible / hidden / readonly-placeholder`、来源和 `submitPolicy`，不能只因为“属于详情字段”就渲染空 `Output`。
- 页面 Header / 页面级按钮区只能放入 FDS 页面按钮区、Figma/PageSchema、UI Contract、项目 confirmed baseline 或用户确认明确为该区域的动作。取消单据、撤回、作废、删除等业务动作若仅由状态流/API 证明存在，默认保持 hidden 或 needs-confirmation，不得当作 Header 按钮。
- 页面工具栏和表格工具栏是不同区域。设计写“页面工具栏按钮：新建、删除、导出、导入”时，默认 `uiArea=page-toolbar`，消费组件为 `Header` children，验收证据必须能排除 `Table.buttons`；FDS/TDS 在列表或表格组件章节下写“列表头按钮区 / 行列表头按钮区 / 明细表列表头按钮区 / 表格工具栏按钮区：新建、保存、删除、导出”时，默认 `uiArea=table-toolbar`，消费组件为对应 `Table.buttons`。不得把表格工具栏按钮上提到页面 Header，也不得在 Table 上方额外自绘独立按钮容器来替代 `Table.buttons`；不得把页面工具栏按钮下沉到 `Table.buttons`，除非来源明确要求这种布局。只看到“明细表”或“Table”不自动要求按钮进入 `Table.buttons`；必须有工具栏按钮来源和 sourceRegion。
- 审计/后端生成只读字段的 create/edit/detail 可见性、readonly/hidden 原因和 `submitPolicy` 必须由 Field Visibility Matrix / Field Editability Matrix 逐字段确认，并以 FDS/TDS/API/Figma、用户或业务规则为来源。参考页的 create 态隐藏只能作为 `reference-code-fact`，不得成为默认要求。若当前 mode 无可显示值，不得为了占位渲染空 `Output`；display-only 字段不得进入 submit payload。
- UI 编辑态权威来源是 routeContext + UI Contract + 业务状态守卫；DataSet `editFlag` 只能作为展示或提交字段。
- 详情只读字段默认使用项目确认的 Form + Output 范式；裸 div/grid 只能作为项目 confirmed 证据的 follow-project 选择。
- 详情页、表单页、头行页和 Tab 明细页默认只有一个主滚动容器。外层 `Content` / `.page-content` 已负责滚动时，内部明细 Table 不使用动态 `autoHeight maxHeight`；列表页可以沿用项目确认的 `autoHeight maxHeight`，但不得把列表页配置无条件复制到详情明细表。
- 默认不新增无意义封装。标准 HZERO / Choerodon 组件、权限按钮、renderer helper、导入导出组件、Attachment、request/helper、DataSet factory、route/openTab helper 和 i18n 调用，优先直接使用项目 confirmed API 与明确 props。只有满足以下条件之一才允许新增 wrapper/helper：目标项目已有 confirmed golden-baseline / project-compatible 统一封装；封装承载跨文件复用的非平凡平台契约；封装隔离已确认的版本差异、权限/租户/request 协议或组件 API 差异；或设计明确要求公共扩展点。单文件、单组件、只转发 props、只重命名 import、只包一层默认值、隐藏 generatedCandidate / missing / permission / i18n / request / LOV / attachment 状态的封装默认禁止。
- Design 若允许新增或复用 wrapper/helper，必须记录 `wrapperJustification`、`wrapperScope`、`wrappedApi`、`projectEvidence` 和 `rejectedDirectUseReason`；缺这些字段时按直接使用标准 API 处理。
- i18n 默认直接使用项目标准 `intl.get(key).d(defaultValue)` 与 `formatterCollections`。不得新增局部 `t()` / `intlLabel()` / `intlPrefix()` / namespace helper 包装 i18n key，除非目标项目 confirmed golden-baseline 明确要求且不会隐藏 key 来源，也不会把 key/对象传给组件二次解析。
- 导入导出若被需求、FDS/TDS/API/模板资产或 Button Contract 标为 required，默认必须使用 HZERO 标准导入导出组件或项目 confirmed wrapper；参数或契约事实不完整时使用 mock/generatedCandidate 候选常量先支撑标准组件实现，并在 Contract Check / Verification / Handoff 标明来源未确认，不得设计隐藏入口、入口占位、普通按钮、提示入口或 disabled/no-op 假按钮。

这些默认值用于当前 Mock demo Design 收口，不覆盖 Target Placement、当前 Mock 契约或运行期 static gate。production-ready/真实 API 目标进入后续独立集成 advisory，不作为当前例外 gate。

## Output Requirements
- Design 输出必须包含 UI Contract 摘要、缺失/冲突项、generatedCandidate 项和确认人。
- 页面按钮或业务状态动作适用时，Design 输出必须包含 Action Entry Matrix / Button Semantic Matrix 摘要和 `actionEntryMatrixStatus` / `buttonSemanticMatrixStatus`；动作入口位置或按钮语义缺失、冲突或 needs-confirmation 时不得声明 `production-compliant` 或进入 production-ready implementation。
- 复杂页面、多人并行或 UI Contract 过长时，可拆出 `frontend/design/ui-contract.md`。
- UI Contract 不得声明 production-ready；生产可用性由后续 Review/Verification/Handoff 根据 process-control 门禁判断。

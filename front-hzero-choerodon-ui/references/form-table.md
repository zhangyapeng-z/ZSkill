# Choerodon Form / Table / 页面模式参考

## 目录
- 事实边界
- Form
- Table
- DynamicFilterBar
- 页面模式
- 需要确认的未定项

## 事实边界
本文件只记录常见 Form/Table/页面模式中可直接影响实现和审查的事实。

如果这里没有覆盖某个事实，不要编造。应视为未确认，并要求提供用户输入、接口契约或项目证据。

## Form
Pro Form 支持校验定位、默认表格布局、网格布局、分组输入、可配置校验展示、标签行为和溢出 tooltip 处理。

本场景常见的 Form/field 枚举与类型事实：
- 字段类型和校验相关常量在新增枚举导入前，应先遵循目标项目已有的 import 风格。
- 涉及 Form/field 的枚举型 props、字段模式、校验展示、布局、触发模式或文本域 resize 等能力时，必须记录 enum provenance：Evidence enum import map、目标项目 import 证据、`references/enum-map.md` generatedCandidate/fallback 或 not-applicable reason。不要在同一 feature 内一处用枚举、一处用等价字符串；reference import 不得单独标为项目 confirmed。
- 高频 Pro form/field 枚举领域包括字段类型、表单布局、标签布局/对齐、校验展示，以及 TriggerField、IntlField、TextField、TextArea 的模式。
- 如果项目已经从固定子路径（如 `choerodon-ui/pro/lib/field/enum` 或 `choerodon-ui/pro/lib/form/enum`）导入，就保持这种风格，不要混用等价字符串字面量。

从枚举事实迁入的常见 Form/field 导入与成员：
- `choerodon-ui/pro/lib/field/enum`: `ShowHelp.tooltip`, `ShowHelp.newLine`, `ShowHelp.label`, `ShowHelp.none`.
- `choerodon-ui/pro/lib/form/enum`
  - `LabelAlign`: `left`, `center`, `right`.
  - `LabelLayout`: `horizontal`, `vertical`, `placeholder`, `float`, `none`.
  - `FormLayout`: `table`, `none`.
  - `ResponsiveKeys`: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`.
  - `ShowValidation`: `tooltip`, `newLine`.
  - `SpacingType`: `around`, `between`, `evenly`; `RequiredMarkAlign`: `left`, `right`.
- `choerodon-ui/pro/lib/intl-field/enum`: `IntlType.singleLine`, `IntlType.multipleLine`.
- `choerodon-ui/pro/lib/text-area/enum`: `ResizeType.both`, `vertical`, `horizontal`, `none`.
- `choerodon-ui/pro/lib/text-field/enum`: `ValueChangeAction.blur`, `ValueChangeAction.input`; `GroupItemCategory.before`, `after`, `help`, `input`.
- `choerodon-ui/pro/lib/trigger-field/enum`: `TriggerViewMode.popup`, `drawer`, `modal`.

常见用法模式：
- 单记录新增/编辑：`DataSet + Form`。
- create/edit/copy：可编辑业务字段使用对应 Pro field 组件和 `name` 绑定；不要使用 `Output` 代替可编辑输入。
- 只读详情：按场景使用 Form 只读模式或 `Output`。
- 弹窗表单：`Modal/Drawer + Form + DataSet`。
- 字段组件：优先通过 `name` 绑定到 DataSet 字段。
- 提交：优先走 DataSet/Form 提交链路，而不是临时拼接按钮序列化逻辑。

高频 Form props：
- 不依赖 DataSet 的提交：`action`、`method`、`target`、`processParams`
- 布局：`layout`、`columns`、`labelWidth`、`labelAlign`、`labelLayout`、`labelTooltip`、`labelWordBreak`、`useColon`、`requiredMarkAlign`、`separateSpacing`、`spacingType`
- 需求/FDS/TDS/Figma/UI Contract 或项目 confirmed baseline 未明确 `labelLayout` 时，前端设计阶段默认语义为 `horizontal`，实现使用 `LabelLayout.horizontal` 或项目 confirmed 等价 enum。`labelLayout="placeholder"` / `LabelLayout.placeholder` 会把字段 label 放到输入框 placeholder 中，不显示常规左侧/顶部 label；`labelLayout="none"` / `LabelLayout.none` 会隐藏 label。它们只适合搜索条件、紧凑筛选区或已确认无标签表单。详情、编辑、新建和只读业务表单默认必须使用可见 label 布局，除非 UI Contract、Figma 或项目 confirmed baseline 明确要求无标签形态。
- 页面级基础信息 / HeaderForm 必须同时消费 `Form Composition Contract` 和 `Basic Info Form Layout Contract`：页面容器拥有 DataSet、pageMode、validation 和页面动作；Form 展示组件接收 `dataSet`、`mode`，通过 `name` 渲染已定义字段。DataSet 负责字段 metadata 和动态可编辑性，Form 负责组件选择、字段顺序与网格，不得在 Form 内复制字段配置、重建 DataSet 或维护竞争性本地字段状态。
- 参考页面出现的 `columns=3`、`labelWidth=120`、`LabelLayout.horizontal`、固定 `colSpan=3` 或 create 态字段显隐处理，先记录为 `reference-code-fact + sourceRef:line`。其中 create 态显隐只能作为参考事实，不能作为默认表单布局基线。仅当已确认页面存在基础信息 / HeaderForm、设计输入只给出高层结构且缺列数/容器宽度/跨列/标签/响应式细节、并且原型/Figma、用户、项目 confirmed baseline 未覆盖时，触发默认布局规则；参考页未设置 `max-width` 不等于允许补固定宽度。
- 默认表单布局基线：页面级 `Content` 使用 `containerWidthPolicy=content-available`；响应式为 `xs=1, sm=1, md=2, lg=3`，`lg` 初始使用 `columns=3`、`labelWidth=120`、`LabelLayout.horizontal`；短字段初始 `colSpan=1`，长值 Lov 可优先评估 `colSpan=2`，地址、备注、长文本、富文本、附件优先跨当前整行。Implementation 可按可用宽度、字段密度、标签/值长度和字段语义记录 `layoutAdjustmentReason` 后调整 `3/2/1` 列、labelWidth、跨度或断点，不需要补外部布局来源，也不设字段数自动阈值。审计/后端生成字段的 create/edit/detail 可见性、readonly/hidden 原因和 `submitPolicy` 不属于布局默认，必须由 Field Visibility Matrix / Field Editability Matrix 决定。该规则以 `default-form-layout-by-design-rule` 记录，可进入 runnable implementation。普通 Modal、窄 Drawer 或可用宽度不足是常见调整场景；固定 `max-width` / 居中仍必须有来源。
- 短字段、长值 Lov、长正文和审计字段的策略仍按 Field Visibility / Editability Matrix 决定。目标页面确认列数变化时，整行字段的 `colSpan` 必须等于当前列数，不能继续复制参考页的 `colSpan=3`；字段顺序由 UI Contract 决定，Implementation 不得用空只读字段凑布局。
- 绑定：`dataSet`、`dataIndex`、`record`、`pristine`
- 校验/渲染：`showValidation`、`autoValidationLocate`、`fieldHighlightRenderer`
- 事件：`onSubmit`、`onReset`、`onSuccess`、`onError`

`record` 的优先级高于 `dataSet + dataIndex`。

Form 下直属的字段组件可使用 `rowSpan`、`colSpan`、`newLine`、`label`、`name`、`labelWidth`、`hidden`、`useColon`、`requiredMarkAlign` 等布局属性。

`hidden` 只是隐藏字段，并不代表“跳过校验”；仍需考虑校验行为。

实现前检查：
- Form 绑定的是 `dataSet` 还是 `record`。
- 字段是否已存在于 DataSet。
- 校验应落在 `fields`、Form 布局还是提交流程。
- 对于下拉/状态字段，在加入 Form 前是否已确认选项来源、提交值、默认值及后端是否接受。
- 避免对应该由 DataSet 接管的下拉/状态字段再额外保存本地 `value/onChange` 状态。

## Table
Pro Table 适用于排序、查询、分页、自定义操作、拖拽、虚拟滚动、聚合、分组等一体化行为。

本场景常见的 Table 枚举与类型事实：
- 高频 Pro Table 枚举领域包括 `TableMode`、`TableEditMode`、`TableQueryBarType`、`TableButtonType`、`TableCommandType`、`ColumnLock`、`ColumnAlign`、selection mode、分页/高度枚举和排序范围选项。
- 当页面模式支持时，行内编辑应优先使用框架编辑模式和列级 `editor` 元数据。
- 除非目标项目本身就这么写，否则不要在同一页面混用等价字符串字面量和框架枚举。
- 对 `lock`、`align`、`editMode`、`queryBar`、`mode`、command/button type 等枚举型 Table props，应优先沿用 Evidence enum import map 或项目既有 enum import；若项目用字符串且 reference 允许，保持一致，但必须避免 `lock: true`、拼写不明或同一页面混用。只有 `references/enum-map.md` 或场景 reference 证据、无项目证据时，应标 generatedCandidate/missing，不得让 Implementation 猜。

从枚举事实迁入的常见 Table 导入与成员：
- `choerodon-ui/pro/lib/table/enum`
  - `TableMode`: `list`, `tree`; `TableEditMode`: `cell`, `inline`.
  - `TableQueryBarType`: `normal`, `bar`, `none`, `advancedBar`, `professionalBar`, `filterBar`, `comboBar`.
  - `TableButtonType`: `add`, `delete`, `remove`, `save`, `query`, `reset`, `expandAll`, `collapseAll`, `export`.
  - `TableCommandType`: `edit`, `delete`.
  - `ColumnLock`: `left`, `right`; `ColumnAlign`: `left`, `center`, `right`; `DragColumnAlign`: `left`, `right`; `RowBoxPlacement`: `start`, `end`.
  - `SelectionMode`: `rowbox`, `treebox`, `click`, `none`, `dblclick`, `mousedown`.
  - `TablePaginationPosition`: `top`, `bottom`, `both`; `TableHeightType`: `auto`, `fixed`, `flex`; `TableAutoHeightType`: `maxHeight`, `minHeight`.
  - `ScrollPosition`: `left`, `right`, `both`, `middle`; `HighLightRowType`: `click`, `focus`.
  - `GroupType`: `header`, `column`, `row`, `none`; `SortRangeOption`: `currentDataSort`, `allDataSort`.
  - Re-export: `Tooltip as TableColumnTooltip` from `../core/enum`.
  - `TableColumnResizeTriggerType`: `hover`, `mouseDown`; `TableBoxSizing`: `content`, `wrapper`; `MultiDragSelectMode`: `keyboard`, `checkbox`.
- `choerodon-ui/pro/lib/performance-table/enum`: `TableQueryBarType.professionalBar`, `TableQueryBarType.filterBar`.
- `choerodon-ui/pro/lib/table/query-bar/quick-filter/QuickFilterDataSet`: `AdvancedFieldSet.fieldName`, `comparator`, `tableName`, `alias`, `source`, `conditionType`.

`TableQueryBarType`、`ColumnAlign`、`TableAutoHeightType` 这类重名枚举存在于多个模块中；必须从组件实际使用的 table/performance-table 模块精确导入。

`selectionMode` 是 Table 交互选择方式，必须使用 `SelectionMode.*`，例如 `selectionMode={SelectionMode.rowbox}`；不要用 DataSet 的 `DataSetSelection.single/multiple`，后者只属于 `new DataSet({ selection: DataSetSelection.multiple })`。`selectionMode="rowbox"` 这类裸字符串也不得作为新增实现形态。

常见用法模式：
- 标准列表：`DataSet + Table`。
- 查询列表、详情页明细表、主从子表、Tab 内表格和弹层内表格只要存在筛选条件，默认使用 `queryFields` 或 `queryDataSet` + Table filterBar 查询形态；`queryBar` 代码按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态。普通管理列表和明细表筛选不得手写独立 `<Form dataSet={queryDataSet}>` + `<Table queryBar={TableQueryBarType.none}>`，除非 UI Contract、FDS/TDS、用户确认或项目 confirmed wrapper 明确要求外置筛选区/非 filterBar 模式，并记录 mode、sourceRef、reason 以及查询/重置/刷新如何回到 Table/DataSet 查询链路。
- 普通管理查询列表的 ListDS 默认 `autoQuery=true`，加载页面即首查；只有前置查询条件、自定义设置、route/search 派生参数、外部选中态、F 型布局受控列表或项目 wrapper 控制查询时机时，才使用 `autoQuery=false` 并在条件就绪后主动 `dataSet.query()`。
- 表格工具栏：FDS/TDS/UI Contract 写“表格工具栏”“批量按钮区”“明细表工具栏按钮区”时，默认映射为 Table `buttons` 或项目等价表格封装。该规则适用于普通列表页、弹窗内表格、Tab 内表格和主从 child Table；不要在 Table 外手写独立 toolbar 替代表格内建按钮区，除非有项目统一封装或相似页面证据。若设计写“页面工具栏 / page-toolbar / 列表页标题区按钮”，默认由 `Header` children 消费，不得因为按钮视觉上在表格上方就放入 `Table.buttons`。
- 列定义：当列由 DataSet 字段支撑时，优先写 `{ name: fieldName }`。
- 行内编辑：页面模式支持时，优先使用列级 `editor`。
- 选择/批量操作：需确认 `selection`、`primaryKey`、`cacheSelection` 和后端协议。
- 分页/排序/筛选：需确认行为由后端还是前端负责。

高频 Table props：
- 数据/列：`dataSet`、`columns`、`groups`、`header`、`footer`、`border`
- 选择：`selectionMode`、`alwaysShowRowBox`、`showSelectionTips`、`showCachedTips`、`showAllPageSelectionButton`、`selectionColumnProps`
- 查询/按钮：`buttons`、`buttonsLimit`、`queryFields`、`queryFieldsLimit`、`queryBar`、`queryBarProps`、`searchCode`
- 编辑/展示：`mode`、`editMode`、`pagination`、`filter`、`treeFilter`、`editorNextKeyEnterDown`、`keyboard`
- 行/展开：`onRow`、`rowHeight`、`defaultRowExpanded`、`expandedRowRenderer`、`expandRowByClick`
- 性能/定制：`virtual`、`virtualCell`、`virtualSpin`、`autoHeight`、`customizable`、`customizedCode`、`columnResizable`、`columnHideable`、`columnDraggable`、`rowDraggable`
- 树：`treeLoadData`、`treeAsync`、`treeQueryExpanded`

推荐优先使用的列属性：
- `name`：绑定 DataSet 字段。
- `editor: true`：在可行时让列复用字段元数据。
- `renderer`：在大表中应保持轻量。
- `command`：只用于目标项目和组件版本已确认的内置命令数组，例如 `TableCommandType.edit/delete` 或等价标准命令；不得把 `command` 写成 `({ record }) => ...` 自定义渲染函数。
- `sortable` 和 `filter` 不能替代后端查询建模。
- 只有当内置字段映射不足时，才使用自定义 `editor`、`renderer` 和输入逻辑。

### 表格工具栏 buttons
- 表格级动作优先放入 Table `buttons`：例如新增、保存、删除、移除、重置、导出、批量操作和项目 confirmed 自定义按钮。
- “按钮在表格上方”只说明 UI 位置，不说明可以脱离 Table，也不说明必须进入 Table；实现时先判断动作归属是页面级 Header/Toolbar、Table 工具栏还是行操作列。
- 页面级动作如返回、提交、审批、撤回、整单保存，以及 FDS/TDS/UI Contract 只写“页面工具栏 / page-toolbar / 列表页标题区”的同步、全量同步、刷新状态等按钮，通常属于 Header/Page Toolbar；行级详情、编辑、删除属于操作列；批量新增、表内保存、表内删除、表格导出通常属于 Table `buttons`。
- `buttons` / table toolbar buttons 必须保持 Choerodon Pro Table 支持的数组形态，例如标准字符串、配置元组或项目确认的自定义按钮数组元素。禁止把 `<></>`、单个 ReactNode、普通对象、函数返回的非数组、条件表达式混合后的 `false/null/''` 直接交给 `buttons`；条件按钮应先构造明确类型的数组并过滤到组件可消费元素。运行时报 `forEach is not a function` 时，优先检查 `Table.buttons`、`columns`、`column.command`、`queryFields`、`fields[].options` 等应为数组/集合的 props 是否被 Fragment、函数、对象或 raw response 替代。
- Table 外手写 `<div className="*-toolbar">`、普通 `Button` 列表或自定义按钮容器，若没有项目统一封装证据，应按 Pro Table 模式偏差处理；还要检查是否绕过 DataSet 新增、保存、删除、选择态、禁用态、校验、权限和导出链路。
- `buttons` 中混放普通按钮、自定义 JSX 和标准导入/导出组件时，先核对实际渲染 DOM、组件 wrapper 和 CSS 命中位置，再做局部 spacing/alignment 修复。不得把多个裸 `<a>`、Fragment 或自定义按钮挤在一起的问题升级为权限组件替换；`ButtonPermission` 只能来自 Button Contract 的 required 结论。
- 表格工具栏视觉修复应说明 spacing 来源：Table 内建按钮样式、项目等价 wrapper、组件 props，或命中实际 toolbar 节点的局部 class。CSS 无效果时先检查 class 是否加在 Table 外层、是否被组件内部结构隔离、选择器是否覆盖 `buttons` 直接子节点或导出组件触发按钮，不得在未验证 DOM 命中的情况下继续改业务组件形态。

### 操作列 renderer
- 操作列必须是 `columns` 最后一项；除非项目表格封装自动注入操作列并有证据。
- 固定右侧使用 `ColumnLock.right` 或项目 confirmed 等价 enum 导出；不要用 `lock: true` 或 `lock: 'right'` 代替右锁定。
- Choerodon Pro Table 的操作列如果包含多个动作，必须使用 `front-hzero-renderer` 内置 `c7nOperatorRender(actions, record, options)` / `operatorRender(actions, record, options)` 或已记录 `project-override` 的等价 helper；helper import/export、operators payload 和 JSX 误用检查归 `front-hzero-renderer`。
- 直接返回多个按钮/链接 Fragment 是反模式；操作动作、更多菜单、权限和状态守卫归本 skill 的 row-actions scenario reference。
- 当前 HZERO 目标中，Choerodon Pro Table `column.command` 会按命令数组/可迭代集合消费；`command: ({ record }) => ...` 这类函数形态即使能通过构建，也可能在运行时触发 `columnCommand.forEach is not a function`。自定义行操作应写在 `renderer` 中并调用 `c7nOperatorRender` / `operatorRender`；只有目标项目 wrapper 明确把 `command` 函数转译为 renderer 时，才可记录为 confirmed project override。
- `PermissionButton type="text"` 只用于 Table 行操作列，包括详情页中的明细表、子表行操作列；行操作列不要使用 `type="c7n-pro"`。
- Header、PageHeader、页面级 Toolbar、表格上方工具栏、表单普通按钮或详情页非表格按钮不适用行操作列限制；C7N 场景下这些非行操作列 `PermissionButton` 按项目规范优先使用 `type="c7n-pro"`。
- PermissionButton 固定入口、Provider 入参字段、旧组件禁用和旧 props 迁移按 `front-hzero-permission-button`。
- Review 时，HZERO + Choerodon 操作列多动作未使用 `c7nOperatorRender` / `operatorRender` 或已记录 `project-override` 方案应至少标为 major；若导致按钮不可见、溢出或交互不可达，标为 blocking。

性能：
- 复杂 Pro Table 在大数据量下成本较高。
- 对于大数据简单展示场景，应评估分页、`virtual`、`virtualSpin` 和 PerformanceTable。
- 在未检查 API 和项目先例前，不要把 PerformanceTable 用于复杂可编辑或重查询场景。

PerformanceTable：
- 主行数据是普通 `data`，不是 DataSet。
- 适用于不需要 DataSet 驱动行行为的大数据简单展示。
- QueryBar 可以使用 DataSet，但主表行仍是普通数据。
- 重要 props 包括 `columns`、`data`、`height`、`rowHeight`、`rowKey`、`loading`、`virtualized`、`wordWrap`、`isTree`、`rowSelection`、`customizable`、`customizedCode`。
- 开启虚拟滚动时，应使用稳定的 `rowKey`。

## DynamicFilterBar
当页面需要模糊查询、动态查询字段、条件组、保存筛选或快速列展示配置时，使用 Table filterBar 查询形态。普通 HZERO/Choerodon 管理列表也默认使用 `filterBar` 语义，`queryBar` 代码写法按 enumProvenance 选择 `TableQueryBarType.filterBar` 等 enum 形态；缺项目证据时先查 `references/enum-map.md` 并默认使用 fallback enum。

要点：
- 基础用法可依赖 `DataSet.queryFields`。
- 详情页中的明细表、行表、子表或 Tab 内表格如果有类别、金额区间、日期区间、状态等筛选条件，也属于 Table 查询区，必须优先进入 `queryFields/queryDataSet + filterBar`，并按 enumProvenance 生成 `TableQueryBarType.filterBar`。Review 不得只因“Form 已接入查询链路”就判定闭合；手写筛选 Form 或非 filterBar 模式是 UI 形态偏差，除非有明确设计来源，且 `queryBar` 仍必须使用 enum 形态。
- `onQuery`、`onReset`、`onRefresh`、`onBeforeQuery`、`onFieldEnterDown` 应放在 `queryBarProps` 中，而不是作为顶层 `Table` props。
- 新生成 mock/demo 查询不得通过本地过滤、模块内存数组、组件内 seed/filter、`src/utils/mock.ts` 或 `loadData(localFilteredData)` 实现；发现此类 local-filter / inline mock 成功路径时必须阻断并清理，不得作为 `mock-request`、降级分支、待替换保留项或验收依据。
- 其他已确认的自定义查询/重置行为应接入 `queryBarProps.onQuery` 和 `queryBarProps.onReset`；如果项目包装层暴露了自定义查询/重置 props，应确认它们最终转发到了 Pro Table 的 `queryBarProps`，而不是顶层 Pro Table props。
- FDS/TDS 出现“搜索框、关键字搜索、模糊查询、快速搜索”时，必须在 `queryBarProps` 中开启 `fuzzyQuery` 或记录项目不支持证据；可按 UI Contract 配置 `fuzzyQueryPlaceholder`。
- `queryBarProps` 不支持 `fuzzyQueryField` / `fuzzyQueryFields`。模糊查询字段映射属于 QueryDS/queryFields 和 UI Contract 的 `fuzzyQueryFields`，不得作为 Table 组件参数生成。
- `queryBarProps` 的每个 key 必须能追溯到 Choerodon UI Pro Table query bar typed surface 或 confirmed 项目 wrapper 源码/类型/样例证据；不得按语义自造 `searchFieldName`、`keywordField`、`fuzzySearchField` 等参数。
- 当前资产确认的常用 `queryBarProps` 包括 `fuzzyQuery`、`fuzzyQueryOnly`、`fuzzyQueryPlaceholder`、`onQuery`、`onReset`、`onRefresh`、`onFieldEnterDown`、`autoQueryAfterReset`、`refreshBtn`、`searchCode`、`queryFieldsLimit`、`dynamicFilterBar`。其它 key 使用前必须补组件库类型或项目 wrapper 证据。
- 每个查询字段必须明确组件类型，例如 `TextField`、`Select`、`NumberField`、`DatePicker`、`Lov`，并记录是否多选、是否允许清空、默认值和选项来源。
- 查询必须回到第一页；刷新保留当前页；重置清空查询条件并回到第一页。项目封装已有默认行为时记录项目证据。
- 后端条件组能力需要已确认的 `searchCode`。
- `Table.queryFields` 可以覆盖查询控件渲染，但不负责定义查询字段。
- 独立使用 DynamicFilterBar 时，必须显式传入 `queryFields`；DataSet 查询字段不会自动渲染进去。
- `fuzzyQueryOnly: true` 适合仅做模糊查询的页面。
- `queryFieldsLimit` 默认值为 `3`。
- 动态筛选配置包括 `prefixes`、`suffixes`、`fuzzyQuery`、`conditionList`、`tableFilterAdapter`、`searchText`。

如果后端没有筛选条件协议，不要添加 `searchCode`。

## 页面模式
默认映射：
- 单页新增/编辑/详情：DataSet + Form。
- 查询/列表：DataSet + queryFields/queryDataSet + Table。
- 只读详情：Form + Output；数组明细使用 Table；禁止无依据的 div/grid 自绘字段布局。
- 行内编辑：带 editor 的 Table 列 + DataSet submit。
- 主从：父 DataSet + 子 DataSet，通过 `children + cascadeParams` 连接。
- 树：`idField + parentField` 或 `childrenField` + Tree/Table 树形行为。
- 上传页：Attachment/Upload + 业务 DataSet/Form/Table。
- Modal/Drawer 页面：Modal/Drawer + Form/Table + 清晰的生命周期与校验策略。

## 需要确认的未定项
- 字段清单和列清单。
- 查询字段以及后端分页/排序/筛选协议。
- create/update/delete/export URL 和响应结构。
- 行为发生在页面级、modal 级，还是嵌在某个 HZERO route/page 中。

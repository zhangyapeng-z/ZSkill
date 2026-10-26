# 设计分析参考

## 输入识别
- Figma URL：解析 `fileKey` 和 `node-id`；如果用户只给文件级链接，优先通过 question 询问目标 Frame 或让用户确认默认节点，不得只在普通输出中写“请确认节点”。
- 截图/PRD/原型：只能作为设计证据，不能替代接口契约和项目源码证据。
- 多页面设计：先分页面、再分区块；不要一次性把全部 frame 混成一个页面。

## 页面模式
- `list`：有查询区、工具栏、表格、分页或批量操作。
- `form`：以字段录入和提交为主，可能有分组、步骤、底部操作。
- `formWithTable`：顶部标题/操作，主体包含基础信息表单区和内嵌表格区；常见于中台新增、编辑、详情或主单+明细行页面。
- `detail`：只读字段、状态、附件、流程信息、操作按钮。
- `masterDetail`：主表/主列表切换详情、子表、行级展开或关联区域。
- `treeList`：左树右表、组织/分类树、目录树。
- `dashboard`：指标卡、图表、快捷入口，通常不直接映射为 DataSet 表单。
- `uploadImport`：上传、附件、导入导出模板、进度或结果表。
- `componentShowcase`：设计系统或组件规范展示节点，包含基础、行内编辑、树形、拖拽、禁用行、多状态等分组；用于沉淀组件映射，不直接当作业务页面。

## 区块识别
- 顶部标题/说明：页面 title、breadcrumb、PageHeader 或 Header。
- 查询区域：紧邻表格上方，包含输入、下拉、日期、查询/重置按钮。
- 工具栏：新增、删除、导入、导出、批量操作等按钮集合。
- 表格：表头行、重复数据行、操作列、状态列、分页。
- 表单：label-value 对齐、分组标题、必填标识、输入控件。
- 标签页：顶部 `一级tab`、选中态/未选中态、下划线或主题色文本；通常映射为页面内容分组，而不是路由 Tab，除非项目路由明确要求。
- 弹窗/抽屉：浮层容器、遮罩、标题、底部操作按钮。
- 空/错误状态：Empty、Result、Alert、提示文案。

## UI Contract seed 识别
- 列表页：识别查询区、工具栏、表格、分页、操作列后，生成 `DataSet + Table + filterBar` seed，并记录 enumProvenance 以决定 `TableQueryBarType.filterBar` 等 enum 形态。出现关键字、搜索框、模糊搜索时追加 `fuzzyQuery` 候选。
- 查询字段：从输入框、下拉、日期、LOV、范围控件识别 QueryFields Schema 候选，记录组件类型、是否多选、是否允许清空、默认展示状态和 `queryFieldsLimit` 候选。
- 表格：识别列顺序、操作列、固定列、分页和行操作。操作列 seed 必须要求最后一列、`ColumnLock.right`，并禁止 `lock: true` / `lock: 'right'`。
- 详情页：只读单对象区块生成 `Form + Output` seed；履历、教育、附件等数组区块生成 Table/Attachment seed；禁止 `div/grid` 手写详情。
- 弹框/抽屉/overlay：生成 mask、z-index、portal、不透明背景和关闭后无遮挡 seed；Header、固定表头、固定列或列表内容穿透到 overlay 上方属于 blocking 风险。
- HZERO 边界：页面容器、route/menu、PermissionButton、i18n、platform 能力只输出候选或缺口，不从 Figma 文案推导真实编码。
- mock/demo：如果设计转 demo，列表/查询默认生成 `queryMode=mock-request` seed；`service/mock + loadData`、模块内存数组、`src/utils/mock.ts` 或组件内 filter 必须作为 blocking cleanup，不能作为生成 demo 策略。

## F 型布局识别
- 当页面同时出现顶部标题/操作、顶部查询/筛选区、左侧记录列表、右侧详情区时，设置 `page.layout=fLayout`；页面类型可按业务主形态继续使用 `masterDetail`、`detail` 或 `formWithTable`。
- F 型布局至少抽象出 `header`、`listHeader`、`list`、`listItem` 四类区域；右侧详情分组映射为 `contentCard`，无数据/无权限态映射为 `emptyPage`。
- 左侧列表如果有折叠按钮、拖拽宽度、加载更多、状态标签、列表表格切换或多选，需要作为 UI Contract seed 的 requiredRules 记录。
- 右侧详情如果包含保存按钮、只读/编辑字段、Tabs 吸附或多 ContentCard，需要记录 `_LOCATED_DATA_` 选中项来源、详情 DataSet 加载触发、保存后刷新定位和滚动容器风险。
- F 型布局下游必须触发 `front-hzero-enterprise-page` 的 f-layout scenario reference；普通表格查询仍同时触发 `front-hzero-choerodon-ui` 的 query-table scenario reference，右侧详情存在头行明细事务时同时触发 `front-hzero-choerodon-ui` 的 master-detail scenario reference。

## UI 来源优先级和冲突处理
- UI 显示布局优先级：用户明确确认 > Figma/PageSchema confirmed > 目标工程同类页面基线 > FDS UI 描述 > 后端 TDS 前端提示。
- 业务契约优先级：用户明确确认 > FDS/TDS/API/DTO/权限/平台协议 > 目标工程业务证据 > Figma 可见文案。
- Figma/PageSchema confirmed 应作为页面布局、区块顺序、视觉层级、字段显示顺序、按钮位置、列表/表单/详情/弹层形态的首要视觉证据。
- FDS/TDS/API 仍是业务能力、字段语义、接口、状态流转、权限、route/menu 和生产请求契约的首要证据。
- 当 Figma 与 FDS/TDS 不一致时，必须输出 `uiBusinessConflicts`，不能静默合并。若只是视觉呈现差异且业务能力完整覆盖，可按 Figma 布局继续；若影响业务能力、字段语义、权限、接口或验收，必须标记 `conflict/missing` 并交由主流程确认。

## 中台表单页识别模式
真实样例 `中台表单 / node-id=2:2282` 暴露了以下可复用模式：
- 根节点宽度 1440，纵向布局，顶部区域 padding `16px 48px 0px`，主体区域 padding `16px 48px`。
- 顶部 Header：左侧 24px Page title，右侧紧凑按钮组，按钮可能包含主按钮、线框按钮、纯 icon 按钮。
- Header 下方一级 Tab：选中态组件名 `一级tab / 状态=sel`，未选中态 `一级tab / 状态=unsel`。
- Basic Information 卡片：标题条 + 白底内容区，内容区内按行排列表单项。
- 表单项：组件集 `表单`，实例名 `类型=文本输入框, 标签位置=上下结构, 大小=紧凑`；内部有 `表单标签` 和 `文本输入框`。
- 必填：`表单标签` 的 `componentProperties.必输=true`，并出现 `*` 文本；输入框效果可能为 `input/@show-inputUnderline-required`。
- 表格卡片：标题 `Table`，右侧文本按钮和 icon 按钮组，下面有 `临时筛选` 与表格网格。
- 临时筛选：包含 `模糊搜索`、`默认筛选`、刷新、筛选项文本、下拉单选、LOV、时间、时间段、添加筛选。
- 表格：每列常由一个纵向 frame 表示，首个子节点是 `表头`，后续重复 `表格内容`；需转置为 Table columns + sample rows，而不是按 Figma 列 frame 生成 DOM。

## 占位文案处理
- `Page title` 可作为页面标题占位，不代表最终业务标题。
- `Label` 表示字段标签占位；字段 `name` 和真实 label 均为 `missing`，除非用户或接口契约补充。
- `Button` 表示按钮文案占位；只能确认按钮数量、主次、icon 和位置。
- `Table title`、`Table text` 表示表头/单元格占位；只能确认列数、行数和表格结构。
- `Please enter` 表示文本输入 placeholder，可映射为输入框候选，但不能推出字段业务含义。

## PageSchema 字段来源标记
- `confirmed`：来自 Figma 文案、用户明确输入、接口契约、项目源码或相似页面。
- `inferred`：仅从视觉形态推断，如下拉候选、日期候选、金额候选。
- `missing`：生成代码前必须确认，如接口、权限、字段真实类型。

## 字段候选类型
- 文本输入：单行输入框、搜索框，标记 `candidateType: string`。
- 紧凑上下结构表单：Figma 组件集为 `表单` 且内部 `文本输入框`，标记 `candidateType: string`，同时记录 `layout: verticalCompact`。
- 数字/金额：右对齐数字、金额符号、小数位，标记 `candidateType: number | currency`。
- 日期/时间：日期格式、日历图标、时间范围，标记 `candidateType: date | dateTime | dateRange`。
- 枚举：下拉箭头、状态 tag、少量固定选项，标记 `candidateType: lookup`，但不得编造 `lookupCode`。
- LOV：带搜索/选择弹窗意味、对象编码+名称，标记 `candidateType: lov`，但不得编造 `lovCode`。
- 附件/上传：上传按钮、附件列表、拖拽区，标记 `candidateType: attachment | upload`，但不得编造 bucket 或协议。

## 质量要求
- PageSchema 应表达业务结构，而不是 Figma 层级树。
- 表格应抽象成 columns/rows/actions/filterBar，而不是保留每一列的纵向 frame 结构。
- 表单应按行、列数、必填和控件类型抽象，不保留每个组件内部 label/input frame。
- 保留视觉约束：布局密度、区块顺序、重要文案、主次按钮、响应式风险。
- 保留 UI Contract seeds：每个列表、筛选、表格、详情、overlay、权限按钮和 mock/demo 风险都应进入 seed 或明确不适用。
- 保留来源优先级：涉及 Figma/FDS/TDS 混合输入时，PageSchema 和 UI Contract seeds 必须记录 `layoutAuthority`、`businessAuthority` 和冲突处理结论。
- 不保留无意义层级：auto layout 包裹、装饰性 frame、重复背景层。

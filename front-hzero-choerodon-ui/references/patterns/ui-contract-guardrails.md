# Choerodon UI Contract Guardrails

用于 Choerodon UI Pro / C7N 页面实现、审查和问题修复时的专项守卫。它承接上游 UI Contract，但只约束 Choerodon 组件、DataSet、Table、Form、Modal/Drawer、PermissionButton 和 mock/production 数据链路。

## 阅读路由
- 区分企业前端流程级 guardrail 和 Choerodon 组件级规则时读 `与企业前端 Guardrail 的边界`。
- 判断是否适用、L1 是否例外时读 `使用条件` 和 `L1 例外`。
- 编码前缺 UI Contract 或 evidence 时读 `编码前必读资产`。
- 列表、查询、操作列、mock request 和详情展示分别读 `列表与查询条`、`Table 列与操作列`、`DataSet 与 Mock Request`、`详情与只读展示`。
- 弹层、Review 和验证时读 `Modal / Drawer / Overlay`、`Review 阻塞项`、`验证清单`。

## 与企业前端 Guardrail 的边界

- 企业前端 `front-hzero-enterprise-design` 的 UI Contract guardrails 负责设计期 UI Contract 是否生成、来源优先级和无来源 UI 禁止规则。
- 企业前端 `front-hzero-enterprise-process-control` 的 UI runtime gates 负责运行期流程级门禁：UI Contract 是否继承、是否进入 Review/Verify/Handoff、产物路径和 lessons learned。
- 本文负责 Choerodon 组件级门禁：Table/DataSet/Form/Output/Modal.open/PermissionButton/mock request 的写法、反模式和 local-filter / inline mock blocking 识别。
- 实现阶段先消费上游 UI Contract，再按本文落到 Choerodon 代码。缺少 UI Contract 时，本文只允许输出组件/DataSet 映射建议、待确认项，或返回主流程补资产，不得生成非 runnable 页面骨架。
- 如果流程级和组件级规则冲突，不在代码中自行折中；Review 应记录 `guardrail-conflict` 并建议修订对应 reference。

## 使用条件
- 新增或修改 Choerodon 查询列表、详情、弹窗、抽屉、附件、权限按钮、DataSet transport。
- 前端任务已经进入实现、审查、验证或手测修复阶段。
- 用户手测暴露了组件选型、Table queryBar、Modal/Drawer/Overlay 弹层、只读详情、mock/local-filter、权限按钮或 UI 可用性问题。

## L1 例外

以下场景不强制生成完整 UI Readback Table、UI Contract 或 Evidence，但仍必须遵守 Pro-first、DataSet-first 和“不编造契约”：
- 只解释单一 Choerodon API、props、事件或枚举。
- 只修改无可见 UI 影响的 import、类型、注释、测试或小型工具函数。
- 用户明确要求单文件 L1 修复，且不涉及列表查询、详情、Drawer、权限按钮或 DataSet transport。

若 L1 修改触及可见 UI、查询/分页、详情展示、按钮权限、Modal/Drawer/Overlay 或 transport，执行命中的最小专项检查，并在结果中写明 `uiContract: minimal / not-applicable + reason`。

## 编码前必读资产
编码前必须先完成或读取上游 UI 回读资产：
- UI Readback Table：列表、筛选、按钮、详情区块、字段顺序、交互动作逐项追溯 FDS/TDS/TBS。
- UI Contract：字段、查询、列表列、详情区块、按钮、交互、权限、生产契约状态。
- Choerodon Enum Import Map / enumProvenance：DataSet、Table、Form、Button、Lov、Attachment、Modal/Drawer 等 enum-like props 的项目风格和 import/string 证据。
- Evidence：目标工程、相似页面、路由入口、scripts、包管理器、验证命令候选。

缺失这些资产时，不能直接自由生成完整页面。只能补充待确认项、输出组件/DataSet 映射建议，或返回前端主流程补资产；不得生成非 runnable 页面骨架。

## 列表与查询条
- 普通管理列表默认使用 Choerodon Pro `Table + DataSet + filterBar` 查询形态；`queryBar` 代码按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态，不允许目标项目健康字符串风格。无项目证据时优先使用 `references/enum-map.md` fallback enum，不得默认裸写 `queryBar="filterBar"`。
- 不得优先手写查询 `Form`、局部 `useState` 查询对象或独立查询按钮链路。
- FDS/TDS/TBS 中出现“搜索框、关键字搜索、模糊查询、快速搜索、全文检索”等语义时，必须在 `queryBarProps` 中开启 `fuzzyQuery`，placeholder 使用 `queryBarProps.fuzzyQueryPlaceholder`；`fuzzyQuery=false` 与缺失同等处理。`fuzzyQueryFields` 是 UI Contract / QueryDS 字段映射，不得生成 `queryBarProps.fuzzyQueryField` / `queryBarProps.fuzzyQueryFields`。确无关键字/模糊搜索需求，或项目不支持时，写明 `not-applicable + reason` 或项目证据。
- 每个查询字段必须有 QueryFields Schema：字段名、label、组件类型、是否多选、是否允许清空、默认值、选项来源、查询提交值。
- 查询字段组件类型必须明确为 `TextField`、`Select`、`NumberField`、`DatePicker`、`Lov`、`TreeSelect` 等，不得只写业务字段名。
- `queryFieldsLimit`、默认展示字段、更多筛选字段必须来自 UI Contract 或项目标准；未确认时默认保守使用 `3`，并标记可人工调整。
- 查询必须回到第一页；刷新保留当前页；重置清空查询条件并回到第一页。项目封装已有行为时记录证据。

## Table 列与操作列
- 列表列顺序必须来自 UI Readback Table 或字段映射表；无来源字段不得展示，确需候选展示时标记 `generatedCandidate`。
- 列 label 必须来自 FDS/TDS/UI Contract；i18n key 和 fallback 中文保持一致。
- 默认列宽按类型收敛：姓名/短文本 120，状态/枚举 100，日期 130，金额/数量 120，长文本 220；操作列 120 只适用于单个短动作或无多动作 helper。多动作操作列必须按 `limit` 内可见动作、`operators[].len/title`、按钮间距和“更多”入口预留设置稳定宽度；项目已有列宽规范优先，但不能导致可见按钮文案截断。
- 操作列必须是 `columns` 最后一项。
- 操作列固定右侧必须使用 `ColumnLock.right` 或项目 confirmed 等价 enum；禁止用 `lock: true` 或 `lock: 'right'` 代替右锁定。
- Table enum-like props 如 `queryBar`、`editMode`、`lock`、`align`、`selectionMode`、`heightType` 必须继承 enumProvenance，并必须使用 `TableQueryBarType.*`、`TableEditMode.*`、`ColumnLock.*`、`ColumnAlign.*`、`SelectionMode.*` 等 enum 形态。`selectionMode` 必须来自 `choerodon-ui/pro/lib/table/enum` 的 `SelectionMode.rowbox/treebox/click/none/dblclick/mousedown`，不得写 `DataSetSelection.single/multiple`。健康字符串证据只能作为存量兼容风险记录，不能作为新增组件 props 的实现形态。
- 多动作操作列必须使用 `front-hzero-renderer` 内置 `c7nOperatorRender(actions, record, options)` / `operatorRender(actions, record, options)` 或已记录 `project-override` helper。缺 import/export 时阻塞或补工程，不编造 import 或 payload，也不降级为按钮 Fragment。
- 多动作操作列中 `operators[].len` 必须覆盖 `title` / `ele` 的实际用户可见文案；`options.limit` 只控制溢出数量，不用于修复可见按钮截断。发现前 N 个按钮被省略时，应校准 `len` 和操作列宽度，不得无来源提高 `limit`。
- 操作列“更多”必须由 `c7nOperatorRender` / `operatorRender` helper overflow、项目已有操作菜单、Dropdown/Popover/Menu 等轻量浮层承载；不得使用 Drawer、`Modal.open({ drawer: true })` 或详情弹层承载“更多”菜单。
- 每个按钮必须记录 Button Contract：文案、位置、触发动作、权限适用性、权限码、enabled/disabled 条件、来源文档。
- Header/Toolbar 按钮和 Table 行操作按钮只有在 Button Contract 判定 `permissionRequirement=required` 时才强制使用 `PermissionButton`；行操作通常 `type="text"`，页面级按钮按项目标准优先 `type="c7n-pro"`。`not-applicable` 有来源 reason 时普通 `Button` 可接受。
- PermissionButton 固定入口、Provider 入参字段、权限码数组结构和 Button props 透传按 `front-hzero-permission-button`；旧相似页面不得覆盖该入口。
- 可配置表格必须设置稳定 `customizedCode`，并与 feature/page code 绑定；缺少 namespace/templateCode 时标记 `generatedCandidate`。

## DataSet 与 Mock Request
- DataSet enum-like props 必须先有 enumProvenance。`fields[].type`、`queryFields[].type`、`selection`、`dataToJSON`、`status`、事件名等如果项目风格为 enum，必须导入确认的 `FieldType`、`DataSetSelection`、`DataToJSON` 等；项目风格为 string 且有健康相似页面证据时可保留字符串；相似页面若被判为 legacy-risk、使用 `as any` 或无类型 columns/renderer，必须写入 `rejectedPatternItems`，不能支撑新增页面字符串默认；无证据不得用 `as any` 硬包。
- `production-transport`：接口契约 confirmed 后，DataSet `transport.read` 必须说明 URL/method/payload/page/response adapter。
- `mock-request`：列表 mock demo 必须走 HZERO 本地 devServer middleware 暴露的 HTTP mock API，并让 DataSet `transport.read`、项目 request adapter 或非 DataSet service-action request 请求该来源；DataSet 页面不得用 transport 调业务 service 充当请求链路。
- `local-filter`：只作为 cleanup/rework blocker 识别；新生成 mock/demo 不得使用本地内存数组、组件内 seed/filter、`src/utils/mock.ts` 或 `query -> loadData` 支撑列表查询、分页、重置、刷新，也不得保留为 demo 或降级分支。
- `PageResponse -> DataSet` 映射必须在 request adapter / DataSet transport response adapter 中声明，组件层不得随意解析；不得把本地 `PageResponse` 塞进 `transport.read` 冒充真实接口。
- QueryDS 只管理查询条件，ListDS 只管理列表数据；不要让单个组件混管查询、列表、详情和同步状态。
- `paging=true` 与手动 `loadData` 混用时必须作为 blocking cleanup finding；新生成 mock/demo 分页必须通过 request adapter 或 DataSet transport 验证。
- `new DataSet({ ... } as any)`、`new DataSet(config as any)` 只能作为短期局部类型缺口处理，不能包裹包含 enum-like props 的完整配置。若配置内有 `type/selection/dataToJSON/status/events`，必须先补 enumProvenance 或改为项目确认 enum/string 风格。

## 详情与只读展示
- 新建、编辑、复制、详情页面必须继承 Route Context / Edit Mode Contract。页面业务状态应由 `getRouteContext(location, params)` 或项目等价 wrapper 派生，不得直接依赖 `window.location.hash`、hash 正则或散落 query/params 解析 `editFlag/isCreate/pageMode`。
- 新建路由固定 `/create`；`/detail/create` 属于违规路径，发现后迁移到 `/create`。新建页必须默认 create/editable；DataSet `editFlag` 只作为展示/提交字段，不作为 UI 编辑态权威来源。
- 新建表单默认值必须来自 UI Contract 的逐字段来源。除已确认的系统默认值、当前用户上下文、复制来源或后端回填占位外，不得从详情 mock seed、列表记录、示例数据或当前时间预填业务输入字段；后端生成的编号、状态、审计、申请/提交时间默认不应作为用户可见输入值提前写入。
- 详情只读字段默认使用 Choerodon Pro `Form + Output` 或项目等价只读 Form 模式；禁止用零散 `div/grid` 自绘字段布局。
- Form 必须同时满足 `Form Composition Contract` 和布局合同：页面容器拥有 DataSet、pageMode、record lifecycle、validation 与保存/提交动作；可复用 HeaderForm / DetailForm 只接收 `dataSet`、`mode` 和必要的局部组件参数。DataSet 负责字段 metadata、bind、required、dynamicProps 和动态可编辑性；Form 只负责组件、顺序和布局。展示组件内重建 DataSet、复制字段规则、解析 pageMode、维护竞争性字段 local state 或把全局 disabled Form 当作字段权限/模式逻辑，均属于 `HZUI-LAYOUT-001` finding。
- Form 布局型 props 必须可追溯：`columns`、`labelLayout`、`labelAlign`、`labelWidth`、`colSpan`、响应式列数和 `containerWidthPolicy` 应来自 UI Contract、Figma/PageSchema、项目同类页面、用户确认或 `default-form-layout-by-design-rule`。仅当基础信息 / HeaderForm 已确认、设计输入只给出高层结构且缺布局细节、并且原型/Figma、用户或项目基线未覆盖时，采用默认基线：`containerWidthPolicy=content-available`、`xs=1, sm=1, md=2, lg=3`、`lg=3` 列、`labelWidth=120`、横向 label、短字段初始单列、长值 Lov 可优先评估两列、长正文优先跨当前整行。可按可用宽度、字段密度、标签/值长度和字段语义记录 `layoutAdjustmentReason` 后调整列数、labelWidth、跨度或断点，无需补外部布局来源，也不设字段数自动阈值。审计/后端生成字段的可见性和提交策略由 Field Visibility Matrix / Field Editability Matrix 决定，不属于布局默认。该默认可作为 runnable implementation 依据。固定 `max-width` 或居中策略仍必须有来源。目标页面确认列数变化时，整行字段必须使用当前列数的 `colSpan`；字段顺序由 UI Contract 决定。
- Form/Button enum-like props 必须可追溯：`labelLayout`、`labelAlign`、`layout`、Button `color`、`funcType`、`type` 等不得只凭记忆裸写，也不得用项目字符串风格作为新增实现形态。必须导入并使用 `LabelLayout.*`、`LabelAlign.*`、`ButtonColor.*`、`FuncType.*` 等 enum 或项目 confirmed 等价 enum 导出。
- 单对象字段使用 `Form + Output`；履历、教育、语言、附件明细等数组字段使用 Choerodon Pro Table。
- 详情区块顺序必须按 FDS/UI Contract；每个字段归属到已确认分组，如基本信息、归档信息、求职意向、履历、附件。
- 详情字段值过长时必须按 Detail Field Overflow UX Rules 处理，不得只通过放大 Modal / Drawer 宽度解决。邮箱、手机号、编号、姓名、公司名、职位名、地址和短标签等短语义字段默认可用单行省略 + Tooltip 展示完整值；备注、驳回/拒绝原因、经历描述、富文本和长正文默认使用多行块或设计确认的 2/3 行省略。AI 可按字段语义和项目证据默认选择 `valueOverflowPolicy`；只有 FDS/TDS/Figma/项目基线/用户输入冲突，或策略会改变业务可读性、验收含义、复制/查看完整内容能力时才触发 question。
- 不得新增 FDS/TDS/TBS/UI Contract 未要求的摘要头、统计卡片、候选人概览区或装饰性标题块。
- 敏感字段只消费后端返回的 `*Masked` 或已确认脱敏字段；前端不得自行造脱敏规则。
- 附件展示必须区分可访问、失败、无附件；local mock 下不得宣称真实下载已验证。
- 长详情页、头行页和 Tab 明细页必须有明确滚动容器。HZERO `Header` 与 `Content` 必须作为 Fragment 下相邻根节点；业务 wrapper、section 样式、底部 padding 和滚动相关样式应位于 `Content` 内部，不得包住整组 `Header + Content`。检查 Page/Content、业务 wrapper、Tabs/TabPane、Table body、固定 Header/Toolbar 和父微前端容器的 height/overflow 关系；不要把滚动问题简单归因于样式是否被注释。实现应保证长内容、小视口和大量明细行时可滚到最后一区块，固定表头/固定列/页头不遮挡内容。
- 当 HZERO `Content`、`.page-content` 或页面级容器已经承担详情/头行页主滚动时，内部明细 Table 默认不得使用 `autoHeight={{ type: TableAutoHeightType.maxHeight, ... }}`、`heightType=maxHeight` 或等价依赖视口剩余空间反复计算高度的配置。该配置适合单一列表页、固定查询区 + 主表格页；复制到详情底部明细表会与页面滚动容器争夺高度，滚到底部时可能因 Table 重新计算 max-height 改变页面总高度，触发浏览器滚动位置反复修正。详情/头行明细表默认自然撑开并由页面统一滚动；若确需限制明细区域高度，使用有设计来源的稳定容器高度或明确 `height`，并验证底部不抖动。

## Modal / Drawer / Overlay
- Modal / Drawer / Overlay 的形态必须来自需求/FDS/TDS、Figma/PageSchema、UI Contract、项目同类页面证据或用户确认；不得默认写死为 Drawer。详情、表单、导入组件、预览等业务弹层统一使用工程已有 `Modal.open` 或已确认等价 wrapper 打开；确认需要 Drawer 后必须使用 `Modal.open({ drawer: true, resizable: true, ... })` 或等价 wrapper；确认普通 Modal 后必须使用 `Modal.open({ ... })` 或等价 wrapper。该规则不适用于操作列“更多”溢出菜单；破坏性动作二次确认仍可按项目规范使用 `Popconfirm`、`Modal.confirm` 或等价确认组件。
- 若需求/FDS/TDS/Figma/UI Contract 明确指定普通弹窗、Modal 或对话框，必须使用普通 Modal 或项目等价对话框；不得为了复用默认写法改成 Drawer。若明确指定抽屉/Drawer，必须使用 Drawer 或项目等价抽屉；不得降级为普通 Modal。
- 不得默认改用 JSX Modal/Drawer、组件常驻渲染加 visible/open state 或自绘 Overlay；`<Modal drawer visible>`、`<Modal visible>`、`<Modal open>`、`<Drawer visible>` 和 `visible/open state + 常驻 JSX` 对新增或重构业务弹层是严格反模式。已有 legacy 写法维护时必须记录兼容原因；新增或重构业务弹层必须迁移到 `Modal.open` 或已确认等价 wrapper。
- 查看详情 Drawer 的内容组件应拆成纯内容组件，由列表页或触发方在点击事件中调用 `Modal.open({ drawer: true, resizable: true, ... })` 打开；不得在页面 JSX 中常驻渲染隐藏 Drawer 再通过 visible/open state 切换。若为了支持“上一个/下一个”记录切换而需要状态，状态应在内容组件内维护当前业务主记录，或使用已确认的 modal update/recreate 机制；不得因此退回常驻 JSX Drawer。
- 所有业务 Modal / Drawer / Overlay 的宽度严格按 UI Contract；设计未指定宽度时，普通表单 Modal 默认 `size=small`（约 520px 或项目 small 等价值），详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并必须记录 readabilityRisk、Form columns/colSpan 与 `valueOverflowPolicy`。medium、large、百分比宽度或 980px 等宽框只在设计/Figma/PageSchema/项目 confirmed baseline/用户明确要求时使用；不得仅因相似页面常见宽框就自行放大，也不得为解决单个长字段而放大弹层。
- Modal / Drawer / Overlay 不得在 `visible=false` 时仍以可见层级覆盖页面；`Modal.open` 应由点击事件触发，或由受控 effect 严格限制生命周期。
- 使用 effect 打开 Modal / Drawer / Overlay 时必须评估依赖项，避免数据刷新或 loading 更新重复打开。
- 详情 loading/数据更新不得造成 Modal / Drawer / Overlay 重建；必要时把 open lifecycle 与 content update 分离。
- Modal / Drawer / Overlay 的 content/body/wrapper 必须有不透明背景；必须验证 mask、z-index、Portal 容器、背景层级和关闭后 Header/列表无遮挡。
- Header、固定表头、固定列、列表内容或页面容器出现在 Modal / Drawer / Overlay 内容层上方时，一律视为层级穿透；生产或 production-ready 任务中按 blocking 处理。
- 关闭 Modal / Drawer / Overlay 后必须验证筛选状态保留、分页状态不丢失、列表操作仍可点击。

## Review 阻塞项
以下问题在生产或 production-ready 任务中应至少标为 major；造成不可用时标为 blocking：
- 手写查询 Form 替代 `Table + filterBar`，且无工程证据。
- 关键字/模糊搜索未开启 `fuzzyQuery`、显式 `fuzzyQuery=false`、误写 `queryBarProps.fuzzyQueryField/fuzzyQueryFields`，或未解释不支持原因。
- 操作列不是最后一列，或使用 `lock: true` 代替右锁定。
- 多动作操作列未使用已确认 HZERO helper 且无降级说明。
- `limit` 内可见行操作按钮被截断，或通过提高 `limit`、取消 overflow、展示全部动作掩盖 `len/title/width` 不匹配。
- DataSet/Table/Form/Button enum-like props 缺 enumProvenance，或用 `as any` 包住整段配置逃逸类型和枚举证据。
- 项目 enum 风格下裸写 `type: 'string'`、`selection: 'multiple'`、`dataToJSON: 'dirty'`、`queryBar="filterBar"`、`editMode="inline"`、`lock: 'right'`、`labelLayout: 'float'`、`color="primary"`、`funcType="flat"` 等且无降级说明。
- DataSet 项目 string 风格下混入未确认 enum import，或同一 feature 对等 props 一处字符串一处 enum；组件 props 不允许 string 风格作为新增实现形态。
- 操作列“更多”使用 Drawer/Modal 承载，或被错误归入 Detail / Drawer Contract。
- PermissionButton 未通过 `front-hzero-permission-button` 检查，或 Provider 入参字段与目标项目契约不一致；导致权限失效或运行时异常时 blocking。
- 弹层形态与需求/FDS/TDS/Figma/UI Contract 明确要求不一致，例如普通弹窗被实现为 Drawer，或 Drawer 被实现为普通 Modal。
- 详情只读字段使用 `div/grid` 自绘。
- 新建页业务字段被 mock seed、示例数据、历史详情数据或当前时间预填，且 UI Contract 未给默认值来源。
- `labelLayout`、`labelAlign`、`columns` 等 Form 布局 props 无来源，导致 label/value 结构或列数与设计/项目规范不一致。
- 长详情、头行 Tab 或大量明细页面不可滚动，滚动容器错误，滚到底部反复抖动，或固定 Header/Toolbar/Tabs/Table 遮挡内容。
- 详情页、表单页、头行页或 Tab 明细页在页面级 `Content` 已承担主滚动时，内部明细 Table 使用 `autoHeight maxHeight` / `TableAutoHeightType.maxHeight` / 等价动态 max-height，且无稳定容器高度、UI Contract 来源和底部滚动验证。
- 新建/编辑/复制/详情页面直接解析 `window.location.hash`、hash 正则或散落 query/params 判断业务状态，缺少统一 routeContext；或 DataSet `editFlag` 反向控制 UI 编辑态。
- Modal / Drawer / Overlay 首屏自动覆盖页面、重复打开、背景/层级穿透、Portal 容器错误；业务弹层未使用 `Modal.open` 或等价 wrapper；新增或重构业务弹层仍使用 JSX Modal/Drawer + visible/open state；Drawer 缺少 `resizable: true`；弹层宽度偏离设计，普通表单 Modal 设计未指定宽度时缺少 small 默认，或详情 Drawer / 高密度详情缺项目默认尺寸、readabilityRisk 与 `valueOverflowPolicy`。
- local-filter / 本地内存 seed-filter 冒充 mock-request 或 production transport，或本地 `PageResponse` 直接接入 `transport.read`。
- 代码新增无 FDS/TDS/UI Contract 来源字段、摘要区、统计卡片或候选展示。

## 正例与反例
正例：
- `DataSet queryFields + Table filterBar + queryBarProps.fuzzyQuery`，并按 enumProvenance 使用 `TableQueryBarType.filterBar`。
- enumProvenance 标明 DataSet 项目 string 风格时，DataSet 字符串配置有项目相似页面证据；组件 props 使用确认 enum import。
- `columns` 最后一项为操作列，`lock: ColumnLock.right`，多动作使用已确认 HZERO helper。
- 只读详情 `Form + Output`，数组明细用 Pro Table。
- 新建表单只展示 confirmed 系统默认值；业务输入为空或来自明确当前用户/复制来源。
- 长详情页明确 Content/wrapper 滚动边界，小视口可滚到最后一区块；详情明细 Table 不与页面主滚动容器竞争动态高度，底部滚动无抖动。
- Modal / Drawer / Overlay 使用项目 `Modal.open` / `Modal.open({ drawer: true, resizable: true })` 或 wrapper，点击触发，关闭后清理。
- mock-request 使用可请求 mock API；local-filter / inline mock 成功路径必须标为 blocking cleanup，不得写 `usable=true`。

反例：
- 手写查询 `Form`、局部 `useState` 查询条件、按钮直接过滤数组。
- 自绘 Modal / Drawer / Overlay、JSX Modal/Drawer 常驻渲染或 visible state 写法与项目 Modal.open 模式冲突。
- `lock: true`、操作列放中间、按钮 Fragment 直接堆在 renderer。
- `new DataSet({ ... } as any)` 包住 `type/selection/dataToJSON`；Table/Form/Button 裸写枚举字符串。
- 只读详情用 `div/grid` 手排字段。
- 新建表单从 `detail-create.json`、mock seed 或当前时间批量塞默认业务值。
- 未确认 `labelLayout: 'float'`、`columns: 4` 等布局 props，却改变详情字段结构。
- DataSet `transport.read` 指向空 URL、data URL、或直接塞本地 PageResponse。

## 验证清单
- buildable：lint/typecheck/build 可运行项完成；目标工程未安装依赖时单列为环境前置未满足，依赖型验证写 `not-run + blocked-by-missing-dependencies`，`buildable=unknown`，不得写成业务 blocker 或 `buildable=false`。
- static anti-pattern：按 `static-anti-pattern-checklist.md` 检查本轮 changed files；命中反模式必须进入 Review finding 或 Implementation 自查结果。
- enumProvenance：检查代码中的 enum-like props 与 UI Contract 的项目风格一致；未运行类型检查时也必须做静态一致性审查。
- reachable：路由可达，菜单/权限状态已记录 confirmed 或 generatedCandidate。
- usable：首屏有 Table DOM、数据行/空态、分页；有行操作契约且当前状态存在可见动作时操作列可见；筛选、重置、刷新、分页、详情打开/关闭可用。
- UI against design：实现后回读 UI Contract，记录覆盖率、偏差、fixedBy 和仍需确认项。
- routeContext/editMode：刷新编辑 URL、`/create` 无 query 新建、保存后跳转和切换不同 id 的编辑态行为符合设计；`/detail/create` 命中即 failed。
- create defaults/layout/scroll：新建页默认值、详情 Form 布局 props 和长内容滚动必须有实际检查结果；详情/头行明细表还必须检查是否误用 `autoHeight maxHeight` 以及滚到底部是否抖动。无法运行浏览器时列为 not-run 风险。
- manual checklist：手测问题按设计偏差、组件选型错误、样式层级、数据链路、验证缺失、资产缺失分类，并回灌 lessons learned。

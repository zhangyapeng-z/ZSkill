# Frontend UI Runtime Gates

本文是 UI Contract 进入 Task、Implementation、Review、Verification 和 Handoff 后的运行时门禁、组件选型、Review、Verification 和资产回灌参考。Frontend Design 阶段的精简 UI 合同在 `front-hzero-enterprise-design` 的 UI Contract guardrails。

## 阅读路由
- 区分流程级 UI 门禁和 Choerodon 组件规则时读 `与 Choerodon Skill 的边界`。
- 判断是否需要 UI runtime gate 时读 `适用范围` 和 `编码前 UI 回读`。
- Task / Implementation 前补齐 UI 分区时读 `UI Contract 必填分区`、`列表页规则`、`详情与 Modal / Drawer / Overlay`。
- 处理 DataSet、Mock Request、权限或按钮时读 `DataSet 与 Mock Request`、`权限、路由和按钮`。
- Review / Verification / Handoff 时读 `禁止自由发挥`、`Review 阻塞项`、`Browser / Manual Checklist` 和 `Lessons Learned 回灌`。

## 与 Choerodon Skill 的边界

- 本文是运行期流程级 guardrail，负责 UI Contract 继承、Task/Implementation 拒收条件、Review/Verify/Handoff 门禁和 lessons learned 回灌。
- `front-hzero-choerodon-ui` 的 UI contract guardrails 是组件实现级 guardrail，负责 Choerodon Pro Table、DataSet、Form、Output、Modal/Drawer、PermissionButton 和 local-filter / transport 的具体写法。
- 两者重复出现时按职责分层归属：本文覆盖流程门禁、产物路径和确认状态；Choerodon skill 覆盖组件 API、反模式、降级条件和代码写法。
- query-table、row-actions、master-detail 已退休为 `front-hzero-choerodon-ui` 下的 scenario reference；本文只引用 `HZUI-*` gate 和验收状态，不再承载这些场景的完整 SOP。
- 权限按钮、renderer/helper、附件、导入导出、HZERO 通用组件和 mock-request 的实现细则分别归 `front-hzero-permission-button`、`front-hzero-renderer`、`front-hzero-attachment`、`front-hzero-import-export`、`front-hzero-common-components` 和 `front-hzero-mock-request`。
- 若两处规则发生冲突，不直接在 Implementation 中取舍；应在 Review/Handoff 中标记 `guardrail-conflict`，并优先修订对应职责层的 reference。

## 适用范围

- HZERO + Choerodon 列表、详情、Modal/Drawer/Overlay 弹层、主从、附件、权限按钮和 mock/demo 页面。
- FDS/TDS/TBS 到前端代码实现前的 UI 设计回读。
- Implementation 后的 UI against design 审查、runtime/manual checklist 和 lessons learned 回灌。

不适用于纯接口、纯后端、纯构建诊断或不涉及页面 UI 的小范围 `regular-change`；但小范围 `regular-change` 若改动可见 UI、DataSet transport、权限按钮或页面交互，也应执行命中的最小 UI contract，不需要生成完整 UI Contract 文档。

## 编码前 UI 回读

Frontend Design 或 Task Breakdown 进入 Implementation 前，必须形成 `UI Readback Table`。它可以写入设计文档、任务文档或单独 `ui-contract.md`，但不得只停留在对话里。

`UI Readback Table` 至少包含：

| 项 | 必填内容 |
| --- | --- |
| 页面/区域 | 列表、筛选、工具栏、操作列、详情 Header、基本信息、详情区块、附件、Modal/Drawer/Overlay 弹层、按钮 |
| UI 要求 | 展示字段、组件类型、字段顺序、按钮位置、默认状态、交互动作 |
| 来源 | FDS / TDS / TBS / Figma / 工程证据路径和章节 |
| 状态 | confirmed / generatedCandidate / missing |
| 结构边界 | `expectedSurface / forbiddenSurface / requiredVisibleByDefault`，仅对 Header、基本信息、详情/明细 Tabs、工具栏、弹层等高风险区域必填 |
| 实现位置 | 目标组件、DataSet、service、route、样式或验证产物 |
| 验证方式 | Review 静态检查、runtime/manual、Network、console、截图或 not-applicable |

没有来源的字段、区块、按钮、统计卡片、摘要头、候选人概览区不得实现；确需补充时标记 `generatedCandidate` 并进入确认或替换清单。

### No Source, No UI Element

- 功能文档、FDS/TDS、Figma/PageSchema、目标工程证据和用户确认都没有描述的页面能力、按钮、行操作、Tab、弹层、附件、导入导出、统计卡片、额外字段或分组，不得由模型自行补齐到 confirmed 设计或实现中。
- 字段是否展示、展示位置、组件类型、布局顺序、按钮区域、交互动作、弹层形态、默认值、编辑态/只读态、状态展示、样式结构和数据处理入口，都属于受控实现范围。没有 UI Contract、Task Breakdown、目标工程 confirmed baseline 或用户确认来源时，不得在 Implementation 阶段自行补齐或改写。
- 新增容器、改变父子承载面、把一个区域包进另一区域、合并/拆分区域、或把元素移动到 `forbiddenSurface`，都属于结构漂移。缺来源时不得以“统一容器”“方便复用”“修复 Review finding”为理由落代码；应回 Design / Task 补 `expectedSurface / forbiddenSurface` 或删除漂移实现。
- 区块标题、页面 Header 标题、标题后缀、摘要头和标题旁状态/金额/数量等辅助展示都属于 UI 元素；没有 UI Contract 或明确来源时，不得把 Form 字段移到标题或 Header 中重复展示。状态字段在 Field Visibility Matrix / Field Editability Matrix 中已定义为 `Tag/Output` 时，Implementation 应在字段位置展示，不能额外拼到 section title 后。
- Figma/PageSchema 可作为布局、文案、区块、按钮位置和弹层形态来源；不能单独确认业务能力、接口、权限、状态流转、LOV/lookup、附件/导入导出协议或生产请求参数。
- 功能文档有业务能力但 Figma 未画出时，必须在 UI Contract 标记 `layoutAuthority=fds-ui / missing` 和 `needs-question` 或记录明确不做的 UI 入口；不得凭经验添加按钮位置。
- Figma 画出 UI 元素但 FDS/TDS/API 未提供业务契约时，只能作为 `generatedCandidate / partial`，必须进入 Contract Check 或 question；不得实现为 production-ready。
- 目标工程同类页面的常见按钮或布局只能作为 `project-baseline` 候选。若本功能文档和 Figma 均未提及，默认不实现；需要沿用时必须写入 `generatedCandidate`、来源路径、确认人和替换/确认清单。

这部分只负责运行期复核上游 `UI Readback Table` 是否被消费；Design 如何形成这些字段，统一以 `frontend-ui-contract-guardrails.md` 为准。

## UI Contract 必填分区

设计文档必须包含 `UI Contract`，至少覆盖：

- `List Contract`：查询字段、字段组件、模糊查询、默认展示字段、更多筛选、表格列顺序、列宽、操作列、分页、刷新、重置。
- `Route Context / Edit Mode Contract`：详情、新建、编辑、复制页面的 routePattern、idSource、isCreateSource、editableDerivation、pageModeDerivation、queryParser、editableAuthority 和 saveRedirectPolicy。
- `Field Visibility Matrix` / `Field Editability Matrix` / `Empty / Derived Field UX Rules`：字段存在来源与 create/edit/detail/list/query 展示策略拆开记录；页面模式 create/edit/copy/detail/approval/readonly/mixed 下每个字段的 `visibleIn`、editable/readonly/disabled/hidden 状态、原因来源、组件类型、默认值策略、submitPolicy、空态文案和派生/保存后生成规则。
- `Detail Contract`：详情区块顺序、区块标题文案、标题附加信息是否允许、字段分组、只读字段组件、数组字段展示方式、附件入口、敏感字段、按钮 enabled/disabled 条件、`expectedSurface / forbiddenSurface / requiredVisibleByDefault`、长内容滚动边界和明细表高度策略。若 HZERO `Content` / `.page-content` 或页面级容器已承担主滚动，详情/头行明细 Table 默认不得使用 `autoHeight maxHeight` / `TableAutoHeightType.maxHeight` / 等价动态 max-height；确需内部滚动时必须写明稳定高度或明确 `height` 来源。
- `Detail Record Navigation Contract`：当详情 Modal / Drawer / 当前页详情在同一表面内切换业务主记录时必须填写，记录导航范围、当前 id 来源和运行时类型、方向/目标参数、筛选快照来源、边界行为、加载失败处理，以及切换后必须刷新的 Header、基本信息、详情区块、Tabs、子表和附件区域。触发条件是主业务对象身份变化；分页、轮播、步骤向导、Tab/区块切换、附件/图片预览翻页不适用。
- `Modal / Drawer / Overlay Contract`：组件选型证据、打开方式、生命周期、宽度、Portal/挂载容器、背景、遮罩层级、关闭后状态。
- `Component Contract`：Table、DataSet、Form、Output、Card、PermissionButton、Modal.open、Attachment、i18n、customizedCode、componentApiProvenance（组件 import、命名空间、静态子组件和版本/API 证据）、enumProvenance（DataSet/Table/Form/组件枚举型 props 的 Evidence enum import map、项目 import 或 reference generatedCandidate/fallback 证据）。
- `Frontend ID Runtime Contract`：主键、外键、URL query/path ID、Lov/Select value、Table rowKey、DataSet primaryKey、`@Encrypt` 字段和 ID 数组的前端运行时类型；必须按 `frontend-id-runtime-contract.md` 区分 DB/API declared type 与 frontend runtime type。
- `Interaction Contract`：查询回第一页、刷新保留当前页、重置清空条件并回第一页、关闭详情/业务弹层不丢列表筛选/分页、生产模式导航边界。

规则：
- 这里列的是运行期必须被消费的 section，不要求在本文再次解释 Design 如何写表、如何问问题、如何生成 generatedCandidate。
- Task/Implementation/Review 只需要针对命中的 section 做消费校验和拒收，不要把这里的分区说明转抄回 agent/template。

## 列表页规则

- 默认使用 Choerodon Pro `Table + filterBar` 查询形态；`queryBar` 代码按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态，不允许字符串形态。除非工程证据证明不支持、目标项目已有不同封装，或 UI Contract / 用户确认 / FDS/TDS 明确 `queryAreaPolicy=none-by-design` 或其它 `queryBarMode` 且有 `sourceRef/reason`。该规则同时适用于普通列表、详情页明细表、主从子表、Tab 内表格和弹层内表格的筛选条件；不得因区域是详情页内明细就改成外置查询 Form。
- 出现“搜索框 / 关键字搜索 / 模糊查询”时，必须开启 `queryBarProps.fuzzyQuery=true` 或项目等价写法，并按需使用 `queryBarProps.fuzzyQueryPlaceholder`；`fuzzyQuery=false` 与缺失同等处理。不得生成 `queryBarProps.fuzzyQueryField/fuzzyQueryFields`，字段映射必须保留在 UI Contract 和 QueryDS/queryFields。确无关键字/模糊搜索需求时，必须在 UI Contract 写 `not-applicable + reason`。
- `queryAreaPolicy=required-filter|required-fuzzy` 时，查询字段必须生成 QueryFields Schema：字段名、label、组件类型、是否多选、是否允许清空、默认值、数据来源。
- `queryAreaPolicy=required-filter|required-fuzzy` 时必须声明 `queryFieldsLimit`、默认展示字段和更多筛选字段；`none-by-design` 时必须声明无筛选来源和原因，不要求 queryFields。
- 普通查询列表/表格的 ListDS 默认 `autoQuery=true`，首屏自动触发 `transport.read`。只有前置查询条件、自定义设置、权限/租户上下文、route/search 派生参数、外部选中态、F 型布局受控列表或项目 wrapper 控制查询时机时，才允许 `autoQuery=false`；此时必须声明 `manualQueryTrigger` 并在条件就绪后主动 `dataSet.query()`。
- 操作列必须是 columns 最后一项；固定右侧按 enumProvenance 使用 `ColumnLock.right` 或项目 confirmed 等价 enum 导出，禁止用 `lock: true` 或 `lock: 'right'` 表示右锁定。该右锁定要求只针对行操作列；普通业务列只有在 UI Contract、用户确认或项目 confirmed baseline 明确要求时才固定。
- 操作列标题必须表达整列语义，默认使用 `操作` / action / operation 或项目 confirmed 等价文案；不得把单个行操作“详情/detail”作为操作列 header/title。
- 自定义行操作不得使用 `column.command` 函数形态承载。当前 HZERO 目标中 Choerodon Pro Table `command` 按命令数组/可迭代集合消费；`command: ({ record }) => ...` 会绕过 renderer/helper 合同，并可能在运行时触发 `forEach is not a function`。多动作或自定义动作必须通过 `renderer` 调用 `c7nOperatorRender` / `operatorRender` 或已确认 project override。
- 操作列“更多”是行操作溢出入口，必须使用 `front-hzero-renderer` 内置 `c7nOperatorRender` / `operatorRender` helper 的 overflow 能力、项目已有操作菜单、Dropdown/Popover/Menu 等轻量浮层；不得使用 Drawer、Modal.open drawer 或详情弹层承载“更多”菜单。
- 使用 `c7nOperatorRender` / `operatorRender` 时，operators item 必须符合 `{ key, ele, len, title }` 或 confirmed project shape；生成 action object 时必须显式补 `title`，并与 `ele` 按钮展示文案同源。裸 JSX 元素数组会因缺 `action.ele` 被过滤为空，不能作为操作列按钮可见性的通过证据。
- 列宽默认值只能作为最小可读宽度或初始宽度参考，不得把所有普通业务列机械生成为固定 `width`：姓名/短文本约 120，日期约 130，状态/枚举约 120，金额/数字约 120，长文本约 220。字段较少、总列宽明显小于内容区宽度的列表，必须至少选择名称、描述、分类名称等主文本列采用 `minWidth`、可伸缩列、项目 wrapper 自适应配置或等价策略吸收剩余宽度；不能用“参考页固定宽度”替代本页 UI Contract。只有 Figma/PageSchema、UI Contract、用户确认或项目 confirmed baseline 明确要求固定宽度时，普通业务列才可写死 `width`。
- 操作列 120 只适用于单个短动作或无多动作 helper。多动作操作列必须按 `limit` 内可见动作、`operators[].len/title`、按钮间距和“更多”入口预留确定稳定宽度，UI Contract 可覆盖但不能小于可见按钮完整展示所需宽度。操作列宽度稳定不代表其它业务列都应固定。
- 表格可配置时必须设置稳定 `customizedCode`，并与 feature/page code 绑定。
- 查询必须回到第一页；刷新保留当前页；重置清空查询条件并回到第一页。

这些是列表页运行期默认门禁；更细的组件 API、renderer/helper 调用签名、行操作 payload 和查询表格场景细则分别回到 `front-hzero-renderer`、`front-hzero-choerodon-ui` 的 row-actions scenario reference 与 query-table scenario reference。

## DataSet 与 Mock Request

- `QueryDS` 只管理查询条件；`ListDS` 只管理列表数据；状态函数集中到 store / DS helper。
- DataSet fields、queryFields、transport、selection、status、dataToJSON、事件名和字段类型等枚举型配置必须声明 enumProvenance。优先消费 Evidence enum import map；项目已使用 `FieldType`、`DataSetSelection`、`DataToJSON` 等枚举时沿用枚举；项目使用字符串且 reference 支持时可保持字符串；只有 reference、无项目证据时只能 generatedCandidate/missing，不得标为 confirmed。同一 feature 不得混用等价字符串和枚举。
- enumProvenance 必须覆盖代码中实际会写入的 enum-like props，不只覆盖“典型字段”。至少包括 DataSet `fields[].type`、`queryFields[].type`、`selection`、`dataToJSON`、`status`、事件名，Table `queryBar`、`editMode`、`lock`、`align`、`selectionMode`，Form `labelLayout`、`labelAlign`、`layout`，Button `color`、`funcType`、`type`，以及 Lov/Attachment/Modal/Drawer/Dropdown 的模式类 props。Table `selectionMode` 的 enum 域是 `SelectionMode.rowbox/treebox/click/none/dblclick/mousedown`，不得把 DataSet `selection` 的 `DataSetSelection.single/multiple` 复用到 Table JSX。
- 项目风格必须在 Design / Task 中收口为 `component-enum`、`dataSet-enum`、`dataSet-string`、`mixed-needs-decision`、`missing` 或 `not-applicable`。组件 props 必须导入项目确认 enum 或项目 confirmed 等价 enum；`dataSet-string` 必须记录相似页面或项目字符串风格证据；`mixed-needs-decision/missing` 不得进入 runnable implementation。
- ID-like 字段的 DataSet field、primaryKey、Table rowKey、Lov/Select value 和 route/path 参数必须继承 `frontend-id-runtime-contract.md`。即使 MDS/API schema 写 `number`，前端 runtime 默认按 `string` 处理；mock/API adapter 入口应统一 `String(id)`。
- 普通 DataSet 查询优先使用 DataSet `queryFields/queryDataSet/transport.read`；不要把业务查询职责放到 Table 层 `queryDataSet/onQuery/onReset`，除非工程已有封装证据。
- 列表、详情、弹层等多个页面确实复用 DataSet 时，只能复用 DataSet 字段配置、transport builder、adapter 或工厂函数；不得跨页面导出并共享同一个 `new DataSet(...)` 实例。共享实例会导致查询条件、current record、脏数据、分页和缓存状态在多 Tab、多详情记录或列表详情切换时串扰。
- mock/demo 查询必须走 `mock-request`：DataSet `transport.read`、项目 request adapter 或非 DataSet / 明确 service-action owner 的 service request 请求 HZERO 本地 devServer middleware 暴露的 mock API。DataSet 页面不得用 transport 调业务 service 充当请求证据。
- 新生成页面不得使用 `local-filter`、本地内存数组、组件内 seed/filter、`src/utils/mock.ts` 或 `query -> loadData` 支撑列表查询、分页、重置、刷新；发现即 blocking cleanup/rework，不得作为降级实现或 usable=true 证据。
- `PageResponse -> DataSet` 映射应发生在 request adapter / transport response adapter 中，并声明 content/rows、totalElements/total、page/size、空态、错误态；不得把本地 `PageResponse` 直接塞进 `transport.read` 冒充请求链路。
- `production-transport` 不得 silent fallback 到 mock store、静态 seed、本地内存数组或 local-filter。

这部分只保留 UI/runtime 必须关心的 DataSet 与 mock-request 边界。servicePrefix、mock middleware、runtime store、adapter、分页结构、`API_HOST` 拼接等更细规则，以 `front-hzero-mock-request` 的 runtime gate 和 `generated-code-static-quality-gate.md` 为准。

## 详情与 Modal / Drawer / Overlay

- 页面模式必须先声明：create、edit、copy、detail、approval、readonly 或 mixed。create/edit/copy 中 FDS/TDS/UI Contract 标为可编辑的字段必须使用 Choerodon Pro 可编辑输入组件并通过 Form/DataSet `name` 绑定；不得套用详情 `Form + Output` 导致字段只读。
- 新建、编辑、复制、详情页面必须声明 Route Context / Edit Mode Contract，并优先通过 `useLocation()`、`useParams()` 和 `getRouteContext(location, params)` 或项目等价 wrapper 派生 `id/isCreate/pageMode/editable`。不得生成或读取 route/query `editFlag`，也不得用 `window.location.hash.includes(...)`、hash 正则或散落 query/params 解析来判断业务状态。
- 新建页路由固定使用 `/create`，查看/编辑固定使用 `/detail/view/:id`、`/detail/edit/:id`。`/detail/create` 属于违规路径，发现后必须迁移到 `/create`。
- `/create` 必须默认进入 `isCreate=true`、`editable=true`、`pageMode=create`；`?editFlag=true` 命中时必须迁移。
- 新生成列表入口、openTab 和保存后跳转不得主动生成 `?editFlag=true/false`、`?mode=edit/view` 或 `?action=create` 来表达页面模式；查看、编辑、新建必须进入 path pageMode，例如 `/create`、`/detail/view/:id`、`/detail/edit/:id` 或项目确认等价路径。
- UI 可编辑性以 routeContext、UI Contract 和业务状态守卫为权威来源。DataSet 中的 `editFlag` 只能作为展示、提交或后端字段，不能反向覆盖页面编辑态。
- 保存后如果业务要求停留编辑态，跳转必须显式保留编辑 path/pageMode；若应进入只读详情，也必须有 FDS/TDS/UI Contract 或用户确认来源。query 只保留来源、返回、详情内子 Tab、navigationToken 等辅助状态。
- create/edit/copy 中只读或禁用字段必须写明原因来源，例如单号后端生成、主键不可改、审计字段、状态锁定、权限不足、审批只读、敏感字段仅返回 masked 值。缺少来源时不得自行降级为 `Output`、`readOnly` 或 `disabled`。
- create/edit/copy 的默认值必须逐字段声明来源：FDS/TDS/API 明确默认、后端保存回填、当前用户/组织上下文、复制来源或用户确认。新建页默认应为空白可输入态，除已确认系统默认值外不得从详情 mock seed、列表首行、历史运行态或示例数据预填业务输入值。状态、编号、审计、申请时间等若由后端生成或提交时产生，前端不得无来源地作为新建表单的用户可见预填；确需隐藏初始化时必须说明不会污染 submit payload 或用户可见值。
- create/edit/copy/detail 的字段可见性必须按 UI Contract 的 `visibleIn` 或等价字段矩阵执行。`creationDate`、`lastUpdateDate`、`createdBy`、`lastUpdatedBy`、`objectVersionNumber`、单据编号、审批状态、提交时间、更新时间、后端计算合计/比例等后端生成或保存后派生只读字段，必须逐字段确认 create/edit/detail 的 `visible / hidden / readonly-placeholder`、readonly/hidden 原因、displayTiming 和 `submitPolicy`；参考页的 create 态隐藏不能成为默认结论。当前 mode 无可显示值时，不得渲染空 `Output`、不得占用表单布局；display-only 字段不得进入 submit payload。
- 新建未保存态不得额外展示无来源的摘要块、状态块、标题附加状态或说明文案，例如“当前状态：新建”“待提交”“系统生成后回填”等内部占位。若 UI Contract 要求展示创建中状态，必须有 `sourceText`、展示区域、组件形态和 submitPolicy；否则按无来源 UI 元素处理。
- 详情只读字段必须使用 Choerodon Pro `Form + Output`；不得用裸 `div/grid` 拼只读详情。
- `Form + Output` 是只读展示容器，不是字段语义降级许可。主数据字段必须展示 `displayField`、`*Name` 或等价描述字段，枚举字段必须展示 `*Meaning` / value meaning，附件字段必须使用附件只读组件、附件列表或已确认 wrapper；只有 raw `*Id/*Code/*Uuid` 时必须标记 display contract 缺失和 replacement，不得把 raw Output 当作展示契约闭合。
- Form 的布局型 props 必须有来源：`columns`、`labelLayout`、`labelAlign`、`labelWidth`、`colSpan`、响应式列数和 Output 展示形态应来自 Figma/PageSchema、UI Contract、项目同类页面或用户确认。只确认“Form + Output”不等于确认 label/value 上下结构或具体列数。需求/FDS/TDS/Figma/UI Contract 或项目 confirmed baseline 未明确 `labelLayout` 时，Frontend Design 必须默认写入 `labelLayout=horizontal` 和 `labelLayoutSource=default-horizontal-by-design-rule`；不得留到 Implementation 阶段猜测，也不得标为 generatedCandidate。
- 详情、编辑、新建和只读 `Form + Output` 默认必须有用户可见 label。`labelLayout="placeholder"` 会把字段 label 放进输入框 placeholder，`labelLayout="none"` 会隐藏 label；这两种只允许用于搜索条件、紧凑筛选区、项目 confirmed golden-baseline 或 UI Contract 明确要求的无标签表单。业务详情表单、只读 Output 表单和需要验收字段含义的表单不得默认使用 `placeholder/none`。若字段 DataSet label 已定义但页面不可见 label，按 label layout 问题处理，不得误判为 locale 或 DataSet 字段缺失。
- 详情字段值过长必须有 `valueOverflowPolicy`。邮箱、手机号、编号、姓名、公司名、职位名、地址和短标签等短语义字段默认可用单行省略 + Tooltip / title 显示完整值；备注、驳回/拒绝原因、经历描述、富文本和长正文默认用多行块、富文本只读组件或设计确认的 2/3 行省略。AI 可按字段语义、FDS/TDS/Figma、项目基线和 Field Usage Matrix 默认判定策略并记录 `decisionSource=AI-semantic-default` 或证据来源；只有策略影响业务可读性、验收含义、复制/查看完整内容能力，或证据冲突时才触发 question。不得把所有长文本字段都推给用户选择，也不得把长正文强制单行省略。
- 履历、教育、语言、获奖等表格型数组/集合字段必须使用 Choerodon Pro Table；单对象字段使用 Form + Output。集合字段必须来自 Detail Collection Contract，包含 `apiField`、item columns、rowKey、`component=Choerodon Pro Table` 和字段名来源；不得用项目只读表格、薄 wrapper、`ul/li`、原生 `<table>`、`renderPlainList`、逗号拼接、JSON stringify 或模板字符串替代。
- Detail Collection Contract 的 `apiField` 必须与 TDS/MDS/API/DTO 字段名一致，mock/demo 数据也必须同名。若存在旧字段别名或第三方字段名，必须在 service/adapter 集中转换并记录来源；详情组件内直接读取无来源别名（例如契约是 `workExperienceList` 却读 `workExperiences`）按字段契约偏差处理。
- 同一详情 Modal / Drawer / 当前页详情内支持切换业务主记录时，必须形成 Detail Record Navigation Contract。实现必须有单一当前记录状态源，例如内容组件 state、route/path id、已确认的 modal update/recreate 机制或 owner DataSet / record 重新绑定；切换成功后 Header/标题、基本信息 Form、详情区块、Tabs、子表、附件和状态按钮必须读取同一当前记录。不得只触发外层 `loadData/queryDetail` 后让 `Modal.open` 创建时的 children 继续消费旧闭包或旧 record；不得让 Header 与子表分别读取不同数据源。
- 详情区块顺序必须按 FDS/TDS/Figma/UI Contract 来源顺序；但“区块/section/order”只表示信息架构，不自动授权 HZERO Card/CardTitle、白底、边框、圆角、阴影、独立背景或其它强视觉容器。只有 UI Contract、Figma/PageSchema、项目 confirmed baseline 或用户确认明确 `visualContainer=Card/project-card` 时才使用卡片；缺来源时默认同一 `Content` 下连续表单区 + 区块标题 + 必要间距。
- 长详情页、头行页、Tab 明细页必须声明滚动边界：页面 Content、业务 wrapper、Tabs/TabPane、Table body、固定 Header/Toolbar 和 Modal/Drawer body 的高度/overflow 责任。HZERO `Header` / `Content` 必须作为页面根 Fragment 下的相邻节点；不得用业务 wrapper 包住整组 `Header + Content`，否则会破坏 `.page-container -> .page-head / .page-content-wrap / .page-content` 的高度和滚动语义。页面级业务容器、section 背景、底部 padding 和局部样式应放在 `Content` 内部；只有目标项目证据确认时才允许使用 `Content className` 或 `wrapperClassName`。不得只依赖浏览器默认 body 滚动或未知父容器。实现后必须验证长内容可滚到最后一个区块，固定表头/固定列/页头不遮挡内容，滚动不丢失 Tab、筛选和编辑态。
- 当页面 Content 已是主滚动容器时，详情/头行页底部明细 Table 默认自然撑开并跟随页面滚动；不得从列表页复制 `autoHeight={{ type: TableAutoHeightType.maxHeight, ... }}`、`heightType=maxHeight` 或等价依赖视口剩余空间动态计算高度的配置。该类动态 max-height 只适合单一列表页、固定查询区 + 主表格页。若在详情底部启用，Table 重新计算高度可能改变页面总高度，导致滚到底部后浏览器反复修正 scrollTop。必须限制明细区域时，使用 UI Contract 确认的稳定容器高度或明确 `height`，并验证滚到底部和连续新增多行后不抖动。
- HZERO 页面级 Provider 必须有来源。默认根结构是 Fragment 下相邻 `Header` 与 `Content`；不得默认用 `UrlHistoryProvider`、`HistoryProvider`、`ConfigProvider`、自定义 Context Provider 或业务 wrapper 包裹整组 `Header + Content`。只有 UI Contract、项目 `golden-baseline` 已按 `goldenBaselineStatus=confirmed` 和合法 `baselineConfirmationSource` 确认，或明确功能需求确认时才允许；相似页面中的 Provider 必须先按 baselineComparison 评级，legacy/unknown 不得复制。
- HZEROJS 微前端页面的 HZERO Page、Provider、intl 和 notification 必须优先走项目 alias / MF shared 入口。`Header` / `Content` 默认从 `components/Page` 合并导入，`intl` 默认从 `utils/intl` 默认导入，`formatterCollections` 默认从 `utils/intl/formatterCollections` 默认导入，`notification` 默认从 `utils/notification`；不得写 `import { formatterCollections } from 'utils/intl'`，该 alias 在部分 HZERO 工程只重导出默认 `intl`，会导致运行时 `formatterCollections is not a function`。不得使用 `@common/components/lang/index`、`components/lang` 等旧 `lang` 封装替代 formatterCollections，也不得使用任意非标准来源的 `xxx({ code: [...] })(...)` HOC 或为 formatterCollections 做项目 wrapper 探索。不得在新增或修改页面里直接使用 `components/Page/Header`、`components/Page/Content`、`components/Page/BackBtn`、`hzero-front/lib/components/Page/Header`、`hzero-front/lib/components/Page/Content`、`hzero-front/lib/components/Page/BackBtn`、`hzero-front/lib/components/Page`、`hzero-front/lib/components/UrlHistoryProvider`、`hzero-front/lib/utils/intl/intl`、`hzero-front/lib/utils/notification` 等 Page 子路径或深层入口，除非目标工程明确证明这些入口仍会被 barrel / babelResolvePath / MF shared 统一到同一 runtime。`useUrlHistory must be used within a UrlHistoryProvider` 在微前端中优先按重复 `hzero-front` runtime/context 排查：检查是否因 Page 子路径或深层导入绕过共享映射，让 `Header -> BackBtn -> useUrlHistory()` 消费了另一份 `UrlHistoryContext`；不得先补页面级 Provider 来掩盖重复依赖。
- 每个详情字段必须归属到 FDS 对应分组，例如基本信息、归档信息、求职意向、履历、附件。
- 敏感字段只消费后端返回的 `*Masked` 字段，不在前端自行脱敏；未返回则展示空/占位。
- Modal / Drawer / Overlay 的形态必须来自需求/FDS/TDS、Figma/PageSchema、UI Contract、项目同类页面证据或用户确认；不得默认写死为 Drawer。业务弹层统一使用工程已有 `Modal.open` 或已确认等价 wrapper；确认需要 Drawer 后必须使用 `Modal.open({ drawer: true, resizable: true, ... })` 或等价 wrapper；确认普通 Modal 后必须使用 `Modal.open({ ... })` 或等价 wrapper。使用前必须检索工程既有示例。设计只确认 Drawer 交互形态时，Implementation 仍必须继续落到 `Modal.open` 调用形态；不能把 Drawer 语义自由实现成组件内常驻 JSX。
- 若需求/FDS/TDS/Figma/UI Contract 明确指定普通弹窗、Modal 或对话框，必须使用普通 Modal 或项目等价对话框；不得为了复用默认写法改成 Drawer。若明确指定抽屉/Drawer，必须使用 Drawer 或项目等价抽屉；不得降级为普通 Modal。
- JSX Modal / Drawer、组件常驻渲染加 visible/open state 或自绘弹层不得作为新增业务弹层默认方案；`<Modal drawer visible>`、`<Modal visible>`、`<Modal open>`、`<Drawer visible>` 和业务 `*Visible/*Open` state 控制常驻弹层在新增或重构业务详情、表单、预览、导入组件时严格禁止。维护 legacy 写法必须记录兼容原因，生产化重构应迁移到 `Modal.open`。
- 所有普通业务 Modal / Drawer / Overlay 的尺寸必须严格按设计/Figma/PageSchema/项目 confirmed baseline/用户确认执行；设计未指定宽度时，普通表单 Modal 默认 `size=small`（约 520px 或项目 small 等价值），详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并必须记录 readabilityRisk、Form columns/colSpan 与 `valueOverflowPolicy`。`medium≈720px`、`large≈80%`、百分比宽度、`980px` 等仅在有明确来源时使用。UI Contract 或任务中出现无来源 `60%~80%`、`70%`、`80%`、`980px` 等候选时，应回到 Design/Task 修正，不能由 Implementation 照单实现；不得仅为解决单个长字段展示而放大弹层。
- Modal / Drawer / Overlay 尺寸必须配置在项目 confirmed 的弹层 API 入口（如 `Modal.open({ size })`、`Modal.open({ width })`、wrapper `drawerWidth/modalSize` 等），并有 componentApiProvenance；只给 `style.width`、内容根节点、CSS class 或内部容器设置宽度，不算弹层宽度已配置。
- Modal / Drawer / Overlay 不得在 `visible=false` 时仍以可见层级覆盖页面；`Modal.open` 必须由点击事件触发，或 effect 严格控制依赖和 cleanup。
- Modal / Drawer / Overlay 的 content/body/wrapper 必须有不透明背景；必须验证 mask、z-index、Portal 容器、背景层级和关闭后 Header/列表无遮挡。
- Header、固定表头、固定列、列表内容或页面容器出现在 Modal / Drawer / Overlay 内容层上方时，一律视为层级穿透；生产或 production-ready 任务中按 blocking 处理。
- Modal / Drawer / Overlay 只适用于设计明确的详情、表单、导入组件、预览等业务弹层；不得把操作列“更多”菜单归入 Drawer / Modal Contract。
- 列表行“查看详情”打开 Drawer 时，列表页或触发方负责 `Modal.open({ drawer: true, resizable: true, ... })`；详情组件只作为纯内容组件管理详情数据、当前业务主记录和必要回调。若详情内支持上一条/下一条切换，状态源应在内容组件、route id、owner DataSet/record 或 confirmed modal update/recreate 机制内闭合；不得为了记录切换退回 `visible/open state + 常驻 JSX Drawer`。
- Implementation / Review / Verification / Handoff 必须把 `modalOpenPatternCheck` 作为适用项消费。Review 命中业务 JSX visible/open 弹层后不得进入 Verification；Verify 发现手测反馈、遮罩/关闭/层级异常或 `modalLifecycleContract=partial` 与 JSX visible 命中并存时，必须回流 Review/Implementation；Handoff 不得只把该类问题记录为未验证项后放行。

这部分是运行期 UI gate owner。Design 期的 section 闭合、默认值收口和 generatedCandidate 判定，统一回到 `frontend-ui-contract-guardrails.md`。

## 权限、路由和按钮

- 所有业务按钮必须先在 Button Contract 中标明权限适用性：`required / not-applicable / unknown`、来源和权限码状态。required 动作必须按 `front-hzero-permission-button` 使用固定权限按钮入口；not-applicable 必须写 FDS/TDS、用户确认或项目基线 reason，不能因为看见普通 `Button` 就强行改权限按钮。
- 提交、撤回、作废、删除、复制、审批等敏感状态动作必须在 Button Contract 中记录 `visibleCondition`、`enabledCondition`、`actionGuard` 和状态字段来源。代码生成阶段可以先用最小状态 guard 支撑 demo，但不能只生成按钮显隐/disabled 而让 action 入口无条件执行。
- 来源写“显示/隐藏/仅显示”时进入 `visibleCondition`；来源写“启用/禁用/置灰/可点击”时进入 `enabledCondition`。不得把“仅某状态启用”实现成其它状态隐藏，除非 FDS/Figma/UI Contract 明确写隐藏。
- 业务按钮被禁用时必须有用户可理解的原因来源。删除、提交、撤回、作废、取消单据、保存等关键动作默认需要 `disabledReasonSource` 和 Tooltip/title/project wrapper 等 `disabledTooltipPolicy`；无原因的永久置灰或临时 no-op 不能作为完成态。
- 所有会触发接口、DataSet `query/submit/delete`、service request、mock request 或其它异步业务变更的按钮，必须在 Button Contract 中记录 `asyncAction=true`、`requestOwner`、`loadingPolicy`、`repeatClickGuard` 和 `finallyReleasePolicy`。请求进行中必须有可见 loading / pending 过渡，并禁用或阻断重复触发；成功、失败、取消确认和异常抛出都必须释放 loading。行级动作默认使用 row-level pending key，批量动作使用 batch-level pending key，页面 Header / Toolbar / Modal footer 动作使用 action-level pending key；只有 UI Contract 或项目 confirmed wrapper 明确全局锁定时才允许扩大 loading 范围。
- `destructive=true` 的按钮必须记录 `confirmPolicy`。删除默认属于 destructive；撤回、取消单据、作废、批量删除、已保存明细行删除等破坏性状态动作也默认 destructive。确认弹窗取消时不得发起请求、不得改变状态、不得进入 loading；确认后才允许执行接口动作。
- 按钮态和 action 入口必须共享同一组状态 predicate 或同一来源的 helper，例如 `canSubmit(record)`、`canWithdraw(record)`、`getWithdrawBlockedReason(record)`。UI 隐藏或禁用只是体验层保护，不是业务守卫；即使按钮不可见，handler 仍必须在触发入口二次读取当前状态 code 并阻断非法动作。
- 依赖 Table/DataSet selection 的批量按钮必须有 reactive bridge：`select/unSelect/selectAll/unSelectAll/load/reset` 事件、React state、observable wrapper 或项目 confirmed 封装必须驱动按钮态重新计算。只读取 `dataSet.selected.length` / `dataSet.selected` 而没有触发 React 刷新的实现，按按钮态不可用处理。
- 菜单 code、按钮 code、平台配置状态分开记录；前端接入不等于平台后台菜单已配置。
- route prefix、菜单 path、菜单 code 未确认时只能 `generatedCandidate`，不得声明 confirmed。
- 微前端 `registerRegex` 必须收敛到已确认 prefix，禁止 `\\/.*` catch-all。
- Header / Toolbar 权限按钮和表格行操作权限按钮的 `PermissionButton type` 必须分开：表格行操作权限按钮通常 `type="text"`，Header / Toolbar 权限按钮按工程规范通常 `type="c7n-pro"`。操作列从裸按钮修复为 `c7nOperatorRender` / `operatorRender` 后，仍必须检查 helper payload 内 `ele` 的权限按钮 type；不得把 Header/Toolbar 权限按钮样式或相似页面遗留样式复制到行操作。
- 每个按钮生成 Button Contract：文案、位置、FDS `sourceRegion`、`uiArea`、`semanticKind`、触发动作、`navigationTarget`、`businessMutation`、`statusActionRef`、权限适用性、权限码、visible/disabled 条件、`disabledReasonSource`、`disabledTooltipPolicy`、`selectionReactivePolicy`、`destructive`、`confirmPolicy`、`asyncAction`、`requestOwner`、`loadingPolicy`、`repeatClickGuard`、`finallyReleasePolicy`、来源文档。
- Button Contract / Button Semantic Matrix 默认 `copyPolicy=exact-source`。字段 label、按钮、行操作、状态文案、确认/通知和区块标题等正式用户可见文案必须来自 FDS/TDS/Figma/UI Contract/用户确认；近义改写必须写 `copyOverrideSource`。i18n key 覆盖不能替代 sourceText 保真。
- 按钮语义不得只按文案合并。页面 Header / 页面级按钮区的“取消/返回/关闭”如果来源是导航或关闭语义，必须标记 `semanticKind=navigation`、`businessMutation=none`，只能跳转、关闭或清理本地 UI 状态；不得调用取消单据、作废、撤回、删除等业务状态 API。
- 取消单据、撤回审批、作废、删除等改变业务状态的动作必须标记 `semanticKind=business-state-action`，并引用 `Status Action Matrix`；即使按钮文案同为“取消”，也必须与导航取消拆成不同 `buttonId` 和不同 UI 区域。
- `uiArea` 必须区分 `page-header / page-toolbar / table-toolbar / row-action / modal-footer`。`page-toolbar` 默认由页面 `Header` children 消费，运行期对账时如果该按钮出现在 `Table.buttons`，按消费面混淆处理；FDS/TDS 写表格工具栏或明细表按钮区时，默认落到对应 Table `buttons` 或项目等价表格封装；不得上提到页面 Header 或 Table 外手写 toolbar，除非 UI Contract 有来源。

这里是运行期消费规则；按钮权限组件、行操作 helper、current-tab/dynamic-tab/openTab 和子模块路由系统的实现细则，分别回到 `front-hzero-permission-button`、`front-hzero-choerodon-ui` 的 row-actions scenario reference、`hzerojs-submodule-runtime-gate.md`。

## 禁止自由发挥

- Implementation 阶段只能实现 FDS/TDS、Figma/PageSchema、UI Contract、Task Breakdown、目标工程 confirmed baseline 或用户确认中已经明确的页面元素、布局、字段、组件、按钮、交互、数据展示、默认值、状态逻辑和样式结构。不得以“更醒目”“更方便”“相似页面常见”“状态需要突出”“顺手补一下”等主观理由自行新增、上提、重复展示、隐藏、替换或改变实现。
- 发现设计可能需要增强时，Implementation 必须先删除自由发挥并按 frozen UI Contract 修复；仅 Task 漏映射时内部回 Task Breakdown。确需改变 frozen UI Contract 时返回 `parallel-baseline-invalidated` 并终止旧 run，不得回普通 Frontend Design 或先把增强落到业务页面代码里。
- 可见 UI 区域必须落在 UI Contract / Task Acceptance 的 `expectedSurface`，不得出现在 `forbiddenSurface`。详情/主从页缺特殊来源时，基本信息 Form 默认在 `Content` 内默认可见，不得作为 `Tabs.TabPane` 渲染；明细 Tabs 只承载明细/附件等子区域。新增 `basic/basicInfo` TabPane、把头表单包进 Tabs、页面工具栏下沉 Table 或表格工具栏上提 Header，都必须有明确来源，否则按 `HZUI-DESIGN-001` / `GCSQ-DETAIL-REGION-001` 处理。
- 不得把 Form 字段、状态、编号、金额、数量、审批结果等已在字段矩阵中定义的内容挪到 Header、section title、摘要头、Toolbar 或其它位置重复展示，除非 UI Contract 明确允许该辅助展示的位置、组件和来源。
- 不得把业务动作、按钮位置、弹层形态、区块顺序、字段顺序、字段组件、数据来源、默认值、校验规则、只读/可编辑状态、Tab/Drawer/Modal、摘要展示、样式结构或 request/mock/data adapter 从实现阶段自行“优化”；这些都必须先有设计或任务来源。特别是不得把上游只写的详情区顺序、字段分组或 section title 解释成“每个区域一张卡片”，除非 visualContainer/Style Necessity Contract 已确认。
- 不得新增 FDS/TDS/TBS 未要求的摘要头、统计卡片、候选人概览区、额外分组或内部说明文案。
- 不得展示无来源字段；确需展示时标记 `generatedCandidate` 并请求确认。
- 禁止大段自定义样式复刻组件库能力；优先组件库样式，样式只做间距、背景、层级修正。
- temporary-contract、generatedCandidate 可以在代码注释中清楚标记，但不得变成业务用户可见文案；local-filter / inline mock 不允许作为保留代码注释项，发现成功路径必须清除。
- attachment/import-export/LOV 等标准能力已有 owner 规则时，temporary-contract、generatedCandidate、replacement 和 contract-placeholder 只能进入设计产物、manifest、验证报告和 handoff；不得渲染成业务页面上的“待接标准组件”“未实证”“协议占位展示”等可见元素。
- Choerodon Pro `TabPane` 不得从 `choerodon-ui/pro` 作为独立命名导入，也不得引用 `choerodon-ui/pro/lib/tab-pane`。页签默认使用 `import { Tabs } from 'choerodon-ui/pro'` 后的 `<Tabs.TabPane>`；若抽本地别名，只允许 `const TabPane = Tabs.TabPane` 且必须有 `componentApiProvenance` / 目标项目健康示例证明。`import { Tabs, TabPane } from 'choerodon-ui/pro'` 触发按需构建解析到缺失模块时按构建阻塞处理。
- 禁止用 `as any` 猜测组件 API、静态子组件或命名空间成员，例如 `const { TabPane } = Tabs as any`、`const { X } = Component as any`、`(Modal as any).xxx`。组件、命名空间和静态子组件必须来自确认 import、目标项目示例或组件文档证据。
- 禁止用 `as any` 包裹整段 DataSet/Form/Table 配置来绕过 enumProvenance 或组件 API 证据，例如 `new DataSet({ ... } as any)`、`const commonProps: any = { labelLayout: 'float' }`。确有局部类型缺口时必须收敛到最小字段、写明 reason，并不得掩盖 enum-like props 来源。
- JSX 中使用的组件变量和 `Component.SubComponent` 静态访问必须能追溯到 import 或当前文件定义；未 import 的组件变量（如 `Tabs`、`Modal`、`Table`、`Form`）不得依赖 TypeScript 逃逸或运行时全局。
- 不得把详情页只读模板复制到新建/编辑页。create/edit/copy 中可编辑字段被 `Output`、永久 `readOnly` 或永久 `disabled` 渲染且无来源时，视为 UI Contract 偏差。
- 不得在 Choerodon/DataSet 枚举型 props 上随意裸写字符串、布尔值或混用枚举。若 Evidence enum import map 或项目/API 证据指向枚举，应使用确认的 enum import；若保留字符串，必须能说明项目风格或 reference 支持。reference import 不得单独作为项目 confirmed。

这里是统一的运行期兜底原则。命中具体反模式时，优先用对应 owner gate 编号记录 finding，不在 agent/template 中再复写整段“禁止自由发挥”正文。

## Review 阻塞项

以下命中时至少 major；影响首屏可用、核心流程或误报 production-ready 时 blocking：

- `HZUI-LIST-001`：普通列表、详情页明细表、主从子表、Tab 内表格或弹层内表格存在筛选条件，却缺少 Table filterBar 查询形态、缺 QueryDS/queryFields、或用外置手写查询 Form 替代；实现为 `<Form dataSet={queryDataSet}>` + `Table queryBar={TableQueryBarType.none}` 且无 UI Contract / 项目 wrapper 来源时，按本项处理。若设计明确 `queryAreaPolicy=none-by-design` 或其它 `queryBarMode` 且有 `sourceRef/reason`，缺少 filterBar/queryFields 不按本项处理；但 `queryBar` 字符串形态仍按 enum 违规处理。
- `HZUI-LIST-002`：有关键字/模糊搜索但未开启 fuzzy query。
- `HZUI-LIST-003`：操作列不是最后一列；C7N Pro Table 操作列未使用 confirmed `ColumnLock.right`，误用 `lock=true`、`lock: 'right'`、`fixed: 'right'`，或只配置 `width` 就声明固定。
- `HZUI-LIST-004`：操作列“更多”使用 Drawer/Modal 承载，或点击“更多”后打开抽屉而非轻量操作菜单。
- `HZUI-LIST-005`：多动作操作列未使用 `c7nOperatorRender` / `operatorRender` / confirmed project override，或虽已使用 helper 但 operators payload 内行按钮未按 `type="text"`、未过滤不可见项、item shape 不符合 `{ key, ele, len, title }`、`ele` 不是 ReactNode 行按钮 JSX、required 权限只放在 helper options 而不是按钮组件上，或继承了 Header/Toolbar 样式。因 payload 错误导致按钮为空或 React #130 白屏时，删除 helper改成 Fragment / 按钮数组直接返回仍按本项阻塞。
- `HZUI-LIST-006`：`limit` 内可见行操作按钮被截断，`operators[].len/title/ele` 与操作列 `width` 不匹配，或把按钮文案宽度问题误修成提高 `limit`、取消 overflow、展示全部动作且无 UI Contract / 用户确认来源。
- `HZUI-LIST-007`：Choerodon Pro Table 操作列把 `column.command` 写成函数形态承载自定义动作，或 `command` 返回按钮数组/Fragment/ReactNode 而未走 `renderer -> c7nOperatorRender/operatorRender`；已触发 `forEach is not a function`、首屏崩溃、操作列不可用或仍声明 usable=true/production-ready 时 blocking。
- `HZUI-LIST-008`：操作列 header/title 使用单个动作文案如“详情/detail”，而不是“操作/action/operation”或项目 confirmed 等价文案；误导验收或仍声明 UI Contract matched 时 blocking。
- `HZUI-LIST-009`：`c7nOperatorRender` / `operatorRender` 的 operators payload 使用裸 JSX 元素数组、缺 `ele`、缺 `key`、缺 `title`、`ele` 为 `intl.get(...).d(...)` / 字符串 / 文案变量等非 ReactNode，或未形成 helper 可消费 action object，导致操作列标题存在但按钮为空、React #130 白屏，或 helper 宽度/overflow title 合同无法判定；正确修复是保留 helper并改为完整 `{ key, ele, len, title }`，其中 `ele` 是 helper 可渲染的行操作 ReactNode，required 权限动作使用 `ButtonPermission type="text"` / confirmed 权限按钮 JSX，权限不适用动作必须有 Button Contract `not-applicable + reason`，`title` 与按钮文案同源，不是改成 raw Fragment。已复现按钮不显示、白屏或仍声明 usable=true/production-ready 时 blocking。
- `HZUI-LIST-010`：普通业务列无 `widthPolicy` / `columnWidthSource` / UI Contract / Figma / PageSchema / 用户确认 / 项目 confirmed baseline 来源却写固定 `width`，或把参考页固定列宽当成本页合同。正确实现应按 `widthPolicy` 使用 `minWidth`、主文本列自适应、项目 wrapper auto-fit 或有来源的 `fixedWidth`；字段较少且宽屏留下明显空白、或仍声明 UI Contract matched / production-ready 时 blocking。
- `HZUI-OVERLAY-001`：弹层形态与需求/FDS/TDS/Figma/UI Contract 明确要求不一致，例如普通弹窗被实现为 Drawer，或 Drawer 被实现为普通 Modal。
- `HZUI-OVERLAY-002`：Modal / Drawer / Overlay 自绘、未用 `Modal.open` 或等价 wrapper、挂载生命周期错误、无遮罩、Portal 容器错误、背景/层级穿透；Drawer 缺少 `resizable: true` 或宽度无依据。
- `HZUI-OVERLAY-003`：Modal / Drawer / Overlay 宽度只写在 `style.width`、内容容器或 CSS class，未写到 confirmed 弹层配置入口；普通表单 Modal 设计未指定宽度时没有使用 `size=small`；详情 Drawer / 高密度详情未记录项目默认尺寸、readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`；或自行使用无来源大宽度候选导致弹层过宽。
- `HZUI-DETAIL-NAV-001`：详情 Modal / Drawer / 当前页详情存在业务主记录切换，但缺 Detail Record Navigation Contract、当前记录状态源、modal update/recreate 证据或 owner DataSet / record 重绑证据；导航请求成功后 Header/姓名/基础信息/Tabs/子表/附件仍显示旧记录，或不同区域读取不同当前记录。触发条件只限业务主记录身份变化；分页、轮播、步骤向导、Tab/区块切换和附件/图片预览翻页不按本 gate 判定。影响核心详情流程或仍声明 usable=true/production-ready 时 blocking。
- `HZUI-ROUTE-001`：详情、新建、编辑、复制页面用 `window.location.hash`、hash 正则或散落解析方式判断 `editFlag/isCreate/pageMode`，或缺少统一 routeContext 导致刷新、保存后跳转、切换 id 后编辑态错误。
- `HZUI-ROUTE-002`：`/create` 不带 query 时不能默认进入新建编辑态；使用 `/detail/create` 造成 pageMode 歧义；或仍依赖 `?editFlag=true` 表达新建编辑态。
- `HZUI-ROUTE-003`：DataSet 中的 `editFlag` 被当作 UI 编辑态权威来源，导致 routeContext、UI Contract 与页面实际编辑态不一致。
- `HZUI-FIELD-001`：新建/编辑/复制页面的可编辑字段被实现为 Output/readOnly/disabled 且缺少 FDS/TDS/UI Contract 来源。
- `HZUI-FIELD-002`：新建未保存态无条件渲染审计/后端生成/保存后派生字段空 Output，例如单据编号、审批状态、`creationDate`、`lastUpdateDate`、`createdBy`、`lastUpdatedBy`、`objectVersionNumber`、后端合计/比例，或把这些 displayOnly 字段带入 create submit payload。
- `HZUI-FIELD-003`：详情只读字段用 `div/grid`，未用 Form + Output。
- `HZUI-FIELD-005`：表格型详情集合字段未使用 Choerodon Pro Table、被文本化/native DOM 展示，或组件/mock/service 使用的字段名与 TDS/MDS/API/DTO 契约不一致且无集中 adapter 证据。
- `HZUI-DESIGN-001`：Implementation 自行新增或改变实现：无来源摘要头、统计卡片、额外字段、额外区块、标题附加状态/编号/金额/数量、创建态占位状态块、内部说明文案、按钮位置上提、弹层形态改变、字段顺序或组件改变、默认值改变、编辑态/只读态改变、数据展示重复、样式结构改造、把详情区顺序/分组无来源落成 Card/白底/边框/圆角/阴影等强视觉容器、request/mock/data adapter 自行替换；误报为设计要求或 production-ready 时 blocking。
- `HZUI-CONTRACT-FIDELITY-001`：Implementation / Review 未执行 contract fidelity diff，或可见 UI 与 Field Usage Matrix / Status Action Matrix / Action Entry Matrix / Button Semantic Matrix 漂移：字段 canonical 名被页面层改写、旧字段别名进入 DataSet/Table/Form/guard/payload、按钮/行操作文案近义改写无 `copyOverrideSource`、状态 code/meaning 与 `statusEnumMap` 不一致、required 行操作缺失。导致按钮误显/误禁、payload 错误、用户验收文案不符或误报 production-ready 时 blocking；静态 finding 同步引用 `GCSQ-CONTRACT-FIDELITY-001`。
- `HZUI-FIELD-004`：新建页把业务输入字段用 mock seed、示例数据、历史详情数据或当前时间预填，且 UI Contract 没有逐字段默认值来源。
- `HZUI-LAYOUT-001`：Form 布局型 props 无来源导致详情 label/value 结构、列数、跨列或响应式布局与设计/项目规范不一致。仅当页面级基础信息 / HeaderForm 已确认、设计产物仅有高层结构且缺列数/容器宽度/跨列/标签/响应式细节、并且原型/Figma、用户、项目 confirmed baseline 未覆盖时，必须继承 `default-form-layout-by-design-rule`：`containerWidthPolicy=content-available`、`xs=1, sm=1, md=2, lg=3`、`lg=3` 列、`labelWidth=120`、横向标签、短字段初始 `colSpan=1`、长值 Lov 可优先评估两列和长字段优先跨当前整行。审计/后端生成字段的显隐、只读和提交策略必须另行继承 Field Visibility Matrix / Field Editability Matrix，不属于布局默认。可按可用宽度、字段密度、标签/值长度和字段语义记录 `layoutAdjustmentReason` 后调整列数、labelWidth、跨度或断点；该调整不需要外部设计来源，也不设字段数自动阈值。固定 `max-width`、居中仍必须有来源。Implementation 未落盘/未继承该合同，或调整布局却无合理 `layoutAdjustmentReason`、隐藏业务 label、用长字段撑破列宽且仍声明 UI matched/usable 时，按本项处理；字段顺序按独立 UI Contract 判定。
- `HZUI-LAYOUT-002`：详情、编辑、新建或只读 Form 使用 `labelLayout="placeholder"` / `LabelLayout.placeholder` / `labelLayout="none"` / `LabelLayout.none` 且无 UI Contract、Figma 或项目 confirmed baseline 来源，导致字段 label 不可见。核心业务字段 label 全部或大面积不可见时 blocking。
- `HZUI-SCROLL-001`：长详情页或头行 Tab 页面不可滚动、滚动区域错误、固定 Header/Toolbar/Tabs/Table 遮挡内容，业务 `<div>` 包住 HZERO `Header + Content`，或缺少长内容滚动验收。
- `HZUI-SCROLL-002`：页面级 Content 已负责滚动时，详情/头行明细 Table 使用动态 `autoHeight maxHeight` 且无稳定高度来源；若已复现滚到底部反复来回滚动，按 blocking 处理。
- `HZUI-DATA-001`：local-filter 伪装成 production transport，或本地 PageResponse 直接塞进 transport.read。
- `HZUI-PERM-001`：PermissionButton 类型、权限码、菜单/按钮权限混用。
- `HZUI-ROUTE-004`：route/menu/registerRegex 未确认却声明完成。
- `HZUI-VERIFY-001`：build 通过但 reachable/usable 未证明却声明可交付。
- `HZUI-COMP-001`：组件 API 未确认却用 `as any` 解构/访问，或 JSX/静态子组件引用未导入变量；导致 `<Component> is not defined`、`Cannot read properties of undefined` 等运行时错误时 blocking。
- `HZUI-ENUM-001`：Choerodon/DataSet 枚举型 props 缺 enumProvenance、同一 feature 混用等价字符串和枚举、把 `enum-map.md` fallback 冒充项目 confirmed、或使用布尔/拼写错误替代枚举；导致组件行为错误、DataSet 配置失效或运行时错误时 blocking。
- `HZUI-ENUM-002`：整段 DataSet/Form/Table 配置用 `as any` 包裹，且其中包含 `type/selection/dataToJSON/queryBar/editMode/lock/labelLayout/color/funcType` 等 enum-like props；缺来源时至少 major，掩盖运行时配置错误时 blocking。
- `HZUI-ID-001`：ID-like 字段缺 Frontend ID Runtime Contract，或实现中把 `*Id`、`*Ids`、path/query ID、Lov/Select value、DataSet primaryKey、Table rowKey 强制转成 number；若 HZERO `@Encrypt` 或 Long 精度导致真实 ID 不可用，按 blocking 处理。
- `HZUI-ATTACH-001`：Attachment 组件、只读展示、`attachmentUuid`、`bucketName`、`storageCode`、目录、模板和预览/下载/删除协议按 `front-hzero-attachment` 审查；无来源硬编码 bucket/storage 未标记 `generatedCandidate/mock-only` 或缺 production replacement，至少 major；误报附件生产能力闭合时 blocking。仅缺 bucket/storage/template 等参数时，Implementation 必须生成 mock/generatedCandidate 参数并继续渲染 confirmed 标准组件，不得因此跳过组件、隐藏 required 附件区或落成占位。附件 required 时不得把 `attachmentUuid` 普通展示、静态附件列表、`*-attachment-contract-placeholder`、`待接标准附件组件`、`editable-contract-pending`、`replacement` 或“本轮不模拟上传/预览/下载/删除”作为页面实现；可见占位至少 major，声明 mock-completed/usable=true/production-ready 时 blocking。`components/Attachment` / `hzero-front/lib/components/Attachment` 默认导入未证明为 React component 就作为 `<Attachment />` 渲染时，按 blocking；典型错误是 React #130 `got object`，应改用目标版本确认的 Choerodon Attachment import（常规为 `choerodon-ui/pro` named import；桶入口循环依赖时为 `choerodon-ui/pro/lib/attachment` 默认导入）或 confirmed wrapper。浏览器报 `ReferenceError: Attachment is not defined` 且栈涉及 `choerodon-ui/pro` 桶入口时，应记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed` 并回 Implementation 修复，不得归因成附件参数缺口。若以 `hzeroAttachmentConfig` 等配置名导入并只传给 `components/RichTextEditor` / `NewRichTextEditor`，按 HZERO 通用组件配置检查，不按 JSX 组件误用处理。

规则：
- 这里保留 UI 运行期最常见的 findings-first 阻塞项，用于 Review/Verification 快速落点。
- Review / Verification / Implementation 需要引用本节时，优先写 `HZUI-*` gateId，再补文件、证据和 owner reference。
- 命中 request/mock/submodule/attachment/import-export/renderer/permission/common component 等专项主题时，应同时回到对应 owner reference 或 skill 取证；这里不是这些主题的唯一规则源。

## Browser / Manual Checklist

每次页面交付必须生成 runtime/manual checklist。缺外部页面运行态证据时也必须以 `not-run-in-verification + reason` 写入 verification report。

最小清单：

- 列表首屏：表格 DOM、数据行、分页、操作列、无 fatal console/network error。
- 操作列可见性：当当前状态存在可见行操作时，操作列 header/title 为 `操作` / action / operation 或项目等价文案，且每个应显示的行操作按钮真实可见；只看到列标题但按钮为空按 failed。
- Runtime console：若浏览器日志出现压缩 chunk 栈、`forEach is not a function`、`Cannot read properties of undefined (reading 'get')`、React #31/#130 或组件初始化异常，必须记录 URL、chunk 文件名、关键栈帧、反查到的组件/源码文件和已回扫的集合 props / renderer / Output renderer。遇到 `record.get` 空值错误时，必须检查详情、create、未加载态和 Output renderer 中所有裸 `record.get(...)`，并要求改为 `record?.get(...)` 或显式 guard；不得只凭 build passed 或单点猜测修复声明 usable。
- 查询：模糊查询、查询回第一页、重置清空并回第一页、刷新保留当前页。
- Modal / Drawer / Overlay：点击打开、宽度或尺寸、mask、z-index、Portal 容器、背景不透明、Header/列表不穿透、关闭后页面无遮挡、筛选/分页不丢。
- 详情内容：区块顺序、Form + Output、数组 Table、集合字段名与 API/MDS 对齐、附件三态、敏感字段。
- 详情主记录切换：仅当合同声明同一详情表面可切换业务主记录时执行；刷新页面后打开详情，切换到另一条主记录再切回，Header/标题、基本信息、详情区块、Tabs、子表和附件同步变化，首尾边界按钮态或提示符合合同，Network / DataSet 证据中的 currentId、targetId 或 direction 与响应记录一致。
- 新建/编辑/复制：可编辑字段可输入、默认值逐字段符合 UI Contract、必填校验触发、只读/禁用字段原因符合 UI Contract。
- 长详情滚动：增加足够多区块、明细行或浏览器小视口后，页面可滚到最后一个区块；Header、Toolbar、Tabs、固定表头/列不遮挡内容；滚到底部和连续新增多行后滚到底部均不出现反复来回滚动。
- 路由编辑态：列表进入编辑、直接刷新编辑 URL、`/create` 无 query 新建、保存后跳转和切换不同 id 均符合 Route Context / Edit Mode Contract；`/detail/create` 命中即 failed。
- 权限按钮：位置、类型、文案、权限码来源、disabled 条件。
- 接口动作按钮：点击后 loading / pending 过渡可见，重复点击被禁用或 handler 阻断；请求成功、失败和异常后 loading 释放。破坏性接口动作必须先确认再发请求；取消确认不得出现 Network/DataSet 请求、状态变更或 loading 残留。
- 数据链路：mock-request/production-transport 证据，Network 或 DataSet 行为；若发现 local-filter、inline mock 或本地内存成功路径，必须标记为 blocking cleanup，不得 usable=true。

## Lessons Learned 回灌

用户手测反馈和修复后必须形成 `assetFeedback / lessonsLearned`；若反馈暴露的是公共规则、模板、agent 消费或机械扫描缺口，Handoff 前必须给出 `assetSuggestion`、owner 文件和状态，不能只在业务修复摘要里写“已修复”。

| 字段 | 说明 |
| --- | --- |
| issue | 用户反馈或手测问题 |
| category | 设计偏差 / 组件选型错误 / 样式层级 / 数据链路 / 验证缺失 / 资产缺失 |
| rootCause | 文档有而没做=实现偏差；文档无但工程有规范=资产缺失；两者都无=需澄清 |
| fixedBy | 修复文件、任务或 finding id |
| assetSuggestion | 需要增强的模板、reference、agent 或 checklist |
| status | open / applied / deferred |

# Choerodon UI - 设计与契约

## 阅读路由
- Choerodon UI 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 组件决策契约
组件选型、页面模式、代码实现和审查都必须能回答：
- 组件体系：项目自定义组件、HZERO 封装、`choerodon-ui/pro`、基础 `choerodon-ui`、其它第三方 UI 库或原生元素；业务组件默认 Pro-first，且必须声明 componentApiProvenance 的 importFamily / wrapperEvidence / foreignApiEvidence。
- 原生元素边界：组件选择顺序必须是命中场景的 `front-hzero-*` 专项 skill / HZERO / Choerodon 内置组件规则 -> 项目 confirmed 组件或 wrapper -> 原生 HTML DOM fallback。项目 wrapper 只有在 confirmed 等价承载标准能力、未命中 legacy/anti-pattern 且不削弱 owner 规则时才可采用；只有专项 skill / 内置组件规则不适用或目标环境明确不可用，且项目也找不到合格组件/wrapper 时，才允许 native DOM；必须记录 nativeFallbackEvidence、搜索范围、排除原因和替换风险。
- 数据绑定：是否由 DataSet 字段、`queryFields/queryDataSet`、Table column `name/editor`、Form 字段 `name` 或本地只读展示承载。
- 事实证据：字段、选项来源、组件 API、import 风格、生命周期、权限和协议哪些已确认，哪些待确认。
- 替代排除：为什么不用项目组件、HZERO / Choerodon 内置组件、基础组件、手写 React state、原生表单、Upload 替代 Attachment、Select 替代 Lov，或 Lov 替代 Select。
- 降级边界：事实不足时只输出候选组件和建模位置，不输出真实-looking props、events、默认值、`bind`、URL/method、bucket、上传协议或返回映射。

## 目标
把 Choerodon UI 任务收敛到一个可执行入口中，优先走 DataSet-first 和 `choerodon-ui/pro`，避免在 DataSet、Form、Table、页面模式和组件选型之间反复分流。

负责：
- 场景识别和任务分流。
- DataSet-first 建模。
- Form/Table/页面模式/组件组合方案。
- 最小实现或审查路径。
- 验证和不确定性处理。

不负责：
- HZERO 工程位置、路由、菜单权限、微前端或运行时配置。HZERO + Choerodon 场景先由 HZERO 约束定工程边界，再用本 skill 做 DataSet/Form/Table/组件实现。
- 在没有 HZERO 上下文或项目证据时，把纯 Choerodon UI / Pro / C7N 表单、表格、DataSet 或组件选型问题扩展成 HZERO 路由、菜单、微前端、运行时、构建或权限问题。
- 编造接口 URL、字段清单、lovCode、lookupCode、bucket、上传协议、后端响应结构或未确认组件 API。
- 从页面名称、业务对象名或常见经验推导字段名、service 函数名、权限 action、`bind` 返回字段或附件标识字段。
- 用 `mock`、`demo` 前缀把未确认字段、路由、权限码、i18n key、service/helper 或附件标识字段包装成 confirmed 代码；默认 mock demo 下只能作为 `generatedCandidate/mockOnly` 并进入 replacement。
- 把“按常规先写”“后面我再改”“直接帮我写”理解为字段、接口、权限、路由或生产契约确认。
- 推广基础 `choerodon-ui` 组件作为业务默认实现。团队默认优先使用 `choerodon-ui/pro`。
- 用其它组件库的同名组件 API 反证或补全 C7N / `choerodon-ui/pro` 组件事实。`hzero-ui`、antd、Ant Design Pro、Arco、Fusion、Material UI、Element、项目旧 wrapper 或任意参考仓库样例，都不能证明 C7N 组件支持同名 props、events、静态方法或数据入口；把这类外部 API 写进 C7N 组件属于 blocking 级严格禁止项。

## Reference 路由
按需查本目录 `references/`：DataSet/Form/Table、组件、配置、API 和模式骨架分别在同名主题文件中；patterns 已拆成 topic files，先读最小匹配项，例如 `references/patterns/query-list.md`、`references/patterns/form-edit.md`，不要外显内部查阅路径。

最小读取规则：
- DataSet 建模：先读 `references/dataset.md`。
- Form/Table：先读 `references/form-table.md`。
- Lov/Attachment/Modal/Button 等组件：先读 `references/components.md`。
- 配置和上下文：先读 `references/configuration.md`。
- 页面组合：只读命中的一个 `references/patterns/<topic>.md`。
- 只有主场景文档没有覆盖具体 props、methods、events、默认值或组件行为时，才读 `references/api.md`。
- 涉及 DataSet/Table/Form/Button/Lov/Attachment/Modal 等 enum-like props 时，必须优先读取 `references/enum-map.md` 查找 Choerodon fallback 枚举域和重名导入边界；它是无项目证据时的首选枚举候选表，但只能生成 `generatedCandidate / fallback`，不得替代目标项目 import 证据或被标为项目 confirmed。
- 不得为了确认通用 Choerodon API 全仓搜索目标项目源码；目标项目源码只用于确认项目封装、import 风格、局部配置覆盖、相似页面写法或用户指定文件。

`references/patterns/*` 是按 topic 拆分的二级 reference。高频组合场景只读最小匹配文件：
- Choerodon UI Contract 专项守卫：`references/patterns/ui-contract-guardrails.md`。
- Choerodon 静态反模式检查：`references/patterns/static-anti-pattern-checklist.md`。
- 查询列表页：`references/patterns/query-list.md`。
- 新增/编辑/详情表单：`references/patterns/form-edit.md`。
- 弹窗/抽屉、LOV、值集、附件上传：`references/patterns/modal-lov-attachment.md`。
- 行内编辑：`references/patterns/table-inline-edit.md`。
- 主从/头行：`references/patterns/master-detail.md`。
- 导入导出：`references/patterns/import-export.md`。
- 树表/层级数据：`references/patterns/tree-data.md`。
- HZERO 已确认工程、路由、权限、i18n 和页面容器后的内容区交接：`references/patterns/hzero-handoff.md`。
- DataSet mock/demo transport 可运行边界：`references/patterns/dataset-mock-transport.md`。

枚举、类型和导入事实按场景读取：DataSet 看 `references/dataset.md`，Form/Table 看 `references/form-table.md`，组件看 `references/components.md`，配置看 `references/configuration.md`。其中 enum-like props 的候选枚举域和导入歧义优先回到 `references/enum-map.md` 对齐；reference import 永远不能单独确认为项目 import。

## 任务分流
0. 先判断任务属于 `choerodon-ui/pro`、`choerodon-ui/dataset` 还是基础 `choerodon-ui`：业务表单/表格/查询/提交/上传/弹窗优先 Pro；DataSet 是核心数据资产；基础组件只作为纯展示/布局或 Pro 不覆盖时的兜底。
1. 页面级需求：先判断页面模式，再进入 DataSet 和组件组合。
2. 表单/表格/查询/提交/校验/联动：先做 DataSet 建模。
3. 具体 Form 或 Table 改造：确认 DataSet 边界后再落到组件属性和交互。
4. 组件选择问题：先判断是否需要 DataSet，再优先选择 Pro 组件；仅当 Pro 无合适组件或任务是纯展示/布局时，才考虑基础组件。输出时必须说明选中组件、绑定方式、已确认事实、被排除的候选和仍缺的组件/API 事实。
5. 需要具体参数、方法、事件、默认值、枚举/类型或骨架代码：先查对应场景文档，例如 `references/form-table.md`、`references/dataset.md`、`references/components.md`、`references/configuration.md` 或命中的 topic pattern；涉及 enum-like props 时优先查 `references/enum-map.md` 对齐 fallback 枚举域和重名 import；场景文档未覆盖具体 API 事实时，再按最小读取规则查 `references/api.md`。`enum-map.md` 只能提供 generatedCandidate / fallback，不是项目 confirmed 证据。
6. 上传、Lov、值集、树、动态筛选、主从/头行、导入导出、性能等复杂专题：先查对应 reference 或 `references/patterns/` topic，再输出结论。
7. Choerodon 列表、查询条、详情、Modal/Drawer/Overlay、PermissionButton、local-filter 或 DataSet transport 的实现/审查/修复任务，必须应用 `references/patterns/ui-contract-guardrails.md` 的专项守卫；PermissionButton 入口和 Provider 契约同时应用 `front-hzero-permission-button`；实现后或审查时按 `references/patterns/static-anti-pattern-checklist.md` 做最小静态反模式检查。
8. 多轮对话中，如当前会话已经进入本 skill 的 Choerodon/DataSet/Form/Table 范围，后续继续实现、排障、审查或优化同一任务时，默认先沿用本 skill 的检查清单、reference 路由和 DataSet-first 规则，再做最小必要代码探索；不要静默退回成无 skill 约束的普通仓库搜索。
9. 审查任务：findings-first，先确认页面性质是生产、用户确认的临时 mock/demo 还是不确定；再列风险和修复方向，最后给摘要。

## Choerodon UI Contract 守卫
- 编码前必须读取或生成 UI Readback Table、UI Contract 和 Evidence；缺失时只允许输出组件/DataSet 映射建议、待确认项，或返回前端主流程补资产，不得生成非 runnable 页面骨架。
- L1 纯 API/props 解释、无可见 UI 的 import/type/注释/测试小修不强制生成完整 UI Contract；若 L1 触及可见 UI、查询、详情、Modal/Drawer/Overlay、权限按钮或 transport，执行命中的最小 UI Contract 和静态反模式检查。
- 普通管理列表默认使用 Choerodon Pro `Table + DataSet + filterBar` 查询形态；`queryBar` 代码写法按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态，不能使用目标项目健康字符串风格。UI Contract、Figma、FDS/TDS 或用户确认明确要求其它查询条模式时，记录 `queryBarMode + sourceRef + reason`，但代码仍必须使用 enum。无项目证据时先查 `references/enum-map.md`，默认走 asset/fallback enum，不得把 `queryBar="filterBar"` 当作新增页面默认写法。
- 组件 API 证据必须按 import family 隔离：`choerodon-ui/pro`、基础 `choerodon-ui`、`hzero-ui`、antd、其它第三方 UI 库和项目 wrapper 分别记录。非 C7N import family 的样例只能作为 `foreignApiEvidence/negativeEvidence/sourceContamination`，不能写入 C7N `componentApiProvenance=confirmed`；若只能找到跨库样例，应返回补证据或改为 C7N 正向模式。任何跨库 API 污染命中都必须阻塞实现和审查通过，不得用 generatedCandidate、mock/demo、`as any` 或 wrapper 薄封装放行。
- FDS/TDS 中出现关键字、搜索框或模糊查询时，必须配置 `queryBarProps.fuzzyQuery` 或记录项目不支持证据。
- 查询字段必须形成 QueryFields Schema：字段、label、组件类型、是否多选、是否允许清空、默认值、选项来源和查询提交值。
- 操作列必须是最后一列；右锁定使用 `ColumnLock.right` 或项目 confirmed 等价 enum 导出，禁止用 `lock: true` 或 `lock: 'right'` 代替。
- 新建、编辑、复制、详情页面必须继承 Route Context / Edit Mode Contract：页面业务状态由 routeContext、UI Contract 和业务状态守卫决定；不得直接用 `window.location.hash`、hash 正则或散落 query/params 判断 `editFlag/isCreate/pageMode`；DataSet `editFlag` 只作为展示/提交字段。
- 页面模式必须先区分 create/edit/detail/copy/approval/readonly/mixed。只读详情默认使用 `Form + Output`；create/edit/copy 中应可编辑的业务字段必须使用已确认的 Choerodon Pro 输入组件和 `name` 绑定，不得套用 `Output` 只读模板。数组/集合明细必须消费 Detail Collection Contract 的 `apiField`、columns、rowKey、fieldNameSource 和 mockFieldPolicy；表格型详情集合只能使用 Choerodon Pro Table，不允许项目 confirmed 只读表格、wrapper、HZERO 非表格组件或原生 DOM fallback 替代。禁止无依据的摘要头、统计卡片、自绘 `div/grid` 详情，以及把集合字段用 `ul/li`、文本拼接、JSON stringify 或模板字符串展示。集合列必须绑定 MDS/TDS/API 原始 item 字段名，不得把真实字段改造成无来源 `title/organizationName/timeRange/description` 这类通用 shape；如需 view model，必须集中 adapter 并记录字段映射。
- 详情、表单、导入组件、预览等业务弹层的形态必须来自需求/FDS/TDS、Figma/PageSchema、UI Contract、项目同类页面证据或用户确认；不得默认写死为 Drawer。业务弹层统一用 `Modal.open` 或已确认等价 wrapper 打开，不得默认使用 JSX `Modal` / `Drawer` 常驻渲染加 visible state；`<Modal drawer visible>`、`<Modal visible>`、`<Modal open>`、`<Drawer visible>` 和 `visible/open state + 常驻 JSX` 对新增或重构业务弹层是严格反模式。若已确认使用 Drawer，必须使用 `Modal.open({ drawer: true, resizable: true, ... })` 或等价 wrapper，并控制打开、关闭、清理、重复打开、背景、Portal 容器和层级。所有业务 Modal / Drawer / Overlay 的宽度必须严格按设计要求；设计未指定宽度时，普通表单 Modal 默认 `size=small`，详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并记录 readabilityRisk、Form columns/colSpan 与 `valueOverflowPolicy`；不得自行生成宽框。尺寸必须配置在 confirmed Modal/Drawer API 入口（如 `size`、`width` 或 wrapper `drawerWidth/modalSize`），只写 `style.width` 或内容容器宽度不算通过。普通业务 Modal 也必须通过 `Modal.open({ ... })` 或等价 wrapper 打开。操作列“更多”是行操作溢出菜单，必须使用 HZERO renderer skill 已确认的操作列 helper、项目操作菜单、Dropdown/Popover/Menu 等轻量浮层，不得使用 Drawer。
- 新生成 mock/demo 不得使用 local-filter、本地内存 seed/filter、`src/utils/mock.ts` 或 `service/mock + loadData`；可运行 mock 必须走 DataSet `transport.read` / 项目 request adapter 请求 HZERO 本地 devServer middleware 暴露的 HTTP mock API。发现 local-filter / inline mock 成功路径必须阻断并清理，不得直接把本地 `PageResponse` 接入 DataSet `transport.read` 冒充真实 API。
- 实现后必须执行 UI against design 静态/契约对账，并输出 browser/manual checklist；浏览器运行态只消费外部 runtime acceptance 或用户手工证据，并把组件选型、数据链路或 UI 可用性问题回灌 lessons learned。

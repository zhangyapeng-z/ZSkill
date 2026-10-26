# Choerodon UI - 实现与工程证据

## 阅读路由
- Choerodon UI 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## DataSet-first 规则
- 业务 UI 默认从 `choerodon-ui/pro` 查找组件；基础 `choerodon-ui` 仅作为纯展示、布局、反馈或 Pro 不覆盖时的兜底。
- 可见业务 UI 的组件选择顺序固定为命中场景的 `front-hzero-*` 专项 skill / HZERO / Choerodon 内置组件规则 -> 项目 confirmed 组件或 wrapper -> 原生 HTML DOM fallback。项目 wrapper 只有在 confirmed 等价承载标准能力、未命中 legacy/anti-pattern 且不削弱 owner 规则时才可采用；只有专项 skill / 内置组件规则不适用或目标环境明确不可用，且项目也找不到合格组件/wrapper 时，才允许原生 `<table>`、`ul/li`、`div/grid` 等 DOM；代码旁或交付产物必须能追溯 `nativeFallbackEvidence`，否则不得实现。
- 标准表单：`DataSet + Form + fields`。
- 标准列表：`DataSet + Table + fields + queryFields/queryDataSet`。表格列 `columns[].name` 必须能回溯到主列表 DataSet `fields[].name`，并在该字段上提供 label/type/renderer 所需元数据；`queryFields` 只定义查询条件，不替代表格展示字段。
- 新增或重构的资产基线 Choerodon Pro Table 默认在函数组件或自定义 Hook 内声明 `const columns = useMemo<ColumnProps[]>(...)`，并以 `<Table dataSet={dataSet} columns={columns} ... />` 消费。普通业务列、列级 `editor`、renderer、操作列和列宽策略都收敛到该数组；不生成 `<Table><Column ... /></Table>` 子节点写法。只有项目 wrapper、递归/运行时动态列或组件版本兼容性明确要求 JSX 子列时允许例外，且代码近邻必须记录 `tableColumnComposition=jsx-children`、`sourceRef` 和 reason；`sourceRef` 必须是相对当前 validator root 可读取的源码路径，旧页面样式本身不能作为来源。
- C7N 组件 API 必须由同一 import family、同一项目 wrapper 源码/类型或目标项目 confirmed 用法证明；不能跨库继承同名组件 API。`Table/Form/Modal/Drawer/Upload/Attachment/Select/Lov/DatePicker/Button/Tabs/Tooltip/Tree/Cascader` 等同名组件在不同库中的 props、events、静态方法和数据入口默认互不兼容。跨库 API 污染一律 blocking，不得进入 runnable implementation、mock-completed、usable=true 或 production-ready。
- `Select` / `Lov` / `Upload` / `Attachment` / `Modal` / `Table` 等高风险 props 或 static options 若确需使用项目 confirmed API，必须在代码近邻留下结构化 `componentApiProvenance`，至少包含 component、prop/option、`confirmed`、同 import family 或 confirmed wrapper source/evidence 和 reason；文件顶部笼统声明、foreignApiEvidence、negativeEvidence 或 sourceContamination 不能作为放行证据。无证据时优先改回 DataSet/lookup/标准组件建模，不要生成 `options/onChange/value` 等看似可用但来源不明的 props。
- Choerodon Pro `Table` 的数据入口必须是 `dataSet={listDs}` 或项目 confirmed 等价 Pro 封装；严格禁止把 `hzero-ui` / antd / 其它组件库 Table 的 `dataSource`、`rowKey`、`onChange`、`rowSelection`、`pagination` 迁移到 `choerodon-ui/pro` Table 后再用 `getCollection(dataSource)`、`loadData` 或局部数组适配。相似仓库中非 C7N Table 的 `dataSource` 写法只能作为负例或迁移风险，不是 Choerodon Pro 组件 API 证据。
- Table 行内编辑若已选择 `editMode={TableEditMode.inline}` 或项目 confirmed 等价 enum，优先使用框架内置编辑链路：列直接声明 `editor`/`editor={true}`，命令列优先使用内置 `edit`/`delete`/`save` 等能力或与其一致的项目写法。不要先引入额外的 `record.getState('editing')`、本地状态或自定义编辑态，除非项目现有模式或已验证需求明确需要 custom inline。
- 查询协议：接口契约已确认时，优先进入 `queryFields`、`queryDataSet`、`queryParameter` 或 `transport.read`；未确认时只描述待补位置。
- 列表、详情明细表、主从子表、Tab 内表格或弹层内表格存在筛选条件时，必须优先把筛选建模到 `queryFields/queryDataSet + Table filterBar`；`queryBar` 代码写法必须按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态。不得用外置 `<Form dataSet={queryDataSet}>`、独立查询/重置按钮和 `Table queryBar={TableQueryBarType.none}` 替代推荐 filterBar。只有 UI Contract、Figma、FDS/TDS、用户确认或项目 confirmed wrapper 明确外置筛选区/非 filterBar 模式时，才允许偏离，并必须记录 mode、sourceRef、reason 以及外置筛选如何调用 DataSet query/reset/refresh。
- 显式 `queryDataSet` 必须传 `DataSet` 实例，不得把 `DataSetProps` 配置对象、`createQueryDS()` 配置工厂或对象字面量直接赋给主 DataSet 的 `queryDataSet`。推荐拆成 `createQueryDSConfig(): DataSetProps` 与 `createQueryDataSet(): DataSet`；项目既有 `createQueryDS()` 配置工厂可保留，但调用点必须 `new DataSet(createQueryDS())`。
- 本地固定候选 `fields/queryFields[].options` 使用 DataSet 实例时，必须通过顶层静态导入 `import { DataSet } from 'choerodon-ui/pro'` 后写 `options: new DataSet({ data, selection: false, paging: false })`；不得在字段配置里生成 `new (require('choerodon-ui/pro').DataSet)(...)` 或其它动态 require 构造。该配置只作用于内层 options DataSet；外层普通列表 DataSet 仍按 `autoQuery=true` 优先首查，除非存在前置条件或受控查询时机。`paging: false` 不可省略，否则静态数组会被默认分页逻辑误当分页响应处理。
- 提交协议：优先进入 `transport`、`submit()` 和 `dataToJSON`。
- 字段规则：优先进入 `fields`，包括 label、type、required、validator、lookupCode、lovCode、options、textField/valueField、dynamicProps/computedProps。
- 列表列字段规则：生成或修改 Table `columns` 时，除纯操作列、选择列、展开列和有明确 `renderer/header` 且不依赖 DataSet label 的派生列外，每个 `{ name: fieldName }` 都必须在同一个主 ListDS `fields` 中存在对应字段；不得因为该字段已出现在 `queryFields` 就省略 `fields`。反向也成立：只进入 `fields` 的字段不会自动成为查询条件，需求要求筛选/搜索时仍必须进入 `queryFields/queryDataSet`。
- 组件绑定：Pro 字段组件优先通过 `name` 绑定 DataSet 字段，不重复保存本地 `value/onChange`。
- 日期/时间展示：DataSet `FieldType.dateTime/date/time/week/month/year` 字段进入 Table renderer、Output renderer、详情 JSX 或其它自定义展示时，必须按 `dateTimeRenderContract`、组件默认展示、项目 confirmed date renderer，或显式 `value?.format(format)` 转成 string/ReactNode；不得直接返回 `value`、`record.get(dateField)` 或 moment-like 对象作为 React child。已出现 React #31、列表/详情不可用或仍声明 `usable=true`/production-ready 时，按 `HZC-DATETIME-RENDER-001` blocking 处理。
- 详情数组/集合字段必须按 Detail Collection Contract 实现：集合根字段和 item 列字段使用 MDS/TDS/API 原始字段名，mock/demo response 保持同名；旧别名、UI view model 或双 shape 只能形成 contract conflict / migration finding，不得在新实现中增加兼容 adapter。经历、教育、语言、获奖等表格型 repeated records 只能使用 Choerodon Pro Table；附件按附件专项组件规则处理。不得在详情内容组件内使用项目只读表格/薄 wrapper、手写 `SimpleCollectionTable`、原生 `<table>`、`ul/li`、JSON stringify、模板字符串或 `title/organizationName/timeRange/description` 这类自造通用字段作为完成态展示。
- Lov、Select、Attachment 缺少生产业务参数时，先按 owning reference 保留标准组件形态和 DataSet 建模位置；`lovCode/lookupCode`、`textField/valueField/bind`、`lovPara` 参数名/来源字段/空值行为/级联清理策略、附件 bucket/storage/template 等仅缺参数时，输出 `generatedCandidate/mockOnly/placeholderParameter` 并登记 replacement，不得退化为 TextField、普通 Upload、静态列表或 disabled/no-op。只有字段语义、value shape、返回对象结构或组件可实例化条件无法形成候选时，才只输出确认清单并返回 Design / Contract Check。
- 写 DataSet 字段前必须对账 `LOV Lookup Binding Contract`、编码候选表和字段语义。Implementation 不得把上游明确为 `lovCode` 的字段自行改写成 `lookupCode`，也不得把上游明确为 `lookupCode` 的普通枚举改成 object Lov；若设计文档内部映射表与 DataSet 示例冲突，先返回 Design / Contract Check 标记 `conflict`。仅有后端 `@LovValue` 或平台值集术语时，必须按前端语义显式记录转换：普通枚举/状态/类型用 `Select + lookupCode` 或本地 options 候选，主数据对象选择用 `Lov + FieldType.object + bind`。
- DataSet `fields` 与 `queryFields` 分别形成独立绑定图。每个区域内 `name` 必须唯一，object LOV 容器使用独立 `*Lov/*Obj` 名称，`bind` 只能从容器属性单向回填 API 原始业务、展示或查询叶子字段；不得把 `itemCategoryId/itemId` 等 `*Id` API 叶子字段改成 object 容器，也不得用正确的 `itemCategoryObj/itemObj` 容器再以 `*IdValue/*CodeValue` 别名替代提交字段。真实后端别名是唯一例外，目标字段对象内必须记录非空的 `lovBindingAlias=confirmed`、`sourceRef` 和 `reason`。禁止 `name=X` 同时出现 `bind: 'X.<property>'`，也禁止任意间接 `bind` 闭环。修改 DataSet 字段后必须对照全部 bind edge，不得只修复首个运行时报错字段。
- 申请人、员工、部门、组织、供应商、客户、物料、物料类别等主数据 `*Id` 字段如果出现 `lookupCode`，或使用状态/类型值集编码占位，当前实现必须视为字段语义和组件类型偏离；能修复时改成 object Lov 候选和回填字段，缺返回映射时写 generatedCandidate/replacement，不能把该字段标为 mock-completed、usable 或 production-compliant。
- 树/主从：先确认嵌套树、扁平父子或主从关系模型，再按 `children`、`idField + parentField`、`childrenField`、`cascadeParams` 等已确认模式建模；树表细节读 `references/patterns/tree-data.md`。
- 枚举/类型：组件 enum props 必须导入确认 enum 或项目 confirmed 等价 enum 导出；DataSet 配置类可按已确认策略选择 enum 或健康字符串。优先沿用 Evidence enum import map 或目标项目现有 import 路径，避免同一 feature 内混用等价字符串和框架枚举。涉及 DataSet/Table/Form/组件枚举型 props 时，必须先查对应 reference 并记录 enum provenance；reference import 只能作为 generatedCandidate / fallback，不等于项目 confirmed。空项目、缺参考子模块或 asset/fallback baseline 下，DataSet `fields/queryFields[].type` 必须使用 `FieldType.*` 对应枚举成员；任意 `type: '<fieldType>' as const` 仍按裸字符串和类型逃逸处理。不能确认 import 路径时不要编造枚举。
- 跨页选择/变更：优先评估 `cacheSelection`、`cacheModified`，并确认 `primaryKey` 或 unique 字段。
- 渲染期取值优先使用 DataSet Record API，但 Table/Form/Output `renderer`、`render` 或自定义展示参数里的 `record` 可能在 create、未加载或组件探测渲染时为空；读取字段必须使用 `record?.get(...)`、`record && record.get(...)` 或显式 guard。不要把 `toData()` / `toJSONData()` 当作渲染取值入口，也不得直接写 `renderer={({ record }) => record.get(...)}` 或 `TagRender(record.get(...))`。

## 执行流程
1. 判断任务类型：新增、修改、审查、排障、优化、解释。
2. 只在需要确认项目封装、import 风格、局部配置覆盖、相似页面写法、接口契约位置或用户指定目标文件时读取项目上下文；小任务只读必要文件。
3. 确认字段和接口依据：产品/设计文档、用户字段清单、接口契约、Swagger/API 文档、后端 DTO 或用户明确输入。现有相似页面和项目源码只能证明写法、目录、封装或已有契约位置，不能替代新业务字段、接口、权限、LOV、附件或上传协议。
4. 证据充足时输出或实现最小方案；证据不足时先判断是否能按默认 mock/demo 或 generatedCandidate 形成候选。仅缺平台编码或组件参数时继续生成标准组件候选并记录 replacement；缺字段、接口、返回结构、value shape 或写入范围导致无法形成候选时，才只输出建模框架、待确认清单和验证步骤。
   - 自然语言名称、经验性授权、mock/demo 前缀、Lov/Attachment/transport 占位都不能替代字段、接口、权限、返回结构或上传协议契约。
   - Lov 回填和 Attachment 值结构缺证据但字段语义和候选 value shape 足够时，生成 `generatedCandidate/mockOnly` 参数并保留标准组件；完全无法判断对象选择、自由文本、附件 UUID 或文件列表结构时只列待确认。transport 缺协议时写“待确认，暂不配置”，不要写 URL/method、adapter 或推测的 service 函数。
5. 需要具体 API、默认值、组件行为或示例时，按最小读取规则查 `references/`。如果本 skill 没有覆盖该事实，不能继续假设；应列为待确认项。
6. 编码后发现项目验证命令，再运行 lint、typecheck/tsc、test、build 中可行的命令；未运行必须说明原因。

### Mock/Demo 审查边界
- 先确认页面性质；未确认时把“是否临时 mock/demo”列为待确认，不自行假定。
- 用户明确为临时 mock/demo 时，区分生产缺陷和 mock 边界风险；本地 mock、未配置真实 `transport` 或派生权限码不直接判为严重生产缺陷，但必须提示生产前替换真实字段、接口、权限码、附件协议和 DataSet transport。
- 即使是 mock/demo，仍检查 Pro-first、DataSet `name` 绑定、避免不必要的基础组件和字段级本地 `value/onChange`。

## 证据不足时的降级输出
如果缺少字段、接口、lovCode、lookupCode、上传协议、后端响应结构或组件事实：
- 先区分缺口类型。仅缺 `lovCode/lookupCode`、`bind/textField/valueField`、`lovPara` 参数名/来源字段/空值行为/级联清理策略、bucket/storage/template、templateCode、permissionCode 或 locale key 时，不阻塞默认 mock/demo 实现；按标准组件/helper 输出 `generatedCandidate/mockOnly/placeholderParameter`，并写 replacement / Handoff risk。
- 缺口只允许降级参数状态，不允许降级字段语义或组件类别。主数据对象选择缺 `lovCode/bind` 时保留 `Lov + FieldType.object` 候选；普通枚举缺 `lookupCode` 时保留 `Select + local options/lookupCode generatedCandidate` 候选。不得用不相关 `lookupCode` 填充主数据字段，也不得用 `lookupCode` 掩盖上游 `lovCode` 合同冲突。
- 缺字段清单、接口资源、后端响应结构、字段/value shape、写入范围或组件可实例化条件导致无法形成候选时，不生成可运行字段、路由、service/helper、权限码、`bind`、附件标识、`transport`、URL/method、上传参数或内部占位 token。
- 不能形成候选时，只输出 DataSet/页面/组件结构、自然语言待确认项、确认后补充位置和验证方式。

# Choerodon UI - 审查与反模式

## 阅读路由
- Choerodon UI Review、自查、反模式、finding 或合规判断时读取。

## 反模式
- 明确是 Choerodon 表单/表格/查询/提交场景，却先用 React `useState` 手写字段模型。
- 把查询参数散落到按钮点击或页面局部状态中。
- 明细表、子表、Tab 内表格或普通列表存在筛选条件，但实现为外置 `<Form dataSet={queryDataSet}>` + 独立查询/重置按钮 + `Table queryBar={TableQueryBarType.none}`，且没有 UI Contract / 项目 confirmed wrapper 来源。即使查询链路能触发，也应按 filterBar 形态偏差处理；`queryBar="none"` 等字符串形态另按 enum 违规处理；影响统一查询体验、字段折叠、重置/刷新或验收时 major。
- 详情数组/集合字段没有按 Detail Collection Contract 使用 Choerodon Pro Table，而是使用项目只读表格/薄 wrapper、HZERO 非表格组件、手写 `SimpleCollectionTable`、原生 `<table>`、`ul/li`、`div/grid`、JSON stringify、模板字符串或通用 summary 映射，至少 major；导致真实接口下集合为空或误报 demo/production ready 时 blocking。附件集合按附件专项组件规则另行审查。
- 详情集合列字段与 MDS/TDS/API 不一致且无集中 adapter，例如真实 `workExpList[].positionName/companyName/startMonth/endMonth/workDescription` 被组件读成 `title/organizationName/timeRange/description`，或 mock 被改成前端自造 shape 掩盖字段错配。命中按 contract fidelity finding 处理，核心详情区为空或仍声明已验证时 blocking。
- 未确认契约就写真实字段、Lov/lookup、接口、附件、权限或 mock/demo helper。
- 字段语义、`LOV Lookup Binding Contract`、编码候选表和 DataSet 实现之间出现 `lovCode/lookupCode` 漂移时必须形成 finding。典型包括：设计映射表写 `lovCode` 但 DataSet 示例或实现改成 `lookupCode` 且无转换来源；申请人、员工、部门、组织、供应商、客户、物料、物料类别等主数据字段使用 `lookupCode`；`applicantId/deptId/itemCategoryId/itemId` 等字段绑定了状态、紧急程度、采购类型等无关值集编码。影响 required 表单、查询或提交时至少 major；导致对象选择不可用、回填字段缺失、提交字段错误、只读展示 raw ID 或仍声明 usable / production-ready 时 blocking。
- Review 必须按每个 `fields` / `queryFields` 区域复核 DataSet bind graph：字段名是否重复、每条 `container.property -> leaf` 是否单向、是否存在 `X -> X` 或 `X -> Y -> ... -> X`。发现 `FieldType.object` LOV 容器与 leaf 字段复用同名、或仅修复一个 Cycle binding 报错而未回扫同区域全部 bind edge 时，按 `GCSQ-LOOKUP-005` 输出 major finding；已导致页面初始化错误或仍声明 usable / production-ready 时 blocking。
- 从 `hzero-ui`、antd、Ant Design Pro、Arco、Fusion、Material UI、Element 或项目旧 wrapper 样例复制同名组件 props/events/static API 到 C7N / `choerodon-ui/pro` 组件；典型如把其它 Table 的 `dataSource`、`rowSelection`、`pagination`、`onChange` 迁移到 `choerodon-ui/pro` Table，或用 `getCollection(dataSource)` 把数组伪装成 Pro Table 数据入口。命中即 blocking，修复前不得继续交付。
- C7N high-risk prop finding 不是“所有 `Select options/onChange/value` 绝对禁止”，而是要求同 import family 或 confirmed wrapper 证据。Review 只能接受目标代码近邻结构化 `componentApiProvenance`：component、prop/option、`confirmed`、source/evidence、reason 均齐全；文件级笼统注释、跨库样例、foreignApiEvidence、negativeEvidence 或 sourceContamination 不得放行。无证据时应回 Implementation 改为 DataSet/lookup/标准组件建模，或回 Task/Design 补组件 API 证据。
- Choerodon Select / Lov / DataSet field `options` 必须复核运行态集合形态。无项目 wrapper/版本证据时，DataSet `fields/queryFields` 中的本地固定候选默认使用 `new DataSet({ data, selection: false, paging: false })` + `textField/valueField`；普通数组 `options: [{ value, meaning }]`、本地静态 options DataSet 缺 `paging: false`、分页响应对象、Promise、raw response 或 JSX 片段应形成 finding。压缩栈出现 `t.get is not a function` 时，Review 必须把 `Select options` 数组项被按 Record 调用 `get()` 作为优先排查项；出现 `forEach is not a function` 时优先排查 lookup/options 响应集合形态和本地 options DataSet 默认分页。
- `options` 的本地 DataSet 构造应来自顶层静态 `import { DataSet } from 'choerodon-ui/pro'`；字段配置中出现 `new (require('choerodon-ui/pro').DataSet)(...)` 属于生成质量和静态 import provenance 缺口，至少 major，应改为 `options: new DataSet(...)`。
- 在组件 props 中重复定义 DataSet field 已有 label、required、校验和映射。
- 资产基线新增或重构的 Choerodon Pro Table 把常规列写成 `<Table><Column ... /></Table>`，而没有 `columns={columns}`、函数组件/自定义 Hook 内的 `useMemo<ColumnProps[]>`；这是生成形态偏差，至少 major。仅当代码近邻同时存在 `tableColumnComposition=jsx-children`、相对当前 validator root 可读取的 `sourceRef` 和可核验的 wrapper/动态列/版本兼容 reason 时可放行，旧页面写法不能作为例外依据。
- Table 大数据场景不评估 virtual、PerformanceTable 或分页策略。
- DataSet/Table/Form/Button enum-like props、Table columns/renderer/buttons 出现生成缺口时，Review 必须发现并推动修复，不得只标为“后续优化”。典型包括：Table/Form/Button 等组件 props 裸字符串，DataSet `fields[].type/queryFields[].type/selection/dataToJSON` 裸字符串且无健康 `project-string-confirmed`，任意 `type: '<fieldType>' as const` 这类 TS assertion 逃逸，弱类型相邻页面被冒充 confirmed，`new DataSet({ ... } as any)`、`columns as any`、无类型 renderer 参数、或任务中的 `Choerodon enum/TS contract acceptance` 未落到代码。
- 上述 enum/TS 缺口若目标文件可定位且不需要新增业务决策，Review finding 必须进入 `recommendedFixPackage.必须本轮修复项`，建议回 `frontend-implementation-agent` 自动修：补 enum import、给 DataSet config/columns/buttons/renderer 补类型来源、移除 broad `as any`，并在修复后复查静态扫描和类型检查。只有缺项目 enum import 证据、需要选择 DataSet 字符串/枚举策略或会改变业务交互时，才回 Design/Task backfill 或用户确认。

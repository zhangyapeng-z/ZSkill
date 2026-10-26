# Choerodon 映射输出模板

## 使用场景
用于 PageSchema 已形成，目标技术栈为 Choerodon UI / Pro 或 HZERO + Choerodon DataSet，需要把设计结构转成 DataSet-first 的页面映射方案、UI Contract seeds 或专项交接说明。

## 输入摘要
1. PageSchema 类型：`list` / `form` / `formWithTable` / `detail` / `modal` / `drawer` / `componentShowcase` / `unknown`。
2. 主要区域：header、search/filterBar、toolbar、form、table、tabs、modal、drawer、upload。
3. 证据状态：confirmed / inferred / missing。
4. Framelink 证据：`rawInputFormat`、组件证据、图片/SVG 证据、占位文案。

## 映射总则
1. 业务表单、表格、查询、提交、弹窗、上传默认使用 `choerodon-ui/pro`。
2. 标准页面优先 `DataSet + Form/Table`；不要用局部 state 承载字段、查询、提交和校验。
3. 缺字段名或接口契约时，只输出 DataSet 划分和待补位置，不写 `fields.name`、`transport`、URL/method 或 service 函数。
4. `Label`、`Button`、`Table title`、`Table text`、`字段一` 等占位文案不能生成真实字段名、列名、权限动作或 i18n key。
5. LOV、lookup、Attachment、Upload、树、拖拽、行编、分页、排序、筛选都必须等业务协议确认后再生成可运行配置。
6. 映射输出必须携带 UI Contract seeds；这些 seeds 必须继承 `references/component-mapping-guardrails.md` 和 `front-hzero-choerodon-ui`的 UI Contract 守卫。
7. Figma 阶段不能确认 Choerodon 组件 API；任何 `candidate` 都必须交给 `frontend-design-agent` 形成组件契约，并由下游 C7N validator 或项目源码证据确认。
8. UI 显示布局以 Figma/PageSchema confirmed 优先；业务契约以 FDS/TDS/API/用户确认优先。冲突必须输出 `uiBusinessConflicts`，不得用 Figma 文案推导字段名、接口或权限。

## Page Type 映射
| PageSchema 类型 | Choerodon 方案 | DataSet 建议 | 代码输出边界 |
| --- | --- | --- | --- |
| `list` | `DataSet + Table + filterBar` | 一个列表 DataSet；可选 query DataSet 或 queryFields；关键字搜索候选 `queryBarProps.fuzzyQuery=true`；`queryBar` 代码按 enumProvenance 使用 `TableQueryBarType.filterBar` | 有字段/接口时可生成 fields/queryFields；缺接口不写 transport |
| `form` | `DataSet + Form` | 一个表单 DataSet，`autoCreate` 视新增/编辑场景确认 | 缺字段名时只列字段候选，不写真实 `<TextField name>` |
| `formWithTable` | `主 DataSet + 明细 DataSet + Form + Table` | 主表单 DataSet、明细表格 DataSet、查询 DataSet | 缺接口时不写主从提交、分页、行操作协议 |
| `detail` | `DataSet + readonly Form + Output + Table/Attachment` | 详情 DataSet，可拆 related DataSet；数组区块使用 Table | 缺接口时只输出只读结构和待确认读取协议 |
| `modal` / `drawer` | 项目 `Modal.open({ ... })` / `Modal.open({ drawer: true, resizable: true, ... })` / confirmed wrapper + DataSet + Form 候选 | 弹层表单 DataSet，提交/关闭生命周期待确认 | 缺生命周期和接口时不写 submit/onOk 协议；必须记录 overlay 层级规则 |
| `treeList` | `DataSet tree + Table` | 确认 idField/parentField/childrenField 后建模 | 不从视觉树形推导字段名和加载协议 |
| `uploadImport` | `Attachment/Upload + Table/Result` | 附件或导入结果 DataSet 视协议确认 | 不写 bucket、UUID、action、templateCode |
| `componentShowcase` | 组件映射表，不生成业务页面 | 无业务 DataSet；沉淀组件/状态/变体候选 | 只输出组件候选和事实边界 |

## 输出结构
```md
## Choerodon 映射结论
- 页面类型：
- 推荐模式：
- 是否可生成代码：可生成 / 仅映射说明 / 暂停补契约

## DataSet 划分
- 主 DataSet：
- 明细/列表 DataSet：
- 查询 DataSet 或 queryFields：
- 弹层/上传/树/关联 DataSet：

## UI Contract Seeds
| PageSchema 区域 | 推荐 Choerodon 候选 | layoutAuthority | businessAuthority | conflictResolution | 必须规则 | 禁止反模式 | 下游 owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| filterBar | DataSet + Table + filterBar | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / figma-layout-business-covered / needs-question | QueryFields Schema、queryFieldsLimit、关键字搜索候选 fuzzyQuery、enumProvenance 决定 `TableQueryBarType.filterBar` | 手写查询 Form、无来源查询字段、裸写 queryBar 字符串 | frontend-design-agent |
| table | Table columns | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / figma-layout-business-covered / needs-question | 操作列最后一列，`ColumnLock.right`，字段顺序映射 | `lock: true` / `lock: 'right'`、随机列宽、无来源字段 | frontend-design-agent |
| detail | Form + Output / Table | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / figma-layout-business-covered / needs-question | 只读字段用 Output，数组区块用 Table | div/grid 手写详情、无依据摘要头 | frontend-design-agent |
| modal/drawer/overlay | 项目 Modal.open 或封装候选 | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / figma-layout-business-covered / blocked | mask、z-index、portal、不透明背景、关闭后无遮挡 | 自绘 Drawer/Modal、层级穿透、effect 反复打开 | frontend-design-agent |
| mock/demo | DataSet transport.read mock-request 候选 | not-applicable | user-confirmed / fds-tds-api / missing | none / needs-question / blocked | 当前前端服务 origin、Network 可见请求 | service/mock + loadData 伪装 mock-request | frontend-design-agent |

## 组件映射
| PageSchema 区域 | Figma 证据 | Choerodon 候选 | 证据状态 | 待确认 |
| --- | --- | --- | --- | --- |
| header |  | Button / Tabs / Breadcrumb |  | 权限、动作、路由 |
| filterBar |  | queryFields / queryDataSet / filterBar / fuzzyQuery 候选 / enumProvenance |  | 参数名、类型、接口、queryFieldsLimit、TableQueryBarType import 来源 |
| form |  | Form + TextField/Select/Lov/DatePicker/Attachment |  | 字段名、校验、值域 |
| table |  | Table columns / row actions / selection / pagination / lock='right' 操作列候选 |  | 列字段、分页、排序、行操作 |
| detail |  | Form + Output / related Table |  | 详情接口、字段分组、数组字段来源 |
| modal/drawer/overlay |  | 项目 Modal.open({ ... }) / Modal.open({ drawer: true, resizable: true, ... }) / confirmed wrapper 候选 |  | 打开来源、提交、关闭、层级验证 |
```

## 生成边界
可生成：
1. 已确认字段的 DataSet `fields`。
2. 已确认查询参数的 `queryFields`。
3. 已确认列字段的 Table `columns`。
4. 可追溯到 PageSchema 的组件映射建议。
5. UI Contract seeds 和禁止反模式清单。

暂不生成：
1. 未确认 `transport.read/create/update/destroy/submit`。
2. 未确认 URL/method、service 函数、adapter。
3. 未确认 `lovCode`、`lookupCode`、`bind`、Attachment bucket/UUID。
4. 从 Figma 占位文案推导出的字段名、权限 action 和 i18n key。
5. 未经 `frontend-design-agent` 契约化且缺少项目源码或 C7N validator 证据的组件 props、事件、默认值和 Modal 生命周期。

## componentShowcase 输出
当 PageSchema 类型为 `componentShowcase`：
1. 输出组件映射表：Figma 组件/实例 → Choerodon 候选 → 需确认事实。
2. 输出可沉淀到 `references/component-mapping.md` 的状态/变体。
3. 不生成业务页面代码、DataSet `fields`、`transport` 或权限动作。
4. 若用户要实现组件文档页，只生成展示页骨架，并明确它不是业务页面。

## 交接到 choerodon-ui
后续由 `front-hzero-choerodon-ui` skill 确认：
1. DataSet API、Field 配置和提交/查询协议。
2. Form/Table/queryBar/filterBar/DynamicFilterBar 具体用法。
3. Lov/Select/Attachment/Upload/ModalProvider/Drawer 的组件 API。
4. 项目已有 Choerodon 页面模式和验证命令。

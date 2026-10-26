# Choerodon 查询列表

用于包含搜索、分页和表格的列表页。

## 最小形态
- `DataSet` 负责 `queryFields` 和 `fields`。
- `Table` 绑定到该 `DataSet`。
- 普通管理列表默认使用 Table filterBar 查询形态；`queryBar` 代码按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态。UI Contract / FDS/TDS / 用户确认明确要求非 filterBar 模式时可偏离默认语义，但必须记录 mode、sourceRef、reason，且代码仍使用 enum。无项目证据时优先查 `references/enum-map.md` 并使用 fallback enum，不得默认裸写 `queryBar="filterBar"`。
- 优先使用 DataSet `transport.read` 作为唯一查询来源。`queryBarProps` 可以定制行为，但不能成为唯一加载数据的位置。
- HZERO 页面场景必须已经从上游 HZERO/design handoff 中确认目标模块、route/menu 入口、页面容器、权限边界和 i18n namespace。

## 标准 HZERO + Choerodon 列表流程
在 route 和契约已确认后，普通管理/列表页使用此流程：
- Directory: page code under confirmed parent app `src/pages/<page-kebab>/` or micro package `packages/<module>/src/pages/<page-kebab>/`.
- Page files: `index.tsx` for page shell/table actions, `dataset.ts` for DataSet fields/queryFields/transport, `service.ts` for confirmed API calls, `style.less` only for page-local style.
- Route/menu: route path and menu path come from HZERO design or route config; do not derive them from page title.
- Permissions: toolbar and row actions use confirmed permission codes or design-stage `generatedCandidate` codes. Missing permission codes remain 待确认; do not invent slash-style codes such as `/sample/purchase-request/button.create`.
- Query: DataSet `queryFields` own query model; Table filterBar renders and triggers query; generated code uses `TableQueryBarType.filterBar`; custom query/reset must go through DataSet query/reset path. Non-filterBar query modes require explicit design/UI Contract evidence and still use `TableQueryBarType.*`.
- Initial query: ordinary query/list pages default ListDS `autoQuery=true` so the first page load triggers `transport.read` automatically. Use `autoQuery=false` only when the page must first obtain default query conditions, tenant/permission context, route/search-derived params, external selection, or custom settings; then trigger `listDs.query()` from `useEffect`, ListHeader owner action, or a confirmed project hook after those conditions are ready.
- QueryFields Schema: each query field records field name, label, component type, multiple/clearable/default, options source, and submitted query value.
- Fuzzy query: if FDS/TDS mentions keyword/fuzzy search, enable `queryBarProps.fuzzyQuery` and use `queryBarProps.fuzzyQueryPlaceholder` for confirmed placeholder copy, or record project evidence that it is unsupported. Do not put `fuzzyQueryField` / `fuzzyQueryFields` inside `queryBarProps`; field mapping belongs to QueryDS/queryFields and UI Contract `fuzzyQueryFields`.
- Query layout: record `queryFieldsLimit`, default visible query fields and more-filter fields; use `3` only as conservative default when no design/project standard is confirmed.
- Table: columns prefer `{ name: confirmedField }`; custom `renderer` stays lightweight and must not perform business requests.
- Table toolbar: when FDS/TDS/UI Contract names 列表头按钮区、表格工具栏 or 批量按钮区, put add/save/delete/remove/reset/export/batch actions in Table `buttons` or a confirmed project Table wrapper. Do not replace the built-in Table toolbar with an external custom toolbar unless project evidence requires it.
- Operation column: must be the last column, right locked with `ColumnLock.right` or a project-confirmed equivalent enum; when a Choerodon Pro Table row has multiple actions, render through the HZERO helper confirmed by `front-hzero-renderer`; do not return a raw Fragment/list of buttons directly from `renderer`.
- DataSet transport: `transport.read` returns request config directly after URL, method, params, pagination and response shape are confirmed; do not import or call business service from the DataSet file.
- State: loading/empty/error behavior follows project Table/DataSet conventions; do not duplicate loading with unrelated local state unless project wrapper requires it.

## Non-runnable 骨架
- DataSet：`primaryKey` 待确认，`queryFields` 待确认，展示字段待确认。
- Table：绑定 `dataSet`，按 enumProvenance 使用 filterBar 查询形态，列按已确认字段名声明。
- Transport：待确认，暂不配置。

## 护栏规则
- 缺失字段应保留为待确认项。
- 不要编造 `transport.read`、URL/method 占位或 service helper；列表 DataSet 请求不要通过业务 service 包一层。
- 除非项目证据确认，否则不要把业务名词直接转成字段。
- 不要通过通读所有同级页面来推断业务字段；最多只读一两个同模块页面确认风格与文件职责。
- 对于意图建模真实查询行为的页面，不要把本地 mock 过滤与 DataSet query 混成唯一数据源。
- 普通查询列表不要无理由设置 `autoQuery=false`；若因前置条件或自定义设置需要关闭自动首查，必须保留明确的主动 `dataSet.query()` 入口和验证证据。
- 表格工具栏动作默认进入 Table `buttons`；不要把 Table 外手写 toolbar 当作列表头按钮区的默认实现。若项目统一封装要求外置 toolbar，必须记录封装证据以及它如何承接 DataSet 新增、保存、删除、选择态、禁用态、校验和导出链路。
- 对于 HZERO + Choerodon 页面，操作列包含 2 个及以上动作时必须设计为 `front-hzero-renderer` 已确认的 helper 方案；若不能使用，必须说明项目缺少 helper、路径未确认或只有单一动作的降级原因。
- 列表字段顺序和 label 必须追溯 FDS/TDS/UI Contract；无来源字段不得展示，确需展示时标记 `generatedCandidate`。
- 查询必须回到第一页；刷新保留当前页；重置清空查询条件并回到第一页。项目封装已有行为时记录证据。

## 验证
- 编码阶段：优先使用可用的 LSP/typecheck/lint 和 dev server/HMR/browser 检查。
- 最终交付：运行或报告来自设计元数据或项目 scripts 的目标最终 build/compile 命令。
- 验证查询、重置、分页、空状态、错误反馈以及 console/network 错误；有行操作契约时再验证行操作可见性/权限。
- 验证首屏自动查询：普通列表应能在页面加载后看到 DataSet `transport.read` Network 请求；`autoQuery=false` 场景必须证明前置条件就绪后主动触发了 `dataSet.query()`。
- 验证 Table 工具栏按钮来自 Table `buttons` / 项目等价封装，且需求动作逐项可见、可用或有明确禁用原因。
- 首屏 smoke：页面加载后必须能看到 Table DOM、数据行或明确空态、分页；有行操作契约且当前状态存在可见动作时再要求操作列可见。首屏空白或详情/业务弹层覆盖列表为 blocking。
- UI against design：实现后回读 UI Contract，检查筛选字段、列表字段顺序、操作列、详情入口和交互行为。
- 单元测试按风险决定；对于协议适配、查询参数转换、权限 helper 或可复用列/render 逻辑，应运行或补充测试。

## Runnable mock/demo 列表规则
- 新增或改造可运行列表页在缺少生产可达契约时默认适用 mock requests/API mock/data mock；前提是已提供或项目可定位到当前 feature 的 FDS/TDS/MDS/FSS、Swagger、API JSON、DTO、测试数据等字段/API 证据，可形成可请求 mock 数据契约。
- 列表/查询型可运行 mock demo 必须选择 `mock-request`。mock 数据必须由 HZERO 本地 devServer middleware 暴露的 HTTP mock API 返回，并让 DataSet `transport.read` 请求该 API；不得退回纯内存 `local-filter`。
- HZERO mock/demo URL 默认使用 `/_mock/<module>/v1/{organizationId}/...` 独立命名空间，并命中当前 dev server origin；不得使用 `<unconfirmed-gateway-prefix>` 伪装 mock，不得使用 `/api/v1/demo-org` 或硬编码 `demo-org`。
- 微前端子模块由父工程托管时，mock plugin/handler 应归属子模块，但必须被父工程配置显式注册或被父工程聚合 plugin 引用；只在子模块 package 配置里注册不能证明 mock-request 可用。
- 即使后端资产示例为空，也应基于已确认字段和响应结构生成最小可用 mock API response；不要退回成纯内存 mock。
- mock 记录应放在 devServer mock API 背后的 dev-only runtime store 或 route handler 中，而不是只放在模块内存数组里。
- 列表 DataSet `transport.read` 应接到 mock API；若 raw response 已是 DataSet 可消费的 `{ content, totalElements }`、`{ rows, total }` 或数组形态，可通过 `dataKey/totalKey` 直接消费；否则通过 `transformResponse`、adapter 或项目 helper 归一化。筛选应使用来自 FDS/TDS/MDS/FSS/API 契约中已确认的 query fields。
- 不要只用 `useEffect + loadData` 取代 DataSet 查询；Table 的 query、reset、refresh 和 pagination 都会调用 `dataSet.query()`，仍必须请求 mock 数据源。
- 禁止使用 `data:application/json` 作为 DataSet mock URL；详见 `dataset-mock-transport.md`。

## 查询模式模板
| mode | 适用场景 | 必须说明 | 禁止 |
| --- | --- | --- | --- |
| `mock-request` | HZERO 本地 devServer middleware 暴露 mock API | mock API mount、响应 shape、query adapter、pagination、Network URL/method/query/body | 空 transport、data URL、service/mock + loadData 冒充 mock-request |
| `blocked-local-filter` | 发现 local-filter、inline mock、模块内存数组、组件内 seed/filter、`service/mock + loadData` | blocking cleanup/rework、清除后改为 mock-request 或 production-transport | 冒充 mock-request/真实接口、作为新生成列表 mock 策略或降级分支保留 |
| `production-transport` | API 契约 confirmed | URL/method/payload/response、错误处理 | 未确认 URL/method |

列表查询实现必须让 query/reset/refresh/pagination 走同一链路；不能让按钮查询、DataSet query 和 Table 展示各自读不同数据源。

## 批量选择
- 批量删除、批量提交、批量导出等操作必须把 `selectedRecords` 兜底为 `[]`。
- 空选时应提示或 no-op，不得读取 undefined 后崩溃。

## 本地 options 和未确认 LOV/lookup
- 未确认 `lovCode` / `lookupCode` 前，Select 和必填枚举字段使用本地 `options`。
- 本地 options 必须与 mock 数据字段值一致，避免展示/保存漂移。
- 本地 mock/demo options 常量统一命名为 `MOCK_*_OPTIONS` 或 `DEMO_*_OPTIONS`，并在生产替换清单中标记替换为真实 LOV/lookup/值集。
- 后续接入真实 LOV/lookup 时，把本地 options 写入 production replacement checklist。

## 空 transport 使用场景
- 允许：非页面交付的只读说明片段，且不包含运行态列表、查询、分页、重置、刷新或业务数据成功路径。
- 禁止：用户明确内存演示、空 `transport` 但声称已完成真实查询、按钮查询、DataSet query、Table 展示各走不同数据源、缺少 query/reset/refresh 说明、直接把本地 `PageResponse` 接入 DataSet `transport.read` 冒充真实 API；命中时必须 blocking cleanup/rework。

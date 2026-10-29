# Data / Service Runtime Gates

用途：承接 `front-hzero-enterprise-design` 中已冻结的 `serviceRequestContract`、`tenantContext` 和 `Route Context / Edit Mode Contract`，用于 Task、Implementation、Review、Verification 和 mock-to-production replacement。

## Tenant Context Runtime

- Task Breakdown 必须把 tenantContext 写入每个涉及 API、附件、导入导出、LOV/lookup 或 production replacement 的任务验收。
- Implementation 只能使用设计/任务中的 tenantContext 来源。
- 若找不到项目 helper 或无法确认 alias/export，只能返回阻塞或回到 Frontend Design；若仅缺工程 helper 证据，写 `deltaExploreReason=open-item-requested` + `targetedDeltaScope=other` 做 targeted evidence backfill。不得自行读 store、硬编码路径、创建本地 resolver 或引入默认租户常量。
- mock 切真实 API 时必须同时关闭或保留 tenant/organizationId 替换项。
- Review 必须检查 DataSet/service URL 是否来自确认的 request helper、`getPlatformVersionApi` 或 `getCurrentOrganizationId()` 策略。
- 本轮新增的 `getOrganizationId/getTenantId/resolveOrganizationId/resolveTenantId` 或默认租户常量用于租户级 API path 时，必须 blocking。
- 误用 `getUserOrganizationId()` / `currentUser.organizationId` 拼租户级路径、重复拼接租户路径、tenantContext 缺失却声明 production-ready，至少 major；影响真实 API 租户时 blocking。

## Request / Service Runtime

- production service / DataSet transport 必须使用已确认 request helper 或 request adapter。
- 未经确认不得出现原生 `axios/fetch/XMLHttpRequest` production transport。
- 不得新造本地 request base resolver 替代项目 request/env/helper 契约。
- `API_HOST` 必须按 baseUrlStrategy 使用；HZERO request 内置 API_HOST 时不得重复拼接。
- 真实请求 URL 必须包含已确认服务前缀、baseUrlStrategy、envSource 和路径参数来源；不能只做占位符字符串替换后声明 production transport 已闭合。
- API/MDS/Swagger 中的 `/v1/{organizationId}/...` 只能作为 `resourcePath`；production service 必须拼接已确认 `servicePrefix`，例如 `/<servicePrefix>/v1/{organizationId}/...`。只保留 `/v1/...` 或把 `<unconfirmed-gateway-prefix>` 当成真实服务前缀，至少 major；声明 production-ready 时 blocking。
- servicePrefix 来源必须可追溯：项目公共配置/env helper、相似 service、用户确认或后端服务编码候选。只有后端服务编码推导出的 `/hspd` 等候选只能标 `generatedCandidate`，不得单独支撑 production-ready。
- mock/demo 与真实 API 双链路必须通过模块级开关显式分流：默认 mock，只有 `<MODULE>_USE_MOCK=false` 精确字符串切真实；DataSet transport 和页面 action service 必须共用同一 baseUrl 派生，但 DataSet transport 不得通过业务 service 发起请求。
- 不得假设存在公共包；只有工程无公共配置时，才允许在业务包内生成 `src/utils/servicePrefix.ts` 作为过渡。若项目已有公共配置却重复造本地 helper，或依赖不存在的 common 包，至少 major。
- 生产目标 service 不得出现模块级 `runtimeStore`、前端内存分页/过滤/保存/删除/状态流转、`window.location.origin + '/mock-data'` 或原生 `fetch` 静态 seed 作为成功路径。若为 mock/demo，必须声明 `queryMode=mock-request`、`mockApiMode=hzero-dev-server-middleware`、devServer middleware/plugin 注册计划、替换清单和 handoff 限制；本地内存、inline mock、`src/utils/mock.ts` 或 local-filter 成功路径必须 cleanup/rework blocked，不得作为降级分支保留。
- 可编辑详情、主从、流程页必须继承 Design 的 DataSet/service 契约：DataSet 管理的 read/create/update/destroy/submit 必须收敛在 DataSet `transport`，transport 默认返回 request config；页面级提交、撤回、作废、复制、导出等非 DataSet 生命周期动作才使用 service action。仅 `queryDetail + loadData` 或页面层手工拼 payload 不能作为 production-ready 依据。
- 每个运行态动作必须只有一个权威数据入口：`DataSet transport`、`service action` 或 `confirmed hybrid wrapper`。这里的 `confirmed hybrid wrapper` 只能表示 DataSet transport 与页面 service action 共享不发请求的 URL/query/payload/response helper 或同一个项目 request adapter；不得表示 DataSet `transport.*` 委托业务 service 函数。DataSet `transport.read/create/update/destroy/submit` 不得 import 或调用业务 service 函数；相似页面中的 `transport.read: () => service.query()` 只能作为 legacy signal，不得作为新代码默认范式，也无需为该判断额外探索前端工程。若 HeaderDS/LineDS 定义了 `transport.submit/create/update/destroy`，页面保存按钮默认必须调用对应 DataSet submit；若页面保存改走 service 手工保存，则设计/任务必须声明 `runtimeDataEntry.owner=service-action`，并移除或禁用 DataSet submit。DataSet submit 与页面 service 同时存在但无法证明其中一个退出运行入口，或 URL、method、payload builder、response adapter、mock handler、runtime store 任一不一致，按 `HZC-DATA-ENTRY-DRIFT-001`；声明 production-ready 或 usable=true 时 blocking。
- 详情/编辑页 DataSet read 的主身份来源必须与 Route Context 一致：path id 进入 `create*DetailDS(id, auxiliaryQuery)` 闭包、`queryParameter/setQueryParameter` 或 confirmed wrapper 后再由 `transport.read` 拼 path。不得依赖 `detailDs.read({ id })`、`ds.read({ xxxId, navigationToken })` 等对象作为第一个参数注入业务 data；Choerodon 会把第一个参数按 page 语义处理。若 `transport.read` 用 `data.xxxId || ''` 拼详情 path，且该 data 只来自页面手动 `read({ xxxId })`，按 `GCSQ-DATASET-READ-001`；导致 `/resource//detail`、`/resource/undefined/detail`、mock/API 路由不匹配或详情无数据时 blocking。
- Header/Line 主从保存必须在同一个 contract 中说明保存粒度：header-only / header-with-lines / line-batch / line-inline / status-action。HeaderDS submit、LineDS submit、页面 service save、mock route handler 必须共享同一 payload assembler 或同源字段映射；不得让 DataSet 契约、service 契约和 mock 契约各自维护一套 header/line 字段。
- 保存、删除、提交、撤回、作废等 action 必须在函数入口二次校验状态和必要的业务条件；按钮 hidden/disabled 不能替代运行时 guard。
- 状态动作必须使用状态 code 字段，不得使用 `statusMeaning`、`authorizationStatusMeaning` 等展示字段进行判断。

## Route Context Runtime

- 页面组件不得直接依赖 `window.location.hash.includes('editFlag=true')`、hash 正则或散落读取 `location.search`、`window.location.hash`、`params.xxx` 判断业务状态。
- 详情、新建、编辑、复制页面必须优先使用 `useLocation()` 和 `useParams()`，从 path params 派生页面主身份，再通过页面级或模块级 helper 统一封装为 `getRouteContext(location, params)`。
- `getRouteContext(location, params)` 至少返回 `id`、`isCreate`、`pageMode`、`editable`；复杂页面可额外返回 `rawSearch`、`source`、`returnTo`、`activeTab`、`navigationToken` 或 `queryStateKey`。不得生成或读取 `editFlag/mode/action` query 决定 `pageMode`。
- `/create` 必须默认 `isCreate=true`、`editable=true`、`pageMode=create`；`?editFlag=true` 命中时必须迁移。新建路由固定 `/create`，`/detail/create` 属于违规路径，发现后迁移。
- URL 参数解析使用 `URLSearchParams` 或项目已确认等价 wrapper。`editFlag/mode/action` query 不得表达页面身份或 pageMode；存量链接必须迁移到 canonical path。
- 新生成列表入口、openTab 调用和保存后跳转不得主动 emit `?editFlag=true/false`、`?mode=edit/view` 或 `?action=create` 来表达页面模式；必须跳转到内置 `/create`、`/detail/view/:id`、`/detail/edit/:id`。
- route params、query、state 或 openTab search/state 中的 ID-like 参数必须继承 `frontend-id-runtime-contract.md`：前端运行时按 string 传递，不得强制 `Number(id)`。
- 页面是否可编辑以 `routeContext` 派生结果、UI Contract 和业务状态守卫为准；DataSet 字段中的 `editFlag` 只能作为展示、提交或后端字段，不得反向覆盖页面编辑态。
- 保存、新建转详情或复制转编辑后的跳转必须按 `saveRedirectPolicy` 保留或切换 path 中的 `pageMode`；query 只能保留来源、返回、详情内子 Tab、navigationToken 等辅助状态。
- 切换不同 id、刷新详情页或动态 Tab 复用组件时，异步加载状态必须绑定当前 id，避免旧记录编辑态复用。

## Route Context Review / Verification

Review 命中以下情况至少 major，影响新建、编辑、保存或详情可用时 blocking：

- 使用 hash includes、hash 正则或散落解析方式判断 `editFlag`、`isCreate`、`pageMode`。
- 新生成入口或跳转 URL 使用 `?editFlag=true/false`、`?mode=edit/view`、`?action=create` 表达页面模式、详情 ID 或 Tab 唯一性。
- `/create` 打开后不是默认编辑态，或实现仍使用 `/detail/create`。
- DataSet 中的 `editFlag` 被当作 UI 编辑态权威来源。
- 保存后应保持编辑态但跳转丢失编辑 path/pageMode，或应进入只读详情却无来源地继续编辑。
- 路由 id 变化后旧记录状态可短暂放行保存、提交、取消或删除。
- route/query/path ID 被 `Number()`、`parseInt()` 或一元 `+` 强转，导致加密 ID 或 Long ID 丢失。

Verification 或 runtime/manual checklist 至少覆盖：

- 列表点击编辑进入编辑态。
- 直接刷新编辑 path/pageMode 的详情 URL 后编辑态符合预期。
- `/create` 不带 query 也默认新建可编辑；`/detail/create` 不得作为验收路径。
- 保存后跳转是否按 `saveRedirectPolicy` 保留或切换编辑 path/pageMode。
- 切换不同 id 或不同 Tab 时不复用旧记录编辑态。

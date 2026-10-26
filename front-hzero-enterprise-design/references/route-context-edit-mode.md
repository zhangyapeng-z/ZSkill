# Route Context / Edit Mode Contract

本文用于沉淀 HZERO / Umi / Choerodon 页面中的路由参数解析、页面模式和编辑态控制规则，避免详情、新建、编辑、复制页面因为 hash/search 解析差异导致编辑态丢失或状态误判。

## 适用范围

- 新建、编辑、复制、详情、审批、只读和 mixed 表单页面。
- 列表进入详情、详情刷新、保存后跳转、同一路由切换不同记录、动态 Tab 或 HZERO openTab 场景。
- 任何通过 URL 参数、route params、query、state 或 DataSet 字段判断页面业务状态的实现。

不适用于纯静态展示页、无路由参数的局部组件或只处理外链 URL 的逻辑。

## 设计期必填契约

UI Contract 或 Frontend Design 必须声明 `Route Context / Edit Mode Contract`：

| 字段 | 说明 |
| --- | --- |
| routePattern | 目标 route path，必须按内置规范使用 `/<module>/requisition/create`、`/<module>/requisition/detail/view/:id`、`/<module>/requisition/detail/edit/:id`；`/<module>/requisition/detail/create` 属于违规路径，发现后迁移到 create path；固定复用页签可为 `/<module>/requisition/detail` |
| idSource | `useParams()` / path params / confirmed tab context / navigation state / sessionStorage fallback / project wrapper / not-applicable；非 create 默认必须能从 path params 得到记录 id；只有 `routeOpenMode=hzero-openTab-reusable-fixed-path` 已确认时，才允许记录 id 来自 confirmed tab context / navigation state / sessionStorage fallback / project wrapper |
| isCreateSource | `/create` 路径或 not-applicable；新生成代码不得用显式 query 或 `/detail/create` 判断 create |
| editableDerivation | path pageMode + 用户动作 + 状态守卫 / not-applicable；不得生成或读取 route/query `editFlag` |
| pageModeDerivation | 从 path 中的 create / edit / copy / view / detail / approval / readonly 派生；固定复用详情页签可从 confirmed tab context / navigation state / sessionStorage fallback / project wrapper 派生 edit/view；不得用 `?editFlag=true/false`、`?mode=edit/view` 或 `?action=create` 作为新生成页面模式 |
| queryParser | `URLSearchParams` / 项目等价 wrapper；不得直接正则匹配 hash |
| editableAuthority | UI 可编辑性的权威来源，默认 `routeContext + UI Contract + business status guard` |
| dataSetEditFlagUsage | DataSet 中的 `editFlag` 是否只是展示/提交字段；不得作为 UI 编辑态权威来源 |
| saveRedirectPolicy | 保存后切换或保留 path 中的 pageMode，例如进入 `/detail/view/:id` 或保留 `/detail/edit/:id` |
| reusableTabContextPolicy | 固定详情复用页签时必填：context 写入来源、刷新/聚焦更新机制、缺 context 的刷新降级行为、tab 标题同步策略；其它场景 not-applicable |
| status | confirmed / generatedCandidate / missing / conflict / not-applicable |

## 降级和阻塞

- 目标项目没有 `useLocation/useParams` 但存在项目路由 wrapper 时，允许使用项目 wrapper，必须记录 evidence。
- 只有外链、静态页面或无业务状态的页面可写 `not-applicable + reason`。
- 缺少 routePattern、idSource、pageModeDerivation 或 editableAuthority 时，新建/编辑/详情任务不得进入 runnable implementation，应回 Frontend Design / Task Breakdown 补齐。
- 若设计要求 HZERO openTab、dynamic Tab 或同 route 多实例，还必须同时闭合 `routeOpenMode`、`tabTitle`、`dws/queryStateKey`；Route Context 不能替代 routeOpenMode 契约。`routeOpenMode=hzero-openTab-reusable-fixed-path` 还必须闭合 `reusableTabContextPolicy`。
- 新生成详情/编辑/新建页面必须用内置 route path 表达页面身份：新建 `/create`，查看/编辑 `/detail/view/:id`、`/detail/edit/:id`。`/detail/create` 属于违规路径，发现后迁移到 `/create`。`editFlag` 可以由 `pageMode` 派生给页面内部或 DataSet 使用，但不得反过来作为 UI 编辑态、Tab 唯一性或 route 身份来源。
- 历史 query 链接兼容不属于页面生成合同。迁移任务必须先把旧入口改写到 canonical path，不能在新页面保留双解析分支。
- 固定 path 复用详情页签是受控例外：只有 `routeOpenMode=hzero-openTab-reusable-fixed-path` 已由用户确认或运行态证据确认时，view/edit 记录 id 和 pageMode 才可不进入 URL path。该例外必须明确 create 独立固定 path、detail 固定 path、context 来源、刷新缺 context 行为、标题同步和保存后跳转；否则仍按 path params 范式处理。

## Runtime Handoff

Task、Implementation、Review 和 Verification 必须继承本设计契约；实现规则、Review 拒收项和 browser/manual checklist 集中在 `front-hzero-enterprise-process-control` 的 data-service runtime gates。

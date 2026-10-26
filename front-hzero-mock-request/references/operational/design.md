# Mock Request - 设计与契约

## 阅读路由
- Mock Request 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 职责边界
- 不负责完整 Frontend Design、UI Contract、路由菜单、权限、i18n、LOV/lookup、附件、导入导出设计；这些仍归属 `front-hzero-enterprise-design` 和对应领域 skill。
- 不负责完整 Task/Implementation/Review/Verification/Handoff 编排；执行期流程仍归属 `front-hzero-enterprise-process-control`，但 mock-request 规则以本 skill 为事实源。
- 不提供多套 mock 方案选择。标准 mock-request 只有一种：HZERO 本地开发服务器上的 HTTP mock API。

## Question Gates
- 关键生产契约缺失且用户未要求真实 API 联调 / production-ready 时，默认进入 `mock-request` / `demo-slice`，并记录 `mockDemoDecisionStatus=default-mock-demo`、`runtimeDataPathDecision=requestable-demo-mock`、production replacement 清单和 demo 交付上限。不得为默认 mock/demo 单独请求确认。
- 用户明确要求真实 API 联调 / production-ready 或拒绝 Mock 时，当前企业前端编排仍固定进入 `mock-request`，并把真实诉求写入后续独立集成与稳定化 advisory。只有 mock-request 的 devServer/request/plugin 接线、当前 Mock 必需契约或写入范围无法自动闭合时，才返回 `questionGate.required=true`、`template=Missing Contract Confirm` 或对应工程接线 gate、`resolved=false`，交给 frontend-auto / Lite 统一处理。
- 用户要求切真实 API，但 `backendApiReadiness` 不是 `closed`、只闭合部分 API、替换范围影响页面结构/权限/平台协议，或验证口径不清时，不得直接实现 production transport。必须返回 `questionGate.required=true`、`template=Production Replacement Confirm`、`resolved=false`，并保留 `pendingReplacementItems`。
- 已存在未解决 `questionGate` 或 `questionGateQueue` 时，Task、Implementation、Review、Verification 和 Handoff 都不得把结果推进为 `usable=true`、`production-ready` 或 DONE。

## 职责范围
- 需要设计或检查 `queryMode=mock-request`、默认 mock/demo 决策、Mock API Contract 或可请求 mock demo。
- 需要生成或审查 `/_mock/<module>/v1/{organizationId}/...`、devServer middleware、父工程 mock plugin、runtime store 或 mock handler。
- 需要规范 mock/production 双链路 prefix helper、`<MODULE>_USE_MOCK !== 'false'` 默认 mock 语义、静态 env 注入和 service/DataSet baseUrl 派生。
- 需要判断 mock demo 的 `reachable/usable` 是否已由运行态证据闭合，或从 mock-request / partial 切到真实 `production-transport`；发现 local-filter / inline mock 时只能进入 blocking cleanup/rework。

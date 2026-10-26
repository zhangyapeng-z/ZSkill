# Frontend Runtime Acceptance Control

本文定义普通 Verification 之外的最小页面运行态验收。它只在成功标准要求页面真实可达/可用、核心演示路径闭合、`reachable/usable=true`、production-ready 或完整验收时成为 Handoff 前置门禁；默认 demo-slice 未要求运行态闭合时可 `not-required`，并保留 `reachable/usable=unknown`。

是否 required 只取决于用户明确交付目标或已确认 acceptance，不取决于“页面存在”“已有 dev server”“缺截图/Network 证据”或流程希望获得更完整证据。未明确要求时固定走 `required=false + status=not-required/not-run + conditional`，不得为了补运行态证据暂停前后端编码、回普通 Verification 或询问用户是否接受。

## Boundary

- `frontend-verify-agent` 不启动 dev server、不打开浏览器，也不把 HTTP 200、mock JSON、build 或静态 validator 当成页面可用证据。
- Runtime Acceptance 由主流程安排的外部浏览器验收、独立专项执行环境或用户手工证据提供。服务启动诊断可由 build/start 专项处理，但服务启动本身不等于验收通过。
- 证据必须写入 `verification.runtimeAcceptance`，并引用按 `templates/runtime-acceptance.md` 形成的 artifact 或等价结构化记录。
- 本资产不内置浏览器执行器。即使已有可访问服务、route 和稳定 locator，也只能消费外部专项验收或用户手工证据；不得由普通 Verification 或优化工具 manifest 伪造运行态通过。

## Required Checks

每个适用检查必须使用 `passed / failed / not-run / not-applicable`：

1. `routeLoad`：目标 route 可打开，无 404、白屏或阻塞型 runtime error。
2. `primaryRender`：当前页面核心区域真实渲染。列表页必须同时记录 Network 返回记录数和 Table 实际行数；详情页记录目标实体和关键字段渲染。
3. `responseConsumerShape`：外部响应的 bare-array、bare-object、page-response、data-envelope 或 project-adapter 与 DataSet/service 消费端一致。只有 HTTP 200 或非空 JSON 不算通过。
4. `requiredInteractions`：只验证本轮 required 的查询/重置/分页、LOV、create/edit/load/save/cancel、状态动作、导入导出等；非本轮能力写 not-applicable。
5. `runtimeErrors`：console、unhandled rejection、关键 Network 失败和组件 runtime error 无 blocking 项。

## Progression

- 全部 required checks passed：可结合 Review、Verification 和交付目标判断 `reachable/usable`；Runtime Acceptance 本身不推导 production-ready。
- 任一 required check failed：记录失败断言、页面路径、输入、期望/实际、截图或日志路径，回 Implementation；修复后只复跑失败项及受影响项。
- required 但 missing/not-run：Handoff 只能 conditional/blocked，`reachable/usable=unknown`，不得回普通 Verification 启动服务补跑。
- 仅当用户已明确要求本轮闭合 runnable/production-ready/完整验收，且继续需要账号、环境、外部权限或用户手工输入时，才允许进入用户等待；否则直接保留 conditional 和 manual checklist。
- response 有数据但 UI 未渲染时，优先检查 DataSet/service adapter、`dataKey/totalKey`、response unwrap、字段名和 row key，不得以接口 200 关闭问题。

## Result Contract

`verification.runtimeAcceptance` 至少包含：

```yaml
required: true | false
status: passed | failed | not-run | not-required
source: external-browser-run | user-manual-evidence | external-specialty | not-applicable
evidencePath: <path | null + reason>
scopeFingerprint: sha256:<changedFiles + routes + checks>
routeLoad: { status, evidence }
primaryRender: { status, networkRecordCount, renderedRecordCount, evidence }
responseConsumerShape: { status, producerShape, consumerShape, evidence }
requiredInteractions: [{ id, status, evidence }]
runtimeErrors: { status, evidence }
failedAssertions: []
```

页面运行态观察不能跨 changedFiles 或 route 变化复用为 passed；指纹变化后只复用 checklist，不复用通过结论。

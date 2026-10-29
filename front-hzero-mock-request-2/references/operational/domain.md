# Mock Request - 领域细节

## 阅读路由
- Mock Request 其它不归入阶段的领域细节、交叉引用或 proof 结构命中时读取。

## References
- `references/design-contract.md`：Frontend Design / Contract Check 阶段的 Mock API Contract。
- `references/runtime-gate.md`：Task、Implementation、Review、Verification、Handoff 的 mock-request 运行时门禁。
- `references/mock-runtime-store-example.md`：mock-request runtime store、状态流转和列表/详情同源示例。
- `references/production-switch.md`：从 mock-request / partial 切换到真实 production-transport 的 replacement slice，并清理 local-filter / inline mock 违规。

## Reference Loading Policy
- Design / Contract Check 阶段读 `references/design-contract.md`。
- Task、Implementation、Review、Verification、Handoff 或 mock-demo `reachable/usable` 闭合判定读 `references/runtime-gate.md`。
- 需要生成或审查 runtime store、状态流转 handler、列表/详情同源刷新时，同时读 `references/mock-runtime-store-example.md`。
- 后端 API readiness 已闭合、用户要求切真实接口，或处理 `productionReplacementTrigger` 时读 `references/production-switch.md`。
- 只需要快速判断时先读本文件的 Core Rules；命中具体阶段再读对应 reference。

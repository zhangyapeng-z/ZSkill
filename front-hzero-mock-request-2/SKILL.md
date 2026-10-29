---
name: front-hzero-mock-request
description: 当任务涉及 HZERO 前端 mock-request 时使用，覆盖本地 devServer HTTP mock API、mock/production prefix helper、DataSet/service 请求链路、runtime store、mock-demo 验证事实门禁，以及 mock 切真实 API replacement slice。
---

# HZERO Mock Request Frontend

## Scope
- `front-hzero-mock-request` 是 Mock Request 任务的执行入口，不是完整知识库。
- 先用本文件选择 Mock Request 需要的 reference，再按阶段读取细则。
- Mock Request 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- Mock Request 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 Mock Request 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 Mock Request import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 Mock Request reference 停止、降级或写入 replacement。

## Reference Routing
- Mock Request 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- Mock Request 设计/契约/问题门禁：`references/design-contract.md`、`references/operational/design.md`。
- Mock Request 实现/修复/工程证据/交付替换：`references/operational/implementation.md`。
- Mock Request 其它领域细节：`references/mock-runtime-store-example.md`、`references/operational/domain.md`、`references/production-switch.md`、`references/runtime-gate.md`。
- Mock / production prefix helper 生成模板：`front-hzero-enterprise-process-control` 的 `service-prefix.ts.template` 模板。生成 `src/utils/servicePrefix.ts` 时必须先读该模板并只替换占位符；不得自由拼写 origin helper、mock mount 或 env switch。

## Shared Governance
- Mock Request 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- Mock Request 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- Mock Request 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

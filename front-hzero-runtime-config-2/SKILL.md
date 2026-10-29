---
name: front-hzero-runtime-config
description: 当任务涉及 HZEROJS 运行时配置、app.tsx、routes-config 或 layout 扩展的配置、审查或调试时使用，覆盖 appInit、rootLayoutConfig、innerLayoutWrapper、addLayoutHeaderExtra、addLayoutExtra、layout/header/workbench/user menu/plugin 扩展、request/response 全局拦截、跨系统导航 hook、Choerodon UI configure、ConfigProvider 和局部 wrapper 配置。
---

# HZERO 运行时配置

## Scope
- `front-hzero-runtime-config` 是 运行时配置 任务的执行入口，不是完整知识库。
- 先用本文件选择 运行时配置 需要的 reference，再按阶段读取细则。
- 运行时配置 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 运行时配置 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 运行时配置 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 运行时配置 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 运行时配置 reference 停止、降级或写入 replacement。

## Reference Routing
- 运行时配置 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 运行时配置 设计/契约/问题门禁：`references/operational/design.md`。
- 运行时配置 实现/修复/工程证据：`references/operational/implementation.md`。
- 运行时配置 审查/反模式/合规：`references/operational/review.md`。
- 运行时配置 验证/构建/运行态：`references/operational/verification.md`。
- 运行时配置 其它领域细节：`references/core-utils.md`、`references/layout-extension.md`、`references/patterns.md`、`references/runtime-config-checklist.md`、`references/schema-packets.md`。
- 运行时配置 templates：`templates/layout-extension-design.md`、`templates/runtime-config-design.md`。

## Shared Governance
- 运行时配置 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 运行时配置 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 运行时配置 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

---
name: front-hzero-micro
description: 当任务涉及 HZEROJS 微前端、子模块或远程加载的调试、配置、审查或实现时使用，覆盖 remoteEntry.js、PACKAGE_PUBLIC_URL、packages/microConfig.json、window.mfRemotes、registerRegex、mfExposes、MfComponent、getComponent、qiankun、HZERO federation 边界、跨模块组件/卡片和子模块白屏。layout/header/workbench/user menu/plugin 扩展优先使用 front-hzero-runtime-config。
---

# HZERO 微前端

## Scope
- `front-hzero-micro` 是 微前端 任务的执行入口，不是完整知识库。
- 先用本文件选择 微前端 需要的 reference，再按阶段读取细则。
- 微前端 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 微前端 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 微前端 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 微前端 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 微前端 reference 停止、降级或写入 replacement。

## Reference Routing
- 微前端 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 微前端 设计/契约/问题门禁：`references/operational/design.md`。
- 微前端 实现/修复/工程证据：`references/operational/implementation.md`。
- 微前端 审查/反模式/合规：`references/operational/review.md`。
- 微前端 验证/构建/运行态：`references/operational/verification.md`。
- 微前端 其它领域细节：`references/micro-frontend-checklist.md`、`references/patterns.md`、`references/schema-packets.md`。
- 微前端 templates：`templates/micro-diagnosis.md`。

## Shared Governance
- 微前端 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 微前端 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 微前端 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

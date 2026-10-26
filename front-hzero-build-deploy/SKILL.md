---
name: front-hzero-build-deploy
description: 当任务涉及 HZEROJS 前端构建、编译、启动、产物加载诊断、父模块构建、子模块/微包编译、子模块 dev server/HMR、hzero-build、hzero-start、dist/packages、增量构建、remoteEntry.js、PACKAGE_PUBLIC_URL、microConfig、chunkError 或远程模块加载时使用。运行时联邦消费或组件暴露设计优先使用 front-hzero-micro。
---

# HZERO 前端构建与产物加载

## Scope
- `front-hzero-build-deploy` 是 构建与产物加载 任务的执行入口，不是完整知识库。
- 先用本文件选择 构建与产物加载 需要的 reference，再按阶段读取细则。
- 构建与产物加载 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 构建与产物加载 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Scenario Trigger Map
- `performance`：命中大表、渲染卡顿、首屏/加载慢、chunk/remote 体积、性能审查、性能验证建议、构建产物性能或运行态性能诊断时，必须读取 `references/scenarios/performance.md`；业务页面实现仍回对应阶段 agent，构建产物和验证证据由 build/deploy owner 承接。

## Workflow
1. 将 构建与产物加载 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 构建与产物加载 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 构建与产物加载 reference 停止、降级或写入 replacement。

## Reference Routing
- 构建与产物加载 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 构建与产物加载 设计/契约/问题门禁：`references/operational/design.md`。
- 构建与产物加载 实现/修复/工程证据：`references/operational/implementation.md`。
- 构建与产物加载 审查/反模式/合规：`references/operational/review.md`。
- 构建与产物加载 验证/构建/运行态：`references/frontend-verification-levels.md`、`references/operational/verification.md`。
- 构建与产物加载 其它领域细节：`references/build-stage-checklist.md`、`references/patterns.md`、`references/schema-packets.md`。
- 构建与产物加载 场景 references：`references/scenarios/performance.md`。
- 构建与产物加载 templates：`templates/build-diagnosis.md`。

## Shared Governance
- 构建与产物加载 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 构建与产物加载 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 构建与产物加载 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

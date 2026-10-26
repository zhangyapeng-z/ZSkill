---
name: front-hzero-permission-button
description: 当任务涉及 HZERO/C7N 前端权限按钮时使用，覆盖 Header/Toolbar/页面级按钮、Table 行操作、详情按钮、明细行按钮、导入导出上传预览等 required 业务动作的权限按钮入口、ButtonPermission 固定 import、permissionList 对象数组契约、PermissionProvider 对齐、按钮 type 和旧组件反模式。
---

# HZERO 权限按钮前端规范

## Scope
- `front-hzero-permission-button` 是 权限按钮 任务的执行入口，不是完整知识库。
- 先用本文件选择 权限按钮 需要的 reference，再按阶段读取细则。
- 权限按钮 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 权限按钮 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 权限按钮 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 权限按钮 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 权限按钮 reference 停止、降级或写入 replacement；只缺权限码、`permissionList` 候选值或平台登记证据时，不得停止生成权限按钮，必须用 generatedCandidate 权限码继续接固定组件，并默认写成 `permissionList` 对象数组。

## Reference Routing
- 权限按钮 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 权限按钮 设计/契约/问题门禁：`references/operational/design.md`。
- 权限按钮 实现/修复/工程证据：`references/operational/implementation.md`。
- 权限按钮 审查/反模式/合规/交付收口：`references/operational/review.md`。
- 权限按钮 其它领域细节：`references/operational/domain.md`。

## Shared Governance
- 权限按钮 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 权限按钮 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 权限按钮 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

---
name: front-hzero-renderer
description: 当任务涉及 HZERO 企业前端 renderer/helper 或 Table/Form 自定义渲染入口时使用，覆盖 hzero-front / utils/renderer 渲染工具、TagRender、enableRender、yesOrNoRender、dateRender、dateTimeRender、numberRender、operatorRender、c7nOperatorRender 的 import 证据、函数签名、Table/Form renderer 调用形态、columns[].renderer/render/command、状态标签、日期数值展示、启用禁用展示、操作列 helper、operators payload、record.get guard 和 JSX 组件化误用检查。
---

# HZERO Renderer 前端规范

## Scope
- `front-hzero-renderer` 是 Renderer 任务的执行入口，不是完整知识库。
- 先用本文件选择 Renderer 需要的 reference，再按阶段读取细则。
- 出现 `renderer`、`render`、`command`、`columns[].renderer/render/command`、`TagRender`、`operatorRender`、`c7nOperatorRender`、`record.get` 展示读取、`Output renderer` 或操作列自定义按钮渲染时，至少需要判断本 skill 是否适用；操作列动作语义和右锁定归 `front-hzero-choerodon-ui` 的 row-actions scenario。
- Renderer 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- Renderer 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 Renderer 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 Renderer import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 Renderer reference 停止、降级或写入 replacement。

## Reference Routing
- Renderer 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- Renderer 设计/契约/问题门禁：`references/operational/design.md`。
- Renderer 实现/修复/工程证据：`references/operational/implementation.md`。
- Renderer 审查/反模式/合规：`references/operational/review.md`。
- Renderer 验证/构建/运行态：`references/operational/verification.md`。
- Renderer 其它领域细节：`references/renderer-helpers.md`。

## Shared Governance
- Renderer 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- Renderer 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- Renderer 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

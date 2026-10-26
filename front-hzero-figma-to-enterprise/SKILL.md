---
name: front-hzero-figma-to-enterprise
description: 当输入包含 Figma URL、node id、设计截图、PRD/prototype 或 design-to-code 需求，并需要在 Choerodon UI / Pro、HZEROJS 页面或项目自定义组件体系内做企业前端页面分析、PageSchema、组件映射或设计交接材料时使用。覆盖 Figma 数据提取、PageSchema 分析、组件映射优先级、DataSet/HZERO 边界、资源、澄清和验证规划；完整业务实现必须回到 frontend-auto-agent。
---

# Figma 到企业前端

## Scope
- `front-hzero-figma-to-enterprise` 是 Figma 到企业前端 任务的执行入口，不是完整知识库。
- 先用本文件选择 Figma 到企业前端 需要的 reference，再按阶段读取细则。
- Figma 到企业前端 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- Figma 到企业前端 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 Figma 到企业前端 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 Figma 到企业前端 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 Figma 到企业前端 reference 停止、降级或写入 replacement。

## Reference Routing
- Figma 到企业前端 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- Figma 到企业前端 设计/契约/问题门禁：`references/design-analysis.md`、`references/integration-boundaries.md`、`references/operational/design.md`。
- Figma 到企业前端 实现/修复/工程证据：`references/figma-mcp-workflow.md`、`references/operational/implementation.md`。
- Figma 到企业前端 审查/反模式/合规：`references/component-mapping-guardrails.md`、`references/operational/review.md`。
- Figma 到企业前端 验证/构建/运行态：`references/operational/verification.md`、`references/visual-verification.md`。
- Figma 到企业前端 其它领域细节：`references/component-mapping.md`、`references/conversion-evaluation.md`、`references/custom-component-discovery.md`、`references/figma-cache-and-frontend.md`、`references/framelink-output-shape.md`、`references/operational/domain.md`、`references/samples/data-display-selector.md`、`references/samples/form-showcase.md`、`references/samples/navigation-query-feedback.md`、`references/samples/table-showcase.md`、`references/url-parsing.md`。
- Figma 到企业前端 templates：`templates/choerodon-mapping-output.md`、`templates/code-generation-boundaries.md`、`templates/delivery-plan.md`、`templates/hzero-mapping-output.md`、`templates/page-schema-output.md`、`templates/page-schema.md`。
- Figma 到企业前端 scripts：`scripts/extract-page-schema.js`。

## Shared Governance
- Figma 到企业前端 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- Figma 到企业前端 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- Figma 到企业前端 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

---
name: front-hzero-enterprise-design
description: 当 frontend-design-agent 需要生成或更新企业前端设计契约时使用，覆盖 Frontend Design、Contract Check、UI Contract、目标落位、候选编码和设计确认。仅用于设计契约阶段；实现、验证、审查、Handoff 汇合和执行期流程控制归 front-hzero-enterprise-process-control。
---

# Enterprise Frontend Design

## Scope
- `front-hzero-enterprise-design` 是 企业前端设计 任务的执行入口，不是完整知识库。
- 先用本文件选择 企业前端设计 需要的 reference，再按阶段读取细则。
- 企业前端设计 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 企业前端设计 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；企业设计模板和流程治理 reference 已固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实。命中专项场景时默认先记录 `specialtyTriggers[]` 和风险域；只有 Design agent 判定需要加载专项 owner reference 时，才消费对应 `front-hzero-*` 细则。目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级标准事实。

## Workflow
1. 将 企业前端设计 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 企业前端设计 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；企业模板/流程治理已固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费。专项场景默认只记录 trigger、riskDomain 和 Contract Check 摘要；若 Design agent 已按加载条件读取专项 owner reference，再消费其明确细则。目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 企业前端设计 reference 停止、降级或写入 replacement。

## Reference Routing
- 企业前端设计 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 企业前端设计 设计/契约/问题门禁：`references/contract-asset-discovery.md`、`references/frontend-id-runtime-contract.md`、`references/frontend-ui-contract-guardrails.md`、`references/hzero-request-service-contract.md`、`references/operational/design.md`、`references/technical-design-gate.md`、`references/tenant-context-contract.md`。
- 企业前端设计 其它领域细节：`references/backend-tds-frontend-hints.md`、`references/baseline-comparison-rubric.md`、`references/engineering-structure-and-coding.md`、`references/generated-code-conventions.md`、`references/hzerojs-asset-baseline.md`、`references/hzerojs-enterprise-page-composition-example.md`、`references/hzerojs-submodule-development.md`、`references/operational/domain.md`、`references/route-context-edit-mode.md`。
- 企业前端设计 templates：`templates/architecture-design.md`、`templates/contract-check.md`、`templates/gate-question-templates.md`、`templates/target-placement-backfill-checklist.md`、`templates/technical-design.md`、`templates/ui-contract.md`。

## Shared Governance
- 企业前端设计 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 企业前端设计 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 企业前端设计 使用 mock/demo、业务参数 generatedCandidate 或 runtime 未验证时，必须保留 verification 记录；内置 Standard Component Coordinates 本身不需要 replacement。

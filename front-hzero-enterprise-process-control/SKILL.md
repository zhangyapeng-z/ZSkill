---
name: front-hzero-enterprise-process-control
description: 当企业前端进入执行期流程控制时使用，覆盖 frontend-auto、Task、Implementation、Review、Verification、Handoff、Lite 汇合、并发控制、写入范围、frontend-stage-result、mock 切真实 API 和交付资产模板。不负责生成前端设计契约；设计阶段归 front-hzero-enterprise-design。
---

# Enterprise Frontend Process Control

## Scope
- `front-hzero-enterprise-process-control` 是 企业前端流程控制 任务的执行入口，不是完整知识库。
- 先用本文件选择 企业前端流程控制 需要的 reference，再按阶段读取细则。
- 企业前端流程控制 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 企业前端流程控制 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Workflow
1. 将 企业前端流程控制 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 企业前端流程控制 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 企业前端流程控制 reference 停止、降级或写入 replacement。

## Reference Routing
- 企业前端流程控制 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 企业前端流程控制 设计/契约/问题门禁：`references/operational/design.md`、`references/schema-field-contract-gates.md`。
- 企业前端流程控制 Implementation：`references/operational/implementation.md`；只在进入编码实现或实现返工时读取。
- 企业前端流程控制 Review：`references/operational/review.md`；只在进入 Review/Final Review 时读取。
- 企业前端流程控制 Verification：`references/operational/verification.md`；只在进入验证或窄复验时读取。
- 企业前端流程控制 stage progression：`references/frontend-stage-progression-gates.md`；只在 owning stage 准备进入下一阶段时读取对应小节。判断 evidence 缺口、用户等待、Execution Proof 自动补齐或 telemetry 降级时，同时读取 `references/frontend-context-handoff-control.md#Evidence Layers And User Wait Boundary`。
- 企业前端流程控制 审查/反模式/合规：`references/final-output-quality-gate.md`、`references/generated-code-static-quality-gate.md`。
- 企业前端流程控制 上下文/证据分层/交付/汇合/替换：`references/frontend-context-handoff-control.md`、`references/operational/handoff.md`。
- 企业前端流程控制 标准 import 坐标：`references/frontend-standard-import-coordinates.md`。生成或审查 Component Import / API Provenance、标准组件、固定 helper、权限按钮、renderer、导入导出、Page alias、i18n、Attachment 或 HZERO 通用组件 import 时读取。
- 企业前端流程控制 其它领域细节：`references/backend-api-readiness-for-frontend.md`、`references/data-service-runtime-gates.md`、`references/frontend-compliance-manifest-governance.md`、`references/frontend-concurrency-control.md`、`references/frontend-fusion-checklist.md`、`references/frontend-locale-external-allowlist.md`、`references/frontend-optimization-execution-control.md`、`references/frontend-skill-common-governance.md`、`references/frontend-stage-result-field-governance.md`、`references/frontend-standard-import-coordinates.md`、`references/frontend-ui-runtime-gates.md`、`references/frontend-validator-fix-routing.md`、`references/frontend-validator-rule-index.md`、`references/frontend-write-scope-control.md`、`references/hzero-choerodon-production-compliance-gate.md`、`references/hzerojs-submodule-runtime-gate.md`、`references/input-root-multi-module-discovery.md`、`references/operational/domain.md`、`references/retrospective-hardening.md`、`references/schema-runtime-gates.md`。
- 企业前端流程控制 templates：`templates/artifact-index.md`、`templates/backend-api-readiness-checklist.md`、`templates/current-tab-menu-reuse-best-practice.md`、`templates/evidence.md`、`templates/frontend-compliance-manifest.md`、`templates/frontend-dry-run-checklist.md`、`templates/frontend-index.md`、`templates/frontend-response-scenarios.md`、`templates/gate-question-templates.md`、`templates/handoff-status-summary.md`、`templates/implementation-dispatch-plan.json.template`、`templates/implementation-result.md`、`templates/lessons-learned.md`、`templates/manual-checklist.md`、`templates/open-tab-reusable-fixed-path-best-practice.md`、`templates/optimization-execution-manifest.json.template`、`templates/production-replacement-checklist.md`、`templates/review-report.md`、`templates/runtime-acceptance.md`、`templates/schema-checklist.md`、`templates/submodule-config-single-router.ts.template`、`templates/submodule-config.dev.ts.template`、`templates/submodule-config.ts.template`、`templates/submodule-dev-mock-plugin.js.template`、`templates/submodule-dev-mock.js.template`、`templates/submodule-list-page.tsx.template`、`templates/submodule-package.json.template`、`templates/submodule-router-current-tab.ts.template`、`templates/submodule-router-dynamic-tab-dws.ts.template`、`templates/submodule-router-dynamic-tab-page-modes.ts.template`、`templates/submodule-router-open-tab-page-modes.ts.template`、`templates/submodule-router-open-tab-reusable-fixed-path.ts.template`、`templates/submodule-router.ts.template`、`templates/submodule-tsconfig.json.template`、`templates/task-breakdown.compact.md`、`templates/task-status.compact.md`、`templates/task-breakdown.md`、`templates/task-status.md`、`templates/verification-report.md`。`taskProfile=compact` 优先读取 compact 模板；只有 `taskProfile=expanded / audit` 且存在 production-ready、多模块完整验收、复杂 shared-scope 或用户明确审计要求时才读取完整模板。
- 页面真实可达/可用、核心演示路径闭合或 production-ready 要求：读取 `references/frontend-runtime-acceptance-control.md` 和 `templates/runtime-acceptance.md`；该门禁独立于普通 Verification。
- 进入 Task 或后续阶段的提效工具执行证据：读取 `references/frontend-optimization-execution-control.md` 和 `templates/optimization-execution-manifest.json.template`；规则中出现脚本名不等于已执行。

## Shared Governance
- 企业前端流程控制 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 企业前端流程控制 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 企业前端流程控制 使用 mock/demo、业务参数 generatedCandidate 或 runtime 未验证时，必须保留 verification 记录；内置 Standard Component Coordinates 本身不需要 replacement。

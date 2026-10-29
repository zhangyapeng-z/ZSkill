---
name: front-hzero-enterprise-page
description: 当任务涉及创建、修改、审查、排障或设计 HZERO 企业页面/业务页面时使用，覆盖 Header、Content、PageHeaderWrapper、i18n/intl、Permission/permissionList、request/service/model、loading、notification、upload/import/export、文件预览、值集/LOV，以及 HZERO + Choerodon DataSet 页面边界。
---

# HZERO 企业页面

## Scope
- `front-hzero-enterprise-page` 是 企业页面 任务的执行入口，不是完整知识库。
- 先用本文件选择 企业页面 需要的 reference，再按阶段读取细则。
- 企业页面 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- 企业页面 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。

## Scenario Trigger Map
- `f-layout`：命中 F 型布局、左列表右详情、吸附详情、ListHeader/ListItem、TabsAdsorptionContainer、`_LOCATED_DATA_` 或列表详情联动时，必须读取 `references/scenarios/f-layout.md`；详情集合内的 DataSet / Table / Form 规则同时回 `front-hzero-choerodon-ui`。
- `customization`：命中二开、客制化、route override、priority、租户定制、主题字体、headScripts、标准包覆盖或客户化资源隔离时，必须读取 `references/scenarios/customization.md`，不得用普通页面 wrapper 掩盖覆盖边界。

## Workflow
1. 将 企业页面 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 企业页面 import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。
4. 缺少关键契约时按已加载 企业页面 reference 停止、降级或写入 replacement。

## Reference Routing
- 企业页面 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 企业页面 设计/契约/问题门禁：`references/mock-contract-boundary.md`、`references/operational/design.md`。
- 企业页面 实现/修复/工程证据：`references/operational/implementation.md`。
- 企业页面 审查/反模式/合规：`references/operational/review.md`。
- 企业页面 验证/构建/运行态：`references/operational/verification.md`。
- 企业页面 其它领域细节：`references/common-patterns.md`、`references/core-utils.md`、`references/i18n-permission-request.md`、`references/page-delivery-checklist.md`、`references/patterns.md`、`references/schema-packets.md`、`references/tsconfig-paths.md`、`references/value-set-lov.md`。
- 企业页面 场景 references：`references/scenarios/f-layout.md`、`references/scenarios/customization.md`。
- 企业页面 templates：`templates/page-design.md`。

## Shared Governance
- 企业页面 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 企业页面 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 企业页面 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

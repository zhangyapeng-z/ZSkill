---
name: front-hzero-choerodon-ui
description: 当任务涉及 Choerodon UI Pro / C7N 前端实现、审查或排障时使用，尤其是 DataSet-first 页面、Form/Table、fields、queryFields、queryDataSet、transport、events、Lov、Attachment，以及 HZERO 边界已确认后的 Choerodon DataSet 页面部分。业务 UI 优先使用 choerodon-ui/pro；只有 Pro 无合适组件或任务仅涉及纯展示/布局时才使用基础 choerodon-ui。
---

# Choerodon UI

## Scope
- `front-hzero-choerodon-ui` 是 Choerodon UI 任务的执行入口，不是完整知识库。
- 先用本文件选择 Choerodon UI 需要的 reference，再按阶段读取细则。
- Choerodon UI 结论必须来自用户确认、FDS/TDS/API、目标工程源码、运行日志或已加载 reference。
- Choerodon UI 业务字段、接口、权限、租户规则、项目 wrapper/exportShape 和生产运行状态必须另有用户、FDS/TDS/API、目标工程或运行证据；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 明确的内置标准坐标、固定 helper、标准 UI 形态和拒收项是规范事实，目标工程证据只能补充、确认 wrapper/override 或证明冲突，不能因缺失而降级。只有专项 skill / HZERO / Choerodon 内置组件规则都不适用或目标环境明确不可用，且项目也找不到合格组件/wrapper 时，才允许原生 HTML DOM fallback；必须记录搜索范围、排除原因和替换风险。

## Scenario Trigger Map
- `query-table`：命中查询表格、列表查询、filterBar、queryFields、queryDataSet、分页/排序/筛选、Table 查询区、模糊查询或查询区策略时，必须读取 `references/scenarios/query-table.md`，不得只按通用 Table 规则生成。
- `row-actions`：命中操作列、行按钮、更多操作、禁用态、隐藏态、lock/right lock、`c7nOperatorRender`、`operatorRender`、renderer payload 或 action object 时，必须读取 `references/scenarios/row-actions.md`，并同步 `front-hzero-renderer` 的 helper 合同。
- `master-detail`：命中头行明细、主从、header-line、明细表保存、明细行状态、父子关联键或详情内 Pro Table 时，必须读取 `references/scenarios/master-detail.md`；页面布局和 HZERO 容器边界同时回 `front-hzero-enterprise-page`。

## Workflow
1. 将 Choerodon UI 请求归类为 design、implementation、review、verification、handoff 或领域问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对 Choerodon UI import、route、script、request、permission、runtime 和 generatedCandidate 做证据确认；命中场景的对应 `front-hzero-*` 专项 skill 及已加载 owner reference 固化的内置标准坐标、固定 helper、标准 UI 形态和拒收项按规范直接消费，目标工程证据只用于确认 project wrapper/override、兼容性或冲突，不能因缺失而降级。实现可见业务 UI 前必须先按“命中场景的 `front-hzero-*` 专项 skill / HZERO / Choerodon 内置组件规则 -> 项目 confirmed 组件或 wrapper -> 原生 DOM fallback”排序；项目 wrapper 只有在 confirmed 等价承载标准能力、未命中 anti-pattern 且不削弱 owner 规则时才可采用，原生 DOM 只能在前两类无可用方案且已文件化原因时使用。表格型详情集合不走该 fallback 顺序，固定使用 Choerodon Pro Table。
4. 缺少关键契约时按已加载 Choerodon UI reference 停止、降级或写入 replacement。

## Reference Routing
- Choerodon UI 阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- Choerodon UI 设计/契约/问题门禁：`references/operational/design.md`、`references/patterns/ui-contract-guardrails.md`。
- Choerodon UI 实现/修复/工程证据：`references/dataset.md`、`references/operational/implementation.md`、`references/patterns/dataset-mock-transport.md`。
- Choerodon UI 审查/反模式/合规：`references/operational/review.md`、`references/patterns/static-anti-pattern-checklist.md`。
- Choerodon UI 验证/构建/运行态：`references/operational/verification.md`。
- Choerodon UI 交付/汇合/替换：`references/patterns/hzero-handoff.md`。
- Choerodon UI 其它领域细节：`references/api.md`、`references/components.md`、`references/configuration.md`、`references/enum-map.md`、`references/form-table.md`、`references/patterns/form-edit.md`、`references/patterns/import-export.md`、`references/patterns/master-detail.md`、`references/patterns/modal-lov-attachment.md`、`references/patterns/query-list.md`、`references/patterns/table-inline-edit.md`、`references/patterns/tree-data.md`。
- Choerodon UI 场景 references：`references/scenarios/query-table.md`、`references/scenarios/row-actions.md`、`references/scenarios/master-detail.md`。

## Shared Governance
- Choerodon UI 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- Choerodon UI 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- Choerodon UI 使用 mock/demo、reference-generatedCandidate 或未验证平台坐标时，必须保留 verification 与 replacement 记录。

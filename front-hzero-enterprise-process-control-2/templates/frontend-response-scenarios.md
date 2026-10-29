# Frontend Response Scenarios

本模板只用于 `frontend-auto-agent` 的响应外形，不参与阶段门禁。字段事实仍来自 schema、Design/Task/Review/Verification/Artifact 结果。

## 新增页面但生产契约缺失
- 输出当前阶段、执行模式、契约状态、runnable、候选值来源、缺失合同和下一步。
- 用户未要求 production-ready 时采用默认 requestable mock demo，并把真实 API、权限、菜单、LOV/附件/导入导出参数放入 replacement。
- 用户要求 production-ready 时停在 Contract Check/Design，不生成 production runnable。

## HZERO + Choerodon 完整页面
- 说明外层 Design handoff 与内部 `Task -> Implementation -> Review -> Verification -> Artifact`；production-ready/high-risk 增加 Final Review。
- 必须说明 direct owning-agent 调度；`frontend-general-agent` 只作 fallback。
- 输出 route/menu、permission、page composition、i18n、DataSet/service、附件/导入导出、验证和 replacement 的命中摘要，不展开未命中矩阵。

## 小范围单文件修改
- 输出 `frontendExecutionMode=regular-change`、目标文件、successCriteria、`Implementation -> Verification`、compile/build 事实和未验证项。
- 目标文件不明确时只做最小定位；多个候选影响写入时进入范围确认。

## General fallback 合同
- 明确当前 Todo、stage-result、delegated agent、next-stage-recommendation 和回到 frontend-auto-agent。
- fallback 不改变 owning stage，不把 general 当 owning agent。

## HZERO 构建诊断
- 输出目标包、cwd、package manager/scripts 证据、HZERO tooling、候选或已执行命令、构建产物/部署路径和未验证项。
- 单一构建问题不进入完整页面交付链路。

## Figma/PageSchema 证据缺失
- 只输出 Figma evidence status、缺失 URL/node/screenshot/cache、可继续的最小证据和业务契约缺口。
- 不确认视觉、接口、权限、路由、LOV 或附件生产参数。

## 响应状态头

```text
当前阶段：
前端执行模式：
契约状态：
可用性状态：
是否 runnable：
下一阶段：
产物路径：
未验证项：
专项边界处理：
```

轻量问答可缩成 3-5 行；进入实现、验证、Review、Handoff 或 runnable 判断时使用状态头。

# Backend TDS Frontend Hints

用途：规范前端流程读取后端 TDS 中“前端相关设计/要求”的处理方式。后端 TDS 可能包含页面、菜单、按钮、字段、查询、权限或交互描述，但这些内容通常是跨端提示，不等于完整 Frontend Design。

## Core Rule

后端 TDS 中的前端相关内容不屏蔽，但默认按 `backend-provided-hint / partial` 吸纳。它可以提供后端契约、平台约束和候选信息，但不能单独闭合前端 UI Contract、组件选型、字段顺序、页面布局或 runnable implementation。

## Classification

| 内容类型 | 可吸纳为 | 默认状态 | 不能直接做什么 |
| --- | --- | --- | --- |
| API URL/method、DTO/schema、response shape、错误结构 | backend contract input | confirmed / partial，取决于证据完整度 | 不能自动确认前端 request helper、tenantContext、DataSet adapter |
| 字段含义、状态流转、按钮可用条件 | cross-end constraint | partial / generatedCandidate | 不能自动确认 UI 字段顺序、编辑态、组件类型 |
| 权限资源、菜单 code、route/menu 候选 | platform/backend hint | generatedCandidate / partial | 不能自动确认平台已登记或 routeOpenMode |
| 租户、附件、导入导出、LOV/lookup、templateCode、bucket | backend/platform hint | partial / generatedCandidate | 不能自动确认前端 helper、下载/上传协议或生产替换完成 |
| 页面布局、组件选型、查询条、抽屉/弹窗、样式、字段展示顺序 | UI candidate | generatedCandidate / partial | 不能单独标记 UI confirmed |

## Confirmation Rules

- 后端 TDS 可以确认“业务 API 资产”的一部分，但前端可调用契约必须继续检查 `serviceRequestContract`、`tenantContext`、分页/排序/过滤参数、response adapter、错误结构和下载/导出 helper。
- 后端 TDS 可以提供字段、状态、权限和按钮可见性约束，但 UI Contract 必须用 FDS、用户确认、Figma/PageSchema、Frontend Evidence、目标工程模式和 Choerodon/HZERO 规范复核。
- 后端 TDS 中的前端页面描述如果与 FDS、用户确认、Frontend Evidence、UI Contract 或 baselineComparison 冲突，必须标记 `conflict / needs-confirmation`。
- 后端 TDS 中缺失某个前端能力，不表示该能力不需要；必须回到 FDS、前端设计和 Contract Check 判断是否 missing。

## Required Output

Design / Contract Check 应记录 `Backend TDS Frontend Hints`：

| field | 说明 |
| --- | --- |
| hintArea | api / field / status-flow / permission / route-menu / lov-lookup / attachment / import-export / ui-layout / component / interaction / other |
| hintContent | 摘要 |
| source | TDS 路径、章节或行号 |
| absorbedAs | backend-contract / cross-end-constraint / ui-candidate / platform-candidate |
| defaultStatus | confirmed / partial / generatedCandidate / conflict / not-applicable |
| frontendRecheckRequired | yes / no |
| confirmationSourceNeeded | FDS / user / Figma / evidence / UI Contract / platform export / API doc |

## Blocking Defaults

以下情况不得进入 production-ready：

- 只有后端 TDS 写了页面/按钮/字段，但缺 Frontend Design UI Contract。
- 只有后端 TDS 写了 API URL/method，但缺前端 serviceRequestContract 或 tenantContext。
- 后端 TDS 的前端布局/组件写法与目标工程 evidence 或 Choerodon/HZERO guardrails 冲突。
- 后端 TDS 与 FDS 或用户确认冲突，且未形成澄清结论。

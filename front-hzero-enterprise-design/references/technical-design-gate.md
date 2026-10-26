# 技术设计门禁

## 目标
Frontend Design 负责把需求、接口和页面证据转成可确认、可拆任务、可验证的前端设计文档。它不是编码阶段。

## 必须进入技术设计的场景
- 新增页面、管理页、详情页、主从页、导入导出、上传附件、权限按钮、跨模块改造。
- HZERO + Choerodon DataSet / Form / Table 组合页面。
- 需要新增 route、菜单、权限、i18n、LOV/LV、service/model、DataSet 或上传导出协议。
- 后端/跨端流程输出 Frontend Impact Packet，且影响为“是”或“不确定”。

## 技术设计必须覆盖
- 模板选择：小范围 `regular-change` direct 可不生成前端设计文档；页面交付 / demo-slice / mock-demo / production-ready 前端交付统一使用 `technical-design.md`。复杂度差异不得通过 lite/full 模板分流解决；必须在统一模板内补齐适用契约，不适用项写 `not-applicable + reason`，缺失、冲突或待确认项写入澄清或阻塞项。
- 设计输入来源：功能文档、接口列表、页面/交互资料、后端资产来源。
- Frontend Design workspace：`sdd-workspace/changes/{change-id}/frontend/design/`，默认只用于 `frontend-design.md` 和 `contract-check.md`；`frontend-clarifications.md`、`ui-contract.md` 和 `production-replacement-draft.md` 只在确有需独立跟踪的阻塞澄清、复杂 UI Contract 或 mock/demo 临时契约草稿时生成。
- Frontend execution workspace：`sdd-workspace/changes/{change-id}/frontend/`，用于 evidence、tasks、verification、review、handoff 和 figma-cache 子目录。
- Contract Check：Backend Asset Coverage，以及字段、接口、路由、权限、i18n、LOV/LV、上传、导入、导出、附件协议的 `confirmed / partial / generatedCandidate / missing / conflict / not-applicable` 状态。
- 编码候选表：`routePath`、`menuPath`、`routeOpenMode`、`tabTitle`、`dws/queryStateKey`、`permissionCode`、`i18nCode`、`lovCode`、`lookupCode` 的 `confirmed / generatedCandidate / missing / conflict / not-applicable`、来源规则、用途、确认人和实现策略。
- transitionalCopy 清单：过渡/诊断/演示提示文案、承载位置、是否进入代码、是否用户可见和生产前处理方式；默认承载于 Handoff/替换清单/验证报告/开发态日志，不渲染到页面 UI。
- 目标工程和目录计划：父应用、微包、页面目录、路由配置入口、DataSet/service/style 文件职责。
- 数据层设计：字段映射、queryFields、transport、分页/排序/筛选、提交 payload、返回结构。
- 组件和交互：查询、重置、新增、编辑、详情、删除、提交、导入导出、上传预览、批量操作、异常/空态/loading。
- 验证方案：lint、typecheck/tsc、test/build 触发条件、dev server/HMR/browser/manual 行为验收和未验证风险。
- Frontend Design State Machine：`draft / needs-user / blocked-by-contract / ready-for-design-confirm / confirmed` 的当前状态、转移原因、允许下一阶段和禁止动作；默认 mock demo 自动确认时必须记录 `designConfirmationSource=default-mock-demo-policy`、`designConfirmQuestionToolCall=not-applicable` 和 `autoConfirmReason`。
- Design Completeness Policy：企业前端编排固定使用 `minimum-codable` 完成 Mock demo，要求首轮完整分类、可编码骨架和 mandatory self-check 通过，不要求全部生产事实 confirmed。`production-complete` 只作为后续独立集成稳定后的目标；用户要求 production-ready/真实 API 时先记录 advisory，不改变当前策略。阻塞只用于影响当前 Mock demo 的缺口。
- First-pass Gap Classification：所有未知项必须分类为 blocking、generatedCandidate、verification 或 not-applicable，并说明下游承接方式；工程事实缺口允许 targeted evidence backfill，但 backfill 不能替代 Source Inventory、Coverage Ledger 和 blocking gate 自检。
- Design Understanding Deviation Check：Figma、FDS/TDS/API、后端 TDS 前端提示、工程证据、相似页面和用户描述之间的疑似理解偏差、冲突来源、裁决方式、questionGate 和下游影响。

## 编码前确认规则
- 缺少功能文档或接口列表时，不生成可开发设计文档；输出 `设计输入不足`、`继续需要` 和可填写资料清单。
- 设计文档必须使用统一 `technical-design.md` 模板；不得通过选择废弃 lite 模板省略风险。普通页面在统一模板内用 `not-applicable + reason` 收敛，high-risk/production-ready 场景必须补齐关键契约。
- 关键生产契约缺失、冲突或仅 partial 时，设计状态为 `blocked-by-contract` 或 `待人确认`，不得输出 production-ready 结论。
- 设计文档和 Contract Check 必须文件化到 `sdd-workspace/changes/{change-id}/frontend/design/`；条件澄清、独立 UI Contract 和 production replacement draft 按需生成或内嵌。任务、验证、Review、Handoff 和 Figma 缓存必须文件化到 `sdd-workspace/changes/{change-id}/frontend/`。模块名、功能名不明确、当前 SDD 项目根目录不可写或用户禁止创建对应目录时，说明未文件化原因。
- 只有设计文件化、关键契约可开发且 Design Confirm 通过后，才可进入 Task Breakdown。
- 缺少编码候选表时不得进入 Task Breakdown；存在可按规范生成但未生成的 i18n/permission/lov/lookup 候选值时，设计门禁不通过。
- 关单默认执行 first-pass closeout with mandatory self-check：FD-G1~FD-G10 任一不通过时先分类失败项。阻塞类转 `blocked / needs-user`；可候选类补 `generatedCandidate + replacement / verification gate`；验证类进入 Verification checklist；工程事实类可做 targeted evidence backfill。`minimum-codable` 不追求 production confirmed，但必须满足 Source Inventory、Design Coverage Ledger、No Silent Missing 和 Blocking Gate；`production-complete`、高风险或用户明确完整闭环可追加 refine。达到预算后仍有阻塞类失败时输出 `fuseTriggered=true`、`blocked / needs-user` 和 `closeoutLoopResult`；非阻塞候选/验证缺口不得继续自修或包装成 confirmed。
- 缺少 Frontend Design State Machine 或 Design Understanding Deviation Check 时，不得把设计状态写为 `ready-for-design-confirm / confirmed`；没有自动确认条件证据时，不得写 `auto-confirmed-for-demo`。

## 反模式
- 用相似页面、页面名、Figma 文案或经验补齐接口、字段、权限、路由或平台协议。
- 把 `generatedCandidate` 写成 `confirmed`。
- 已有编码规范和基础事实时仍退化成 `.mock`，或让 Implementation 临场生成候选编码。
- 把 `mock/demo`、`generatedCandidate`、`待替换`、`未接生产接口`、`request helper 待确认`、`SecurityToken 待确认`、`Figma 未确认` 等内部临时说明直接放到页面 UI。
- 设计未确认就进入 production runnable code。
- 未记录状态机和设计理解偏差检查，只用“已分析 / 已确认 / 参考现有页面”概括推进依据。
- 普通页面在统一模板中堆填无关章节，导致确认摘要淹没关键契约。
- high-risk/production-ready 场景借废弃 lite 模板或省略填写压缩页面区域、生产替换、验证或 Review 边界。

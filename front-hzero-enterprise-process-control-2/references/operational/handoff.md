# 企业前端流程控制 - 交付与替换

## 阅读路由
- 企业前端流程控制 阶段汇合、交付摘要、模板治理、production replacement 或跨阶段规则归属判断时读取。

## Rule Governance Boundary
- 跨阶段规则的事实源必须是对应 reference；agent、template、checklist 只消费摘要和结构，避免口径漂移。
- agent 和 template 默认只保留阶段职责、结构字段、输出合同和 stop condition；跨阶段细则、反模式、gate 解释和示例优先沉到 owning reference，并通过 `gateId + owner reference + 当前 reason/evidence` 引用，避免在多个 agent/template 内重复展开。
- 仅当规则同时满足“跨至少两个执行阶段、影响至少两个 consumer、可机械检查、存在统一回退动作”时，才允许进入本 skill；否则应下沉到 owning frontend skill / reference。
- mock/demo 请求链路、父工程 mock plugin、runtime store、Network 验证、`reachable/usable` 事实和 mock 切真实 API 的事实源是 `front-hzero-mock-request`；本 skill 只保留执行期阶段路由和流程模板。
- HZEROJS 子模块骨架、`config/config.dev.ts`、父工程注册、route 聚合、`registerRegex`、页面目录和 DataSet/stores 布局的事实源是 `references/hzerojs-submodule-runtime-gate.md`；Design 侧只同步 `front-hzero-enterprise-design` 的 HZEROJS 子模块落位合同 和 `engineering-structure-and-coding.md` 的目录计划口径。
- DataSet、UI runtime、local-filter、共享 DataSet 实例和 mock-request UI 验收的事实源是 `references/frontend-ui-runtime-gates.md` 与 `references/generated-code-static-quality-gate.md`；Review/Verify/Task 模板只继承拒收和验证表达。
- `frontend-stage-result` 字段必须区分核心汇合字段和条件/信息字段。Lite 汇合、frontend-auto 汇合、artifact 汇总必须显式消费核心字段；非核心字段若不要求所有 consumer 直接读取，必须在校验脚本中登记豁免和原因，不能依赖隐式漏检。
- 模板优先承载结构，不长期承载整段规则解释。若模板正文持续膨胀，应先把细则回收到 owning reference，再让模板保留字段、状态和值域约束。
- 涉及真实工程行为的条目以样例生成、validator 或手工回归证据作为验证来源；规则文字本身不作为验证证据。

## Templates
- `templates/task-breakdown.md`：任务定义和计划基线模板，覆盖文件映射、依赖图、并行切片、共享文件锁、任务验收和实现交接。
- `templates/submodule-package.json.template`：新建 HZEROJS Umi 子模块 `package.json` 模板，scripts 为硬必选；files 使用裁剪后的安全默认边界并排除 `.umi/.umi-production`；dependencies/peerDependencies 等字段必须按项目证据补充。
- `templates/submodule-tsconfig.json.template`：新建 HZEROJS Umi 子模块 `tsconfig.json` 模板，生成时直接复制该 JSON 内容；除项目模板或用户模板明确覆盖外，不自行增删字段、不写 `compilerOptions.paths`。
- `templates/submodule-config.dev.ts.template`：新建 HZEROJS Umi 子模块 `config/config.dev.ts` 最小模板，禁止 `extendParentConfig`。
- `templates/submodule-config.ts.template`：新建 HZEROJS Umi 子模块 `packages/<module>/config/config.ts` 的主配置模板，包含从 `@hzerojs/plugin-micro` 导入的 `extendParentConfig`、`routes` 聚合、`hash` 和 prefix-scoped `registerRegex`；禁止 `@hzerojs/preset-hzero/lib/*` 深路径。
- `templates/submodule-config-single-router.ts.template`：单路由文件模式的 `config/config.ts` 模板，使用 `import route from './router'`、`routes: route` 和从 `@hzerojs/plugin-micro` 导入的 `extendParentConfig`。
- `templates/submodule-router.ts.template`：单路由文件模式的 list-only / 单子页面 `config/router.ts` 基础模板；有详情/新建/编辑子页面时不得用它生成同级独立 route。
- `templates/current-tab-menu-reuse-best-practice.md`：当前页打开详情 / 复用当前菜单页签的 route config、列表导航、详情 routeContext、React hooks 边界和验证证据最佳实践。
- `templates/submodule-router-current-tab.ts.template`：单路由文件模式的 current-tab list/create/view/edit 父子路由模板；`routeOpenMode=menu-current`、`detailViewInteractionMap=current-tab-page` 或用户选择“当前页打开详情 / 复用当前菜单页签”时优先使用。
- `templates/submodule-router-open-tab-page-modes.ts.template`：单路由文件模式的 list/detail create/view/edit 父子路由 + 普通 HZERO 系统页签 path 参数模板；用于 `routeOpenMode=hzero-openTab-path-params` 已确认、页面模式和记录身份进入 path 的场景；该模板不单独证明一个详情页签会被复用。
- `templates/submodule-router-open-tab-reusable-fixed-path.ts.template` + `templates/open-tab-reusable-fixed-path-best-practice.md`：单路由文件模式的新建独立、编辑/详情固定 path 复用最佳实践；用于 `routeOpenMode=hzero-openTab-reusable-fixed-path` 已确认、连续打开不同已有记录只保留一个详情页签的场景。
- `templates/submodule-router-dynamic-tab-page-modes.ts.template`：单路由文件模式的 list/detail create/view/edit 父子路由 + dynamic-tab 模板；用于详情/编辑/新建需要独立 HZERO 系统页签且页面模式进入 path 的推荐场景。
- `templates/submodule-router-dynamic-tab-dws.ts.template`：单路由文件模式的 list/detail 父子路由 + dynamic-tab + `dws: true` 模板；仅用于已确认同 pathname 不同 search/query 需要独立 HZERO 系统页签的兼容场景。
- `templates/submodule-dev-mock-plugin.js.template` / `templates/submodule-dev-mock.js.template`：mock-request 命中时的子模块 dev middleware plugin/handler 模板；必须由父工程显式注册或聚合注册后才算生效。
- `templates/frontend-compliance-manifest.md`：HZERO + Choerodon 页面/子模块跨阶段合规清单，覆盖 request、DataSet、字段、状态机、权限、i18n、LOV/lookup、附件、导入导出、操作列、静态门禁和生产替换项。
- `templates/task-status.md`：AI 驱动任务状态回写台账模板，覆盖 lane/status、状态流水、阻塞、Review/Verification 链接和返工链接。
- `templates/frontend-index.md`：`sdd-workspace/changes/{change-id}/frontend/index.md` 过程入口索引模板，只记录路径、状态摘要、当前阶段和开放事项。
- `templates/evidence.md`：Explore / Evidence 阶段工程证据模板，供 Design、Task、Verification 按需引用。
- `templates/gate-question-templates.md`：切真实 API、写入范围和验证降级接受等执行期 question 模板；浏览器/dev server 验证范围不再使用 question，默认只记录 not-run 和补跑清单。
- `templates/schema-checklist.md`：`frontend-stage-result` 与 `task-status.md` 字段完整性、一致性和汇合判定检查模板。
- `templates/frontend-dry-run-checklist.md`：回放 Explore -> Design -> Task -> Implementation -> Review -> Verify -> Handoff 的规则可执行性检查模板。
- `templates/backend-api-readiness-checklist.md`：后端 API readiness 的事实分级、运行证据和独立联调测试准备状态机械检查模板；不驱动前端自动 production replacement。
- `front-hzero-mock-request` 的 production switch 合同：后端 API service 已闭合后，从 mock-request 切换到真实 production-transport 的 replacement slice；发现 local-filter / inline mock 时必须 cleanup/rework。
- `templates/review-report.md`：独立 Review 报告模板，记录 `frontend-review-agent` 真实调度证据；fallback 模式记录 `frontend-general-agent -> frontend-review-agent`，同时保留 Review 结果、范围指纹、findings、修复包和验证缺口。
- `templates/verification-report.md`：验证报告模板。
- `templates/manual-checklist.md`：runtime/manual 页面验收清单模板。
- `templates/artifact-index.md`：`sdd-workspace/changes/{change-id}/frontend/handoff/artifact-index.md` 产物索引模板。
- `templates/handoff-status-summary.md`：`frontend/handoff/frontend-handoff.md` 状态摘要模板。
- `templates/production-replacement-checklist.md`：mock/demo 和临时平台契约最终生产替换清单模板。
- `templates/lessons-learned.md`：用户手测问题、根因和资产增强建议回灌模板。

## Short Closeout Policy
- Handoff / Artifact 默认是 Short Closeout：`handoffProfile=short`、`artifactIndexProfile=minimal`、`replacementProfile=triggered-only`。只做最终状态封口、路径索引、Review/Verification 摘要、未验证项、blockers、production replacement 主项和下一步映射。
- Short Closeout 只消费 canonical sources：`frontend/index.md`、`tasks/task-status.md`、Review 报告、`verification/verification-report.md`、`handoff/artifact-index.md`、`handoff/production-replacement-checklist.md` 和已压缩 evidence capsule。
- Short Closeout 不重新读取目标前端工程源码、不重新解析长 diff、不读取完整历史对话、不重跑验证命令、不发起二次 Review。状态源冲突时最多回读对应 canonical source；仍冲突则按 invalid early return 在同一前端子流程回状态 owner 调和，不得用 `blocked / conditional` 掩盖内部不一致。只有 dirty/conflict、越界写入或外层 gate 无法调和时才最终 `blocked`。
- `frontend-stage-result` 默认使用 `fieldProfile=core-only`；条件字段只在本次命中 gate、schema audit、validator repair、production-ready、完整验收或用户显式要求 full-debug 时展开。
- `artifactIndexProfile=minimal` 只列核心汇合产物和本轮命中 gate 的 artifact；不为未命中的 artifact 批量生成 `missing/not-applicable` 行。production-ready、完整验收、schema audit、validator repair、full-debug 或用户显式要求时才使用 `artifactIndexProfile=full`。
- required production replacement 仍必须有 `production-replacement-checklist.md`；缺清单时由当前 Handoff 补写，不得先输出 `blocked/missing` 交给 Lite 返工。Short Closeout 只引用命中主项和路径，不复制完整明细。`replacementProfile=triggered-only` 只展开本轮命中的替换类别；production-ready、完整验收、schema audit / full-debug 或用户显式要求完整清单时才使用 `replacementProfile=full`。
- Short Closeout 不降低 gate：Review、Verification、Compliance Manifest、mock-request validator、production replacement 等已选择阶段的 required 内部结果合同未闭合时，必须在同一前端子流程回 owning stage 补齐；外部 runtime、production-only 或允许 `not-run/unknown + reason` 的缺口才降级为 `conditional`；只有不可自动闭合且影响当前路径的问题才最终 `blocked`。

## Route Handoff Gate
- Handoff 必须复核 Design、Task、Implementation、Review 和 Verify 中的 route/menu/openTab 事实。新生成 HZEROJS 子模块 route config 不得出现任何 `redirect` route；若上游写了“父路由 redirect 到 `/list`”、父级 `redirect + routes`、同父级 path redirect 子路由或单独叶子 redirect，Handoff 不能照抄为交付方案，也不能把它列为可接受的 production replacement 临时项。
- 命中 route `redirect` 时，Handoff 必须把它列为 blocker / route-system finding，交付状态最高 `blocked`，下一步回到 Frontend Design / Task Breakdown / Implementation，修正为菜单、navigation 或 openTab 直接进入真实列表 path，并同步候选访问路径。
- 正式平台菜单仍指向父级 path 时，Handoff 只记录“平台菜单入口需调整到真实列表 path 或固定 `import { openTab } from 'utils/menuTab';` 的 navigation 入口”，不得建议在前端 route config 增加 redirect。

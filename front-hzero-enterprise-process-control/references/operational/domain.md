# 企业前端流程控制 - 领域细节

## 阅读路由
- 企业前端流程控制 其它不归入阶段的领域细节、交叉引用或 proof 结构命中时读取。

## References
- `references/frontend-fusion-checklist.md`：Lite 与前端子流程融合总图、分区规则和汇合检查清单。
- `references/input-root-multi-module-discovery.md`：输入根解析、多模块/多 feature 候选枚举、范围确认和多模块执行策略门禁。
- `references/frontend-concurrency-control.md`：Lite 全局并行、前端内部并行、共享文件锁、integration task 和汇合判定。
- `references/schema-runtime-gates.md`：schema checklist 的并发一致性、placement、runtime/compliance 和最终汇合门禁事实源。
- `references/schema-field-contract-gates.md`：schema checklist 中 route、field、style、component/type/provenance 等字段级 contract 的事实源。
- `references/frontend-context-handoff-control.md`：长上下文压缩、阶段输入裁剪、直接调度、状态单源、最大换手深度和阶段摘要。
- `references/frontend-write-scope-control.md`：已有前端文件修改、写入范围确认、`edit` 权限和阶段写入边界。
- `references/backend-api-readiness-for-frontend.md`：后端 API readiness 到前端集成准备、真实 API 试连边界和 production replacement advisory 的规则；不作为自动 replacement slice 触发源。
- `references/frontend-stage-result-field-governance.md`：`frontend-stage-result` 的字段准入、分层、consumer 责任和豁免治理。
- `references/frontend-ui-runtime-gates.md`：UI Contract 进入 Task/Implementation/Review/Verification/Handoff 后的运行时门禁、runtime/manual checklist 和 lessons learned 回灌。
- `front-hzero-mock-request` 的 runtime gate：mock-request 在 Task、Implementation、Review、Verification 和 Handoff 阶段的硬门禁。
- `references/hzerojs-submodule-runtime-gate.md`：HZEROJS 子模块骨架、config.dev.ts 独立启动配置、父工程注册、route 聚合、registerRegex、构建验证和拒收条件。
- `references/data-service-runtime-gates.md`：serviceRequestContract、tenantContext 和 routeContext/editMode 的实现、Review、Verification 和 replacement 门禁。
- `references/hzero-choerodon-production-compliance-gate.md`：HZERO + Choerodon 生产规范符合性门禁，覆盖 queryMode、父工程注册、权限/i18n、字段使用矩阵、状态机、LOV/lookup、组件类型、导入导出、本地 options、全局依赖/lockfile 归因和 Handoff 降级状态。
- `references/frontend-compliance-manifest-governance.md`：compliance manifest 的 gate 准入、owner、模板边界和变更治理。
- `references/generated-code-static-quality-gate.md`：生成代码静态质量门禁，供 Implementation 自查和 Review 使用。
- `references/final-output-quality-gate.md`：最终回复、验证结论和 Handoff 摘要的输出质量门禁，禁止无意义词、乱码、错别字和未解释残留字符。
- `references/retrospective-hardening.md`：手测问题、Review finding、manual finding 和 lessons learned 回灌到资产的规则。

## Reference Loading Policy
- Lite / frontend-auto 汇合只读 `frontend-fusion-checklist.md`、`schema-checklist.md` 和必要的 `frontend-index.md`。
- 用户提供目录、workspace、`@` 引用、文档根路径或其它可展开输入根，且可能存在多个模块/功能时，先读 `references/input-root-multi-module-discovery.md`，再决定是否进入 Explore、Design、Task、Implementation 或写操作。
- 判断 `frontend-stage-result` 字段、核心/条件字段边界或 consumer 校验策略时，先读 `references/frontend-stage-result-field-governance.md`，再回到 `schema-checklist.md` 和校验脚本的对应合同。
- 并发、共享文件锁、integration task 或状态回写只读 `frontend-concurrency-control.md`、`task-breakdown.md` 和 `task-status.md`。
- 判断 schema checklist 的并发一致性检查、运行门禁或最终汇合判定时，先读 `references/schema-runtime-gates.md`，再回到 `templates/schema-checklist.md` 的对应合同。
- 判断 schema checklist 的字段级 contract 长规则时，先读 `references/schema-field-contract-gates.md`，再回到 `templates/schema-checklist.md` 的对应合同。
- 长上下文恢复、阶段换手或输入裁剪只读 `frontend-context-handoff-control.md` 和 `frontend-index.md`。
- 写入范围、dirty/conflict、只读转可写或越界文件只读 `frontend-write-scope-control.md` 和执行期 question 模板。
- UI 运行门禁、页面可用性或用户手测反馈只读 `frontend-ui-runtime-gates.md`、`manual-checklist.md` 和 `lessons-learned.md`。
- mock/demo 查询页只读 `front-hzero-mock-request` 的 runtime gate；后端 API readiness 或真实 API 试连边界只读 `backend-api-readiness-for-frontend.md`、`backend-api-readiness-checklist.md` 和 `front-hzero-mock-request` 的 production switch 合同。
- HZEROJS 子模块运行期只读 `hzerojs-submodule-runtime-gate.md`；serviceRequestContract、tenantContext 或 routeContext/editMode 执行期只读 `data-service-runtime-gates.md`。
- 用户要求判断 HZERO/Choerodon 规范符合性，或阶段产物涉及父工程注册、权限/i18n、字段使用矩阵、状态机、LOV/lookup、组件类型、导入导出、附件、操作列、mock/demo、local-filter / inline mock 违规、production-ready、依赖/lockfile 漂移时，必须读取 `hzero-choerodon-production-compliance-gate.md`，并检查是否存在或需要生成 `templates/frontend-compliance-manifest.md`。
- 判断 compliance manifest 的 gate 准入、owner 或模板边界时，先读 `references/frontend-compliance-manifest-governance.md`，再回到 `templates/frontend-compliance-manifest.md` 和 `hzero-choerodon-production-compliance-gate.md` 的对应合同。
- 涉及自动生成页面、mock/demo、DataSet transport、service、导入导出、附件、权限按钮、LOV/lookup、操作列、用户手测返工或 production-ready 判定时，Implementation 自查和 Review 必须读取并执行 `generated-code-static-quality-gate.md`；Handoff 只读 artifact、handoff、production replacement 和 lessons learned 模板。
- 生成用户可见最终回复、验证结论、Handoff 摘要或 frontend-stage-result 汇总前，必须读取并执行 `final-output-quality-gate.md`。

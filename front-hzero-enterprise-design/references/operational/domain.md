# 企业前端设计 - 领域细节

## 阅读路由
- 企业前端设计 其它不归入阶段的领域细节、交叉引用或 proof 结构命中时读取。

## Reference Loading Policy
- 默认只读 Design Core、`templates/technical-design.md` 和 `templates/contract-check.md`。
- 只有命中对应能力时才读取 Contract Rules：UI 页面读 UI Contract；ID-like 字段读 ID Runtime；详情/编辑态读 Route Context；租户级 API 读 Tenant Context；生产 request 读 HZERO Request；子模块读 Submodule Design；mock/demo 读 `front-hzero-mock-request` 的 Design Contract。
- 只有需要生成候选编码时才读 `generated-code-conventions.md`。
- 命中 HZEROJS 空项目、参考资产缺失/不可读、无可采纳相似页面或缺少页面域分层参考时，读取 `references/hzerojs-asset-baseline.md` 和 `references/hzerojs-enterprise-page-composition-example.md`。
- Explore/Evidence、Task、Implementation、Review、Verification、Handoff、frontend-stage-result、并发、写入范围、生产替换执行和复盘回灌，默认使用 `front-hzero-enterprise-process-control`。

### Design Core
- `references/technical-design-gate.md`：Frontend Design 门禁和编码前确认规则。
- `references/contract-asset-discovery.md`：Contract Check 和后端/通用契约资产发现规则；生成 `contract-check.md` 前必须使用。
- `references/backend-tds-frontend-hints.md`：后端 TDS 中前端相关设计/要求的吸纳、降级、复核和冲突处理规则。
- `references/engineering-structure-and-coding.md`：工程结构、目录计划和编码规则前置。
- `references/baseline-comparison-rubric.md`：工程现状与标准范式冲突时的 follow-project / follow-baseline / follow-asset-baseline / merge / block 判断准则。

### Contract Rules
- `references/frontend-ui-contract-guardrails.md`：Design 阶段 UI Readback、UI Contract、UI 来源优先级和无来源 UI 禁止规则。
- `references/frontend-id-runtime-contract.md`：前端 ID runtime、Long/BIGINT、加密 ID、rowKey 和 Lov value 类型规则。
- `references/route-context-edit-mode.md`：详情、新建、编辑、复制页面的 routeContext、URL 参数解析、pageMode 和 UI 编辑态权威来源规则。
- `references/tenant-context-contract.md`：前端 `organizationId` / `tenantId` 获取、site/tenant 角色路径、`getCurrentOrganizationId` 和 `getUserOrganizationId` 边界规则。
- `references/hzero-request-service-contract.md`：HZERO request/service、API_HOST 内置拼接、服务前缀、原生 axios/fetch 例外和 base URL resolver 边界规则。
- `references/hzerojs-submodule-development.md`：HZEROJS `packages/<module>` 子模块落位、父工程注册候选、registerRegex 和 parentSrcWritePolicy 设计合同。
- `references/hzerojs-asset-baseline.md`：HZEROJS 空项目、缺失参考资产或无可采纳参考模块时的资产基线。
- `references/hzerojs-enterprise-page-composition-example.md`：无参考基线下页面域分层、constants/service/stores/components/Table 边界示例。
- `front-hzero-mock-request` 的 Design Contract：列表/查询型 mock demo 的 mock-request Design / Contract Check 合同。

### Candidate Rules
- `references/generated-code-conventions.md`：候选 route/permission/i18n/LOV/lookup 编码规则。

### Design Templates
- `templates/technical-design.md`：统一前端技术设计文档模板；页面交付 / demo-slice / mock-demo / production-ready 前端交付均使用该模板，不适用项写 `not-applicable + reason`。
- `templates/contract-check.md`：独立 Contract Check 模板；`contract-check.md` 是契约状态事实源。
- `templates/architecture-design.md`：架构设计输出模板。
- `templates/ui-contract.md`：编码前 UI 回读表、列表/详情/抽屉/Button/Interaction Contract 模板。
- `templates/target-placement-backfill-checklist.md`：历史 feature 缺 Target Placement Contract 时的补合同模板。
- `templates/gate-question-templates.md`：前端设计确认、缺失契约、routeOpenMode、native HTTP、导入/导出入口模式等设计期 question 模板；执行期 question 使用 `front-hzero-enterprise-process-control` 的执行期 question 模板。

## Resources

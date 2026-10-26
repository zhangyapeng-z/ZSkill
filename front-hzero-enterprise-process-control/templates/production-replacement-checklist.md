# 生产替换草稿 / 最终清单模板

Feature：<feature>
Feature Root：`sdd-workspace/changes/{change-id}/`
Frontend Root：当前 SDD 项目根目录下的 `sdd-workspace/changes/{change-id}/frontend/`
设计阶段草稿位置：`contract-check.md#Production Replacement Draft` / `sdd-workspace/changes/{change-id}/frontend/design/production-replacement-draft.md`
Handoff 最终路径：`sdd-workspace/changes/{change-id}/frontend/handoff/production-replacement-checklist.md`
模式：design-draft / handoff-final
状态：draft / confirmed / completed
backendApiReadiness：`status=closed` 仅在 `implementationStatus=completed + runtimeAvailability=verified + runtimeEvidence` 可追溯时成立；CTS 仅完成代码时为 `status=partial + reason=implementation-complete-runtime-unverified`
productionReplacementTrigger：pending / triggered / completed / blocked / not-applicable
queryMode：mock-request / production-transport / partial / blocked / unknown；local-filter / inline mock 只能触发 cleanup/rework blocker，不得进入 replacement 保留项
productionComplianceState：production-compliant / production-candidate / mock-demo-compliant / non-compliant / not-applicable
replacementProfile：triggered-only / full
initialSwitchMode：env-switch-only / not-run / not-applicable
mockRetention：retain-dev-mock / runtime-connected-mock-cleanup-required / not-applicable
switchEnvVar：<MODULE>_USE_MOCK / not-applicable / missing
productionEnvValue：false / not-applicable / missing
triggeredCategories：API / service-prefix / switch-env / route-menu / route-title / permission / lookupCode / lovCode / lovPara-contract / bucket / import / export / i18n / field-shape / demo-value / local-options / mock-store-query-mode / validation-guard / production-compliance / transitional-copy / verification-rerun

> 设计阶段只保留 draft 语义，优先嵌入 `contract-check.md`；内容过大时使用 `production-replacement-draft.md`。`production-replacement-checklist.md` 只用于 Handoff 最终资产，避免和 TDS 前端设计契约混淆。

| 类型 | 当前临时值/策略 | 生产契约来源 | 影响文件 | 替换方式 | 状态 | 负责人/确认人 |
| --- | --- | --- | --- | --- | --- | --- |
| API | 待填写 | 待确认 | 待填写 | 替换 service/transport | pending | 待确认 |
| service-prefix | resourcePath `/v1/{organizationId}/...` / servicePrefix generatedCandidate / missing | 项目公共配置、相似 service、后端服务编码或用户确认 | servicePrefix helper / service / DataSet | 确认 `/<servicePrefix>`，不得只用 `/v1/...` 或误用 `<unconfirmed-gateway-prefix>`；无公共配置时业务包本地 helper 可作为过渡 | pending | 前端平台/后端 |
| switch-env | 默认 mock / `<MODULE>_USE_MOCK=false` 切真实 | Contract Check 已确认 `switchEnvVar` + 部署/启动约定 | servicePrefix helper / CI/deployment / verification | `env-switch-only` 时应用源码不改；生产仅注入实际 `switchEnvVar=false`，默认 mock、精确字符串 `'false'` 切真实，并补外部 Network smoke 证据 | pending | 前端平台/测试 |
| route/menu | 待填写 | 待确认 | config/routes / 平台菜单 | 前端 route 中的 `authorized: true/title` 可作为候选/开发可访问配置；生产前仍需维护平台菜单入口、角色权限、菜单标题和多语言；若菜单入口当前指向父级 path，需调整为真实列表 path 或固定 `import { openTab } from 'utils/menuTab';` 的 navigation 入口，不得用 route `redirect` 兜底 | pending | 待确认 |
| route-redirect | not-applicable / blocker | 不允许 | config/router.ts / config/routes/** / Design / Task / Handoff | 新生成 HZEROJS 子模块 route config 不得出现任何 `redirect` route；若设计或实现要求父路由 redirect 到 `/list`、父级 `redirect + routes`、同父级 path redirect 子路由或单独叶子 redirect，必须回到 Design/Task/Implementation 修正，不能作为可接受的生产替换项 | not-applicable / blocked | 前端负责人 |
| route-title | `authorized: true` 临时中文 title / 生产 title 编码候选 / not-applicable | 平台菜单标题 + 平台多语言 | config/routes / 平台菜单 / 平台多语言 | 仅 `authorized: true` route 需要前端 title；前端临时生成值必须是中文标题，生产前再改为平台可识别字符串编码，优先 `hzero.common.*`，业务命名空间编码需到 `/hpfm/prompt` 补译文；不得写 `intl.get('xx')` 表达式；新增/生成 route config 不写 `titleType` | pending / not-applicable | 平台菜单/多语言确认人 |
| permission | `.mock` | 权限资源 | buttons/routes | 替换权限码 | pending | 待确认 |
| lookupCode | `.mock` | 值集资产 | dataset/constants | 替换 lookupCode | pending | 待确认 |
| lovCode | `.mock` / generatedCandidate code | LOV/主数据资产 | dataset/constants / DataSet fields / Compliance Manifest | 替换 lovCode，并确认 value/text/bind、返回对象字段、单选/多选和展示字段 | pending | 待确认 |
| lovPara-contract | missing / partial / generatedCandidate `lovPara` / not-applicable | LOV 参数契约、API 查询参数、级联行为 | DataSet dynamicProps / Compliance Manifest / UI Contract | 确认 `paramName`、`paramSourceField`、`sourceTiming`、`emptyValueBehavior`、`cascadeClearPolicy`、`confirmedSource`；缺确认前不得生成固定空字符串或猜测参数，不得声明 production-ready | pending / not-applicable | 平台/后端/业务 |
| bucket | `.mock` | 文件服务协议 | Attachment | 替换 bucket/protocol | pending | 待确认 |
| import | `Import` 标准入口已接 / missing / blocked / templateCode 待确认 | 导入模板与通用导入协议 | import action / confirmed current wrapper | 补齐 templateCode、prefixPath/action、结果反馈、错误明细、关闭刷新或关闭 missing/blocked | pending | 待确认 |
| export | `ExcelExportPro` 标准入口已接 / missing / blocked / runtime not-verified | 导出协议 | export action / confirmed current wrapper | 补齐查列/导出两阶段参数、templateCode、文件响应、异步结果或关闭 missing/blocked | pending | 待确认 |
| i18n | `platform-locale-keys.json` 中的 pending key + `.d()` 默认文案 | HZERO `/hpfm/prompt` 平台多语言 | intl keys / platform locale ledger | 在平台逐 key 配置译文并回填 confirmed 来源证据 | pending | 平台多语言确认人 |
| field-shape | mock/demo 字段 shape | FDS/TDS/MDS/FSS/API/DTO 契约证据 | DataSet/mock data/table/form/service | 对齐字段和 payload；FSS 仅作后端/通用契约来源，不作为前端产物落点 | pending | 待确认 |
| demo-value | `demoGeneratedValue` / placeholder / contract-example-values | 真实业务样例、测试数据准备或生产接口返回 | devServer mock handler / runtime store / verification / handoff | 保留或替换演示值；demo 值只证明页面演示，不作为业务事实、create/edit 默认输入、submit payload 来源或 production-ready 证据 | pending / not-applicable | 前端/测试/业务 |
| local-options | `MOCK_*_OPTIONS` / `DEMO_*_OPTIONS` | LOV/lookup/值集 | constants/dataset | 替换为真实值集/LOV | pending | 待确认 |
| mock-runtime-path | `mock-request` / `blocked-local-filter` / `dev-mock-retained` | API/mock 策略 | dataset/service/dev-mock | 保留 `dev-mock/**` handler/plugin/store；仅当 local-filter、inline mock、页面内存 store 或 silent fallback 仍进入 production success path 时清理。`env-switch-only` 不删除 mock 源码 | pending | 前端 |
| validation-guard | header+line 校验、状态守卫 | 业务状态机/校验规则 | page actions/dataset | 对齐真实状态和校验 | pending | 待确认 |
| production-compliance | mock-demo-compliant / production-candidate / non-compliant | HZERO/Choerodon production compliance gate | route registry / permission / locale / options / package-lock | 补齐 active registry、权限/i18n、真实值集/LOV、依赖归因和验证证据；无来源/未授权漂移需清理或确认 | pending | 待确认 |
| transitional-copy | demo/diagnostic copy | 产品/i18n | Handoff / replacement checklist / verification report / dev log；默认不进入 page UI | 删除、隐藏或替换为正式 i18n；如需页面可见需产品/测试确认 | pending | 待确认 |

## 未确认项
- 字段清单：待确认
- 请求/响应结构：待确认
- tenant/organizationId 取值方式：待确认（按 `front-hzero-enterprise-design` 的 tenantContext 合同；必须区分当前租户 `getCurrentOrganizationId()` 与用户所属租户 `getUserOrganizationId()`；必须记录 resolverProvenance，禁止本轮新造 resolver 或默认租户常量）
- Figma 视觉确认：待确认

## 后续协作清单
| 优先级 | 事项 | 用户需要提供 | 影响 | 回到阶段 | 阻塞 production-ready | 阻塞 reachable/usable | 建议确认人/来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 必须补齐 | 真实接口运行验证与逐 API 响应消费 | 已部署/可访问环境的 HTTP smoke、integration test、browser Network；每个 API 的 `responseHandling`、分页/字段/错误契约 | production-ready | Backend readiness / Contract Check / Implementation | yes | no | 后端/测试 |
| 平台执行 | 生产环境 mock 开关注入 | 在部署/CI 注入已冻结的 `switchEnvVar=false`；不是业务用户要补充 request/helper 路径 | production-ready | deployment handoff / runtime acceptance | yes | yes | 前端平台/运维 |
| 必须补齐 | 权限码/菜单资源 | 菜单权限导出或平台权限编码 | production-ready | Contract Check / Frontend Design / Implementation | yes | no | 权限平台 |
| 必须补齐 | `authorized: true` 路由标题 | 平台菜单标题、title 字符串编码和译文；业务命名空间编码需到 `/hpfm/prompt` 补译文；确认前端 route title 使用字符串编码而非 `intl.get()` | production-ready | Contract Check / Frontend Design / Handoff | yes | no | 平台菜单/多语言 |
| 必须补齐 | LOV/lookup/bucket/templateCode | 平台编码、返回字段、display/value、LOV 查询参数名、参数来源字段、来源时机、空值行为、级联清理策略、上传/导入协议 | production-ready | Contract Check / Frontend Design / Implementation | yes | no | 平台/后端 |
| 建议补齐 | Figma 视觉确认 | Figma 可读链接、node-id 或人工验收结论 | visual-fidelity | Evidence / Frontend Design | no | no | 设计/产品 |
| 建议补齐 | 页面运行态/手工验收 | 可访问 URL、账号/租户、测试数据、验收步骤或用户手工证据 | reachable/usable | 独立 runtime acceptance / 用户手工验收 | no | yes | 测试/业务 |

> Handoff 输出必须把本清单提炼为“后续协作项”，并按必须补齐 / 平台执行 / 建议补齐 / 可选优化分组。HZERO 标准 `request`、`getResponse`、默认 mock switch 表达式和标准 import 坐标不属于用户确认项；只有项目冲突、非 HZERO 工程或实际业务 API 契约缺失才进入确认。

## 类别展开策略

- `replacementProfile=triggered-only` 是默认模式。mock/demo 或临时平台契约场景下，只展开本轮命中的替换类别，并在 `triggeredCategories` 中列出触发原因。未命中类别不得批量生成 `not-applicable` 长表，可在摘要中写 `not-triggered + reason`。
- `replacementProfile=full` 仅用于 production-ready、完整验收、schema audit / full-debug 或用户显式要求完整清单。此时必须覆盖：route/menu、route-title、permission、API/transport、service-prefix、switch-env、field-shape、i18n、lovCode/lookupCode、lovPara-contract、local-options、bucket/templateCode、export/import、mock-runtime-path、validation-guard、production-compliance、transitional-copy 和验证补跑；确实不适用的类别写 `not-applicable + reason`，不得省略。
- 无论 profile 如何，已命中的关键类别不得折叠或遗漏；影响 production-ready、reachable 或 usable 的替换项必须进入用户可见后续协作摘要。

## mock 切真实 API
- 本清单在企业前端编排中只作 advisory，不触发 Lite/frontend-auto replacement。后端 readiness closed 也只表示可作为后续集成证据，不能自动设置开关。
- 独立联调测试必须先得到 `mockAcceptance=passed`，再得到 `backendIntegrationSignal=service-started | user-confirmed-service-available`，随后首次动作仅为 `<MODULE>_USE_MOCK=false` 环境注入和前端重启/重建。
- 首次试连应用源码变更必须为零；保留 `dev-mock/**` 是预期结果。不得同时修改 adapter、field-shape、service-prefix、LOV/lookup、权限、菜单、i18n、`API_HOST`、proxy 或业务代码。
- API、field-shape、mock-runtime-path、local-options 等 pending 项先保持提示状态。只有真实 Network/页面失败证据命中对应项后，才转成定向修复任务；未失败项不得批量替换。
- 实际修复完成后只复跑失败路径和受影响项。只有真实请求行为、Review/Verify/Handoff 和完整生产门禁均闭合时，相关项才可标为 completed 并参与 production-ready 判断。

## transitional-copy 页面 UI 边界
- 默认不得把内部临时说明渲染到业务页面 UI；这类说明应保留在本清单、Handoff、验证报告、实现摘要或开发态日志。
- 页面 UI 中禁止出现 `mock/demo`、`generatedCandidate`、`待替换`、`未接生产接口`、`request helper 待确认`、`SecurityToken 待确认`、`Figma 未确认` 等内部词。
- 若演示验收需要可见标识，必须记录产品/测试确认来源，并替换为正式业务文案和 i18n key。

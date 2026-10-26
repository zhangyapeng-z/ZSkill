# Backend API Readiness For Frontend

用途：把后端编码、接口契约和运行可用事实转成前端与独立联调测试可消费的 `backendApiReadiness`。前端侧消费该结构字段；后端/Lite 若提供 standalone readiness JSON，仅作为同结构校验输入，不要求前端读取固定名 `backend-api-readiness.json`。该状态用于证据分级和集成准备提示，不是 Lite 或 `frontend-auto-agent` 自动切真实 API 的触发器。

## 阅读路由
- 判定字段结构时读 `Readiness Schema`。
- 区分“编码完成”和“服务可用”时读 `Closed 判定`。
- 判断下一步属于前端编排还是联调测试时读 `阶段所有权`。
- readiness 不闭合、部分 API 或存在冲突时读 `阻塞或回退条件`。

## 核心边界

- 企业前端编排始终完成 `queryMode=mock-request` 的 Mock demo，不因 CTS 完成或 readiness 更新切真实 API。
- Lite 只消费 readiness 事实并输出集成准备提示，不设置 `<MODULE>_USE_MOCK=false`，不启动服务，不调度 production replacement slice。
- 真实 API 首次试连只属于独立 `hzero-local-integration-test`，且必须先完成 Mock 验收，再确认后端服务已启动或由用户明确确认可用。
- 首次试连只改变已确认的 Mock 环境变量；adapter、字段、LOV、权限、菜单、i18n、`API_HOST`、proxy 和业务代码均不主动修改。
- 只有试连产生可复现失败证据后，才把窄修复包交给对应 owning agent；修复后只复跑失败路径和受影响项。

## Readiness Schema

```yaml
backendApiReadiness:
  status: closed | partial | missing | conflict | not-applicable
  implementationStatus: completed | partial | missing | conflict | not-applicable
  runtimeAvailability: verified | failed | unknown | not-run | not-applicable
  runtimeEvidence:
    verifiedBy: integration-test | http-smoke | deployed-contract-test | browser-network | not-run
    source: string | null
    coveredApiKeys: string[]
    verifiedAt: string | null
    environment: string | null
  source:
    tdsPath: string | null
    mdsPath: string | null
    ctsResultPath: string | null
    fssPath: string | null
    verificationEvidence: string | null
  apis:
    - apiKey: string
      required: boolean
      purpose: list | detail | create | update | delete | submit | cancel | options | other
      status: closed | partial | missing | conflict | not-applicable
      method: string
      path: string
      serviceRequestContract: confirmed | partial | missing | conflict | not-applicable
      requestParams: confirmed | partial | missing | conflict
      responseShape: confirmed | partial | missing | conflict
      responseHandling: hzero-get-response | dataset-native | dataset-data-key-total-key | data-envelope | project-adapter | not-applicable
      responseHandlingEvidence: string | null
      fieldMapping: confirmed | partial | missing | conflict
      paginationProtocol: confirmed | partial | missing | conflict | not-applicable
      errorShape: confirmed | partial | missing | conflict
      authTenantSecurity: confirmed | partial | missing | conflict | not-applicable
      tenantContext: confirmed | partial | missing | conflict | not-applicable
      tenantResolverProvenance: confirmed | partial | missing | conflict | not-applicable
      implementationEvidence: code-inspection | unit-test | integration-test | not-run
      runtimeAvailability: verified | failed | unknown | not-run | not-applicable
      runtimeVerifiedBy: integration-test | http-smoke | deployed-contract-test | browser-network | not-run
      runtimeEvidenceSource: string | null
      frontendReplacementItem: API | field-shape | mock-runtime-path | local-options | none
      blocker: string | null
  integrationAdvice: waiting-backend | ready-for-independent-integration | runtime-failed | not-applicable
  reason: string
```

## Closed 判定

`backendApiReadiness.status=closed` 只表示 required API 已有可追溯的运行可用证据，可作为后续独立联调测试输入。它不表示前端已完成真实 API 接入，也不授权 Lite 或企业前端编排切换。

Closed 必须同时满足：

- API URL/method、serviceRequestContract、请求参数、分页/排序/筛选、响应结构、逐 API `responseHandling`、字段映射和错误结构已确认。
- 每个 required API 都有非空 `responseHandlingEvidence`。非 DataSet service action 的 HZERO 基线为 `hzero-get-response`；DataSet read 默认 `dataset-native`，仅按实际契约使用其它 consumer。
- 涉及租户、组织、权限、SecurityToken/CSRF、附件、导入导出或 LOV/lookup 时，相关上下文和来源已确认或有 `not-applicable + reason`。
- `implementationStatus=completed`，且每个 required API 有后端实现证据。
- `runtimeAvailability=verified`，顶层 `runtimeEvidence.source` 非空，`coveredApiKeys[]` 覆盖全部 required API；每个 required API 均为 `status=closed + runtimeAvailability=verified` 且有合法 `runtimeVerifiedBy/runtimeEvidenceSource`。
- 运行证据来自已部署或可访问环境中的 integration-test、HTTP smoke、deployed contract test 或浏览器 Network。代码检查、构建通过、Swagger/OpenAPI、接口平台注册、数据库脚本存在和自然语言“后端已完成”均不能代替。

若 CTS 只完成一版编码、服务尚未启动，或数据库脚本、值集/LOV、审批、接口平台注册等运行环境准备尚未完成，必须写：

```yaml
backendApiReadiness:
  status: partial
  implementationStatus: completed
  runtimeAvailability: unknown | not-run
  integrationAdvice: waiting-backend
  reason: implementation-complete-runtime-unverified
```

该状态可保留完整 API 契约和生产替换提示，但不得声明 API 可用，不得触发任何前端真实链路动作。

## 阶段所有权

| 阶段 | 可执行动作 | 禁止动作 |
| --- | --- | --- |
| 后端 CTS | 输出实现状态、契约和已有运行证据 | 把编码完成写成 runtime verified |
| Lite / 企业前端编排 | 完成 Mock demo；记录 readiness、生产替换提示和 `mockIntegrationState` | 自动调度 replacement、设置 Mock 开关、启动服务、主动改真实 transport |
| 独立本地联调测试 | Mock-first 验收；确认后端可用；仅设置 `<MODULE>_USE_MOCK=false` 做首次试连；收集 Network/页面证据 | 首次试连时主动改 adapter、字段、LOV、权限、菜单、i18n、API_HOST、proxy 或业务代码 |
| 定向修复 | 消费集成失败证据，按 owner 最小修复并窄复测 | 无失败证据时做猜测性生产改造 |

真实 API 试连的必要信号固定为：

```yaml
mockAcceptance: passed
backendIntegrationSignal: service-started | user-confirmed-service-available
switchAction: env-only
```

`backendApiReadiness.status=closed` 可作为后端可用证据来源之一，但不能单独替代本次联调测试的 Mock 验收和 backendIntegrationSignal，也不能触发同一 `frontendAutoRunId` 恢复。

## 阻塞或回退条件

以下情况不得切换真实 API：

- Mock 页面、Mock 数据或核心交互存在明显问题，`mockAcceptance!=passed`。
- 后端服务未启动且用户未明确确认可用。
- readiness 只有 `implementationStatus=completed`，但 `runtimeAvailability=unknown/not-run`。
- API URL、请求/响应形态、分页、租户、安全或 serviceRequestContract 存在 missing/conflict。
- Mock 环境变量名、真假语义或浏览器 Bundle 注入未确认。
- 首次试连需要同时修改 `API_HOST`、proxy、adapter、字段、LOV、权限、菜单、i18n 或业务代码才能继续。

前四类保持 `waiting-backend-integration` 或输出契约缺口；环境变量切换合同缺失时输出 `mock-switch-contract-defect` 并交给前端定向修复，不得在联调测试步骤中顺手改 `config*.ts`。

## FSS 与汇合

FSS 可记录 API 契约、readiness、联调测试入口和生产替换提示，但不是切换触发源。Lite 的 Mock demo 汇合不因真实 API 尚未试连而阻塞后端/通用资产生成；只需明确非 production-ready 和后续独立集成步骤。

`frontend-stage-result` 建议包含：

```yaml
queryMode: mock-request
mockIntegrationState: mock-demo-completed | waiting-backend-integration | ready-for-independent-integration
backendApiReadiness:
  status: closed | partial | missing | conflict | not-applicable
  implementationStatus: completed | partial | missing | conflict | not-applicable
  runtimeAvailability: verified | failed | unknown | not-run | not-applicable
productionReplacementTrigger: pending | not-applicable
pendingReplacementItems: []
nextStageRecommendation: independent-local-integration-test
```

`productionReplacementTrigger=pending` 在这里仅表示清单尚未通过真实运行验证，不是自动调度指令。只有独立联调测试及后续定向修复稳定完成，并具备 Review/Verify/Handoff 事实后，才允许其它流程声明 `production-transport` 或 `production-ready`。

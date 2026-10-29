# Backend API Readiness Checklist

用途：机械区分后端编码事实、运行可用事实和后续独立联调测试准备状态。该清单不驱动 Lite 或 `frontend-auto-agent` 自动切换真实 API。

## 输入

- `backendApiReadiness` 对象；如后端/Lite 提供 standalone readiness JSON，可作为同结构校验输入
- TDS/MDS/API 契约与 CTS 结果
- 逐 API 运行证据（如存在）
- 前端 Contract Check、Mock 双链路和生产替换提示

## 检查项

| 检查项 | 通过条件 | 结果 |
| --- | --- | --- |
| implementationStatus | required API 有 Controller/service/DTO 等实现证据 | pass / partial / failed |
| runtimeAvailability | 已部署或可访问环境有 integration-test、HTTP smoke、deployed contract test 或 browser Network 证据 | pass / unknown / not-run / failed |
| requiredApiCoverage | 每个 required API 均有逐项状态；closed 时 `coveredApiKeys[]` 完整覆盖 | pass / partial / failed |
| apiContract | URL/method、请求参数、response shape、分页、错误结构已确认 | pass / partial / failed |
| responseHandling | 每个 required API 有明确 consumer 和非空 evidence | pass / partial / failed |
| serviceRequestContract | request helper、resourcePath/servicePrefix、env source 和 switchEnvVar 已确认 | pass / partial / failed |
| tenantAndSecurity | 租户、组织、权限、SecurityToken/CSRF 有来源或 `not-applicable + reason` | pass / partial / failed |
| mockSwitchContract | 默认 Mock、静态 env key、精确 `'false'` 切真实、浏览器 Bundle 注入路径已确认 | pass / partial / failed |
| mockAcceptance | 当前独立联调测试已先完成 Mock 数据、页面和核心交互验收 | passed / failed / not-run |
| backendIntegrationSignal | 当前后端服务已启动或用户明确确认可用 | service-started / user-confirmed-service-available / missing |

代码检查、构建、Swagger/OpenAPI、接口平台注册、数据库脚本、值集/LOV、审批流程和自然语言“后端已完成”只能支撑 implementation/contract，不得单独把 runtimeAvailability 写为 verified。

## 判定

| 判定 | 条件 | 动作 |
| --- | --- | --- |
| `implementation-complete-runtime-unverified` | 实现完成但服务未验证 | 企业前端编排继续并完成 Mock demo；输出 `waiting-backend-integration` |
| `ready-for-independent-integration` | readiness 运行证据有效，或本次后端服务已启动/用户明确确认可用 | 只允许进入独立联调测试；仍须先有 `mockAcceptance=passed` |
| `ready-for-env-only-trial` | `mockAcceptance=passed`、backendIntegrationSignal 有效、switch contract pass | 仅注入 `<MODULE>_USE_MOCK=false` 并重启/重建前端观察 Network |
| `mock-switch-contract-defect` | env key、真假语义或 Bundle 注入缺失 | 停止试连，输出前端定向修复包；不得在集成步骤改 config |
| `contract-or-runtime-blocked` | API 契约冲突、后端不可用或 Mock 验收失败 | 保持 Mock，按证据回对应 owner |

任何判定都不得产生 `create-production-replacement-slice`、`create-partial-replacement-slice` 或恢复同一 `frontendAutoRunId` 自动切换的动作。

## 输出摘要

```text
[Backend API Readiness Checklist Result]
readinessStatus: closed / partial / missing / conflict / not-applicable
implementationStatus: completed / partial / missing / conflict / not-applicable
runtimeAvailability: verified / failed / unknown / not-run / not-applicable
runtimeEvidence:
  verifiedBy: integration-test / HTTP smoke / deployed contract test / browser Network / not-run
  source: string | null
  coveredApiKeys: []
mockAcceptance: passed / failed / not-run
backendIntegrationSignal: service-started / user-confirmed-service-available / missing
integrationAdvice: waiting-backend / ready-for-independent-integration / ready-for-env-only-trial / blocked
switchEnvVar: <MODULE>_USE_MOCK / missing / not-applicable
switchAction: env-only / not-run
sourceChangesAllowedDuringInitialSwitch: none
pendingAdvisoryItems: []
reason:
```

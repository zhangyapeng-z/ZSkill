# Mock To Real API Integration Switch

用途：定义 Mock demo 阶段应预置的双链路，以及后续独立联调测试中首次从 Mock 试连真实 API 的最小动作。本文不授权 Lite 或 `frontend-auto-agent` 自动执行生产替换。

## 阅读路由

- 企业前端编排、Lite 汇合或当前交付边界：阅读“所有权边界”和“前端编排输出”。
- Mock/真实请求双链路实现：阅读“Mock Demo 双链路”。
- 独立联调测试首次试连：按“首次真实 API 试连”和“观察与状态”执行。
- 真实 API 试连失败后的回流修复：阅读“失败修复合同”。

## 所有权边界

- 企业前端编排：生成并验证默认 Mock 的双链路代码，保留 `dev-mock/**`，输出生产替换提示；不切真实 API。
- Lite：汇合 `mock-demo-completed` 和 readiness 事实；不设置环境变量，不启动服务，不恢复 frontend-auto 做 replacement。
- `hzero-local-integration-test`：先验收 Mock，再确认后端服务可用，随后仅通过 Mock 环境变量做首次真实 API 试连。
- 前端 owning agent：只在联调测试返回可复现失败证据后做定向修复。

`backendApiReadiness.status=closed`、CTS 编码完成或用户说“接口好了”均不是企业前端编排的切换触发器。首次试连必须同时具备：

```yaml
mockAcceptance: passed
backendIntegrationSignal: service-started | user-confirmed-service-available
switchContract: confirmed
switchAction: env-only
```

## Mock Demo 双链路

Mock demo 实现必须预先具备同一业务请求链的 Mock/真实前缀切换能力：

```text
mock/demo:  <current-dev-server-origin>/_mock/<module>/v1/{organizationId}/...
real API:   /<servicePrefix>/v1/{organizationId}/...
```

默认 Mock，只有 Contract Check / Task 明确的 `switchEnvVar` 精确等于字符串 `'false'` 时才走真实前缀：

```ts-template
const <FEATURE>_SERVICE_PREFIX = '/<servicePrefix>';
const <FEATURE>_MOCK_PREFIX = '/_mock/<module>';

export const get<Feature>ServicePrefix = () => <FEATURE>_SERVICE_PREFIX;
export const get<Feature>MockOrigin = () =>
  typeof window === 'undefined' ? '' : window.location.origin;
export const get<Feature>MockPrefix = () =>
  `${get<Feature>MockOrigin()}${<FEATURE>_MOCK_PREFIX}`;
export const is<Feature>MockRequestMode = () =>
  process.env.<MODULE>_USE_MOCK !== 'false';
export const get<Feature>ApiPrefix = () =>
  is<Feature>MockRequestMode()
    ? get<Feature>MockPrefix()
    : get<Feature>ServicePrefix();
```

生成时必须满足：

- `<MODULE>_USE_MOCK` 替换为已确认的静态 env 属性名，不使用动态 key，不二次猜测变量名。
- 未设置、`true`、`1` 或空字符串均继续走 Mock；仅精确 `'false'` 切真实 API。
- `MOCK_PREFIX` 使用当前 dev server origin，避免项目 request helper 将裸 `/_mock` 拼到远端 `API_HOST`。
- DataSet read、详情、保存、删除、提交、撤回和其它 action 共用同一个 prefix helper；不得列表走 Mock、动作走真实 API。
- service 层不保留 `mockRequest` / `realRequest` 两套长期业务实现；Mock/真实只切请求前缀，payload、consumer 和错误处理尽量共用。
- `queryMode` 是流程状态，不进入业务源码、URL、query、body 或 DataSet 参数。
- `dev-mock/**` handler/plugin/store 保留，用于开发和回归；生产请求路径不得 silent fallback 到 Mock。
- local-filter、inline mock、页面内存 seed/store、`data:` URL 或静态数组成功路径不属于可保留双链路，必须在 Mock demo 实现阶段按既有质量门禁修复，不能等首次真实试连时顺手清理。

## 前端编排输出

企业前端编排只输出提示，不执行切换。生产替换清单至少记录：

```yaml
queryMode: mock-request
switchEnvVar: <actual-env-key>
mockEnvValue: <actual-mock-value>
realApiEnvValue: false
defaultMode: mock
devMockRetention: keep
mockIntegrationState: mock-demo-completed
nextStage: independent-local-integration-test
advisoryItems:
  - real API URL/servicePrefix runtime verification
  - response envelope and pagination verification
  - field/LOV/permission/menu/i18n/platform configuration verification
  - write action and error-state verification
```

这些项目是后续观察清单，不是当前 Implementation 任务。不得因为清单存在就主动改 adapter、字段、LOV、权限、菜单、i18n、`API_HOST`、proxy 或业务代码。

## 首次真实 API 试连

标准顺序不可调整：

1. 使用 Mock 值启动前端。
2. 验证 Mock 数据、页面加载和当前范围内核心交互。
3. 若 Mock 有明显问题，停止在 Mock 阶段并形成定向修复输入，不启动后端切换步骤。
4. 等待后端服务启动成功，或取得用户明确的服务可用确认。
5. 确认 env key、真假语义和浏览器 Bundle 注入均已存在。
6. 停止当前前端进程；仅把 `<MODULE>_USE_MOCK=false` 注入启动环境，并按项目公开命令重启或重建前端。
7. 观察启动日志、页面行为和浏览器 Network，记录实际 URL、status、payload、response shape 和错误。

首次试连的允许变更只有启动环境变量。不得同时执行以下动作：

- 删除或改写 `dev-mock/**`。
- 修改 `API_HOST`、proxy、runtime config、request helper 或 servicePrefix。
- 修改 DataSet adapter、`dataKey/totalKey`、字段映射、LOV/lookup、权限、菜单、路由、i18n 或业务组件。
- 新增 production replacement Task、cleanup slice 或猜测性兼容代码。

若前端环境变量未进入实际生效的浏览器 Bundle，输出 `mock-switch-contract-defect` 并停止试连；该问题交给前端 owning agent 定向修复，不在联调测试步骤中直接修改 `config*.ts`。

若前端进程当前未运行，标准流程仍应先按 Mock 模式启动并完成 Mock 验收。只有恢复同一代码修订、且已有可追溯 `mockAcceptance=passed` 证据时，才可直接用 real API env value 启动继续试连；必须记录复用证据，不能把“前端尚未启动”当成跳过 Mock-first 的理由。

## 观察与状态

关闭 Mock 只证明前端尝试进入项目已有真实请求链路，不证明请求已到达目标后端。必须按实际证据分级：

| 观察 | 状态 | 下一步 |
| --- | --- | --- |
| Network 仍命中 `/_mock/<module>` | `switch-not-effective` | 输出 env 注入/构建配置失败证据，定向修复切换合同 |
| Network 离开 Mock，但网关/服务不可达 | `real-api-routing-failed` | 保留 URL/status 和后端可用证据，交后端/环境 owner |
| HTTP 200 但页面无数据 | `data-consumer-shape-failed` | 记录 response 与 DataSet/consumer 期望，交前端定向修复 |
| 字段、分页、LOV、权限或动作失败 | `contract-drift` | 逐项记录实际失败，只修对应契约和代码 |
| 核心路径通过但仍有未测项 | `real-api-connected-conditional` | 输出未验证项，等待后续反馈迭代 |
| 多轮目标范围验证稳定且完整生产门禁闭合 | `production-ready` | 由后续完整 Review/Verify/Handoff 判断 |

不得单凭环境变量值、dev server 启动、HTTP 200 或响应非空声明真实 API 可用、页面 usable 或 production-ready。

## 失败修复合同

实际失败必须先形成运行证据包，再进入修复：

```text
[Frontend Repair Input]
sourceStage: local-integration-test
mode: real-api
mockAcceptance: passed
backendIntegrationSignal: service-started | user-confirmed-service-available
switchEnvVar: <actual-env-key>
network: <method url status request/response summary>
expected: <expected behavior or contract>
actual: <actual behavior>
classification: <mock-switch | data-consumer-shape | contract-drift | route-menu-runtime | backend-api | unclear>
allowedRepairScope: <evidence-backed files/contracts only>
resumeNode: real-api-trial
```

修复规则：

- 只修证据指向的失败，不执行清单中尚未失败的其它“生产替换”项目。
- adapter、字段、LOV、权限、菜单、i18n、`API_HOST`、proxy 或业务代码只有在对应失败证据成立时才进入修复范围。
- 修复后只复跑失败路径和受影响项，然后返回独立联调测试继续观察。
- `dev-mock/**` 始终保留；真实路径不得回退到 Mock 数据掩盖错误。

## 结果摘要

```text
[Real API Integration Trial]
mockAcceptance: passed / failed / not-run
backendIntegrationSignal: service-started / user-confirmed-service-available / missing
switchAction: env-only / not-run
switchEnvVar: <actual-env-key | missing>
queryModeObserved: mock-request / real-api / unknown
networkEvidence: <summary | not-run>
trialStatus: waiting-backend-integration / real-api-trial / feedback-pending / real-api-connected-conditional / blocked
sourceChangesDuringInitialSwitch: none
advisoryItems: <list>
repairInput: <path/summary | not-applicable>
```

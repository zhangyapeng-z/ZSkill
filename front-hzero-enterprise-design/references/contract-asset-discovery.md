# 契约资产发现

## 阅读路由
- 需要判断先读哪些契约资产时读 `搜索范围`。
- 需要决定是否允许跨 `sdd-workspace/**` 兜底搜索时读 `兜底搜索触发与预算`。
- 需要限制搜索成本和停止条件时读 `搜索预算`。
- 需要为不同缺口构造检索词时读 `关键词组`。

## 目标
在生成企业前端页面前，从工程和 `sdd-workspace` 等资产中发现字段、接口、值集、LOV、权限、附件、导入导出和多语言证据，避免编造生产契约。

## 搜索范围
- 当前 Change Root：`sdd-workspace/changes/{change-id}/fds.md`、`tds.md`、`mds/**`、`fss/**`、`frontend/design/**`。
- 后端/通用资产缺项兜底：当前 Change Root 下指定文件或目录不存在、为空、明显过期或无法覆盖关键契约时，允许在 `sdd-workspace/**` 下按模块名、功能名、服务简码、接口路径、DTO/entity 名、权限码、菜单名、值集/LOV/lookup、bucket、templateCode 等关键词定向发现相关后端/通用资产；该兜底必须遵守下方“兜底搜索触发与预算”，不得无条件横向扫描。
- 外部契约来源：Swagger/OpenAPI、后端 handoff metadata、DTO/schema/API 文档、平台菜单/权限/值集/LOV 导出、用户提供的接口清单。
- 目标工程相似页面：route、openTab/Tab 打开方式、PermissionButton、DataSet/service、i18n、Attachment、Export/Import。

读取顺序：
1. 先读当前 Change Root 下的 `fds.md`、`tds.md`、`mds/**`、`fss/**`，形成字段、API、权限、菜单、值集、导入导出、附件和状态流转的统一契约视图。`tds.md` 中的前端相关段落必须按 `references/backend-tds-frontend-hints.md` 单独归类为 backend-provided hint，不得直接当作完整 Frontend Design。
2. 当前 Change Root 缺项时，不按固定旧分区机械读取；应先列出缺项，再按“兜底搜索触发与预算”判断是否在 `sdd-workspace/**` 下检索后端/通用资产，并记录检索词、命中路径、预算使用和未命中项。
3. 外部契约来源只在用户提供、上游 handoff 指明或当前资产不足以判断 production-ready 时读取，并记录来源类型和可信度。
4. 必要时最小读取后端源码或配置证据，例如 controller、DTO、entity、mapper、enum/constant、permission/menu config；源码证据用于校验或补缺，不得替代缺失的前端可调用契约。
5. 目标工程相似页面只用于确认写法、目录、封装、前端 request/DataSet 模式和已有契约位置，不能替代当前 feature 的业务契约。

## 兜底搜索触发与预算

不得因当前 feature 资产缺项而无条件扫描 `sdd-workspace/**`。兜底搜索必须绑定 `missingContractKeys`、关键词组和预算；达到预算、缺少关键词或候选不足以闭合契约时停止，并把状态写为 `partial / missing / conflict`，不得继续横向搜索来追求“更完整”资料。

### 触发条件

只有满足以下任一条件时，才允许进入 `sdd-workspace/**` 兜底搜索：

- 当前 Change Root 下标准资产缺失、为空、明显过期或无法覆盖本轮关键契约。
- Contract Check 已列出关键缺口，且缺口会影响 production runnable、production-ready 或 mock/demo 替换边界，例如 API、字段、权限、菜单、LOV/lookup、附件、导入导出、tenantContext、serviceRequestContract。
- 上游、用户或当前 feature 资产提供了可定向检索关键词，例如模块名、功能名、服务简码、接口路径、DTO/entity 名、权限码、菜单名、值集/LOV/lookup、bucket、templateCode。
- 用户或主流程明确说明相关资产可能在其它 feature / 历史功能中。

不满足触发条件时，必须写：

```text
fallbackSearchStatus=not-run
fallbackSearchReason=当前 Change Root 资产已覆盖关键契约 / 缺少可定向关键词 / 本轮不要求 production-ready / 用户禁止额外读取
```

### 搜索预算

兜底搜索预算默认小于工程 Explore，且只服务当前缺口：

```text
fallbackSearchBudget:
  maxKeywordGroups: 3
  maxSearchCommands: 5
  maxCandidatePaths: 10
  maxFilesRead: 5
  stopWhen: gap-closed / no-keywords / no-hits / budget-exhausted / conflict-found
```

优先搜索当前模块或当前 feature 同层路径；只有当前模块无命中且关键词足够具体时，才扩大到 `sdd-workspace/**`。一旦 `missingContractKeys` 已被确认、明确不存在或出现冲突，就停止搜索，不继续读取相似资产。

### 关键词组

关键词必须由缺口反推，不使用固定大词全扫。每次最多 3 组，优先级为：用户/上游明确关键词 > 当前 FDS/TDS/MDS/FSS/API 中抽出的关键词 > generatedCandidate。只有 generatedCandidate 支撑的命中，不能直接标为 confirmed，最多为 `partial / generatedCandidate`。

```text
API 缺口：serviceCode / controller resource path / DTO/entity name / interface path tail
权限缺口：route/menu path / permission code candidate / action name / feature/module name
LOV/lookup 缺口：field name / lovCode or lookupCode candidate / value set business name
附件/导入导出缺口：bucket / templateCode / importCode / export endpoint / field name / capability name
tenant/serviceRequest 缺口：organizationId / tenantId / request helper name / servicePrefix candidate
```

## 关键字
```text
值集编码
lovCode
lookupCode
多语言
权限
permission
bucket
templateCode
导出
导入
附件
API
DTO
organizationId
tenantId
```

## 输出要求
- 资产存在时，列出路径、标题或 key，并说明只能作为候选还是已确认契约。
- 资产不存在时，写“未找到”，不得生成正式编码。
- 必须输出 `Backend Asset Coverage`：列出已读取、缺失、兜底搜索、冲突、仍需确认和实现结论。没有执行兜底搜索时必须写明原因，例如“当前 feature 资产已覆盖关键契约”“缺少可定向关键词”或“用户禁止额外读取”。
- 必须输出 `Fallback Asset Search`：记录 `triggered`、`triggerReason`、`missingContractKeys`、`keywordGroupsUsed`、`searchBudgetUsed`、`candidatePaths`、`adoptedEvidence`、`unresolvedAfterFallback` 和 `stopReason`。未触发时也要写 `triggered=no + reason`。
- 必须输出 `Backend TDS Frontend Hints`：记录后端 TDS 中的前端相关 API、字段、权限、状态、路由、页面或交互描述，按 `backend-contract / cross-end-constraint / ui-candidate / platform-candidate` 吸纳，并标明是否需要前端复核。
- Contract Check 中每个关键契约必须使用状态 `confirmed / partial / generatedCandidate / missing / conflict / not-applicable` 之一；不得把未读到或只读到相似页面的内容写成 `confirmed`。
- Figma 文案、页面名和相似页面只能作为 UI/工程模式证据，不能升级为接口、权限、字段类型、LOV 或 bucket 契约。
- API / 后端资产结论必须区分两层：
  - `业务 API 资产`：URL、method、DTO/schema、业务字段和后端接口说明。
  - `前端可调用契约`：serviceRequestContract（request helper/import、baseUrlStrategy、envSource、servicePrefix、nativeHttp）、tenant/orgId 参数来源、SecurityToken/权限头、分页/排序/过滤参数、response shape、错误结构、download/export helper 和文件返回协议。
- FSS、`external-assets/api-list.json`、`external-assets/apis/*.json`、Swagger/OpenAPI 或后端接口清单只证明 `apiContractStatus=documented/partial`；它们不能证明后端服务已启动、网关已注册、租户/权限可用、真实 response shape 与文档一致，也不能单独证明 `backendApiReadiness=closed`、`runtimeReachability=reachable` 或 `queryMode=production-transport`。
- serviceRequestContract 必须按 `references/hzero-request-service-contract.md` 判定：HZERO request 默认内置 API_HOST；需求文档未提原生 HTTP 时默认使用 HZERO/project request，不询问用户；文档明确提原生 axios/fetch/外部直连但缺确认时，回到 question。
- tenant/orgId 必须按 `references/tenant-context-contract.md` 判定：前端 `getCurrentOrganizationId()` 表示当前租户 tenantId；`getUserOrganizationId()` / `currentUser.organizationId` 表示用户所属租户，不能默认用于租户级 API path variable。
- 只有两层都确认时，才可写前端 API 契约闭合。只确认 URL/method/DTO 或只读取到 FSS/API 文档时，结论应写 `业务 API 资产较完整；前端可调用契约未闭合`；企业前端编排的 `queryMode` 始终走 `mock-request` 并记录独立集成/production advisory，不因用户要求真实 API 或 production-ready 改成 `partial/unknown/blocked`，也不得静默写成 `production-transport`。
- 后端 TDS 中的 UI/页面描述只作为 UI candidate：页面布局、组件选型、字段顺序、查询条、弹窗/抽屉、样式和交互细节必须由 FDS、用户确认、Figma/PageSchema、Frontend Evidence、UI Contract 或工程模式复核；唯一来源为后端 TDS 时不得标为 UI confirmed。
- 不使用 `API 100%`、`接口 100%`、`接口已完全确认` 等百分比或绝对闭合表述，除非同时列出并确认前端可调用契约的全部必填项。

## Backend Asset Coverage 模板

| 类别 | 标准路径读取 | 兜底搜索 / 外部来源 | 状态 | 缺口或冲突 | 处理结论 |
| --- | --- | --- | --- | --- | --- |
| FDS | `sdd-workspace/changes/{change-id}/fds.md` |  | confirmed / missing / conflict |  |  |
| TDS | `sdd-workspace/changes/{change-id}/tds.md` |  | confirmed / partial / missing / conflict | 后端 TDS 前端段落默认 partial/hint |  |
| MDS | `sdd-workspace/changes/{change-id}/mds/**` |  | confirmed / partial / missing |  |  |
| FSS | `sdd-workspace/changes/{change-id}/fss/**` |  | confirmed / partial / missing |  |  |
| API / DTO |  | Swagger/OpenAPI / DTO/schema / backend handoff / source evidence | confirmed / partial / missing / conflict |  |  |
| apiContractStatus |  | FSS / external-assets API / Swagger / backend source | documented / partial / missing / conflict | documented 只代表文档契约存在，不代表运行可达 |  |
| backendApiReadiness |  | Backend API Readiness / real API verification / dev gateway evidence | closed / partial / missing / conflict / not-applicable | 无运行或后端 readiness 证据时写 missing 或 partial，并标记 reason=unverified |  |
| runtimeReachability |  | Network / HTTP smoke / browser verification / not-run | reachable / failed / unknown / not-run / not-applicable | 文档资产不能写 reachable |  |
| serviceRequestContract |  | request helper / API_HOST strategy / envSource / servicePrefix / nativeHttp confirmation | confirmed / partial / missing / conflict / not-applicable |  |  |
| tenantContext |  | request helper / hzero-front utils / backend path variable / resolverProvenance / source evidence | confirmed / partial / missing / conflict / not-applicable |  |  |
| route/menu/openMode/permission |  | platform export / TDS / FSS / source evidence | confirmed / generatedCandidate / missing / conflict |  |  |
| LOV/lookup/value set |  | MDS / FSS / platform export / source evidence | confirmed / generatedCandidate / missing / conflict |  |  |
| attachment/import/export |  | MDS / FSS / backend handoff / source evidence | confirmed / partial / missing / not-applicable |  |  |

## Fallback Asset Search 模板

| 字段 | 内容 |
| --- | --- |
| triggered | yes / no |
| triggerReason | 当前 feature 缺项 / critical contract gap / 上游指明历史资产 / not-run reason |
| missingContractKeys | API / field / permission / menu / LOV / lookup / attachment / import / export / tenantContext / serviceRequestContract / none |
| keywordGroupsUsed | 最多 3 组；列出来源和可信度 |
| searchBudgetUsed | searches x/5；candidatePaths x/10；filesRead x/5 |
| candidatePaths | 命中路径、来源关键词、是否读取 |
| adoptedEvidence | 被采纳为 confirmed / partial / generatedCandidate / conflict 的证据 |
| unresolvedAfterFallback | 仍缺失或冲突项 |
| stopReason | gap-closed / no-keywords / no-hits / budget-exhausted / conflict-found / not-run |

## Backend TDS Frontend Hints 模板

| hintArea | hintContent | source | absorbedAs | defaultStatus | frontendRecheckRequired | confirmationSourceNeeded |
| --- | --- | --- | --- | --- | --- | --- |
| api / field / status-flow / permission / route-menu / lov-lookup / attachment / import-export / ui-layout / component / interaction / other |  | `tds.md#...` | backend-contract / cross-end-constraint / ui-candidate / platform-candidate | confirmed / partial / generatedCandidate / conflict / not-applicable | yes/no | FDS / user / Figma / evidence / UI Contract / platform export / API doc |

## 缺项处理
- `confirmed`：当前 feature 资产、外部契约或源码证据能明确支撑前端接入，并记录来源。
- `partial`：业务资产存在，但前端可调用契约不完整，例如缺 request helper、分页参数、tenant/orgId、SecurityToken、错误结构或下载协议。
- `generatedCandidate`：可按编码规则或上下文生成候选值，但尚未被用户、平台或后端资产确认。
- `missing`：标准路径和相关兜底搜索均未找到，或用户未提供必要资料。
- `conflict`：多个来源不一致，必须列出冲突来源并回到 Contract Check / Frontend Design / 用户确认。
- `not-applicable`：明确该能力本轮不涉及，并写明理由。
- production-ready 必须要求关键契约为 `confirmed` 或有明确 `not-applicable + reason`；`partial`、`generatedCandidate`、`missing`、`conflict` 均不得升级为生产闭合。
- mock/demo 可接受部分 `generatedCandidate` 或 `partial`，但必须进入 Production Replacement Draft / Checklist，并保留为待替换项。

## Contract Check 结论
- 字段、接口、route/menu/openMode、权限、LOV/lookup、附件/上传、导入导出、tenant/orgId 任一关键项缺失时，生产结论为 `待确认`。
- 默认 mock/demo 后，只能进入 mock/demo 设计和实现，并必须生成生产替换清单。

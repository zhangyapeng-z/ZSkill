# Tenant / Organization Context Contract

用途：统一 HZERO 前端在租户级 API、附件、导入导出、LOV/lookup 和生产替换中获取 `organizationId` / `tenantId` 的规则，避免把当前租户、用户所属租户和后端路径参数混用。

## 语义边界

| 名称 | 语义 | 典型来源 | 使用场景 |
| --- | --- | --- | --- |
| `organizationId` path variable | 后端租户级 Controller 路径参数，语义上作为业务 `tenantId` 传递 | `/v1/{organizationId}/...` | 租户级 API 路径 |
| `tenantId` | 当前业务租户 ID | 当前租户上下文 / 后端路径参数 | service、DataSet transport、附件、导入导出、LOV |
| `getCurrentOrganizationId()` | 前端 hzero-front 工具，实际返回当前租户 `getCurrentTenant().tenantId` | `utils/utils` user 工具 | 前端拼租户级路径或文件服务路径 |
| `getCurrentTenantId()` | 当前租户 ID | `getCurrentTenant().tenantId` | 与 `getCurrentOrganizationId()` 等价语义候选，需确认项目导出 |
| `getUserOrganizationId()` | 用户所属租户 ID，不随当前切换租户变化 | `getCurrentUser().organizationId` | 仅在业务明确需要“用户所属租户”时使用 |
| `isTenantRoleLevel()` | 当前角色是否为租户级角色 | `getCurrentRole().level !== 'site'` | 判断是否需要拼接租户路径 |

## 前端获取规则

- 租户级 API 路径优先使用项目已有 request helper、DataSet helper 或 `getPlatformVersionApi(api)`。
- 必须手动拼接租户级路径时，优先使用 `getCurrentOrganizationId()` 或项目等价 helper；不要直接读取 `window.dvaApp._store`。
- HZEROJS / hzero-front 标准工程中，API path 含 `/v1/{organizationId}` 且未发现项目级租户 resolver 冲突、用户所属租户语义要求或 `getPlatformVersionApi(api)` 可直接覆盖该路径时，tenantContext 必须按 HZERO baseline 自动闭合为 `source=getCurrentOrganizationId`、`resolverProvenance.symbol=getCurrentOrganizationId`、`resolverProvenance.importPath=utils/utils`、`definedInCurrentChange=no`、`userOrganizationUsage=forbidden`、`evidence=HZERO baseline + target project no-conflict scan`。不得向用户询问 `organizationId` 从哪个 helper 取。
- “项目等价 helper”必须是目标工程或 HZERO 已存在的导出符号，并记录 import path、symbol、文件行号证据；Implementation 不得为了通过契约检查而新建本地租户 resolver。
- `getCurrentOrganizationId()` 在 hzero-front 中返回当前租户 `tenantId`，不是后端 `CustomUserDetails.organizationId` 的“用户所属租户”语义。
- 不要用 `getUserOrganizationId()` 拼租户级 API 路径，除非 FDS/TDS/API 契约明确要求用户所属租户。
- `site` 级角色不应拼接当前租户路径；租户级角色才拼接 `/{organizationId}`。优先让 `getPlatformVersionApi(api)` 或项目 helper 处理。
- 附件下载、预览、上传相关 URL 优先复用 `getAttachmentUrl` / 项目附件组件能力；不要手写 `HZERO_FILE`、access token、`H-Request-Id` 或租户路径。

## 禁止项

- 硬编码 `tenantId`、`organizationId` 或默认租户 ID。
- 新建或使用本轮生成的 `getOrganizationId()`、`getTenantId()`、`resolveOrganizationId()`、`resolveTenantId()` 等本地 resolver 包装默认租户值。
- 使用 `DEFAULT_ORGANIZATION_ID`、`DEFAULT_TENANT_ID`、`MOCK_ORGANIZATION_ID`、`MOCK_TENANT_ID`、env/config 默认值或任意常量作为 production transport 的租户级 path variable。
- 在页面、DataSet 或 service 中直接读 `window.dvaApp._store.getState().user.currentUser.tenantId`。
- 用 `getCurrentUser().organizationId`、`getUserOrganizationId()`、`currentUser.organizationId` 作为租户级 API path variable。
- 同时手写 `/v1/${tenantId}` 又调用 `getPlatformVersionApi(api)`，造成租户路径重复。
- 在 mock/demo 中声称 tenant/organizationId 已生产闭合，但未说明真实来源、site/tenant 角色策略和生产替换项。
- 将后端 Controller 的 `{organizationId}` 命名误解为库存组织、业务组织或用户所属租户；业务组织字段必须另行确认，例如 `inventoryOrganizationId`、`companyId` 等。

## Design / Contract Check 要求

Frontend Design 必须在 Contract Status Matrix 或数据层设计中记录：

```text
tenantContext:
  required: yes / no / not-applicable
  apiPathVariable: organizationId / tenantId / none
  source: getPlatformVersionApi / getCurrentOrganizationId / project request helper / backend provided / not-applicable / missing
  resolverProvenance:
    symbol: getPlatformVersionApi / getCurrentOrganizationId / <project-helper> / not-applicable / missing
    importPath: utils/utils / <confirmed import path> / not-applicable / missing
    definedInCurrentChange: yes / no / unknown
    evidence: file path + line / HZERO baseline + target project no-conflict scan / not-applicable / missing
  rolePolicy: tenant-role-only / site-and-tenant / site-only / handled-by-helper / missing
  userOrganizationUsage: forbidden / required-by-business-contract / not-applicable
  status: confirmed / partial / generatedCandidate / missing / conflict / not-applicable
  evidence: file path + line / design source / backend contract
```

缺少 `tenantContext`，或 resolverProvenance 无法证明 helper 是目标工程/HZERO 已存在导出时，前端可调用契约不得标为 `confirmed`，production-ready 不得通过。仅缺用户手工确认但目标为 HZEROJS / hzero-front 标准工程、路径语义为当前租户 `organizationId`、且无冲突证据时，不得阻塞或提问，应使用 baseline `getCurrentOrganizationId` from `utils/utils` 并记录 no-conflict scan。

## Runtime Handoff

Task、Implementation、Review、Verification 和 mock-to-production replacement 必须继承 tenantContext；运行期 resolverProvenance、角色策略和 organizationId 取值检查集中在 `front-hzero-enterprise-process-control` 的 data-service runtime gates。

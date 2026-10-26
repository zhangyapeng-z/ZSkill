# HZERO 企业页面模式

## 阅读路由
- 判断是否只能输出 non-runnable 模式时读 `使用边界`。
- 生成页面骨架前读 `标准页面骨架`。
- 权限按钮、request/service/model 和上传导入导出分别读 `Permission Button 边界`、`request / service / model 边界`、`Upload / Import / Export 边界`。
- HZERO + Choerodon 组合页、列表到详情和详情加载读 `HZERO + Choerodon 页面`、`List To Detail Routing`、`Detail Page Data Loading`。
- mock/demo 或生产替换读 `Static Mock Boundary` 和 `Production Replacement List`。

## 使用边界
这些都是 non-runnable 页面模式。实现前必须确认模块位置、route/menu permission、i18n code、字段清单、API contract、上传/导入/导出协议以及项目包装层。

新增、修改、审查或设计企业页面时，先整理 `EnterprisePageContract`：子模块路径、路由/菜单、页面容器、i18n namespace、权限码、字段清单、接口契约、上传/导入/导出协议、Choerodon 边界和生产替换清单。缺失项用自然语言待确认，不生成 runnable-looking 占位代码。

自然语言页面名不是契约。不要从“供应商管理”“客户管理”这类名称推导 route path、permission action 名、service 函数名、i18n key、DataSet 字段或请求方法。

对于仅有自然语言的草案，优先输出 plan + non-runnable skeleton。在没有项目证据前，不要写出具体 service import、猜测的组件名、`transport` key、URL/method 占位、权限 action 后缀或附件配置 props。

示例中的尖括号占位 token 只表示缺失事实。不要把它们复制进面向用户的回答、注释或生成项目文件中；应将缺失事实改写为自然语言待确认项，例如“i18n namespace 待确认”或“按钮 permission code 待确认”。

## 标准页面骨架

```tsx
import React from 'react';
import { Header, Content } from 'components/Page';

export default function Page() {
  return (
    <>
      <Header title="<confirmedI18nOrTitle>" />
      <Content>
        {/* page content */}
      </Content>
    </>
  );
}
```

说明：
- 部分项目使用 `PageHeaderWrapper`；应遵循项目现有约定。
- 使用 HZERO `Header + Content` 时，`Header` 与 `Content` 必须作为 Fragment 下相邻根节点；不得用业务 `<div className="*-detail/*-page">` 包住整组 `Header + Content`。
- 页面级业务容器、section 背景、底部 padding 和滚动相关样式应放在 `Content` 内部；只有目标项目证据确认时才使用 `Content className` 或 `wrapperClassName`。
- 不得默认使用 `UrlHistoryProvider`、`HistoryProvider`、`ConfigProvider` 或自定义 Provider 包裹整组 `Header + Content`。只有 UI Contract、项目 `golden-baseline` 已按 `goldenBaselineStatus=confirmed` 和合法 `baselineConfirmationSource` 确认，或明确功能需求证明需要该 Provider 时才允许；相似页面中的 Provider 需要先按 baselineComparison 评级。
- 用户可见文案应遵循项目 i18n 约定。
- 添加页面代码前先确认 route/menu/permission。

## Permission Button 边界

```tsx
// Use front-hzero-permission-button for the fixed ButtonPermission entry and provider payload.
// Confirm permission code before rendering protected actions.
// Do not invent action suffixes without an action list; when actions are confirmed, HZERO button permission candidates use dot namespace, for example `sample.purchase-request.button.create`.
```

说明：
- 不要编造 permission code。
- 按钮 permission 应与 route/menu/action 语义保持一致。
- Header、PageHeader 或页面级操作区中的 `PermissionButton` 不适用 Table 行操作列的 `type="text"` 规则；C7N 场景下优先按项目相同位置规范使用 `type="c7n-pro"`。
- 只有 Table 行操作列中的 `PermissionButton` 统一使用 `type="text"`，包括详情页明细表、子表行操作列。

## request / service / model 边界

```ts
// service.ts
export async function confirmedServiceFunction(params) {
  // Implement request details only after the project contract is confirmed.
}
```

说明：
- 不要在点击事件里拼 request 协议。
- request/service/model 结构应与附近页面保持一致。
- 生产 service 默认使用目标工程 HZERO/project request helper，常见为 `utils/request`；不要默认直接使用原生 `axios`、`fetch` 或 `XMLHttpRequest`。
- HZERO request helper 默认视为已内置 `API_HOST` 拼接；service URL 通常使用已确认服务前缀（如 `HZERO_PLATFORM`、业务服务 key）+ API path，不要再手动拼 `API_HOST`，除非相邻项目代码或 request 封装证据证明必须显式拼接。
- 原生 HTTP 只有在需求文档或用户确认明确要求第三方直连、特殊二进制流、特殊 CORS 等场景时才可作为候选；目标项目既有原生 HTTP 代码只能作为实现参考，不能单独授权。需求文档未写时不要询问用户，默认使用 HZERO request。
- 不要新建 `getRequestBase()`、`buildRequestBase()`、`resolveRequestBase()`、`getApiBase()`、`getBaseUrl()` 等本地 base URL resolver 来替代项目 request/env/helper 契约。
- 如果使用 Choerodon DataSet，应在确认后把 CRUD 协议放进 DataSet `transport`。
- 不要导入或调用猜测出来的 service 函数，例如 `querySupplierList`、`createSupplier`、`updateSupplier`。
- 在接口证据出现前，不要写 `transport.read`、`transport.submit`、adapter 函数、URL 占位或 method 占位。

## Upload / Import / Export 边界

说明：
- 只有在项目/后端确认后，才补充 upload、import、export、template、endpoint 和附件标识细节。
- 不要编造 `bucketName`、`bucketDirectory`、`storageCode`、`templateCode`、endpoint 或租户规则。
- 对于 Choerodon attachments，组件/API 细节交给 `front-hzero-choerodon-ui`；HZERO 负责平台契约和页面边界。

## HZERO + Choerodon 页面
- HZERO owns module location, route/menu permission, page container, i18n, permission buttons, and platform contracts.
- Choerodon owns DataSet, Pro components, component API facts, and page pattern details.
- Keep DataSet pages inside HZERO page container and permission model. For `Header + Content`, keep them as Fragment sibling roots; put DataSet/Form/Table business wrappers inside `Content`, not around the HZERO page skeleton.
- Do not add `UrlHistoryProvider`, thin component adapters, `runtimeAdapters`, permission-button fallbacks, local `t()` / `intlLabel()` helpers, or one-off wrappers by default. Required permission buttons follow `front-hzero-permission-button`; other project components and `intl.get(...).d(...)` should be used directly unless a confirmed golden baseline proves the wrapper is the project standard. A wrapper/helper is allowed only when it carries real contract value, such as confirmed project compatibility, cross-file platform protocol reuse, version isolation, or permission/tenant/request/component API normalization; pass-through prop forwarding, import renaming, default-value wrapping, and hiding generatedCandidate/missing state are not valid reasons.

## List To Detail Routing
- Confirm route paths and URL parameter names before implementation.
- In UMI/HZERO pages, prefer project router props or confirmed tab/openTab API for navigation. Use `history.push({ pathname, search })` for ordinary in-app navigation when available.
- Detail pages should read query parameters from `location.search` or the project's confirmed route API.
- Do not manually assign `window.location.hash` for route navigation; it can append a new hash after the current hash and break nested micro frontend URLs.
- If the user requires independent tabs, confirm the HZERO tab API before forcing new-tab behavior. Route paths alone do not prove tab-opening semantics.

## Detail Page Data Loading
- For create/detail/edit shared pages, explicitly derive mode from confirmed URL parameters and status fields, for example create has no id, edit has id plus edit flag, detail has id without edit flag.
- Load and bind all confirmed detail parts: header/base form, line table, approval history, notify/remind records, attachments, or other child sections. If the API detail response includes child arrays, load them into their own DataSets rather than leaving child tables empty.
- Keep DataSet files close to their owning page. A page with one DataSet should usually keep `<name>DS.ts` next to `index.tsx`; use a page-level `stores/` folder only when the page owns multiple DataSets such as header/line/attachment/history, or when DataSet adapters/helpers need grouping. Feature-level `stores/` is acceptable only for real list/detail/shared-page reuse of fields, adapters, or factory functions. Do not share a runtime `DataSet` singleton across pages, and do not put mock runtime stores or direct local data sources in page `stores/`.
- Save/copy/create mock responses must return the confirmed id field so the page can navigate to a stable detail/edit URL and reload data.

## Static Mock Boundary
- When mock/demo is explicitly authorized, put static JSON under the target project's public/static convention or use the existing mock framework.
- When the user asks for mock requests/API mock and backend asset files are available, static JSON or the project's requestable mock mechanism is the default choice. In-memory arrays are only acceptable as internal helpers after the requestable JSON/mock source exists.
- Static mock requests in development should target current dev server origin, not the backend API host. Avoid request helpers that automatically prepend `API_HOST` unless they are configured for static assets.
- For real HZERO runtime environment values in page/service/runtime code, use `import { getEnvConfig } from 'utils/iocUtils';` and read confirmed keys such as service prefixes or `API_HOST`; do not hard-code env values or invent env keys. Static mock JSON should still prefer current dev server origin unless the project confirms a static asset host. HZERO request normally handles `API_HOST`; do not prepend it manually unless the project request wrapper requires an absolute URL.
- Keep mock constants and production replacement notes centralized; real permission codes, LovCode, bucket, templateCode, and i18n namespace still require production confirmation.

## Production Replacement List
- When temporary platform contracts are used, final delivery should include a concise replacement list.
- Cover at least: permission codes, LovCode, lookupCode, i18n namespace/key, attachment bucket/UUID protocol, import templateCode/error download, export configuration, and menu/Tab/openTab behavior.
- For each item, state current temporary value or strategy, what must be confirmed, who/source should provide it if known, and where to replace it in code.
- Carry this list across follow-up turns. If the user asks for later fixes or validation, keep reporting whether temporary platform contracts still exist, have been replaced, or cannot be inherited from context.

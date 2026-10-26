# HZERO Runtime Config Patterns

## 阅读路由
- 使用任何 runtime 配置样例前先读 `Runtime Notes`。
- app 初始化和 runtime export 边界读 `appInit Boundary`、`Runtime Export Boundary`。
- 布局、Header、工作台、用户菜单和插件扩展读 `Layout/Header Extension`、`Workbench / User Menu / Plugin Extension`。
- Choerodon 局部配置、route config、request/header 适配和环境变量读对应 Boundary 章节。
- 跨系统导航读 `Cross-System Navigation Boundary`。

## Runtime Notes
These are non-runnable runtime configuration patterns. Confirm project version, file locations, exported config shape, extension point names, and project conventions before applying.

Keep examples non-runnable unless backed by target-project evidence; do not include directly runnable `appInit`, default runtime export, or header extension exports without confirmed runtime keys.

## appInit Boundary

```ts
// Non-runnable skeleton only. Confirm the target project supports an app-level
// initialization runtime key before replacing this with project code.
// app-level initialization: project-wide initialization only
```

Use only after the target project confirms `appInit` is a supported runtime export. If generated `.umi/core/plugin.ts`, runtime valid keys, project runtime documentation, template evidence, or existing `app.tsx` does not confirm it, do not export it and do not present `export async function appInit()` as runnable code.

Use for:
- project-wide initialization
- tenant/session/bootstrap capability
- confirmed global data needed across modules

Do not use for:
- single-page query initialization
- button state
- form linkage
- page-local data loading

## Runtime Export Boundary

```ts
// Non-runnable skeleton only. Replace with a project-confirmed runtime export
// shape and keys before using in app.tsx.
// runtime configuration: project-wide behavior only
```

Notes:
- Keep project-wide behavior here.
- Do not put ordinary page business logic in runtime export.
- Confirm each config key from project source or maintained HZERO facts.

## Layout/Header Extension

```tsx
// Non-runnable skeleton only. Confirm the extension point name and return shape
// from project source before replacing this with project code.
// header/layout extension: confirmed extension item only
```

Notes:
- Confirm extension point name and return shape from project source.
- Header/layout entries should not depend on a business page render order.
- Confirm permission/tenant visibility if user-facing.

## Workbench / User Menu / Plugin Extension

```tsx
// Confirm the project-specific extension API, code, priority, entrySort, exposed key, and visibility rules.
```

Notes:
- Keep workbench cards and user menu items in runtime/layout extension points, not ordinary page code.
- Confirm whether the extension is contributed by the parent project or a submodule.
- If the UI is federated, confirm package name, exposed key, and whether `registerRegex` must load the contributing submodule.
- Use route config only for routing concerns, not for hiding extension or permission issues.

## Choerodon Local Configuration

```tsx
// Prefer local wrapper / ConfigProvider for module-local behavior.
// Use global configure only for confirmed project-wide behavior.
```

Notes:
- DataSet does not automatically receive React context; follow project `useDataSet` or constructor context patterns.
- Avoid calling global `configure` from a submodule for page-local behavior.

## Route Config Boundary
- Use route config for route registration, title, direct URL access, and override/priority behavior.
- Do not use route config to hide permission or micro-frontend loading problems.
- For HZERO-specific config, prefer `config/` and `hzeroMicro` where applicable.

## Request/Header Adaptation Boundary
- Keep global request interception limited to confirmed cross-cutting behavior.
- Prefer page/service-local handling for page-specific protocol differences.
- Confirm request hook names, request wrapper behavior, token/header policy, and affected modules from project source.
- Do not add broad interceptors for a single page requirement.

## Environment Config Access

```ts
import { getEnvConfig } from 'utils/iocUtils';

const { API_HOST } = getEnvConfig();
```

Use `getEnvConfig` when HZERO page, service, runtime, request, integration, or navigation code needs runtime environment variables such as `API_HOST`, `BASE_PATH`, public URL, tenant-aware gateway, or deployment-time host values.

Notes:
- Import path is `import { getEnvConfig } from 'utils/iocUtils';`.
- Prefer `getEnvConfig()` / confirmed `getEnvConfig('<KEY>')` usage over hard-coded environment values, direct `process.env.<KEY>`, or ad hoc `window` global reads in HZERO runtime/page code. Core utils commonly destructure values such as `ACCESS_TOKEN_NAME`, `HZERO_FILE` and `configureParams` from `getEnvConfig()`.
- Confirm the target env key name from project config, deployment values, existing code, or backend/platform handoff before using it; do not invent new keys.
- Distinguish runtime env from build-time env. Build scripts and config templates may still define placeholders, but runtime page/service code should read confirmed runtime values through `getEnvConfig`.
- Static mock JSON in dev should normally use current dev server origin, not `getEnvConfig('API_HOST')`, unless the project has a confirmed static asset host strategy.

## Cross-System Navigation Boundary
- Confirm whether the project supports `openTab`, route hooks, menu data helpers, or custom navigation wrappers.
- Only intercept navigation when the requirement is cross-page or platform-level.
- Confirm title, route path, query/state, tab uniqueness, token/origin, and session-expired behavior before changing navigation.

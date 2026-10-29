# Choerodon + HZERO Handoff

Use when HZERO has already fixed module location, route, permission, i18n, and page container.

## Minimal shape
- HZERO owns module boundaries, routes, permissions, page container, and platform contracts.
- Choerodon owns DataSet, Pro components, and page-level field modeling.

## Non-runnable skeleton
- HZERO side: module path, route/menu, permission code, i18n namespace, page container, and request helper待确认.
- Choerodon side: DataSet fields, query fields, columns, editors, Lov/Attachment/value-set modeling待确认.
- Transport/upload/export: only after HZERO contract and backend protocol are confirmed.

## Guardrails
- Do not set broad `registerRegex`, interface URLs, permission codes, `lovCode`, or `lookupCode` from this handoff pattern. Development routes may use project-conventional `authorized: true` only as a temporary access setting, and Handoff must remind maintainers to register menu and permission resources on the platform.

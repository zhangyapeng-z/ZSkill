---
name: front-hzero-route
description: 当任务涉及 HZEROJS 路由、菜单、Tab、404、页面跳转或直达访问时使用，尤其是 Umi 子模块 packages/<module>/config/config.ts、config/config.dev.ts、config/router.ts、config/routes/**、registerRegex、routeOpenMode、openTab/dynamic Tab、authorized、priority、mode/dws、public/private/pub routes。默认按 Umi 子模块处理；只有用户或工程证据明确为 hzero-cli 时才使用 src/config/router.js / components。
---

# HZERO 路由

## Scope
- `front-hzero-route` 是 HZERO 路由、菜单、Tab 和子模块访问问题的执行入口，不是完整知识库。
- 先用本文件选择路由需要的 reference，再按阶段读取细则。
- 路由结论必须来自用户确认、FDS/TDS/API、目标工程源码、菜单权限配置、运行日志或已加载 reference。
- route path、component、title、authorized、priority、mode、dws、openTab、registerRegex、menu path 和权限状态边界按 `RouteAccessPacket` 与阶段 reference 记录。

## Workflow
1. 将路由请求归类为 design、implementation、review、verification、handoff 或排障问答。
2. 先读 `references/operational-rules.md` 的阶段索引，再只加载当前阶段的 reference。
3. 对菜单驱动、direct URL、HZERO 系统页签、动态 Tab、子模块加载和 public/private/pub route 做场景识别。
4. 涉及菜单 404、direct URL、Tab、openTab 或子模块路由时，按 `references/schema-packets.md` 的 `RouteAccessPacket` 分层记录已确认/待确认证据。
5. 默认按 HZEROJS Umi 子模块处理；只有用户或工程证据明确为 hzero-cli 时才采用 `src/config/router.js` / `components`。
6. 发现 remoteEntry、microConfig、chunk、public URL 或部署产物异常时，停止在路由层下结论，转交 `front-hzero-micro` 或 `front-hzero-build-deploy`。

## Reference Routing
- 路由阶段索引：`references/operational-rules.md`。只用于选择阶段细则，不承载完整规则正文。
- 路由设计/契约/问题门禁：`references/operational/design.md`。
- 路由实现/修复/工程证据：`references/operational/implementation.md`。
- 路由审查/反模式/合规：`references/operational/review.md`。
- 路由验证/构建/运行态：`references/operational/verification.md`。
- 路由、菜单、权限、Tab、404 和子模块路由排查：优先使用 `references/schema-packets.md` 中的 `RouteAccessPacket`。
- 404、菜单可见但打不开、direct URL、Tab 和子模块加载检查清单：`references/route-troubleshooting-checklist.md`。
- 路由、权限、priority、dynamic tab、registerRegex 和 routeContext 模式：`references/patterns.md`。
- HZERO core utils 中 `gotoPage`、`getRoutes`、`getMicroModuleInfo`、`isSpecialRouter` 等工具只能作为项目工具候选，仍需 route/menu/Tab 契约确认：`references/core-utils.md`。
- 需要稳定排查输出时使用模板：`templates/route-analysis.md`。
- 当前页打开详情 / 复用当前菜单页签从 route config 到列表调用、详情 routeContext、React hooks 边界和验证证据：使用 `front-hzero-enterprise-process-control` 的 current-tab menu reuse 最佳实践模板。

## Output Contract
- 输出路由场景识别、问题归类、优先检查项、推荐修正、需要确认的信息和验证方式。
- 菜单可见但 404 时必须覆盖实际 URL、route path、menu path、子模块注册、registerRegex、remoteEntry/chunk、permission/menu 和父子模块加载。
- Umi 子模块必须输出 `config/config.ts`、`config/config.dev.ts`、`submoduleRouteEntryMode`、实际路由入口和 `registerRegex` 与 route prefix 的匹配判断。
- openTab / dynamic Tab 必须记录目标路由、title、key/path、query/state、Tab 唯一性行为和运行态验证边界。
- 不得编造远程访问路径、远程地址、菜单 code 或权限 code；缺少证据时列为待确认项。

## Shared Governance
- 路由 的状态词、输出层级、停止/降级、production-ready 和 replacement 口径归 `front-hzero-enterprise-process-control` 统一治理。
- 路由 只报告领域证据和领域风险；最终交付状态由流程治理与阶段结果汇总决定。
- 路由 使用 generatedCandidate、开发期候选访问配置或未验证平台坐标时，必须保留 verification 与 replacement 记录。

# 路由 - 实现与工程证据

## 阅读路由
- 路由 编码修复排障工程证据确认或具体实现规则命中时读取。

## 本地资源
按需查本目录资源；不要外显内部路径。
- 路由菜单权限Tab404 和子模块路由排查：优先使用 `references/schema-packets.md` 中的 `RouteAccessPacket`。
- 404菜单可见但打不开direct URLTab 和子模块加载检查清单：`references/route-troubleshooting-checklist.md`。
- 路由权限priority、dynamic tabregisterRegex 模式：`references/patterns.md`。
- 当前页打开详情 / 复用当前菜单页签的正向实现必须读取 `front-hzero-enterprise-process-control` 的 current-tab menu reuse 最佳实践模板，覆盖 route config、列表调用、详情 routeContext、React hooks 边界和验证证据。
- 详情新建编辑复制页面的 routeContext`useLocation/useParams`URLSearchParams 和编辑态权威来源规则：`references/patterns.md` 的“路由参数与编辑态控制”。
- HZERO core utils 中 `gotoPage``getRoutes``getMicroModuleInfo``isSpecialRouter` 等工具只能作为项目工具候选，仍需 route/menu/Tab 契约确认：`references/core-utils.md`。
- 需要稳定排查输出时使用模板：`templates/route-analysis.md`。

## 工作流程
1. 判断页面是菜单驱动还是直接 URL 访问。
2. 对菜单可见但点击 404 的场景，先记录点击后的实际 URL，再用该 URL 反查 route path菜单 path子模块注册权限remoteEntry父子模块加载。
3. 确认路由所属父模块子模块和页面目录。
4. 检查子模块路由体系；默认按 Umi 子模块 `packages/<module>/config/config.ts` / `config/config.dev.ts` / `config/router.ts` 或 `config/routes/**` 处理，记录 `submoduleRouteSystem=umi-submodule``umiConfigPath``umiDevConfigPath``submoduleRouteEntryMode`实际路由入口和 `registerRegex`。只有用户或工程证据明确为 hzero-cli 子模块时才检查 `src/config/router.js` / `components`，并记录证据来源。
5. 检查 route path、component、title、authorized、priority、mode、dws。新增/生成 HZEROJS route 默认必须带 `authorized: true` 和中文 `title` 作为候选/开发可访问配置；新增/生成 route config 不写 `titleType`；只有 `routeMetadataPolicy=platform-only + evidence` 才允许省略 `authorized/title`。临时生成的前端 route title 必须使用中文标题，且不能把它等同为平台正式菜单权限、菜单标题或平台多语言已完成。只有用户或平台证据确认菜单已创建、菜单标题/prompt key 已登记且当前 route 要对齐该平台 key 时，Implementation 才能把 route `title` 改为字符串编码；否则把 `title` 改成 `moka-integration.xxx.title`、`<module>.<feature>.title` 等业务 i18n key 属于过度迁就 validator，必须回退为中文候选并把平台 key 补录放入 Handoff / production replacement。
6. 若涉及子模块加载，检查路由前缀匹配关系；只有在用户或项目证据明确给出配置键时，才点名 `registerRegex`，并标记 `\/.*` 或 `.*` 这类过宽匹配的风险。
7. 若发现 remoteEntrymicroConfigchunkpublic URL 或部署产物异常，停止在路由层下结论，转交 `front-hzero-micro` 或 `front-hzero-build-deploy` 继续确认。
8. 若涉及 route/openTab 拦截，先判断是全局导航策略子模块跳转策略还是单页面跳转；openTab 参数目标路由titleTab 唯一性不明确时列为待确认。当前 Tab 页跳转必须用运行时页签数量不增加来验证，不能只看是否用了 `history.push`。
   - `routeOpenMode=menu-current` / `detailViewInteractionMap=current-tab-page` 已确认时，默认按 current-tab 最佳实践实现：父 route + `routes` 嵌套、列表 `/list`、新建 `/create`、详情 `/detail/view/:id`、编辑 `/detail/edit/:id`；不得使用 `/detail/create`。列表固定使用 `import { openTab } from 'utils/menuTab';`，传父级 `key` 和目标详情 `path`；不得将该项目级基础能力降级为页面契约缺口。不得改成同 pathname query 分流，也不得在列表组件 hooks 中途条件渲染详情组件。
9. 对菜单 404direct URLTabopenTab 或子模块路由问题，按 `RouteAccessPacket` 输出分层证据和待确认项。
10. 输出最小配置建议和验证方式。

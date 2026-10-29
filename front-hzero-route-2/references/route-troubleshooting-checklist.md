# 路由与权限排障检查清单

## 检查顺序
先整理 `RouteAccessPacket`：实际 URL、route path、menu path、component、authorized、permission/menu、registerRegex、remoteEntry/chunk、父子模块加载状态。后续结论必须标明哪些已确认、哪些待确认。

1. 页面是菜单驱动还是直接 URL 访问。
2. 如果菜单可见但点击 404，先记录点击后的实际 URL，并用该 URL 反查前端 route path。
3. 判断子模块路由体系：默认 Umi 子模块检查 `packages/<module>/config/config.ts`、`config/config.dev.ts` 和实际路由入口。仅一个路由文件时检查 `config/router.ts`；多路由文件或项目拆分模式检查 `config/routes/index.js`、FeatureRoute。只有用户或工程证据明确时才检查 hzero-cli `src/config/router.js` / `components`。
4. route path、component 和菜单路径是否一致。Umi 子模块还必须检查 route 是否保持标准 `routes` 结构：一级页面直接 `component`；多子页面使用父级 `routes` 嵌套；父级仅分组时不配 `component`。`split-routes-dir` 模式检查子路由完整绝对 path 和 `@/pages/...` component；`single-router-ts` 模式检查父级绝对 path、子级相对 path、包内页面相对 component 和 `config.ts` 是否引用 `./router`。
5. 子模块是否已注册到父模块，包名与父模块 packages 配置是否一致。
6. 权限是菜单权限问题、直接 URL 场景，还是误用了 `authorized: true`。
7. 如果是子模块页面，`registerRegex` 是否匹配路由前缀，且是否过宽。
8. remoteEntry、microConfig、页面 chunk 是否存在并可加载。
9. 父子模块路由数据是否实际加载到目标子模块。
10. Tab 标题、`mode`、`dws` 是否匹配场景，且新增/生成 route config 未写 `titleType`。
11. route/openTab 拦截是否属于全局导航策略、子模块跳转策略还是单页面跳转。

## 手册补充排查
- 可在浏览器控制台查看全局路由数据，例如 `window.dvaApp._store.getState().global.routerData`，确认目标 route 是否已加载到运行时。
- 如果 routerData 不包含目标路由，优先重新编译当前路由所在子模块。
- 对 Umi 子模块，先确认 route entry mode：`single-router-ts` 要求 `config/config.ts` 引入 `./router` 且 `routes: route`，`config/router.ts` 的 route prefix 与 `registerRegex` 一致；`split-routes-dir` 要求 `config/config.ts` 引入 `./routes` 且 `routes: [...routes]`，`config/routes/index.js` 聚合 FeatureRoute，FeatureRoute 的 route prefix 与 `registerRegex` 一致。不要先按 hzero-cli `components` 补配置。
- 不要为了排查或临时可达把标准 Umi routes 改成 hzero-cli `components`、自定义 router、相对 path、父级分组带 component 或父工程页面 component 路径。
- 如果目标路由来自依赖子模块，确认依赖已安装，并且 `.hzerorc` 或 `config/packages-config.js` 已配置子模块信息。
- 如果 routerData 包含目标路由，再判断它是否是菜单路由；菜单路由需要角色分配菜单权限。开发期新增路由可按项目惯例临时配置 `authorized: true`，但应标记为候选访问配置；非菜单直达路由才把 `authorized: true` 作为访问模式本身讨论。
- 单模块或父模块启动但相关子模块未编译时，目标页面可能无法访问。
- 修改子模块 routes、`config/config.ts`、`registerRegex` 或父工程 packages 注册后，Verification 补跑链路为重建目标子模块、刷新 `microConfig`，并记录重启 dev server / hard reload 的外部 runtime acceptance 或用户手工证据状态；缺外部运行态证据时只记录 `not-run-in-verification` 和未验证影响，否则 routerData 和微前端元数据可能仍是旧值。
- 老版本项目需要检查根目录 `src/getModuleRouters.js` 是否遗漏目标子模块路由。
- 如果路由包含加密参数，不同账号或重新登录后的旧加密参数可能导致 404，不要误判为路由配置错误。
- 低版本升级到高版本后，部分路由可能被弃用或修改，应使用新版本种子数据更新菜单，或根据目标子模块路由文件确认菜单是否应删除。

## 子模块菜单可见但点击 404 必查项
- route path、菜单 path、点击后实际 URL 必须同时比对。
- 子模块注册、父模块 packages 配置、`registerRegex`、remoteEntry/chunk、权限/menu 数据、父子模块加载边界必须分层说明。
- 输出应按 `RouteAccessPacket` 分层组织，不只给“检查权限”或“检查 remoteEntry”的单点结论。
- 验证步骤必须按 URL 与菜单、route 与 component、子模块注册与 `registerRegex`、remoteEntry/chunk、权限/menu 数据、父子模块加载分层输出。
- 不把新增 `authorized: true` 作为菜单 404 的修复建议；开发期候选配置必须同时说明平台菜单和权限资源仍需维护。
- 不编造远程访问路径、远程地址、菜单 code 或权限 code；没有证据时写为待确认。

## 子模块菜单 404 验收基线
- 通过：输出结构包含问题归类、优先检查项、推荐修正、需要确认的信息和验证方式。
- 通过：输出命中 HZERO 路由、微前端、权限联合排查，而不是单一权限或单一资源结论。
- 通过：输出同时覆盖 route path、菜单 path、子模块注册、remoteEntry/chunk、`registerRegex`、权限/menu 数据、父子模块加载。
- 通过：输出覆盖 Umi routes 结构、父级 component 使用、子路由绝对 path、`@/pages/...` component 和路由变更后的 build / microConfig refresh / hard reload。
- 通过：输出包含分层验证步骤，且验证链路从点击后 URL 延伸到 route/component、子模块注册、远程资源、权限/menu 数据和父子模块加载。
- 失败：输出结构缺少问题归类、优先检查项、推荐修正、需要确认的信息或验证方式。
- 失败：默认建议新增 `authorized: true` 修复菜单可见但点击 404。
- 失败：为了排查问题建议或保留非标准 routes 结构，或修改 routes 后未要求重建子模块和刷新 microConfig。
- 失败：编造远程访问路径、远程地址、菜单 code、权限 code 或环境 URL。
- 失败：只输出“检查权限”或“检查 remoteEntry”这类单点建议，未覆盖完整链路。

## 检查点
- `authorized: true` 是否被误用。
- 菜单驱动页面不应通过新增或保留 `authorized: true` 规避权限或 404 排查；开发期已有临时配置时，检查它是否进入交付维护清单。
- 点击后的实际 URL 是否与 route path 完全一致。
- 菜单 path 是否指向了不存在的父路径、子模块前缀或部署前缀。
- 子模块 name 是否与父模块 packages 注册项一致。
- 子模块构建产物是否包含 `remoteEntry.js`、路由数据和页面 chunk。
- `registerRegex` 是否收敛到已确认路由前缀；`\/.*`、`.*` 只能在首屏加载或遗留兼容已确认时保留。
- 是否避免在新增/生成 route config 中写 `titleType`。
- 前端临时生成 route title 是否使用中文标题；是否误把 title 编码作为临时生成值，或误把中文 title 当作生产平台多语言已完成。
- 父级 `routes` 容器是否误配置 `exact: true`；新增/生成 route 是否默认省略 `exact`，若因项目证据显式写 `exact`，是否验证 list/detail/create/edit 等子路由可匹配。
- 动态详情页是否需要 `mode: 'dynamic'`。
- 同 pathname 不同 search 是否需要 `dws: true`。
- openTab 参数、`key` 类型（父级 key / 详情级 key）、目标路由、title、query/state 和 Tab 唯一性是否来自项目证据。
- `openTab.key` 和 `path` 是否都能被 route config 匹配；是否存在 `key` 比 `path` 多 `/edit`、`/view` 等未注册后缀的虚拟 key。
- 固定 `openTab.key` 是否被误判为固定页签复用；若 `path` 携带不同记录 id 或 pageMode，必须通过运行态证明平台不按 path 多开，否则不得声明 reusable。
- `routeOpenMode=hzero-openTab-reusable-fixed-path` 时，是否使用固定 create path + 固定 detail path，record id/pageMode 是否来自 confirmed tab context，是否验证连续点击不同记录详情页签数量不增加。
- query/search 是否只承载筛选、分页、排序、来源、返回、详情内子 Tab 或 navigationToken；是否误承载页面主身份、目标详情页主记录 ID、页面模式或 HZERO Tab 唯一身份。
- 普通菜单 route 的 `authorized: true` 或前端中文 `title` 是否符合项目生成约定，且未被误写成平台菜单权限、菜单标题或平台多语言已完成；`authorized: true` route 是否缺 `title`。
- `routeOpenMode=menu-current` 时，是否已确认 `parentTabKey`、`targetDetailPath`、`mode=route/default` 并已消费固定 `import { openTab } from 'utils/menuTab';`；点击详情/编辑前后 `window.tabsAction.getTabs()` 数量是否不增加；同级独立详情 route + `history.push('/detail')`、详情级 key、`mode: 'dynamic'` 或只靠父子 `routes` 嵌套不能单独作为通过证据。
- `routeOpenMode=menu-current` 时，是否按 current-tab 最佳实践使用父 route + `routes` 嵌套、列表 `/list`、新建 `/create`、详情 `/detail/view/:id`、编辑 `/detail/edit/:id`、父级 `openTab.key` 和目标详情 `path`；是否误用 `/detail/create`、`/list?pageMode=...&id=...` 或在列表组件 hooks 中途 query 分流渲染详情。
- `routeOpenMode=hzero-openTab-path-params` 时，是否已说明该模式只证明 create/view/edit route 可匹配，不保证一个详情页签被复用。
- `routeOpenMode=dynamic-tab` 时，是否已确认 `mode=dynamic`、详情级 key/path、tabTitle、`keyPathRoutable=true`；同 pathname 不同 search 独立 Tab 是否配置 `dws=true`。
- 详情/编辑/新建需要各自独立 Tab 时，是否采用内置 `/create`、`/detail/view/:id`、`/detail/edit/:id` path 参数，并保持 `openTab({ key: path, path })`；是否误用 `/detail/create`；若只靠 `?editFlag=true/false`、`?mode=edit/view`、`?action=create`，是否已报告 migration finding 并迁移，而不是保留 query fallback。
- 子模块路由变更后是否已运行已确认的 `npm run build:ms -- <module>`、刷新 `microConfig`，并记录重启 dev server / hard reload 的外部 runtime acceptance 或用户手工证据状态；未确认脚本存在时是否列为候选而非已执行。

## 常见风险
- 用 `authorized: true` 掩盖菜单权限或子模块加载问题。
- 用全量 `registerRegex` 掩盖子模块路径不匹配问题。
- 只给单点结论，未分层验证 route、菜单、子模块注册、remoteEntry/chunk、权限和父子模块加载。
- 编造远程访问路径、远程地址、菜单 code 或权限 code。
- 菜单可见只说明菜单记录/角色侧大概率存在，不证明 route path、子模块加载或 remoteEntry 正确。
- 路由前缀和 `registerRegex` 不一致。
- 错误 Tab 配置导致页面复用或标题异常。
- route 未注册的虚拟 `openTab.key` 导致空白内容页签，关闭空白页签后露出原先页签。
- 把正常列表筛选、分页、排序或来源/返回 query 误判为路由反模式；真正反模式是 query 承载页面主身份、目标详情页主记录 ID、页面模式或 HZERO Tab 唯一身份。
- 用 route/openTab 拦截掩盖菜单权限、路由注册或子模块加载问题。
- 非标准 Umi routes 结构导致路由无法聚合、父子路由行为不清或微前端路由数据未刷新。

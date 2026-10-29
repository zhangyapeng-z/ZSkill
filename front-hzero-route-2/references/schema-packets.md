# HZERO 证据包 Schema

## 目录
- 证据包使用边界
- RouteAccessPacket
- MicroFrontendPacket
- BuildStagePacket
- EnterprisePageContract
- RuntimeConfigPacket

## 证据包使用边界
本文件用于约束 HZERO 排查和交付中的输入、证据、输出和验证边界。

证据包中的字段可以是“已确认”或“待确认”。缺少证据时应输出自然语言待确认项，不要用包名、页面名、菜单名或环境名推导可运行配置。

## RouteAccessPacket
用于菜单 404、direct URL、Tab、权限、路由覆盖和子模块路由排查。

必查字段：
- 实际 URL：用户点击菜单或直接访问后浏览器中的真实 URL。
- route path：前端路由配置中的 path。
- menu path：后端菜单或菜单种子中的 path。
- routeOpenMode：`menu-current / hzero-openTab-path-params / hzero-openTab-reusable-fixed-path / dynamic-tab / browser-new-tab / direct-url`，以及 Tab key、Tab title、mode、dws、query/state 唯一性；HZERO 应用内 Tab 不等于浏览器 `window.open`。`menu-current/current-tab-page` 若通过 `openTab` 实现，必须记录 `parentTabKey`、`targetDetailPath`、`mode=route/omitted-default-route` 和固定 `navigationApi=builtin-standard: import { openTab } from 'utils/menuTab';` 的消费事实；`hzero-openTab-path-params` 必须记录 create/view/edit 是否进入 path/params，并说明该模式只证明 route 可匹配，不证明详情页签必然复用；`hzero-openTab-reusable-fixed-path` 必须记录固定 create path、固定 detail path、contextSource、refreshMechanism、missingContextBehavior、tabTitlePolicy 和连续点击不同记录的页签数量验证；`dynamic-tab` 必须记录 `tabIdentityPolicy=route-path-exact`、详情级 concrete `targetPath`、`keyPathRelation=key===path`、`mode=dynamic`、`keyPathRoutable=true/false`、`recordIdSource`、`pageModeSource`、`runtimeTitleSource` 和 `titleFormat`，FDS/TDS/用户明确要求同 pathname 不同 search 独立 Tab 时记录 `dws=true`。dynamic-tab 的 key 与 path 必须从同一个已匹配 concrete path 得到，不得分别以记录 ID、标题、虚拟 mode 后缀或旧 path 构造；运行时标题必须来自本次点击记录或确认的详情回读中的同一业务显示字段。详情/编辑/新建等页面模式需要独立 Tab 时，必须记录页面模式是否进入内置 path/params：`/create`、`/detail/view/:id`、`/detail/edit/:id`；`/detail/create` 属于违规路径。必须记录是否保持 `key === path`；query/search 若存在，必须记录它承载的是筛选、分页、排序、来源、返回、详情内子 Tab 或 navigationToken，还是误承载页面主身份、目标详情页主记录 ID、页面模式或 HZERO Tab 唯一身份。
- 子模块名/路由前缀：若页面位于 HZERO 子模块或 `packages/<module>`，必须区分“项目已有父路径”和“无父路径使用子模块名前缀”。已有父路径时 route path 与 menu path 沿用父路径，不额外叠加子模块名；无父路径时才以子模块名作为第一段路径。候选路径来源不清时列为待确认，不得直接确认。
- component：路由实际加载的组件路径或懒加载入口。
- tsconfig paths：目标工程或子模块 `compilerOptions.baseUrl` / `paths` 是否影响 component、`@/*`、`@@/*`、`components/*` 或 `utils/*` 的 import 解析。
- authorized：是否是已确认的 direct URL、菜单外访问场景，或开发期新增路由的候选访问配置；候选配置不得替代正式菜单和权限维护。
- permission/menu：菜单权限、角色分配、按钮权限或权限数据是否已确认。
- registerRegex：子模块路由前缀匹配规则及是否过宽/过窄。
- remoteEntry/chunk：目标子模块远程入口和页面 chunk 是否存在并可加载。
- 父子模块加载状态：父工程是否注册并实际加载目标子模块路由数据。

输出要求：
- 菜单可见但点击 404 时，必须同时覆盖实际 URL、route path、menu path、子模块注册、registerRegex、remoteEntry/chunk、permission/menu 和父子模块加载。
- 新增子模块页面的 route/menu 候选必须检查父路径和子模块名前缀：项目已有父路径时使用 `/<parent>/<feature>`；没有父路径时使用 `/<module>/<feature>`；不得生成来源不明的 `/<feature>`，也不得把已有父路径错误改成 `/<module>/<parent>/<feature>`。
- 设计阶段未确认 routeOpenMode 时，新增页面默认只能按 `menu-current generatedCandidate` 记录；不得默认实现独立 `openTab`、`mode: 'dynamic'` 或浏览器新标签页。当前 Tab 详情若选择 `menu-current`，必须继续确认父级 `key`、目标详情 path 和 `mode=route/default`，不能只凭嵌套路由或 `history.push` 声明成立。
- FDS/TDS/用户只写“新标签页”时，输出 `ambiguous-new-tab` 待确认项；面向用户提问必须默认展示 `新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页`，以及流程允许时的 `当前菜单页签内打开（变更 FDS）`。标题保持短且稳定，不得标记“推荐”，描述必须详细说明页面行为、适用场景、限制、内部映射和验证影响；任何特殊要求、前置条件、字段缺口、适用例外、生产替换或后续确认要求都必须写进对应选项描述，不得只写在内部记录。不得只给技术枚举或短句；不得把 `hzero-openTab`、`dynamic-tab`、`browser-new-tab`、`HZERO openTab`、“系统页签打开”、“通过 openTab 打开标签页”或“系统动态页签”作为用户可见选项标题。参考子模块、相似页面、工程 evidence 或 routeConfig 不得裁剪、合并、排序或改写这些内置选项；唯一允许影响用户选项集合的参考证据，是同类参考模块在相同入口/目标上存在可采纳且覆盖当前 question 全部入口的 Drawer 实现，此时可追加唯一一个 `抽屉打开` 并标明会变更 FDS。必须记录 `referenceEvidenceInfluence=drawer-option-only`、`overlayEvidence=reference-drawer` 和参考证据；部分入口适用时拆组。不得从参考模块生成 Modal/弹窗选项。普通 route-page、编辑页或详情页的当前页选项必须写 `当前菜单页签内打开`，并使用 `/create`、`/detail/view/:id`、`/detail/edit/:id` 内置 route 模板。`openTab` 只能作为内部导航 API 记录，必须结合父级 key / 详情级 key / 记录级 key 判断当前页复用、可复用独立系统页签或记录级独立系统页签。确认前 `routeOpenMode` 只能是 `generatedCandidate/needs-confirmation`，`detailViewInteractionMap` 不能写 confirmed。
- FDS/TDS/用户写“点击跳转至新建页面 / 点击跳转至编辑页面 / 跳转至对应数据的编辑页面 / 跳转到详情页面”时，记录为 route-page 页面跳转语义；若打开方式仍未确认，按 Open Interaction 模板询问当前菜单页签、系统页签、记录级独立系统页签或浏览器新标签页。参考子模块、相似页面、工程 evidence、routeConfig、`openTab` 或 `mode: dynamic` 默认只能作为内部候选证据；只有满足同类、同入口/目标、可采纳且覆盖全部入口的参考 Drawer 证据时，才可额外引入唯一一个 `抽屉打开` 候选。不得引入 Modal/弹窗候选。
- Open Interaction 的路由/页签类选项默认全部展示：`当前菜单页签内打开`、`新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页`。不得因为当前资料暂缺记录 id、业务单据 id、业务标题、`dws/queryStateKey` 或同 route 多实例证据而隐藏 `每条记录新开独立系统页签`；缺口写入选项描述和记录要求，选择后先保持 `generatedCandidate/needs-confirmation`，补齐后才可 confirmed。其它选项如存在特殊要求、适用例外或后续确认要求，也必须写进对应选项描述。
- 不得把 route config 无法匹配的 `openTab.key` 当作 Tab 唯一性方案。若 route 只有 `/detail/:id`，但打开时使用 `key=/detail/1/edit`、`path=/detail/1`，必须标记 `keyPathRoutable=false` 和 `virtualKeySuffix` 风险；若实际出现空白页签、关闭后恢复旧页签，应优先按 key/path/route 不一致排查。`?editFlag=true/false`、`?mode=edit/view`、`?action=create` 不能作为页面模式或 fallback 读取；命中时必须迁移到 path 中已确认的 `pageMode`。
- `browser-new-tab` 只用于外部链接或明确浏览器级新标签页；内部 hash route 使用 `window.open('#/...', '_blank')` 必须判为反模式或待确认。若 browser-new-tab 确认成立，`window.open` 目标也必须是完整 URL，不得是 `hashPath`、`#...`、`/#...` 或 pathname/search 片段。
- 不把新增 `authorized: true` 作为 404、菜单权限、子模块加载或 route path 问题的修复结论；开发期新增路由若按项目惯例临时使用，必须标记为候选访问配置并进入 Handoff 替换/维护清单。
- 路由 component 或非标准 helper import 不能只按字符串猜测；存在 tsconfig paths 时必须把 alias 解析证据列入候选，仍需确认目标文件存在。`openTab` 例外：固定使用 `import { openTab } from 'utils/menuTab';`，它是项目级基础能力，不形成页面级 import 缺口或用户确认。

## MicroFrontendPacket
用于 remoteEntry、chunkError、子模块白屏、跨模块组件和运行时远程加载问题。

必查字段：
- `PACKAGE_PUBLIC_URL`：静态资源根路径来源。
- `packages/microConfig.json`：远程元数据文件是否存在、是否含目标包。
- `window.mfRemotes`：运行时远程地址是否包含目标包。
- remoteEntry URL：实际访问 URL，必须来自 microConfig、mfRemotes、部署说明或 Network 失败请求。
- 构建产物路径：目标包构建输出中是否存在 `remoteEntry.js` 和页面 chunk。
- 远程访问路径：目标环境可访问路径和静态资源服务路径。
- Network 失败请求：浏览器 Network 中失败的真实 URL 和状态。
- exposes/消费 API：跨模块组件的 exposed key 和加载方式是否已确认。

输出要求：
- `PACKAGE_PUBLIC_URL`、构建产物路径、microConfig、`window.mfRemotes`、remoteEntry URL、远程访问路径和 Network 失败请求必须分别确认，不得相互推导。
- 不依据包名、路由名、菜单名或环境名编造远程地址。

## BuildStagePacket
用于构建、启动、子模块编译、增量构建和产物态验证。

必查字段：
- 阶段分类：本地开发服务/HMR、父模块构建、子模块/微包编译、产物部署、运行时加载或增量构建。
- 包管理器和执行目录：来自项目 scripts、lockfile 或用户确认。
- scripts/tooling：已确认命令和候选命令分开记录。
- 目标模块/包名：父工程、子模块、微包或共享包。
- 构建参数/环境变量：如 public path、增量构建变量或 HZERO tooling 参数。
- 产物路径：构建输出目录、`packages/microConfig.json`、`remoteEntry.js`、chunk。
- 验证结论：dev server/HMR、lint/typecheck、build/compile、Network/browser 中哪些已验证，哪些未验证。

输出要求：
- 候选命令必须标注“待确认”或“项目证据不足”，不能写成已确认命令。
- dev server/HMR 只能证明开发态可用，不能替代 build/compile 或交付验收判断。

## EnterprisePageContract
用于 HZERO 企业页面新增、修改、审查和 HZERO + Choerodon DataSet 组合页面。

必查字段：
- 子模块路径和页面目录。
- 路由/菜单入口、Tab/openTab 行为和 direct URL 边界。
- 页面容器：`Header + Content`、`PageHeaderWrapper` 或项目封装。
- i18n namespace/key 和 `formatterCollections`。
- 权限码：菜单权限、按钮权限、`Permission` / `permissionList` 约定。
- 字段清单：字段名、label、类型、必填、展示/查询/提交归属。
- 接口契约：service/model、request 协议或 DataSet transport。
- 上传/导入/导出协议：bucket、UUID、templateCode、endpoint、错误下载、轮询策略。
- Choerodon 边界：DataSet、Pro Form/Table、Lov、Attachment 等交给 Choerodon 规则确认。
- 生产替换清单：临时 mock/demo 契约最终需要替换的权限、字段、接口、i18n、LOV、上传和导入导出项。

输出要求：
- 生产契约缺失且用户未明确授权 mock/demo 时，只输出待确认项和非 runnable 结构，不生成看似可运行的权限码、service/helper、DataSet transport、上传协议或本地业务 mock。
- HZERO owns 工程、路由、权限、i18n 和平台契约；Choerodon owns DataSet 与 Pro 组件细节。

## RuntimeConfigPacket
用于 `app.tsx`、`routes-config.tsx`、layout/header/workbench 扩展、局部 wrapper 和 Choerodon 配置作用域。

必查字段：
- 配置入口：`app.tsx`、`routes-config.tsx`、`config/`、layout extension、局部 wrapper 或页面代码。
- 作用域：父工程全局、子模块局部、页面局部、角色/租户局部。
- runtime export 是否确认：如 `appInit` 是否是目标项目 runtime valid key。
- 项目版本证据：模板、现有源码、生成的 runtime valid keys 或项目文档。
- 扩展点可用性：header/layout/workbench/user menu/plugin extension 是否存在。
- 跨模块污染风险：全局 request、全局 `configure`、layout wrapper 或运行时 hook 是否影响其他模块。
- 验证方式：lint/typecheck、构建候选、手工检查，以及外部 runtime acceptance / 用户手工证据中的 dev server restart、HMR/browser 状态；普通 Verification 不启动服务或浏览器。

输出要求：
- 未确认 runtime valid key 前，不输出可运行 `export async function appInit()`。
- 普通页面业务逻辑应回到页面、service/model、DataSet 或局部 wrapper。

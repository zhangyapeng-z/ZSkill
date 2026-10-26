# 路由 - 验证与运行态

## 阅读路由
- 路由 验证构建浏览器检查运行态判定或输出检查时读取。

## 输出检查清单
- 路由场景识别。
- 问题归类优先检查项推荐修正需要确认的信息验证方式。
- 菜单可见但 404 时覆盖：实际 URLroute path菜单 path子模块注册路由前缀匹配remoteEntry/chunk权限/menu 数据父子模块加载，并原样写出 `子模块注册``分层验证` 或 `验证步骤`。
- 输出必须围绕 `RouteAccessPacket` 分层记录已确认/待确认，避免只给权限remoteEntry 或 route path 单点结论。
- 菜单权限`authorized`Tab 标题和动态 Tab 判断。
- Umi 子模块必须输出 `config/config.ts``config/config.dev.ts``submoduleRouteEntryMode`实际路由入口和 `registerRegex` 与 route prefix 的匹配判断。仅一个新增路由文件时可使用 `single-router-ts`：`config/router.ts` + `config.ts import route from './router'` + `routes: route`；多路由文件或项目明确拆分时使用 `split-routes-dir`：`config/routes/index.js` + FeatureRoute + `config.ts import routes from './routes'` + `routes: [...routes]`。`config.dev.ts` 缺失会影响子包独立 `start/package-start`，除非有明确项目证据证明该子模块不支持独立启动；hzero-cli 子模块必须输出明确证据来源，否则不得推荐 `src/config/router.js` / `components`。
- Umi 子模块路由必须检查标准 `routes` 结构：普通一级页面直接 `component`；列表/详情/新建/编辑等子页面使用父级 `routes` 嵌套；父级仅分组时不配置 `component`；新生成子模块 route config 不配置任何 `redirect` route；新增/生成 route 默认不显式写 `exact`，只有目标项目现有路由模式或明确证据要求时才写；父级 `routes` 容器不得配置 `exact: true`，并必须验证子路由可匹配。新生成子模块页面默认落到 `src/pages`，`single-router-ts` pages 目录模式可使用 `Requisition/List`、`./Requisition/List` 或 `@/pages/Requisition/List`；`split-routes-dir` 模式通常使用 `@/pages/...`。只有 Target Placement 记录 `pageRoot=src/routes` 且 `pageRootSource=project-evidence/adjacent-module/user-confirmed` 时，才允许用 `@/routes/PrmRequisition/List` 这类项目别名；无参考基线`pageRootSource=asset-baseline/missing` 或缺合同不得生成 `src/routes/**`；完全禁止用 `./routes/...` 冒充 `src/routes`，它会被 Umi 解析成 `src/pages/routes/...`。`../src/pages/...` 这类从 route config 文件位置反推的文件系统相对路径必须判为失败。
- 菜单 path 保留父级 path 时，新增实现必须验证菜单/openTab/navigation/返回列表入口进入真实列表 path；不得新增同父级 path redirect 子路由、父级 `redirect + routes` 或单独叶子 redirect。存量 legacy redirect 必须记录 evidence，并用真实 URL 验证 `/list``/create``/detail/view/:id``/detail/edit/:id` 能命中页面 component，而不是只显示父级标题、显示 404 title、内容区空白或被 redirect 截断；`/detail/create` 命中即 failed。
- 新增/生成 HZEROJS route 默认必须带 `authorized: true` 和中文 `title`，但输出必须标记为开发期/候选访问配置，并在 Handoff 或生产替换清单中提醒后续到平台菜单管理维护正式菜单、权限资源、按钮权限、菜单标题和平台多语言；新增/生成 route config 不写 `titleType`。只有平台菜单已创建、菜单标题/prompt key 已登记且有用户/平台证据确认时，才能把 route `title` 调整为该平台字符串编码；否则验证阶段不得为了清除 `c7nComponentApiValidator` / i18n finding 把 route `title` 从中文候选改成业务 i18n key。机械放行已确认平台 title key 时，运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_submodule_config.py --root <frontend-root> --module <module> --allow-confirmed-platform-title-key --route-metadata-evidence <evidence-file>`，证据文件需包含目标 module、`routeTitlePolicy=platform-menu-confirmed`、平台菜单标题/prompt key 来源和确认状态。只有 `routeMetadataPolicy=platform-only + evidence` 才允许省略 `authorized/title`；运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_submodule_config.py --root <frontend-root> --module <module> --allow-platform-only-route-metadata --route-metadata-evidence <evidence-file>` 放行该省略例外，证据文件需包含目标 module、`routeMetadataPolicy=platform-only`、platform-menu/routeConfig 来源和确认状态。
- 修改子模块路由`config/config.ts``registerRegex` 或父工程包注册后，输出必须包含重建子模块、刷新 `microConfig`、以及重启 dev server / hard reload 的外部 runtime acceptance 或用户手工证据状态；缺外部运行态证据时，写 `not-run-in-verification`、未验证影响和用户自测提示，不默认启动服务或浏览器；`node scripts/refreshMicroConfig.js` 只有脚本存在或项目文档确认时才写为已确认命令。
- openTab 参数目标路由titlequery/stateTab 唯一性行为；固定 `key` 不能单独证明可复用，必须结合 `path` 和运行态页签数量判断。
- 当前 Tab 页详情必须确认父级 `key`目标详情 path`mode=route/default`；动态详情 Tab 必须确认详情级 key/path`mode=dynamic``dws/queryStateKey`。
- 当前 Tab 页详情必须按 current-tab 最佳实践验证：点击新建/查看/编辑前后 HZERO 应用内 Tab 数量不增加，active key 仍为父级 key 或项目确认等价 key，pathname 进入真实 `/create`、`/detail/view/:id` 或 `/detail/edit/:id`；`/detail/create` 命中即 failed，search 不承载 pageMode 或主记录 id。只运行 typecheck/build 时该项只能为 `not-run`。
- `hzero-openTab-reusable-fixed-path` 必须验证 create 固定 path 独立打开，view/edit 固定 detail path 复用，连续点击不同记录详情页签数量不增加，保存后 create tab 关闭或切换到 edit detail tab，刷新固定 detail path 时缺 context 行为明确。
- 动态详情 Tab 的 `key``path` 都必须是 route config 可匹配的真实路径，并且必须由同一个 concrete target path 直接得到，验收为 `key === path`；详情/编辑/新建需要独立 Tab 时必须采用 `/create``detail/view/:id``detail/edit/:id` 这类内置 path 参数范式；`detail/create` 命中即 failed。不用记录 ID、未注册的 key 后缀、旧 path 或单纯 query/search 制造页签身份。query/search 可用于列表筛选分页排序来源返回详情内子 TabnavigationToken 等辅助状态，但不得承载页面主身份目标详情页主记录 ID页面模式或 HZERO Tab 唯一身份。
- 动态详情 Tab 的运行态验收必须对同一记录同一模式连续点击两次，确认只保留一个对应 path 的系统页签；再分别打开同一记录的 view/edit，确认两个 path/页签独立且各自标题来自本次点击记录的确认业务显示字段，标题格式符合合同（例如“申请编号 - 详情/编辑”）。记录 `tabsAction.getTabs()` 或项目等价页签快照的前后数量、active key/path、可见标题和 Console/Network 结果；只运行 typecheck/build 时这些项只能为 `not-run`。
- 不得编造远程访问路径远程地址菜单 code 或权限 code；缺少证据时列为待确认项。

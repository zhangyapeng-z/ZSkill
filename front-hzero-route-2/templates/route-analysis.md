# 路由分析输出模板

## 场景识别
- 菜单页面 / 直接 URL / 动态详情 / Tab 问题 / 404 排障
- 点击后的实际 URL：
- 是否菜单可见但点击 404：

## 问题归类
- 

## 优先检查项
- 

## 推荐修正
- 

## 需要确认的信息
- 

## 验证方式
- 

## 路由与权限判断
- route path：
- component：
- 菜单 path：
- route path 与菜单 path 是否一致：
- menu / permission 证据：
- `authorized` 是否存在：
- `authorized` 是否符合场景：
- 普通菜单 route 的 `authorized: true` / 前端中文 `title` 是否符合项目生成约定，且未被误写成平台菜单权限、菜单标题或平台多语言已完成：
- `authorized: true` route 是否配置 `title`，且未新增 `titleType`：

## 子模块路由体系
- submoduleRouteSystem：umi-submodule / hzero-cli-submodule / parent-app-route / unknown
- 子模块类型证据：用户指定 / config/config.ts / config/routes / src/config/router.js / 相邻模块 / 其他
- Umi config path：`packages/<module>/config/config.ts` / not-applicable / missing
- Umi dev config path：`packages/<module>/config/config.dev.ts` / not-applicable / missing
- Umi route entry mode：single-router-ts / split-routes-dir / unknown
- Umi routes 聚合入口：`packages/<module>/config/router.ts` / `packages/<module>/config/routes/index.js` / not-applicable / missing
- 父级 `routes` 容器 exact：新增/生成 route 默认省略；不得为 `exact: true`；若因项目证据显式写 exact，是否验证子路由可匹配：
- 子路由匹配验证：已验证 / 待验证 / 不适用
- FeatureRoute 文件：`packages/<module>/config/routes/<FeatureRoute>.js` / not-applicable(single-router-ts) / missing
- 是否误用 hzero-cli `components`：
- hzero-cli 证据来源：

## Umi Routes 结构检查
- routeShape：一级 component / 父级 routes 嵌套 / 非标准 / unknown
- 父级 route 是否仅分组：
- 父级分组是否错误配置 component：
- 子路由 path 是否完整绝对路径：
- component 是否统一 `@/pages/...`：
- 是否为了排查临时改成非标准结构：
- `authorized: true` 是否只是开发期候选访问配置：

## 子模块注册与加载
- 所属父模块：
- 所属子模块：
- 子模块是否注册到父模块：
- 子模块包名与父模块 packages 配置是否一致：
- `registerRegex`：
- `registerRegex` 是否过宽或过窄：
- 父子模块路由数据是否命中目标子模块：
- remoteEntry 是否存在并可加载：
- microConfig 是否包含目标子模块：
- 页面 chunk 是否存在并可加载：
- 是否需要转交 `front-hzero-micro` 或 `front-hzero-build-deploy`：

## 路由变更后验证
- 子模块重建命令：`npm run build:ms -- <module>` / not-run + reason；HZEROJS Umi 子模块不接受 yarn、pnpm 或其它 build 命令替换
- `microConfig` 刷新：`node scripts/refreshMicroConfig.js` / 项目等价命令 / not-run / unknown
- dev server 是否已重启：
- 浏览器是否 hard reload：
- 运行时 routerData 是否包含目标 route：

## 子模块菜单可见但 404 分层验证
- URL 与菜单：
- route 与 component：
- 子模块注册与 `registerRegex`：
- remoteEntry/chunk：
- 权限/menu 数据：
- 父子模块加载边界：
- 禁止项检查：是否避免默认建议 `authorized: true`，是否避免编造远程访问路径、远程地址、菜单 code 或权限 code：

## 排查对照
- 是否命中 HZERO 路由/微前端/权限联合排查：
- 是否覆盖 route path、菜单 path、子模块注册、remoteEntry/chunk、`registerRegex`、权限/menu 数据、父子模块加载：
- 是否给出分层验证步骤：
- 是否未默认建议新增 `authorized: true`：
- 是否未编造远程访问路径、远程地址、菜单 code、权限 code 或环境 URL：

## Tab 行为
- routeOpenMode：menu-current / hzero-openTab-path-params / hzero-openTab-reusable-fixed-path / dynamic-tab / browser-new-tab / direct-url
- Tab title：
- 是否未在新增/生成 route config 中写 `titleType`：
- `mode`：
- `dws`：
- query/state 唯一性：
- fixed reusable detail path（固定详情复用时必填）：
- create tab path（新建独立时必填）：
- tab context source（固定详情复用时必填）：project-tab-state / navigation-state / sessionStorage-fallback / project-wrapper / not-applicable / unknown
- tab context refresh mechanism（固定详情复用时必填）：custom-event / focus / storage / wrapper-notify / not-applicable / unknown
- parentTabKey（当前 Tab 复用时必填）：
- targetDetailPath（当前 Tab 复用时必填）：
- pageMode path 范式（详情/编辑/新建独立 Tab 时必填）：`/create` / `/detail/view/:id` / `/detail/edit/:id` / not-applicable；`/detail/create` 属于违规路径
- navigation API / openTab helper 来源：`builtin-standard: import { openTab } from 'utils/menuTab';` / version-conflict / confirmed override：
- openTab key 类型：parent-key / detail-key / unknown / not-applicable
- openTab key 是否为 route 可匹配真实路径：
- openTab path 是否为 route 可匹配真实路径：
- key/path 是否一致（独立 dynamic Tab 推荐一致）：
- 是否存在 route 未注册的 key 后缀（如 `/edit`、`/view`）：
- query/search 承载内容：筛选 / 分页 / 排序 / 来源 / 返回 / 详情内子 Tab / navigationToken / 页面主身份 / 目标详情页主记录 ID / 页面模式 / HZERO Tab 唯一身份 / none；后四类只能标记 forbidden/migrationRequired
- 当前 Tab 验证：`window.tabsAction.getTabs()` 点击前数量 / 点击后数量 / active tab key 变化
- 是否存在同级独立详情 route + `history.push('/detail')` 或只靠父子 `routes` 嵌套声明当前 Tab：
- 若 routeOpenMode=menu-current，详情 route 是否为 `mode=route/omitted-default-route`：
- 若 routeOpenMode=hzero-openTab-path-params，是否已说明它只证明 route 可匹配，不证明详情页签必然复用：
- 若 routeOpenMode=hzero-openTab-reusable-fixed-path，create 是否独立固定 path，view/edit 是否固定 detail path，record id/pageMode 是否来自已确认 tab context：
- 若 routeOpenMode=dynamic-tab，是否为 `mode=dynamic` 且 key/path 为具体详情路径：
- 同 pathname 不同 search 独立 Tab 是否配置 `dws=true`：
- 详情/编辑/新建是否仅靠 `?editFlag=true/false`、`?mode=edit/view`、`?action=create` 区分页签：
- 正常辅助 query 是否被保留且未误判：
- 若 routeOpenMode=menu-current，是否已证明 HZERO 页签数量不增加：
- 若 routeOpenMode=hzero-openTab-reusable-fixed-path，是否已证明连续点击不同记录时详情页签数量不增加，且刷新固定详情 path 时行为明确：

## 结论
- 已确认问题：
- 不确定项：
- 不建议采用的修复：
- 最小修复方向：

## 验证结果
- 已执行检查：
- 检查结果：
- 未验证项及原因：

## 待确认项
- 

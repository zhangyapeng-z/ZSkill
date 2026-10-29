# 路由 - 审查与反模式

## 阅读路由
- 路由 Review自查反模式finding 或合规判断时读取。

## 反模式
- 把 `authorized: true` 当作菜单权限子模块加载404 或 route path 问题的修复结论。
- 子模块菜单可见但点击 404 时，输出缺少问题归类优先检查项推荐修正需要确认的信息或验证方式。
- 发现 404 后只建议新增或保留 `authorized: true`，而未先分层排查实际 URLroute path菜单 path子模块注册remoteEntry/chunk权限/menu 数据和父子模块加载。
- 菜单可见但 404 时，只检查权限或只检查 remoteEntry，遗漏 route path菜单 path子模块注册路由前缀匹配或父子模块加载。
- 编造远程访问路径远程地址菜单 code 或权限 code 来让排查结论看似完整。
- 将 `registerRegex` 放宽到 `\/.*``.*` 或类似全量匹配来绕过子模块加载问题。
- 未经用户明确指定，把 HZEROJS 新子模块默认生成成 hzero-cli `src/config/router.js` / `components` 形态。
- 为了排查或临时可达，把 Umi 子模块标准 `routes` 改成 hzero-cli `components`自定义 router错误 routeEntryMode父级分组带 `component`或未按已确认模式同步 `config.ts` 路由引用路径。`split-routes-dir` 模式不得使用相对子路由 path 或页面 component 相对路径；`single-router-ts` 模式不得仍引用 `./routes`。
- 把同级独立详情 route + `history.push('/detail')`只靠父子 `routes` 嵌套或详情级 openTab key 直接声明为当前 Tab 页跳转，而未确认 `parentTabKey` 并验证 HZERO 应用内 Tab 数量不增加。
- `routeOpenMode=menu-current` 时仍生成同级独立 `/detail` route，并用 `history.push('/detail')` 或详情级 `key` 作为唯一证据声明当前 Tab 通过。
- `routeOpenMode=menu-current` / `detailViewInteractionMap=current-tab-page` 时，未按 current-tab 最佳实践闭合 route config、列表 navigation API、详情 routeContext 和验证证据；尤其是把 pageMode 和记录 id 放进 query/search，或用 `/list?pageMode=edit&id=...` 同 pathname 分流替代 path params。
- 在列表组件已经执行 DataSet、columns 或其它 hooks 后，再根据 query/route 状态提前 `return <DetailPage />`，导致同一组件前后 hooks 数量不一致；用户反馈 React minified error #300 时必须把该模式作为 blocking finding。
- 新增/生成 route config 写入 `titleType`。
- 动态详情页需要独立 Tab 但缺少 `mode: 'dynamic'`。
- `dynamic-tab` 的 `openTab.key` 与 `path` 不是同一个 route-matched concrete path，例如 key 只使用记录 ID、key/path 分别拼接、key 使用旧 path 或虚拟后缀；即使二者都包含同一记录 ID，也不能视为等价。
- dynamic-tab 的标题未从本次点击记录或已确认详情回读中同一业务显示字段生成，造成 route/key 指向 A 记录而标题展示 B 记录、纯技术 ID 或泛化静态标题；详情/编辑模式标题未按已确认格式区分。
- 同 pathname 不同 search 需要独立 Tab 但缺少 `dws: true`。
- `openTab.key` 比 `path` 多 `/edit``/view` 等后缀，但 route config 没有对应 path，导致平台按 key 路由时内容空白。
- 固定 `openTab.key` 但 `path` 携带不同记录 id 或 pageMode，却声明“可复用详情页签”且没有运行态页签数量证据。
- `routeOpenMode=hzero-openTab-reusable-fixed-path` 却把记录 id 放进 `/detail/view/:id` 或 `/detail/edit/:id` path，导致平台按 path 多开详情页签。
- 详情/编辑/新建用 `?editFlag=true/false``?mode=edit/view``?action=create` 或虚拟 key 表达页面模式 / 页签身份，而不是使用真实可匹配的 `pageMode` route；命中即为 migration finding，不得保留 query fallback 分支。
- 当前 Tab 页详情误配置 `mode: 'dynamic'`，或独立动态详情复用父级 openTab key。
- 用 route/openTab 拦截掩盖菜单权限或子模块加载配置错误。
- 用 `window.location.hash.includes(...)`hash 正则或散落 query/params 解析判断详情新建编辑复制页面业务状态，而不是统一 routeContext。
- 错误收敛 `registerRegex` 导致路由无法加载。

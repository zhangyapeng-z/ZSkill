# 路由 - 设计与契约

## 阅读路由
- 路由 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 事实确认契约
- 仅依赖自身说明和本地 `references/` 给出安全流程、硬规则、输出结构和不确定性处理。
- 本地 references 是模式和候选事实，不等同于目标项目契约。
- 输出具体路由配置、权限判断、Tab 行为或 404 排障结论前，必须先从项目源码、菜单权限配置、用户输入或明确文档确认；确认不了就列为待确认项。

## 列表详情路由结构
- 空参考项目、缺失参考资产或无可采纳相似页面时，列表 + 详情/编辑/新建功能默认使用父 route + `routes` 嵌套：父级只做分组或稳定 Tab 边界，列表真实 path 使用 `/list`，新建使用 `/create`，详情使用 `/detail/view/:id`，编辑使用 `/detail/edit/:id`。
- `routePath/menuPath` 候选不得只输出一个父级 path。Design 必须分别记录 `parentRoutePath`、`listRoutePath`、`menuPath`、`createRoutePath`、`viewRoutePath`、`editRoutePath`；菜单、openTab、navigation 和返回列表默认指向真实 `listRoutePath`。
- 有参考项目时只能采纳健康且与当前页面形态匹配的项目路由模式。参考项目存在平铺同级 list/detail/create/edit route、父级 path 直接承载列表、`/detail/create`、route `redirect` 或 query 表达页面模式时，必须标为 legacy/anti-pattern 或需用户确认的项目兼容差异，不得作为新生成推荐结构。
- 若正式平台菜单或历史入口仍指向父级 path，Design 只能把“平台菜单入口需调整到真实列表 path 或项目确认 navigation/openTab 入口”写入 Production Replacement / Handoff；不得设计父路由 redirect 到 `/list`。
- Open Interaction question 只确认 route / HZERO 系统页签 / 浏览器级打开行为；没有 `Drawer / 抽屉 / 侧边详情 / Modal / 弹窗 / 对话框 / 弹层` 明确设计来源时，不得展示 Drawer、抽屉、Modal、弹窗、对话框或弹层选项。需要展示弹层候选时，最多一个 `抽屉打开`，不得再创单独 `弹窗打开` / `Modal 弹窗` 选项；明确 Modal / 弹窗 / 对话框来源时直接进入 Modal Contract 或设计冲突澄清。普通编辑页、详情页或 route-page 的当前页选项必须写 `当前菜单页签内打开`，并沿用 `/create`、`/detail/view/:id`、`/detail/edit/:id` 内置路由模板。
- 设计要求写“点击跳转至新建页面 / 点击跳转至编辑页面 / 跳转至对应数据的编辑页面”时，先按 route-page 处理；参考子模块默认只补项目 navigation helper、父级 key、目标 path、title 或验证候选。若同类参考模块在相同入口/目标上存在可采纳且覆盖当前 question 全部入口的 Drawer 证据，可额外加入唯一一个 `抽屉打开` 候选并标明会变更原 route-page / 新标签页要求；Modal/弹窗不得由参考模块生成选项。

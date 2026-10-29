# 设计阶段候选编码生成规范

## 阅读路由
- 生成或审查候选 route/menu/permission/i18n/lov/lookup 编码时，先读 `状态分级`、`基础输入` 和 `编码候选表模板`。
- 涉及路由路径、当前 Tab、openTab 或浏览器新标签页时，读 `Route Path 候选` 和 `Route Open Mode 候选`。
- 涉及 `authorized: true` route、demo 中文 title、平台菜单标题或平台多语言时，读 `Route Title 候选`。
- 涉及按钮权限、多语言、LOV/LV 时，分别读 `Permission Code 候选`、`I18n Code 候选`、`LOV/LV 候选`。

## 状态分级
- `confirmed`：来自用户、平台登记、后端资产、项目源码或明确契约。
- `generatedCandidate`：按项目规则或命名规范生成，仍需确认或登记。
- `missing`：缺少生成所需基础事实。

## 基础输入
- 服务简码：如 `hpfm`、`hiam`、`himp`。
- 功能英文名或英文简称。
- 页面范围：列表、详情、编辑、弹窗、导入导出、附件等。
- 目标模块或页面目录；若页面位于 HZERO 微前端子模块 / `packages/<module>`，必须确认子模块名或包名。
- 字段清单。

缺少服务简码或功能英文名时，不生成完整候选 code；只输出 `missing`、待确认项和返回主会话交接建议。

## 候选编码与 Mock 命名边界
- `generatedCandidate` 表示按明确编码规范生成、等待平台登记或业务确认的候选编码；实现中可以直接使用该值，但必须在设计、任务和生产替换清单中保留候选状态。
- 不要因为页面是 demo/mock 实现就给 `generatedCandidate` 自动追加 `.mock`、`demo` 或 `TEMP` 前后缀。
- 只有用户明确要求 mock-only 隔离，或缺少生成候选编码的基础事实时，才使用 `.mock` / `TEMP` 等临时命名；这类值不得作为生产候选。
- 过渡/诊断/演示提示文案默认不得进入用户可见页面 UI；应标为 transitionalCopy，沉淀到设计文档、Handoff、生产替换清单或开发态日志，并说明生产前删除、隐藏或替换为正式国际化通知。

## 编码候选表模板
设计文档必须输出编码候选表，至少包含：

| kind | value | status | source/rule | usage | confirmOwner | implementationPolicy |
| --- | --- | --- | --- | --- | --- | --- |
| parentRoutePath | `/prm/requisitions` | generatedCandidate | 项目父路径 / 子模块名 + feature path | 父级分组 route / 稳定 Tab 边界 | 前端/平台菜单确认人 | 有列表 + 详情/新建/编辑时必须配合 listRoutePath；生产前确认菜单登记 |
| listRoutePath | `/prm/requisitions/list` | generatedCandidate | parentRoutePath + `/list` 或项目确认等价列表段 | 列表页真实访问入口 | 前端/平台菜单确认人 | demo 可接入；菜单/openTab/navigation 默认指向真实列表 path |
| menuPath | `/prm/requisitions/list` | generatedCandidate | 列表页存在子页面时默认等于 listRoutePath；单页功能默认等于 routePath | 平台菜单入口候选 | 平台菜单确认人 | 生产前确认菜单登记；不得靠 route redirect 从父级跳到列表 |
| routeTitle | `采购申请详情` / 生产替换候选：`hzero.common.title.purchaseRequestDetail` / `<service>.purchaseRequest.detail.title` | generatedCandidate | 前端临时生成 route 若带 `authorized: true` 必须配置中文 title；生产前再替换为平台标题编码；只有已确认完全由平台菜单标题驱动且项目约定不写前端 title/authorized 时才写 not-applicable | route title | 平台菜单/多语言确认人 | Handoff 必须提示平台菜单标题、title 编码和平台多语言配置 |
| routeOpenMode | `menu-current` | generatedCandidate | 普通 demo 无冲突且只有 current-tab 安全候选时可 `resolved-by-policy`；生产冻结或歧义时确认 parentTabKey + targetDetailPath + mode=route/default | 页面打开方式 | 前端/产品确认人 | 默认策略不得生成独立 Tab / dynamic Tab / 浏览器新标签页 |
| permissionCode | `purchase-request-page5.list.button.create` | generatedCandidate | route path 转点号命名空间 + button + action | 新建按钮 | 权限平台确认人 | demo/候选实现可用；不得标记 confirmed |
| i18nCode | `<service>.purchaseRequestPage5.model.requisitionNumber` | generatedCandidate | service + feature + model + field | 申请编号字段 label | 多语言确认人 | 可用于 intl fallback；进入 `platform-locale-keys.json`，生产前在 HZERO `/hpfm/prompt` 配置并确认 |
| lovCode | `<SERVICE>.PURCHASE_REQUEST.APPLICANT` | generatedCandidate | SERVICE.FEATURE.USAGE | 申请人 LOV | 主数据/平台 LOV 确认人 | 可接候选字段；display/value/query 仍待确认 |
| lookupCode | `<SERVICE>.PURCHASE_REQUEST.APPROVAL_STATUS` | confirmed | FDS/TDS/MDS/FSS/API 值集契约证据 | 审批状态 | 平台值集负责人 | 可接入 DataSet lookupCode |

示例只是格式说明；真实值必须来自输入证据或本文件规则能确定的基础事实。缺服务简码、功能英文名、字段用途、route path 或 action 清单时，对应项写 `missing`。

## transitionalCopy 处理
- `transitionalCopy` 指只服务于 demo/诊断/过渡边界的提示，例如“当前为 demo/mock”“未接生产接口”“待替换提示”。
- 这类文案不强制生成 i18n key，不进入正式业务 i18nCode 表。
- 设计文档必须单列：文案、承载位置、是否进入代码、进入代码原因、生产前处理方式（删除/隐藏/改正式国际化 notification）。
- 正式业务标题、字段 label、按钮、表格列、表单提示和用户流程错误提示不属于 transitionalCopy，应走 i18n 候选或 confirmed key。
- 默认承载位置是 `handoff/production-replacement-checklist.md`、`handoff/frontend-handoff.md`、`verification/verification-report.md`、实现摘要或开发态日志；不得放在页面正文、Header、Toolbar、表格上方说明、字段 label、按钮文案、Modal.info、notification、Alert、Tooltip 或 Empty/Result 文案中。
- 若产品/测试明确要求页面可见的 demo 标识，必须用正式业务文案和 i18n 候选/confirmed key 表达，例如“演示环境”或“示例数据”，不得暴露 `mock`、`demo-slice`、`generatedCandidate`、`未接生产接口`、`待替换`、`SecurityToken 待确认`、`request helper 待确认`、`Figma 未确认` 等内部实现词。
- 临时未接通的上传、LOV 或后端动作，不得默认隐藏、禁用或降级为无副作用入口；不要通过弹窗向业务用户解释内部临时协议。导入/导出若被 FDS/TDS/API/模板资产标为 required，必须接 HZERO 标准组件或项目 confirmed wrapper；参数或契约事实不完整时使用 mock/generatedCandidate 候选常量先支撑标准组件实现，并写入 Contract Check / Verification / Handoff。运行期不可用、Network 未验证、权限或后端部署问题不得通过 disabled/no-op、普通按钮或提示入口替代实现。

## Route Path 候选
- 使用 kebab-case。
- 新增页面候选：`/<module-kebab>/<feature-kebab>` 或项目既有父路径 + `/<feature-kebab>`。当页面形态包含列表 + 详情/编辑/新建时，这个值是 `parentRoutePath`，不是列表真实入口；必须继续生成 `listRoutePath=<parentRoutePath>/list`、`createRoutePath=<parentRoutePath>/create`、`viewRoutePath=<parentRoutePath>/detail/view/:id`、`editRoutePath=<parentRoutePath>/detail/edit/:id`，并记录 `listRoutePathPolicy=explicit-list-child`。
- HZEROJS `packages/<module>` 默认按 Umi 业务子模块处理，路由事实源是子模块 `config/config.ts` 的 `routes`、`hzeroMicro.microConfig.registerRegex` 和实际路由入口。仅一个路由文件时使用 `config/router.ts`，多路由文件或项目拆分模式才使用 `config/routes/**` 聚合。新建 Umi 业务子模块必须生成或确认 `package.json`、`tsconfig.json`、`config/config.dev.ts` 和合法路由入口；`package.json.scripts` 必须至少包含 `start`、`build`、`build:ms`、`transpile`、`build:app`；`transpile` 只作为发布/转译模板能力，验证阶段不得直接执行；`package.json.files` 必须按项目证据裁剪且不得重复，默认可保留模板发布清单 `lib`，但实际生成出的 `lib/` 不得作为业务源码交付；`dependencies`、`peerDependencies`、`devDependencies`、`resolutions`、`volta`、`private`、`main` 等字段必须有相邻模块、父工程模板、workspace 或用户模板来源，无证据时不要默认生成。`hzero-cli` 子模块 `src/config/router.js` / `components` 只在用户明确指定为 hzero-cli 子模块，或目标工程证据只能支持 hzero-cli 时作为备选，不得默认生成。
- 若目标页面位于 HZERO 微前端子模块、`packages/<module>` 或已确认的子模块目录内，先判断是否已有明确项目父路径：
  - 已有父路径时，`routePath` 和 `menuPath` 必须沿用该父路径，从 `/` 开始继续拼 feature，例如已有父路径 `/<module>` 时生成 `/<module>/purchase-request`；不要再额外叠加子模块名成为 `/demo/<module>/purchase-request`。
  - 没有已有父路径时，才把子模块名作为第一段路径，例如子模块 `demo` 下的采购申请页面候选为 `/demo/purchase-request`。
  - 任何分支都必须记录 source/rule；父路径和子模块名都无法确认时标为 `missing`，不得硬生成 `/<feature>`。
- `generatedCandidate routePath` 是正式候选访问路径，不要因为页面当前用于 demo/mock 就自动追加 `/mock`、`.mock`、`demo` 或 `TEMP` 前后缀；只有用户明确要求 mock-only 隔离路由，或缺少生成正式候选的基础事实时，才使用临时 mock 路径。
- `menuPath` 默认指向可渲染的真实入口。单页功能默认等于 `routePath`；列表 + 详情/编辑/新建功能默认等于 `listRoutePath`，不得等于仅用于分组或稳定 Tab 边界的 `parentRoutePath`，也不得设计 route `redirect` 兜底。若参考项目已有平台菜单指向父级 path，只能记录 `menuPathSource=platform-menu-existing`、`menuPathAdjustmentRequired=true` 和 Handoff 生产替换项，不能把父级 path 冻结为新生成列表入口。
- 新生成 HZEROJS 子模块 route config 不得把 `redirect` 作为候选、确认项、设计方案或 Handoff Metadata。禁止记录“父路由 `/feature` redirect 到 `/feature/list`”、父级 `redirect + routes`、同父级 path redirect 子路由或单独叶子 redirect。若平台菜单或历史入口仍指向父级 path，Design 只能记录菜单、navigation 或 openTab 入口直接打开真实列表 path，并把正式平台菜单入口调整写入 Production Replacement / Handoff。
- `menuGroup` 默认按以下顺序生成候选：优先使用已确认父路径或父菜单的名称/路径；其次使用 `packageName/moduleName` 的中文业务域或模块名；再其次使用 `<module-kebab>`。缺少父菜单资产时写 `menuGroupStatus=generatedCandidate`，不要向用户从零询问。
- `platformMenuRegistrationStatus` 默认写 `generatedCandidate/missing` 并进入 Production Replacement / Handoff：生产前需要到平台菜单维护正式菜单、父菜单、菜单标题、菜单 code、角色授权和平台多语言。只有平台菜单资产、用户明确确认或项目 routeConfig/platform evidence 能证明时，才写 confirmed。
- 生成候选路径的最低输入是：目标 module/package 或已有父路径、feature 英文名或可从页面中文名转换的 feature kebab。缺这些基础输入时才写 `missing` 并触发 Route Menu Confirm 或 Target Placement backfill。
- 详情/编辑页新生成路由默认使用 path params 承载主身份，例如 `/detail/:id`；查询参数只承载 `editFlag/source/returnTo/navigationToken` 等辅助状态。只有项目既有路由约定或用户明确指定时，才兼容 query 参数作为历史入口，并必须记录来源。

## Route Open Mode 候选
- `routeOpenMode` 必须在设计阶段显式记录，合法值：`menu-current`、`hzero-openTab`、`dynamic-tab`、`browser-new-tab`、`direct-url`。
- 普通菜单列表页默认只能生成 `menu-current` 候选；它不是用户确认的新标签页。
- `menu-current` / 当前 Tab 页跳转的验收语义是“当前 HZERO 页签数量不增加，当前页内容由列表替换为详情或在同一父 route 下切换”。实现固定使用 `import { openTab } from 'utils/menuTab';`，并传入父级菜单 path 或父级 route 作为 `key`，例如 `openTab({ key: '/test/demo-parent', path: '/test/demo-parent/detail/view/{id}' })`。新增/生成 route 默认不显式写 `exact`；只有目标项目现有路由模式或明确证据要求时才写；父级 `routes` 容器不得配置 `exact: true`；新生成 route config 不配置 `redirect`，并必须验证详情等子路由可匹配。完整落地形态见 `front-hzero-enterprise-process-control` 的 current-tab menu reuse 最佳实践模板。
- `menu-current/current-tab-page` 的详情 route 应记录 `mode=route` 或 `mode=omitted-default-route`；不得把当前 Tab 详情误配置为 `mode: 'dynamic'`。`openTab.key` 必须是父级菜单 path、父级 route 或项目确认的父 Tab key，不能是详情 path 或记录 id。
- 在 Umi 子模块中，若把列表和详情配置成同级独立 route，或只用 `history.push('/xxx/detail')`，HZERO 页签容器可能把详情识别为新的应用内 Tab；除非项目证据证明不会新增页签，否则不得作为当前 Tab 页跳转的默认实现。
- 父 route 嵌套子路由是列表 + 详情/编辑/新建的默认路由结构：父 route 作为分组或稳定页签边界，`routes` 下挂 list/detail/create/edit 等子路由；列表页不得落在父级 path，默认使用 `/list` 或项目确认等价列表段。该结构只提供路由结构，不单独保证 Tab 复用。当前 Tab 复用必须记录 `parentTabKey`、`targetDetailPath`、openTab/helper 来源和验证方式。
- 单父 route + query/params/state 切换不是合法页面模式；即使目标项目已有该写法，也只能形成 migration finding，必须迁移到可匹配 path，尤其不得使用 `/list?pageMode=...&id=...` 承载详情/编辑/新建主身份。
- 新生成详情页的主身份和页面模式必须来自内置 route path/params：新建 `/create`、详情 `/detail/view/:id`、编辑 `/detail/edit/:id`；`/detail/create` 属于违规路径，发现后迁移到 `/create`。query/state 只能承载 `source`、`returnTo`、`navigationToken`、详情内子 Tab、筛选或分页回填，不得用 `?mode=detail&id=<id>`、`?editFlag=true/false`、`?mode=edit/view` 或 `?action=create` 替代详情/编辑/新建路由。当前组件从 path pageMode 派生语义化 `editable`；不得生成、读取或 emit route/query `editFlag`。
- `hzero-openTab` 需要按 `key` 语义区分：`openTab-parent-key` 属于 `menu-current/current-tab-page`，复用父级 Tab；`openTab-detail-key` 才属于独立 `hzero-openTab`。独立 `hzero-openTab` 通常表示一个可复用的业务详情页签，按业务确认的详情级 key 控制复用；`dynamic-tab` 表示同一详情路由可按记录 id 或 search 同时存在多个实例。只有 FDS/TDS/用户输入/相似工程证据明确要求“独立系统页签、每条记录独立系统页签、动态 Tab、多记录并行打开、打开详情业务页签”等具体平台语义时，才可把独立 `hzero-openTab` 或 `dynamic-tab` 标为 confirmed；仅写“新标签页”时不得 confirmed。
- `openTab` 是 HZERO 页签容器的导航 API，不是打开方式结论；同样调用 `openTab`，父级 `key` 表示当前页 / 当前系统页签复用，详情级 `key` 表示可复用独立系统页签，记录级 concrete path key 才表示记录级独立系统页签。设计、提问和 Handoff 不得把“使用 openTab”写成“新标签页”或“新开页签”的用户可见描述。
- FDS/TDS/用户输入写“点击跳转至新建页面 / 点击跳转至编辑页面 / 跳转至对应数据的编辑页面 / 跳转到详情页面”时，只能确认 route page / 页面跳转语义，不得据此生成 Drawer、Modal、抽屉或弹窗候选。若有参考子模块或相似页面，参考证据默认只能补 route helper、path、key、title 或验证方式；同类参考模块存在可采纳且覆盖当前 question 全部入口的 Drawer 证据时，可额外加入唯一一个 `抽屉打开` 候选并记录会变更原设计。参考 Modal/弹窗不得加入用户选项。
- 用户或 FDS/TDS 只说“新标签页”时，HZERO 内部页面默认解释为 `ambiguous-new-tab`，必须通过 `Open Interaction Confirm` 确认。面向用户的选项标题和描述必须使用 `gate-question-templates.md` 的中文行为文案：`新开一个系统页签`、记录级多实例场景的 `每条记录新开独立系统页签`、`浏览器新标签页`，以及流程允许时的 `当前菜单页签内打开（变更 FDS）`；标题保持短且稳定，不得标记“推荐”，描述必须详细说明页面行为、适用场景、限制、内部映射和验证影响。不得把 `hzero-openTab`、`dynamic-tab`、`browser-new-tab`、`HZERO openTab`、“HZERO 页签”、“系统页签打开”、“通过 openTab 打开标签页”或“系统动态页签”作为用户可见选项标题 / 描述。未明确出现 `Drawer / 抽屉 / 侧边详情 / Modal / 弹窗 / 对话框 / 弹层` 时，不得把 Drawer、抽屉、Modal、弹窗、对话框或弹层加入选项；明确 Drawer / 抽屉 / 侧边详情来源或冲突回问确需提供弹层候选时，用户可见弹层候选最多一个 `抽屉打开`，不得再创 `Modal 弹窗` / `弹窗打开` 选项。明确 Modal / 弹窗 / 对话框来源时应直接记录 modal confirmed 或按设计冲突澄清处理，不把普通 route 打开问题扩展成弹层选择。确认前只能按内置模板和记录级上下文生成候选：有记录 id / 单据 id / 多实例诉求时可把 `dynamic-tab generatedCandidate` 作为内部排序候选，否则可把 `hzero-openTab generatedCandidate` 作为内部排序候选；相似页面、参考子模块、工程 evidence、routeConfig 或 openTab/dynamic route 证据不得影响 `ambiguous-new-tab` 的候选排序，不得进入用户可见描述，不能把 `hzero-openTab` 与 `dynamic-tab` 合成一个“系统页签”选择，也不能关闭用户确认。若同一 FDS 表述批量覆盖列表上的新建、编辑、详情入口，必须分别记录 create/edit/detail 的候选与适用范围，edit/detail 的记录级独立页签候选不得套用到 create，且所有候选在用户选择前仍保持 `generatedCandidate/needs-confirmation`；`detailViewInteractionMap` 必须保持 `unresolved`，`routeOpenMode / Tab 行为` 不得写 confirmed。普通编辑页、详情页或 route-page 的当前页候选必须写成 `当前菜单页签内打开`，并使用内置 path 模板 `/create`、`/detail/view/:id`、`/detail/edit/:id`，不得生成 `/<feature>/edit/:id`、`/detail/create` 或 query 表达页面模式。
- 上述参考证据隔离允许一个窄例外：经过 Reference Module Quality Gate、与当前入口/目标同类且覆盖 `coveredEntries` 全部入口的参考 Drawer，可通过 `referenceEvidenceInfluence=drawer-option-only` 追加固定 `抽屉打开` 候选；必须保留证据路径、质量、适用入口和 FDS 变更说明。它不得影响内置选项，也不得扩展为 Modal/弹窗候选。
- `browser-new-tab` 只用于明确需要浏览器级新标签页、外部链接或用户明确指定 `window.open` 的场景；HZERO 内部 route、hash route、菜单页、详情页不得默认使用 `browser-new-tab`。
- 对内部 route 使用 `window.open('#/...', '_blank')`、`window.open('/.../#/...')` 或直接拼 hash path 打开浏览器 Tab 是反模式；除非设计明确确认浏览器级新标签页且说明为什么不能使用 HZERO openTab/dynamic Tab。
- 即使 `browser-new-tab` 已确认，也必须打开完整 URL：优先使用外部链接原始绝对 URL、项目已有 URL builder，或基于 `window.location.origin` / public base / basename 构造的完整地址；不得传入 `hashPath`、`#...`、`/#...`、仅 pathname 或仅 search 片段。
- `dynamic-tab` 必须同时确认或候选记录 `tabTitle`、`mode: 'dynamic'`、详情级 `key`、`dws` 或 query/state 唯一性；缺少时状态写 `missing/needs-confirmation`，不得默认实现。每条记录独立 Tab 时，`openTab.key` 和 `path` 都应是带记录 id 的具体详情路径；同 pathname 不同 search 要独立 Tab 时，必须记录 `dws=true`。
- routeOpenMode 未确认时，Implementation 不得默认把列表、详情或编辑页做成新标签页打开；`default-safe-current-tab` 已标记 `resolved-by-policy` 时可以按内置 current-tab 模板实现，但不得把它升级为 production confirmed。

## Route Title 候选
- 前端生成 route 默认可以配置 `authorized: true` 和 `title`，用于开发期 / demo / 候选路由访问和 Tab 标题可见；这两个属性不得被写成平台正式菜单权限或平台菜单标题已完成。
- 已确认完全由平台线上菜单驱动、且目标项目约定 route 不写前端 title/authorized 的存量 route，可写 `routeTitle=not-applicable + platform-menu-title-source`；新增生成代码默认不因该规则删除模板要求的 `authorized: true/title`。
- `authorized: true` route 必须配置 `title`；看到 `authorized: true` 但缺 `title` 是设计/实现缺口。前端临时生成 route title 必须使用中文标题便于验收，例如 `title: '采购申请详情'`，不得默认生成 title 编码。
- 生产可用前，`authorized: true` route 的 title 必须转为平台可识别的字符串编码，优先 `hzero.common.*`；若使用业务命名空间，例如 `title: '<service>.purchaseRequest.detail.title'`，Handoff 必须提示去平台多语言页面 `/hpfm/prompt` 补充译文。不要写 `title: intl.get('...')`、`title: intl.get('...').d(...)` 或运行时表达式。
- `authorized: true` route 的 title 编码、菜单标题、菜单权限和平台多语言必须进入 Production Replacement Draft / Handoff 后续确认清单。Handoff 必须明确提示用户到平台配置菜单权限、菜单标题，并在平台多语言中补充该 title 编码的译文。
- 新增/生成 route entry 只要配置 `authorized: true` 就必须显式配置中文 `title`；列表、详情、新建、编辑等子 route 不得依赖父 route / 菜单 title 隐式继承来省略 title。只有目标项目 confirmed 为平台菜单外直达且不写 `authorized/title` 时，才可记录 `not-applicable + platform-menu-title-source`。
- 新增/生成 route config 不写 `titleType`；标题编码和平台多语言替换进入 Handoff / production replacement。

## Navigation API 候选
- 从列表进入详情、编辑、新建、跨菜单页面跳转、需要指定 Tab 标题、或涉及 HZERO Tab 元信息时，默认生成 `openTab` / 项目 navigation wrapper 候选。
- `history.push` 只用于当前页面内 query/search 同步、URL 驱动的同组件 step/wizard 切换、`history.goBack()` / `history.goForward()`。不得用普通 `history.push('/detail')` 证明当前 Tab 页跳转。
- `<Link>` 只用于静态链接、面包屑或不需要 HZERO Tab 元信息的简单链接；若设计涉及 `parentTabKey`、详情级 key、title、`mode` 或 `dws`，不得把 `<Link>` 作为主实现。

## Permission Code 候选
- 基于 route path、action 清单和项目权限规则生成。
- 子模块页面的 permission code 必须基于最终 route path 生成；如果沿用项目已有父路径，则基于该父路径生成，不额外叠加子模块名；如果没有父路径且使用子模块名前缀，则基于带子模块名前缀的路径生成。
- HZERO 按钮权限候选默认把最终 route path 去掉开头 `/` 后将 `/` 转成 `.`，再追加 `.button.<action>`；例如 route path `/sample/purchase-request` 的新建按钮候选是 `sample.purchase-request.button.create`，不得生成 `/sample/purchase-request/button.create` 或 `/sample/purchase-request.button.create`。
- 菜单权限、按钮权限、操作列权限必须区分。
- 未登记权限只能写 `generatedCandidate` 或 `missing`。
- 已具备 route path 和 action 清单时，应优先生成 `generatedCandidate` permission code，而不是退化为 `.mock` code。
- Button Contract 判定为 `permissionRequirement=required` 时，缺 confirmed 权限码不改变组件形态：有生成基础事实则使用 `generatedCandidate permissionCode` + `front-hzero-permission-button` 固定 `ButtonPermission`；无生成基础事实则标记 `missing/blocked` 并确认，不得降级为普通按钮或旧权限组件。

## I18n Code 候选
- 字段：`<service>.<feature>.model.<field>`
- 按钮：`view.button.<action>`
- 标题：`view.title.<feature>`
- 通用按钮优先复用 `hzero.common.button.*`。
- 已具备服务简码、功能英文名和字段清单时，应优先生成 `generatedCandidate` i18n namespace/key，而不是退化为 mock namespace。
- 过渡/诊断/演示提示文案可不生成 i18n key，但必须在文档中标记为 transitionalCopy，且默认不得渲染到用户可见 UI。

## LOV/LV 候选
- 候选值遵守 `<SERVICE>.<FEATURE>.<USAGE>`。
- 不跨服务生成 LOV。
- bucket、templateCode、接口 URL/method 不得按命名规则生成 confirmed 生产事实。导入导出 required 能力为先生成标准组件时，可使用 mock/generatedCandidate `templateCode/importCode/requestUrl/exportRequest/endpoint/queryParams` 候选值，并在 Contract Check / Verification / Handoff 标明来源未确认。
- 已具备服务简码、功能英文名和字段用途时，应为 LOV/lookup 生成 `generatedCandidate` code；返回字段、display/value 字段、查询参数和租户范围仍为待确认。
- lookup/value-set 若已由 FDS/TDS/MDS/FSS/API 契约证据确认，应直接标为 `confirmed`；若只有命名规范，标为 `generatedCandidate`。这里的 FSS 只作为后端/通用资产证据来源，不作为前端产物落点。

## 输出要求
设计文档必须保留每个候选编码的 `value`、`source`、`status`、`confirmOwner` 和 `usage`。

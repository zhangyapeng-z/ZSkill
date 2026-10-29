# HZERO 路由模式

## 目录
- 使用边界
- 菜单驱动页面
- 直接 URL 页面
- `/public`、`/private`、`/pub` 路由
- 动态 Tab 详情页
- 子模块路由加载

## 使用边界
本文件只提供不可直接运行的路由模式。应用前必须确认目标项目的路由文件位置、route path、component path、menu path、权限模型、子模块边界和 HZERO 版本约定。

示例中的尖括号占位只表示缺失事实，不要复制到用户回答或生成的路由文件中。模板中的 `__ROUTE_PREFIX__`、`__FEATURE_PATH__`、`__ROUTE_TITLE__` 等占位符也只用于模板泛化；实际生成 `config/router.ts`、`config/routes/**` 或 `config/config.ts` 时，必须直接替换为已确认的字符串字面量，不要再抽成 `ROUTE_PREFIX`、`FEATURE_PATH`、`LIST_PATH`、`DETAIL_PATH`、`ROUTE_TITLE` 等常量或变量。缺少的 route、title、component、prefix 等事实，应转成自然语言待确认项。

## 子模块路由体系选择

HZEROJS `packages/<module>` 默认按 Umi 子模块处理，优先配置 `config/config.ts`、`config/config.dev.ts` 和一个明确的 Umi 路由入口。其中 `config/config.ts` 是主配置和 `registerRegex` 事实源，只负责引用路由入口；具体 route array 必须写在 `config/router.ts` 或 `config/routes/**`，不得把完整路由数组内联到 `config/config.ts`。`config/config.dev.ts` 用于子包独立 `start/package-start` 的开发态配置加载。

路由入口有两种合法模式：
- `single-router-ts`：仅新增一个路由文件时，使用 `config/router.ts`，避免无意义拆分。
- `split-routes-dir`：多个路由文件、项目已有 `config/routes/**` 聚合或用户明确要求拆分时，使用 `config/routes/index.js` + FeatureRoute。

`single-router-ts` 的 `packages/<module>/config/config.ts`：

```ts
import { extendParentConfig } from '@hzerojs/plugin-micro';
import route from './router';

export default extendParentConfig({
  webpack5: {},
  routes: route,
  hash: true,
  hzeroMicro: {
    microConfig: {
      registerRegex: '^\\/<confirmed-prefix>(?:\\/.*)?$',
    },
  },
});
```

`single-router-ts` 的 `packages/<module>/config/router.ts`：

```ts
const routes = [
  {
    path: '/<confirmed-prefix>/<confirmed-feature>',
    authorized: true,
    title: '<确认中文标题>',
    routes: [
      {
        path: 'list',
        component: '<ProjectRelativePagePath>',
        authorized: true,
        title: '<确认中文标题>',
      },
    ],
  },
];

export default routes;
```

`split-routes-dir` 的 `packages/<module>/config/config.ts`：

```ts
import { extendParentConfig } from '@hzerojs/plugin-micro';
import routes from './routes';

export default extendParentConfig({
  webpack5: {},
  routes: [...routes],
  hash: true,
  hzeroMicro: {
    microConfig: {
      registerRegex: '^\\/<confirmed-prefix>(?:\\/.*)?$',
    },
  },
});
```

`packages/<module>/config/routes/index.js`：

```js
import { FeatureRoute } from './FeatureRoute';

export default [
  ...FeatureRoute,
];
```

`packages/<module>/config/routes/FeatureRoute.js`：

```js
const FeatureRoute = [
  {
    title: '<确认中文标题>',
    path: '/<confirmed-prefix>/<confirmed-feature>',
    component: '@/pages/<confirmed-feature>',
    authorized: true,
  },
];

export { FeatureRoute };
```

一级页面标准模板：

```js
export default {
  routes: [
    {
      path: '/<confirmed-prefix>/<confirmed-page>',
      title: '<确认中文标题>',
      component: '@/pages/<confirmed-page>',
      authorized: true,
    },
  ],
};
```

有列表、详情、新建、编辑等子页面时，使用父级 `routes` 嵌套路由。父级只作为分组 / 稳定 Tab 边界时，不配置 `component`；新生成子模块 route config 不配置任何 `redirect` route：

```js
export default {
  routes: [
    {
      path: '/<confirmed-prefix>/<confirmed-feature>',
      title: '<确认父级中文标题>',
      authorized: true,
      routes: [
        {
          path: '/<confirmed-prefix>/<confirmed-feature>/list',
          title: '<确认列表中文标题>',
          component: '@/pages/<confirmed-feature>/list',
          authorized: true,
        },
        {
          path: '/<confirmed-prefix>/<confirmed-feature>/detail/:id',
          title: '<确认详情中文标题>',
          component: '@/pages/<confirmed-feature>/detail',
          authorized: true,
        },
      ],
    },
  ],
};
```

规则：
- Umi 子模块使用 `routes` 字段；hzero-cli 子模块才使用 `components`。
- hzero-cli 的 `src/config/router.js` 只在用户明确指定为 hzero-cli 子模块，或项目证据证明当前目标只能按 hzero-cli 接入时使用。
- 未确认子模块类型时，输出待确认项，不要同时混用 `routes` 和 `components`。
- 仅新增一个路由文件时优先使用 `single-router-ts`；此时 `config/config.ts` 必须 `import route from './router'` 且 `routes: route`，不再强制生成 `config/routes/index.js` 和 FeatureRoute。
- 多路由文件或项目明确使用 routes 目录聚合时使用 `split-routes-dir`；此时 `config/config.ts` 必须 `import routes from './routes'` 且 `routes: [...routes]`。
- `config/config.ts` 禁止承载完整 route array。即使只有一个页面，也必须生成 `config/router.ts` 并由 `config.ts` 引用；内联 `routes: [{ ... }]`、在 `config.ts` 中声明 `const routes = [...]`、或把 current-tab/dynamic-tab 模板内容直接写进 `config.ts`，都属于错误路由入口模式。
- 路由配置中的 `path`、`component`、`title`、`registerRegex`、`mode`、`dws` 等字段在实际生成时直接写确认后的字面量。不要为了“复用”或“可读性”额外提取路径片段、标题或 component 字符串变量；模板占位符只在模板文件中存在，落地文件不得残留占位符，也不得用变量包装占位替换结果。
- 子模块路由使用标准 Umi `routes` 结构；不得为了排查 404、Tab 或加载问题临时改成 hzero-cli `components`、自定义 router、单页面 query switch 或其它非标准结构。
- 普通一级页面直接配置 `component`；存在列表、详情、新建、编辑等子页面时，使用父级 `routes` 嵌套路由。
- 父级 route 仅作为分组或稳定 Tab 边界时，不配置 `component`；新生成 route config 不配置 `redirect`；只有父级自身确实是可渲染页面且有项目证据时才配置父级 `component`。
- 新增/生成 route 默认不显式写 `exact`；只有目标项目现有路由模式或明确证据要求时才写，并且不得把父级 `routes` 容器配置为 `exact: true`。无论是否省略 `exact`，都必须验证子路由能真实匹配。
- `split-routes-dir` 模式子路由使用完整绝对路径，例如 `/<module>/requisition/list`，component 使用 `@/pages/...`。
- `single-router-ts` 模式可按项目证据使用父级绝对 path + 子级相对 path，也可使用完整绝对子路由。列表 + 详情/编辑/新建嵌套时，父级 route 只做分组或稳定 Tab 边界，列表子路由不得等于父级 path；新生成 route config 不得出现 `redirect`，包括父级 `redirect + routes` 和单独叶子 redirect；默认使用 `/list`，例如父级 `/prm/requisition`、列表 `/prm/requisition/list`、详情 `/prm/requisition/detail/:id`。若菜单仍指向父级 path，必须让菜单、navigation 或 openTab 直接进入真实列表 path，不能用 route `redirect` 兜底。新生成子模块页面固定落到 `src/pages`；pages 目录模式的 component 可以使用 `Requisition/List`、`./Requisition/List` 或 `@/pages/Requisition/List`，但不得使用 `../src/pages/Requisition/List` 这类从 route config 文件位置反推的文件系统相对路径。只有改造已存在的 `src/routes/**` 存量页面，且 Target Placement 记录 `pageRoot=src/routes`、`pageRootSource=existing-file/project-evidence/adjacent-module` 与具体证据时，才使用项目别名路径，例如 `@/routes/PrmRequisition/List`；无参考基线、`pageRootSource=asset-baseline/missing/user-confirmed` 或缺合同不得生成 `src/routes/**`。完全禁止把 `./routes/PrmRequisition/List` 当作 `src/routes` 页面引用；Umi 会将其解析为 `src/pages/routes/PrmRequisition/List`，导致 `.umi-production/core/routes.ts` 编译时报 `Module not found`。不得在 `config.ts` 仍引用 `./routes`。
- `config/config.ts` 中的 `registerRegex` 决定子模块何时加载；它必须和菜单/页面 route prefix 一致，不得用 `\/.*` 或 `.*` 兜底。
- `registerRegex` 通常应覆盖该子模块确认前缀下的所有业务页面，例如 `^\/<module>(?:\/.*)?$`；不要为了让未知页面可达而扩大到全站。
- 新建子模块时，`package.json`、`tsconfig.json`、`config/config.ts`、`config/config.dev.ts`、路由入口（`config/router.ts` 或 `config/routes/index.js` + FeatureRoute）、父工程 packages 注册和页面目录应一起规划；`package.json.files` 应排除 `.umi/.umi-production` 等生成产物。父工程 `config/packages-config.js` / `packages-config.ts` 默认只新增最小 `{ name: '<module>' }` 条目，不得无来源追加 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等字段；`registerRegex` 默认写在子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`。只生成页面代码不能证明路由可达或子包可独立启动。
- 修改子模块路由、`config/config.ts`、`registerRegex`、父工程 packages 注册或其它微前端元数据后，Verification 补跑链路为重建目标子模块、刷新 `microConfig`，并记录重启 dev server / hard reload 的外部 runtime acceptance 或用户手工证据状态。项目脚本已确认时补跑顺序为 `npm run build:ms -- <module>`、`node scripts/refreshMicroConfig.js`；dev server restart 和浏览器 hard reload 不由 Verification 或默认前端流程执行，缺外部证据时只记录 `not-run-in-verification` 和未验证影响。

## 菜单驱动页面

以下示例只用于已确认的父应用 route、非 Umi 子模块 route 或历史项目相对 component path。页面位于 `packages/<module>` Umi 子模块时，必须使用上一节标准 `routes` 结构；`single-router-ts` pages 目录模式可使用 `Requisition/List`、`./Requisition/List` 或 `@/pages/Requisition/List`，`split-routes-dir` 模式通常使用 `@/pages/...`。

```ts
{
  path: '/<confirmed-module>/<confirmed-page>',
  component: '<confirmed-component-path>',
  title: '<确认中文标题>',
}
```

注意：
- 前端生成 route 可以按项目默认配置 `authorized: true` 和 `title`，用于开发期 / demo / 生成候选路由可访问和 Tab 标题可见；这不是正式平台菜单权限或平台菜单标题已完成的证据。临时生成的前端 route title 必须使用中文标题，生产前再替换为平台可识别字符串编码和平台多语言。
- 生产交付时必须区分：前端 route 中的 `authorized: true/title` 是候选访问配置；正式菜单入口、角色权限、菜单标题和多语言仍需到平台菜单 / 权限 / 多语言维护。
- 已确认完全由平台线上菜单驱动、且目标项目约定 route 不写前端 title/authorized 的存量 route，可以省略 `authorized: true` 和 `title`，并记录标题来自平台菜单；但新增生成代码默认不应因为这个规则去删除项目模板要求的两个属性。
- 若前端生成模板要求子路由可直达，子路由必须配置 `title`，并按 `authorized: true` title 规则进入 Handoff。
- 诊断访问失败前，先确认菜单入口和角色菜单权限。
- 页面属于子模块时，确认 `registerRegex` 是否匹配路由前缀。
- 菜单可见但点击 404 时，先比对点击后的实际 URL 和 route path，再改权限或路由。

## 直接 URL 页面

只有确认该页面不是普通菜单驱动页面时，才使用这个模式。
页面位于 `packages/<module>` Umi 子模块时，component 必须使用已确认的 Umi 页面引用；`single-router-ts` pages 目录模式可使用 `Requisition/Detail`、`./Requisition/Detail` 或 `@/pages/Requisition/Detail`，`split-routes-dir` 模式通常使用 `@/pages/...`，不得沿用父应用相对路径或 `../src/pages/...` 文件系统相对路径。

临时生成中文 title：

```ts
{
  path: '/<confirmed-module>/<confirmed-detail>',
  component: '<confirmed-component-path>',
  authorized: true,
  title: '<确认中文标题>',
}
```

生产替换后的字符串编码 title：

```ts
{
  path: '/<confirmed-module>/<confirmed-detail>',
  component: '<confirmed-component-path>',
  authorized: true,
  title: 'hzero.common.title.<confirmedTitleCode>',
}
```

注意：
- `authorized: true` 主要用于已确认的直接 URL 访问、菜单权限外页面，或开发期新增路由的临时候选访问配置；临时配置不能替代平台菜单和权限维护。
- `authorized: true` route 必须显式配置 `title`，否则 HZERO Tab 标题可能为空；看到 `authorized: true` 但缺 `title` 应判为配置缺口。
- 前端临时生成 route title 必须使用中文标题，便于开发期 / demo / 候选路由 Tab 可读。进入生产可用前必须在 Handoff / production replacement 中提示：到平台配置菜单权限、菜单标题和平台多语言，前端 route 的 `title` 应改为平台可识别的字符串编码，优先 `hzero.common.*`；业务命名空间编码需到 `/hpfm/prompt` 补译文。不得写 `intl.get('xx')`、`intl.get('xx').d(...)` 或其它运行时表达式。
- 新增/生成 route config 不写 `titleType`；标题编码和平台多语言替换在 Handoff / production replacement 中处理。
- 菜单可见但点击 404 时，不要用这个模式修；应先排查 menu path、route path、子模块注册、`registerRegex`、remoteEntry/chunk、权限和父子模块加载。

## `/public`、`/private`、`/pub` 路由

只有确认页面确实不走普通登录态菜单布局时，才使用这些路由。

### `/public`
- 用于免登录公共页面。
- 页面应使用公共后端接口。
- route path 和 key 包含 `/public`，例如 `/public/<service>/<page>`。
- 路由已定义但不生效时，确认根 router 是否挂载了 `/public` 对应的 `PublicLayout`。

### `/private`
- 用于基于 token 的免登录访问。
- URL 应按目标系统契约携带访问 token。
- route path 和 key 包含 `/private`，例如 `/private/<service>/<page>`。
- 路由已定义但不生效时，确认根 router 是否挂载了 `/private` 对应的 `PrivateLayout`。

### `/pub`
- 用于不展示普通菜单栏和顶部功能条的页面。
- route path 和 key 包含 `/pub`，例如 `/pub/<service>/<page>`。
- 页面仍需明确实现，不要套用普通菜单页面的权限行为。

规则：
- 不要把普通菜单页面改成 `/public`、`/private` 或 `/pub` 来绕过路由或权限问题。
- 不要编造 token 参数名、公共 API 契约或布局可用性；必须从项目代码或平台文档确认。
- 设计文档中只有确认访问模式后，才可把这些前缀作为 `generatedCandidate`。

## 动态 Tab 详情页

只有确认详情页是通过直接导航或页面动作打开，而不是普通菜单入口时，才使用这个模式。
页面位于 `packages/<module>` Umi 子模块时，component 仍必须使用 `@/pages/...`，不得沿用父应用相对路径。

### 每条记录独立详情 Tab

```ts
{
  path: '/<confirmed-module>/<confirmed-detail>/:id',
  component: '<confirmed-component-path>',
  authorized: true,
  mode: 'dynamic',
  title: '<确认中文标题>',
}
```

打开 Tab 时，`key` 和 `path` 都使用可被上面 route 匹配的具体详情路径：

```ts
const detailPath = `/<confirmed-module>/<confirmed-detail>/${id}`;

openTab({
  key: detailPath,
  path: detailPath,
  closable: true,
});
```

### 同一记录的详情/编辑需要两个独立 Tab

当详情态和编辑态本身需要成为两个 HZERO 应用内 Tab，页面模式属于页面身份，应进入 route path，而不是只放进 query/search：

```ts
{
  path: '/<confirmed-module>/<confirmed-feature>/detail/:pageMode/:id',
  component: '@/pages/<confirmed-feature>/detail',
  authorized: true,
  mode: 'dynamic',
  title: '<确认中文标题>',
}
```

```ts
type PageMode = 'view' | 'edit';

function openDetail(record: { id: string }, pageMode: PageMode) {
  const path = `/<confirmed-module>/<confirmed-feature>/detail/${pageMode}/${record.id}`;

  openTab({
    key: path,
    path,
    closable: true,
  });
}

openDetail(record, 'view');
openDetail(record, 'edit');
```

详情页统一从 params 解析页面身份：

```ts
const params = useParams<{ pageMode?: PageMode; id?: string }>();
const location = useLocation();
const routeContext = getRouteContext(location, params);
const editable = routeContext.pageMode === 'edit' || routeContext.pageMode === 'create';
```

新建态默认使用独立可匹配路由，不把 create 伪装成 detail 子态，也不依赖虚拟 key 后缀：

```ts
{
  path: '/<confirmed-module>/<confirmed-feature>/create',
  component: '@/pages/<confirmed-feature>/detail',
  authorized: true,
  title: '<确认新建中文标题>',
}
```

```ts
const path = '/<confirmed-module>/<confirmed-feature>/create';
openTab({ key: path, path, closable: true });
```

新建页通常只有一个稳定 Tab，route `mode` 可省略或使用项目默认 `route`；只有项目明确支持并需要多个新建实例同时打开时，才按 dynamic Tab 设计补充 `mode: 'dynamic'` 和实例级唯一 key。新建页固定使用 `/create`；`/detail/create` 属于违规路径，发现后迁移到 `/create`，不得在 Route Context / Edit Mode Contract 中记录为可接受 routePattern。

注意：
- 只有多个详情需要打开成独立 Tab 时，才使用 `mode: 'dynamic'`。
- 这里的 `authorized: true` 不是修复菜单 404 的手段；先确认直接 URL 或菜单外访问场景。
- HZERO 应用内详情独立 Tab 应优先使用项目已有 openTab/navigation wrapper 或 dynamic route 配置；不要用 `window.open` 拼 hash route 代替。
- 每条记录一个详情 Tab 时，route 必须配置 `mode: 'dynamic'`，`openTab` 的 `key` 和 `path` 都使用带记录 id 的具体详情路径：

```ts
openTab({
  key: `/<prefix>/<feature>/detail/${id}`,
  path: `/<prefix>/<feature>/detail/${id}`,
});
```

- 同一 pathname、不同 search 也需要不同 Tab 时，在 `mode: 'dynamic'` 基础上配置 `dws: true`，并在设计/任务中记录 search/query 的唯一性来源；这通常只用于项目既有兼容或明确确认的特殊场景，不作为详情/编辑/新建页面模式的新代码默认范式。
- dws 推荐模板位于 `front-hzero-enterprise-process-control` 的 dws dynamic-tab route 模板。该模板只用于已确认同 pathname 不同 search/query 独立 HZERO 系统页签；有列表页时仍推荐父 route + list/detail 子 routes，detail 子 route 配置 `mode: 'dynamic'` 和 `dws: true`。新生成记录详情仍优先采用 `/detail/:id` path 参数范式。
- create/view/edit 需要作为普通 HZERO 系统页签打开且要求 URL 直接表达页面模式和记录身份时，推荐模板位于 `front-hzero-enterprise-process-control` 的 open-tab page mode route 模板。有列表页时必须使用父 route + list/create/view/edit 子 routes，子 route 使用 `mode: 'route'` 或省略默认 route；新建默认使用 `/create`，查看/编辑默认使用 `/detail/view/:id`、`/detail/edit/:id`，页面模式和记录身份仍进入 path。该模板只能证明 route 可匹配，不能证明一个详情页签会被复用；若平台按 `path` 区分页签，`/detail/view/:id` 和 `/detail/edit/:id` 会自然打开多个详情页签。
- 需要“新建独立页签，编辑/详情复用同一个详情页签”时，推荐模板位于 `front-hzero-enterprise-process-control` 的 reusable fixed path route 模板，并同步使用 `open-tab-reusable-fixed-path-best-practice.md` 的链路。此模式使用固定 `/create` 作为新建页签，固定 `/detail` 作为编辑/详情复用页签，记录 id 和 `pageMode` 来自已确认的 tab context / navigation state / sessionStorage fallback 或项目等价 wrapper。不得把记录 id 放进可复用详情 path，否则平台按 path 区分时仍会多开页签。
- create/view/edit 需要每条记录或每个 pageMode 成为独立 HZERO 系统页签时，推荐模板位于 `front-hzero-enterprise-process-control` 的 dynamic-tab page mode route 模板。有列表页时仍必须使用父 route + list/create/view/edit 子 routes，子 route 配置 `mode: 'dynamic'`；新建默认使用具体 `/create` path，只有同 pathname 不同 search 也需要独立时才补 `dws: true`。
- `openTab.key` 不得拼出 route config 无法匹配的虚拟地址。错误示例：route 只有 `/<prefix>/<feature>/detail/:id`，却使用 `key='/<prefix>/<feature>/detail/1/edit'`、`path='/<prefix>/<feature>/detail/1'` 来区分编辑态；若平台用 key 参与内容路由或缓存激活，可能打开空白页签。
- `path` 必须是 route config 可匹配的真实路径；`search/query` 只能承载辅助状态。若详情/编辑要两个独立 Tab，必须使用内置 `detail/view/:id`、`detail/edit/:id` path 参数，不用 `?editFlag=true/false`、`?mode=edit/view` 或 `?action=create` 表达页面模式或页签身份。
- 若只是复用父级 Tab，不得把详情 path 或记录 id 作为 `openTab.key`；这会变成详情级业务页签。

### Query/Search 使用边界

query/search 可以使用，但不能承载页面主身份、目标详情页主记录 ID、页面模式或 HZERO Tab 唯一身份。

允许示例：

```txt
/<prefix>/<feature>/list?status=SUBMITTED&page=2
/<prefix>/<feature>/list?keyword=abc&sort=creationDate,desc
/<prefix>/<feature>/list?supplierId=10001&itemId=20001
/<prefix>/<feature>/detail/view/1?source=list
/<prefix>/<feature>/detail/edit/1?returnTo=/%3Cprefix%3E/%3Cfeature%3E/list
/<prefix>/<feature>/detail/view/1?activeTab=approval
/<prefix>/<feature>/detail/view/1?navigationToken=abc
```

禁止作为新生成代码范式：

```txt
/<prefix>/<feature>/detail/1?editFlag=true
/<prefix>/<feature>/detail/1?mode=edit
/<prefix>/<feature>/detail?id=1&mode=view
/<prefix>/<feature>/detail?action=create
/<prefix>/<feature>/detail/1?tabKey=edit
```

判定规则：
- 刷新页面后决定“这是哪个业务页面 / 哪条目标详情主记录 / 哪种页面模式”的信息，放在 route path/params。
- 只影响当前页面展示细节、来源、返回、筛选、分页、排序、详情内子 Tab 激活项或一次性导航关联的信息，可以放在 query/search。
- 需要 HZERO 独立页签区分的信息，优先进入 route path，并保持 `openTab({ key: path, path })`；只有 FDS/TDS/用户明确要求同 pathname 不同 search 独立页签时，才用 `dws/queryStateKey`，项目旧写法不能单独授权该模式。
- `editFlag`、`mode`、`action` 等 query 不能作为页面模式来源或 fallback 读取；命中时必须迁移到 path 中已确认的 `pageMode`，入口也不得主动 emit。

## 当前 Tab 页详情

当前 Tab 页详情的运行时要求是点击列表中的详情/编辑后，HZERO 应用内页签数量不增加，当前菜单页内容被详情替换或在同一父 route 内切换。

推荐实现是使用项目已确认的 `openTab` / navigation wrapper，并让 `key` 复用父级菜单或父级 route 的 Tab key，`path` 指向详情路由：

```ts
openTab({
  key: '/<prefix>/<feature>',
  path: `/<prefix>/<feature>/detail/${id}`,
});
```

其中：
- `key` 是 HZERO 页签身份，必须对应父级菜单 path、父级 route 或项目确认的父 Tab key。
- `path` 是当前 Tab 内实际渲染的详情 route，可以携带记录 id。
- `key` 不得使用详情 path 或记录 id，否则会被识别为新的业务页签。

Umi 子模块路由配置仍应使用稳定父 route 下挂 list/detail 子路由：

```ts
const FeatureRoute = [
  {
    path: '/<prefix>/<feature>',
    authorized: true,
    routes: [
      {
        title: '<确认列表中文标题>',
        path: '/<prefix>/<feature>/list',
        component: '@/pages/<feature>/list',
        authorized: true,
      },
      {
        title: '<确认详情中文标题>',
        path: '/<prefix>/<feature>/detail/:id',
        component: '@/pages/<feature>/detail',
        mode: 'route',
        authorized: true,
      },
    ],
  },
];
```

`mode: 'route'` 可以省略，因为 HZERO/Umi route 默认按普通 route 处理；在设计文档中建议显式记录 `mode=route/omitted-default-route`，避免被误补成 `dynamic`。前端生成代码可按项目默认保留 `authorized: true` 和 `title` 作为候选/开发可访问配置；只有已确认完全由平台线上菜单驱动、且目标项目约定 route 不写前端 title/authorized 时，才可省略这两个属性并记录标题来自平台菜单。无论是否保留前端候选 title，Handoff 都必须提示正式菜单权限、菜单标题和平台多语言仍需平台侧维护。

同父 route 嵌套子路由只负责保证路由结构和详情 path 语义，不能单独证明当前 Tab 复用。菜单 path 指向父 route 还是 list 子路由必须按项目菜单约定确认；无论菜单入口是哪一个，列表和详情都必须处在同一稳定父 route 下，并通过 `openTab({ key: parentTabKey, path: detailPath })` 或项目等价 API 复用父级 Tab key。

单父 route + query/state 切换不是合法页面模式；即使目标项目已有该写法，也只能形成 migration finding，必须迁移到可匹配 path。新生成当前 Tab 页详情时，不要把列表和详情都压在同一个 component 内再用 `?mode=detail` 切换。

query/state 在新生成详情页中只能作为辅助状态，不承载页面主身份、目标详情页主记录 ID 或页面模式：

```ts
history.push({
  pathname: `/<prefix>/<feature>/detail/${id}`,
  search: '?source=list&activeTab=approval',
});
```

其中详情身份来自 `/<prefix>/<feature>/detail/:id`，`source/activeTab` 只表达来源页、返回策略或详情内子 Tab。若需要表达编辑/详情页面模式，应使用内置 `/<prefix>/<feature>/detail/edit/:id`、`/<prefix>/<feature>/detail/view/:id` path 参数。

规则：
- 不要只因为代码使用 `history.push('/<prefix>/<feature>/detail')` 就判定为当前 Tab 页跳转；HZERO 页签容器可能把同级独立详情 route 打开为新的应用内 Tab。
- `routeOpenMode=menu-current` 不推荐默认生成 `/<prefix>/<feature>/detail` 这种同级独立详情 route；除非项目运行时证据证明它复用父 Tab key，否则应使用父 route + `routes` 嵌套子路由，并通过 `openTab` / navigation wrapper 传入父级 `key`。
- `routeOpenMode=menu-current` 时，必须记录 `parentTabKey`、`targetDetailPath`、navigation API 来源和参数形态；验证点击详情前后 `window.tabsAction.getTabs()` 数量不增加，active tab key 等于父级 key 或符合项目定义的同父 route key。
- 新生成详情页不得使用 `/<prefix>/<feature>?mode=detail&id=<id>` 作为页面主路由；query/state 可用于 `source`、`returnTo`、`activeTab`、`navigationToken`、筛选/分页回填等辅助状态，但不得替代 path params 中的详情 id，也不得用 `editFlag/mode/action` 表达页面模式。
- `hzero-openTab` 不是天然“新开 Tab”，也不是天然“可复用 Tab”；`openTab` 是 HZERO 页签容器导航 API，实际行为取决于平台的 key/path 去重策略，并必须通过运行态页签数量验证。固定 `key` 不能单独证明复用；若 `path` 随记录 id 变化，平台按 path 区分页签时仍会多开。`openTab-parent-key` 表示当前 Tab 复用，固定 detail key/path 表示可复用独立业务页签，记录级 concrete path key 才表示每条记录独立业务页签。
- 若需要详情保留列表页签并新开业务页签，应改为 `hzero-openTab` 独立页签或 `dynamic-tab`，并确认详情级 `key`、`title`、`mode`、`dws`。
- FDS/TDS/用户只写“新标签页”时，不能直接判定为 `hzero-openTab`、`dynamic-tab` 或 `browser-new-tab`。应追问这里的新标签页是“新开一个系统页签”“每条记录新开独立系统页签”还是“浏览器新标签页”；若流程允许变更 FDS，可同时提供“当前菜单页签内打开（变更 FDS）”。用户可见标题和描述不得写成 `hzero-openTab`、`dynamic-tab`、`browser-new-tab`、`HZERO openTab`、“系统页签打开”、“通过 openTab 打开标签页”或“系统动态页签”；描述必须详细说明选择后的页面行为、适用场景、限制、内部映射和验证影响。参考子模块、相似页面、工程 evidence、routeConfig 或 `openTab`/`mode: 'dynamic'` 不得裁剪、合并、排序或改写内置路由/页签选项；若同类参考模块在相同入口/目标上存在可采纳且覆盖当前 question 全部入口的 Drawer 证据，可额外追加唯一一个 `抽屉打开` 候选并说明会变更 FDS。参考 Modal/弹窗不得成为选项。普通编辑页或 route-page 的当前页选项必须写 `当前菜单页签内打开`，并继承 `/create`、`/detail/view/:id`、`/detail/edit/:id` 路由模板；确认前 routeOpenMode 只能写 `generatedCandidate/needs-confirmation`，routeMode `dynamic` 只能写候选。

## 跳转 API 选择

HZERO 应用内从一个页面进入另一个页面，默认使用固定坐标 `import { openTab } from 'utils/menuTab';`。`openTab` 可以控制 Tab key、路径、标题和动态 Tab 行为，但它本身不是“新开标签页”的同义词；必须结合 `key`、route `mode`、dws 和运行时页签数量判断。该入口是项目级基础能力，不存在页面级 import 缺口或 route owner 回退；若它导致编译/运行失败，按整个前端项目不可用的构建/运行时故障处理。不得猜测其它 navigation wrapper。`history.push` 只能作为当前组件内 URL 状态变化或浏览器历史栈操作。

规则：
- 列表进入详情、编辑、新建、跨菜单页面跳转、需要指定 Tab 标题或涉及 `mode: 'dynamic'` 时，使用 `openTab`。
- 当前 Tab 页详情使用 `openTab({ key: parentTabKey, path: targetDetailPath })`；`key` 必须是父级菜单 path、父级 route 或项目确认的父 Tab key。
- 独立动态详情使用 `openTab({ key: concreteDetailPath, path: concreteDetailPath })`，route 配置 `mode: 'dynamic'`；同 pathname 不同 search 也要独立时再加 `dws: true`。
- 可复用固定详情页签使用 `openTab({ key: fixedDetailPath, path: fixedDetailPath })`，route 配置 `mode: 'route'` 或省略默认 route；页面模式、记录 id 和标题必须由已确认 tab context / navigation state / sessionStorage fallback 或项目等价 wrapper 同步，并验证连续点击不同记录时详情页签数量不增加。
- `history.push` 只用于当前页面内 query/search 同步、同组件 step/wizard URL 状态变化、`history.goBack()` / `history.goForward()` 等浏览器历史栈操作。
- `<Link>` 只用于静态文字链接、面包屑或不需要 Tab 元信息的简单链接；若需要 HZERO Tab key/title/mode/dws 行为，不使用 `<Link>` 作为主实现。

## Umi Route 参数速查

- `authorized`：前端候选/开发可访问配置；新增生成 route 可按项目默认设置。设置为 `true` 时必须同时设置 `title`，但它不等于平台正式菜单权限已配置。
- `title`：Tab 标题。前端生成 route 若带 `authorized: true` 则必填；临时生成值必须是中文标题，普通平台菜单标题最终来自平台菜单和平台多语言。生产前再替换为平台可识别字符串编码。
- `titleType`：新增/生成 HZEROJS route config 不写该字段；若存量项目自定义支持，必须有项目证据并按存量规则处理。
- `mode`：`route` / `dynamic`。同父 Tab 复用为 `route` 或省略；每条记录独立 Tab 用 `dynamic`。
- `dws`：dynamic with search。同 pathname 不同 search 也要开不同 Tab 时配置 `true`。
- `exact` / `redirect`：新增/生成 route 默认省略 `exact`；只有目标项目现有路由模式或明确证据要求时才写。新生成 route config 不配置 `redirect`；父级 `routes` 容器不得配置 `exact: true`，并必须在验证中证明 list/detail/create/edit 等子路由可匹配。
- `priority`：路由匹配优先级；高优先级覆盖低优先级，只有存在路由冲突或内置页面覆盖证据时才调整。

## 路由参数与编辑态控制

详情、新建、编辑和复制页面不得直接依赖 `window.location.hash` 判断业务状态。

推荐模式：

```ts
const location = useLocation();
const params = useParams();
const routeContext = getRouteContext(location, params);
const editable = routeContext.pageMode === 'edit' || routeContext.pageMode === 'create';
```

规则：
- 页面组件应通过 `useLocation()`、`useParams()` 和 `getRouteContext(location, params)` 或项目等价 wrapper 统一解析 `id`、`isCreate`、`pageMode`，并可派生只读兼容字段 `editFlag`。
- 禁止只用 `window.location.hash.includes('editFlag=true')`、hash 正则或散落的 `location.search / params.xxx` 作为业务状态判断。
- `/create` 必须默认 `isCreate=true`、`editable=true`、`pageMode=create`；不得读取 `?editFlag=true`。新建路由固定使用 `/create`；`/detail/create` 属于违规路径，发现后迁移。
- query 解析使用 `URLSearchParams` 或项目已确认 wrapper，但 query 不得承载页面身份、记录主键或 pageMode。存量 `editFlag/mode/action` 链接必须迁移到 canonical path，不在新页面保留双解析分支。
- 详情页主身份必须来自 path params，例如 `/detail/:id`、`/detail/view/:id`、`/detail/edit/:id`；query/state 只能作为辅助状态，不得用 `?mode=detail&id=<id>`、`?editFlag=true/false`、`?action=create` 取代详情/编辑/新建路由，也不得保留旧链接读取分支。
- UI 是否可编辑以 routeContext、UI Contract 和业务状态守卫为准；DataSet 字段中的 `editFlag` 只能作为展示/提交字段，不作为页面编辑态权威来源。
- 保存后如仍停留编辑态，跳转必须显式保留编辑 path/pageMode；如进入只读详情，必须有业务来源。
- 切换不同 id 或同 route 多 Tab 时，异步加载状态必须绑定当前 id，避免旧记录编辑态复用。

## 浏览器新标签页边界

`browser-new-tab` 只适用于外部链接、跨系统链接，或用户明确要求浏览器级新标签页且设计说明不走 HZERO Tab 的场景。

禁止模式：

```ts
window.open(`#${pathname}${search}`, '_blank');
window.open(`/#${pathname}${search}`, '_blank');
window.open(hashPath, '_blank'); // hashPath 仅包含 #... 时禁止
```

规则：
- HZERO 内部 route、菜单页、详情页、编辑页默认不使用浏览器 `window.open`。
- 用户只确认“新标签页”时，必须追问并使用用户可见选项标题“新开一个系统页签”“每条记录新开独立系统页签”“浏览器新标签页”；流程允许变更 FDS 时可同时展示“当前菜单页签内打开（变更 FDS）”。不得自动生成 browser-new-tab，也不得直接把 `dynamic-tab` 标为已确认；没有明确弹层来源时不得追加 Drawer/Modal/弹窗/抽屉选项。
- 即使确认 `browser-new-tab`，也必须传入完整 URL。完整 URL 应来自外部链接、项目 URL builder，或基于 origin/public base/basename 构造；禁止把 `#...`、`/#...`、pathname/search 片段直接传给 `window.open`。
- `utils/menuTab` 的命名导出 `openTab` 是项目级基础能力；不得将其作为页面级路由阻塞、要求用户提供 helper、猜测其它 import 或用 `window.open` 兜底。若它导致编译/运行失败，按整个前端项目不可用的构建/运行时故障处理。

## 路由工具边界

HZERO core utils 中常见路由工具包括 `gotoPage`、`getRoutes`、`getMicroModuleInfoList`、`getMicroModuleInfo`、`isSpecialRouter`。

规则：
- `gotoPage(pathname, search)` 是基于 dva/router 的普通跳转候选；它不能替代 HZERO `openTab`、dynamic Tab 或菜单数据契约。
- `getMicroModuleInfo(microModule)` 可作为判断目标微前端模块是否存在的候选工具；不能用它证明 `remoteEntry`、chunk、registerRegex 或菜单权限正确。
- `isSpecialRouter` 可用于识别 `/pub`、`/public`、`/private`、`/link`、`/iframe`、`/pure-pub` 等特殊路由候选；特殊访问模式仍需项目路由和布局证据确认。
- 使用这些工具前，必须确认 `utils/utils` alias 和 export 存在；不要把 core 源码路径复制到业务 import。

## 子模块路由加载

```ts
// hzeroMicro 相关配置形态因项目而异。
{
  microConfig: {
    registerRegex: '\\/<confirmed-prefix>',
  },
}
```

注意：
- `registerRegex` 应收敛到已确认的路由前缀。
- 不要默认使用 `\/.*` 或 `.*`；只有父工程首屏装载机制明确要求且目标范围确实覆盖全部路径时才允许宽匹配，并必须记录来源和影响范围。
- 多个配置并存时，检查 `microServices`、`packages` 和 `microConfig` 的优先级。
- 验证父模块已注册子模块包，并确认构建产物或部署资源中存在 `remoteEntry.js` 和页面 chunk。

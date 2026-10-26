# HZEROJS Submodule Runtime Gate

用途：沉淀 `packages/` 子模块的新建、接入、页面开发、Review 和 Verification 最佳范式。Frontend Design 阶段的落位合同在 `front-hzero-enterprise-design` 的 HZEROJS 子模块落位合同。

## 阅读路由
- 判断工程历史写法能否沿用时读 `Evidence vs Baseline`。
- 新建或补齐子模块骨架时读 `Minimum Structure`、`tsconfig.json`、`config/config.ts` 和 `config/config.dev.ts`。
- 接入父工程、路由聚合或 registerRegex 时读 `Parent Registration`、`config/routes` 和 `src/routes-config.tsx`。
- 生成页面和 mock demo 时读 `Page Pattern`、`Mock Request`。
- 验证、Review 或拒收时读 `Verification` 和 `Rejection Conditions`。
- 缺少项目参考但必须给最小骨架时读 `Minimum Skeleton Without Project Reference`。

## Owner Boundary

本文只拥有 HZEROJS `packages/<module>` 子模块的运行期骨架、父工程注册、route entry、`registerRegex`、package/tsconfig/config 模板、mock plugin 接线和子模块验证门禁。

以下内容不在本文扩写：

- 页面 UI、DataSet、Form/Table、filterBar、row actions、master-detail 细则归 `front-hzero-choerodon-ui` 及其 scenario reference。
- openTab/current-tab/dynamic-tab 的业务交互确认归 `front-hzero-enterprise-design` 的设计合同；本文只保留子模块 route 模板和运行拒收。
- mock handler 业务数据、runtime store、servicePrefix、mock-to-production 切换细则归 `front-hzero-mock-request`；本文只保留子模块 plugin/handler 文件位置、模板和父工程注册门禁。
- route/menu/permission/runtime layout 的领域诊断归 `front-hzero-route`、`front-hzero-micro` 和 `front-hzero-runtime-config`。

新增规则若只影响组件写法、页面组合、业务字段、mock 数据语义或单一场景 SOP，应下沉到对应 owner；只有会影响子模块可加载、可构建、可注册或可验证的规则才进入本文。

## Evidence vs Baseline

目标工程证据用于识别项目现状，不等于生成准则。新建或改造 HZEROJS 子模块时，内置规则始终是最低主线；参考工程只能补充项目事实、命名、目录和局部风格。只有证明参考模式比内置规则更完整、更安全或更贴合目标工程运行约束，且不削弱本文 owner gate 时，才允许把该项标记为 `follow-project`。

| 场景 | 决策 |
| --- | --- |
| 工程写法更完整、更安全，且通过 owner gate 证明优于内置规则 | 该项可 `follow-project`，并记录证据路径、优于内置规则的理由和保留的内置门禁 |
| 工程写法只是命名、目录或封装差异，不降低完整性/安全性 | `merge`：内置规则语义和门禁不变，只兼容项目局部差异，并记录与 baseline 的差异 |
| 工程历史模块缺文件、漏父工程注册、缺路由聚合、`registerRegex` 过宽或构建链路不可验证 | 标记 `legacy-risk`，不得作为新代码默认范式 |
| 工程约定与 baseline 冲突且无法判断是否为刻意设计 | `block + confirmationNeeded=yes`，不得直接生成 runnable implementation |

工程探索是拿事实，不是复制历史习惯。新建或改造时应选择不破坏项目运行、且满足最低完整性和安全门禁的方案；历史模块中的问题只能作为兼容风险记录，不能放宽本参考的硬规则。若参考模式只能证明“项目里这样写过”，不能证明其质量或优势，默认 `follow-baseline` 或 `merge`，不得用 `follow-project` 覆盖内置规则。

更优判定和 question gate 按 `baseline-comparison-rubric.md` 的 `Superiority Decision and Question Gate` 执行：AI 只能在 `superiorityEvidence` 可复核且不命中关键冲突时自判；涉及运行行为、接口链路、权限链路、mock/production 数据链路或 owner-confirmed 关键区时，必须进入独立 `questionGateQueue[]` 项。

`baselineComparison` 至少记录：`projectEvidence`、`baselineRule`、`difference`、`decision(follow-project/follow-baseline/merge/block)`、`reason`、`superiorityEvidence`、`aiDecisionAllowed`、`questionReason`、`legacyRisk`、`confirmationNeeded`。

## Minimum Structure

新建子模块最小结构：

```text
packages/<module-name>/
├── package.json
├── tsconfig.json
├── config/
│   ├── config.ts
│   ├── config.dev.ts
│   ├── router.ts               # single-router-ts mode: one route file only
│   └── routes/                 # split-routes-dir mode: multiple route files or explicit split required
│       ├── index.js
│       └── <FeatureRoute>.js
├── dev-mock/                    # optional; mock-request only
│   ├── <module>-dev-mock-plugin.js
│   └── <module>-dev-mock.js
└── src/
    ├── index.less
    ├── routes-config.tsx        # optional; requires user/project confirmation
    ├── utils/
    │   └── constants.ts         # optional
    └── pages/
        └── <PageName>/
            ├── index.tsx
            ├── api.ts
            ├── lang.ts
            ├── types.ts
            ├── <name>DS.ts           # single DataSet page
            ├── stores/               # optional; only for multiple DataSets/helpers
            └── components/
```

如果只是新建空子模块，`src/pages` 可暂不创建；但 `package.json`、`tsconfig.json`、`config/config.ts`、`config/config.dev.ts` 和一个 Umi 路由入口必须存在。路由入口二选一：仅新增一个路由文件时使用 `config/router.ts`；存在多个路由文件、项目已有 `config/routes/**` 聚合模式或用户明确要求拆分时，使用 `config/routes/index.js` + FeatureRoute。`config/config.dev.ts` 用于支持子包独立 `start/package-start` 和开发态配置加载；不得因为父工程启动为主就省略。是否创建 `src/routes-config.tsx` 不得默认强制，应通过项目证据或 question 确认。

`dev-mock/<module>-dev-mock-plugin.js` 和 `dev-mock/<module>-dev-mock.js` 只在 `queryMode=mock-request` 或用户明确要求可运行 mock 时生成；没有 mock 需求时不作为最小骨架必选项。`src/.umi/`、`src/.umi-production/`、`lib/`、`dist/`、`node_modules/` 是生成产物或依赖目录，不得作为新子模块业务目录生成、迁移或提交依据。

## package.json

默认模板：`templates/submodule-package.json.template`。

规则：

- `name` 必须替换为真实 package name，不得残留 `__PACKAGE_NAME__`。
- `scripts` 是新建 Umi 业务子模块硬必选；优先对齐父工程或相邻子模块，无工程模板时使用 HZEROJS Umi 子模块默认命令，至少包含 `start`、`build`、`build:ms`、`transpile`、`build:app`，并保留 `prettier`、`test`、`test:coverage` 候选脚本。`transpile` 属于发布/转译模板能力；Verification 阶段不得把包内 `transpile` 当成直接验证入口，最终编译必须且只能走根命令 `npm run build:ms -- <module>`，不得替换为 yarn、pnpm 或其它 build 命令。
- `files` 必须按项目实际发布边界裁剪；无项目证据时使用模板默认值，保留 `lib`、`config/config.ts` 和 `.umi/.umi-production`、`lib/config/*` 排除项。`lib` 在这里是发布清单口径，不代表业务源码交付；不得把实际生成出的 `lib/` 目录当成页面、DataSet、service、路由证据或 Handoff 资产。不得重复写同一排除项。
- `dependencies`、`peerDependencies`、`devDependencies`、`resolutions`、`volta`、`private`、`main` 等字段必须来自相邻子模块、父工程模板、包管理器/workspace 证据或用户模板；无证据时不要默认生成。不得在新子模块内新增真实 dependency 版本来绕过父工程依赖治理。
- 若项目已有相邻子模块模板，优先 follow project，但必须保留“scripts 必选”“排除生成产物”“files 去重”和“不得引入无来源依赖版本”的约束。

## Parent Registration

父工程注册入口必须先由工程证据确认。常见 active registry 包括根目录 `config/config.ts` 引用的 `config/packages-config.js` / `packages-config.ts`、`.hzerorc.js` / `.hzerorc.json`、workspace / package manager 配置，以及 CI/脚本显式读取的 legacy registry。不要只因为某个示例存在就假设它是唯一入口；无法确认时写 `parentRegistrationStatus=partial/blocked`。

根目录 `config/packages-config.js` 的常见注册形式：

```js
const packages = [
  { name: '<module-name>' },
];

module.exports = packages;
```

规则：

- 只新增当前子模块一行。
- 不顺手注释、取消注释或重排其它模块。
- 不改变已有模块顺序，除非项目有明确排序规则。
- 新建 `packages/<module-name>` 必须同步检查所有 active registry 是否接入；无法确认时阻塞或写入待确认项。
- 如果 active registry 不止一个，必须记录每个入口的状态：`complete / partial / missing / conflict / not-applicable`。任一必要入口缺失，不得声明子模块生产可达。
- `config/packages-config.js` / `hzeroMicro.packages` 只承载子模块包注册，不承载 Umi plugin 注册。不得在包条目中写 `plugins: [require.resolve('../packages/<module>/dev-mock/<module>-dev-mock-plugin')]` 来注册 mock plugin；mock plugin 必须注册到父工程 `config/config.ts` 顶层 `plugins` 数组，或由该数组注册父工程聚合 plugin。

## tsconfig.json

默认模板：`templates/submodule-tsconfig.json.template`。生成新 HZEROJS Umi 业务子模块时，`packages/<module>/tsconfig.json` 直接复制该模板内容，除非项目内已有可采纳子模块模板或用户明确提供模板；不得在生成时自行增删字段、重写 `include/exclude`、调整 `emitDeclarationOnly/outDir/rootDir/baseUrl`，也不得补 `compilerOptions.paths`。

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "emitDeclarationOnly": true,
    "outDir": "./lib",
    "rootDir": "./src",
    "baseUrl": "./"
  },
  "include": ["src"],
  "exclude": [
    "lib",
    "node_modules",
    "build",
    "scripts",
    "acceptance-tests",
    "webpack",
    "jest",
    "src/setupTests.ts",
    "tslint:latest",
    "tslint-config-prettier"
  ]
}
```

规则：

- 子模块必须继承父工程 `../../tsconfig.json`，除非项目证据或用户模板明确不同；使用内置基线时必须与 `templates/submodule-tsconfig.json.template` JSON 等价。
- `rootDir` 指向 `src`，`outDir` 指向 `lib`，`emitDeclarationOnly` 保持发布模板口径。
- `include` 默认只包含 `src`；`lib`、`node_modules`、`build`、`scripts`、`acceptance-tests`、`webpack`、`jest` 和测试 setup 必须排除。
- 不得在子模块 `tsconfig.json` 写 `compilerOptions.paths`；paths alias 继承父工程。
- 新建子模块不得漏 `tsconfig.json`。

## 子模块类型默认值

本参考默认面向 HZEROJS Umi 子模块。除非用户明确说“hzero-cli 子模块”，或目标工程只存在 hzero-cli 路由体系并经工程证据确认，否则新建/改造 `packages/<module>` 时不得生成 `src/config/router.js` / `components` 形态，也不得把 hzero-cli 参数当成默认路由合同。

| 子模块类型 | 默认状态 | 路由入口 | 子路由字段 | 适用条件 |
| --- | --- | --- | --- | --- |
| Umi 子模块 | 默认推荐 | `config/config.ts` + `config/router.ts` 或 `config/routes/**` | `routes` | HZEROJS `packages/<module>` 常规页面、新建子模块、未特别指定的前端交付 |
| hzero-cli 子模块 | 备选 | `src/config/router.js` | `components` | 用户明确指定、历史工程证据只支持 hzero-cli，或迁移任务要求保持 hzero-cli |

## config/config.ts

模板事实源：新建 Umi 子模块时必须先确定 `submoduleRouteEntryMode`。

| submoduleRouteEntryMode | 适用条件 | config.ts 模板 | 路由入口 |
| --- | --- | --- | --- |
| `single-router-ts` | 仅新增一个路由文件，或目标项目相邻模块使用 `config/router.ts` 聚合 | `templates/submodule-config-single-router.ts.template` | `config/router.ts` |
| `split-routes-dir` | 多个路由文件、项目已有 `config/routes/**` 聚合、用户明确要求拆分，或后续明显会多 Feature 并行维护 | `templates/submodule-config.ts.template` | `config/routes/index.js` + `config/routes/<FeatureRoute>.js` |

单路由文件模式不得再强制拆 `config/routes/index.js` 和 FeatureRoute；`config/config.ts` 必须改为 `import route from './router'` 和 `routes: route`。拆分模式则使用 `import routes from './routes'` 和 `routes: [...routes]`。两种模式都必须在已确认 route prefix 后把 `__ROUTE_PREFIX__` 替换为真实前缀。未替换占位符、删除路由入口、删除 `hzeroMicro` 或改成 catch-all，均不得进入 runnable Implementation。

标准主配置正文以 `templates/submodule-config-single-router.ts.template`、`templates/submodule-config.ts.template` 为准。这里不重复维护模板全文；只检查 `routes` 引用形态、`__ROUTE_PREFIX__` 替换结果和 `registerRegex` 收敛是否正确。

根应用配置形态是硬拒收：新建 `packages/<module>/config/config.ts` 不得生成 `import { IConfig } from 'umi'`、`export default { ... } as IConfig`、顶层 `plugins: [require.resolve('hzero-front')]`、顶层 `presets: [require.resolve('@hzerojs/preset-hzero')]` 或顶层 `registerRegex`。这些属于独立 HZERO/Umi 应用配置，不是父工程托管子模块配置；命中时通常会触发 `Invalid config key: registerRegex`，并可能因 preset/plugin 在错误上下文读取微前端配置而触发 `Cannot read properties of undefined (reading 'packages')`。修复必须回到模板形态：`extendParentConfig + routes 接线 + hzeroMicro.microConfig.registerRegex`。

父工程托管 `packages/<module>` 场景下，子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，也不得用顶层 `plugins` 作为 package-start 的补丁入口。`config/config.ts` 只允许通过 `extendParentConfig` 继承父工程 plugins，作为 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig` 的静态接线证据；父工程启动的 mock plugin 生效必须由父工程根 `config/config.ts` 顶层 `plugins` 直接注册子模块 plugin，或注册父工程聚合 plugin。

`extendParentConfig` 导入来源是硬门禁：Umi 子模块 `config/config.ts` 必须使用 `import { extendParentConfig } from '@hzerojs/plugin-micro'`，且必须在目标前端父工程根目录用 Node resolver 证明 `@hzerojs/plugin-micro` 可解析。禁止从 `@hzerojs/preset-hzero/lib/util`、`@hzerojs/preset-hzero/lib/*` 或其它深路径导入 `extendParentConfig`；命中时按不可运行配置处理，不得进入 runnable Implementation、usable=true 或 production-ready。

`registerRegex` 规则：

| 场景 | 规则 |
| --- | --- |
| route prefix 已确认 | 使用 `^\\/<prefix>(?:\\/.*)?$`，或按项目已有 `/pub`、`/public`、`/private` 前缀规则收敛，例如带 private/public/pub 可选前缀的 prefix-scoped 正则 |
| route prefix 未确认 | 不写 catch-all；使用安全占位、阻塞实现或回 Design/Task 确认 |
| 禁止 | 新子模块默认使用 `\\/.*` catch-all |

历史模块中的 `\\/.*` 只能作为遗留事实，不得作为新生成子模块默认范式。

Umi 子模块 `config/config.ts` 必须作为 route-to-module 加载事实源记录：

- 路由入口是否与 `submoduleRouteEntryMode` 一致：`single-router-ts` 使用 `config/router.ts` + `routes: route`；`split-routes-dir` 使用 `config/routes/index.js` + `routes: [...routes]`。
- `hzeroMicro.microConfig.registerRegex` 是否覆盖全部本模块菜单/页面 route prefix，且不过宽。
- route prefix 与菜单 path、平台菜单、按钮权限码分别记录；不能用 `authorized: true` 或宽 `registerRegex` 代替菜单权限。前端生成 route 可带 `authorized: true` 和中文 `title` 作为候选/开发可访问配置；`authorized: true` route 必须配置 `title`，临时 title 不默认生成编码。只有平台菜单已创建、菜单标题/prompt key 已登记并经用户或平台证据确认后，才把 route `title` 调整为平台可识别字符串编码并补平台多语言；在此之前，route title 保持中文候选并进入 Handoff / production replacement，不得为通过页面 i18n 或 C7N validator 提前改成业务 i18n key。
- 如当前页面需要 `/pub`、`/public`、`/private`、`/pure-pub` 等特殊前缀，必须在设计阶段确认访问模式和布局差异，再把这些前缀纳入 `registerRegex`。

## config/config.dev.ts

新建 Umi `packages/<module>` 子模块必须同时生成或确认 `config/config.dev.ts`，以保证用户在子包目录执行 `start/dev/package-start` 时配置文件存在。该文件优先对齐相邻子模块或项目模板；没有项目模板时使用最小开发态配置，不重复承载业务路由事实源。

推荐最小形态：`templates/submodule-config.dev.ts.template`。

```ts
// 在 config.[UMI_ENV].ts 文件中 请不要使用 extendParentConfig
export default {};
```

`config/config.dev.ts` 规则：

- 它是子模块独立启动配置文件，不替代 `config/config.ts` 的 route、`registerRegex` 和 `routes` 聚合事实源。
- 默认最小内容可以是空对象导出；命中 mock-request 时也不得注册 `../dev-mock/<module>-dev-mock-plugin`。不得在 `config.[UMI_ENV].ts` 中使用 `extendParentConfig`，也不得默认 `import config from './config'` 后展开主配置。
- 父工程托管 HZEROJS Umi 子模块默认要求子包独立 start / `package-start` 的静态接线完整。命中 mock-request 时，package-start 只检查脚本、配置和继承证据，必须通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父工程同一 mock plugin；否则后续独立 runtime acceptance 或用户手工启动子模块时不会挂载父工程已注册的 mock middleware。不要先深度探索或要求项目证据证明是否支持子包独立启动；除非用户或目标工程文档明确禁止 package-start，否则直接补齐继承证据。该检查不代表 Verification 阶段执行 `start` / `dev` / `yarn --cwd packages/<module> start`。父工程托管子模块的父工程启动 mock 生效仍必须由父工程 `config/config.ts` 顶层 `plugins` 显式注册子模块 plugin 或父工程聚合 plugin，不能只依赖子模块 `config.dev.ts`。
- 如果目标工程相邻子模块使用不同 `config.dev.ts` 模式，必须 follow project 并记录 evidence；若项目证据证明子包绝不支持独立 start，才可写 `configDevStatus=not-applicable + reason`，否则缺失按子模块骨架缺陷处理。

## config/router.ts 或 config/routes

### single-router-ts

仅新增一个路由文件时，使用 `config/router.ts`，不要为了单个页面额外拆 `config/routes/index.js` 和 FeatureRoute。模板按场景直接选用：

- list-only / 单子页面：`templates/submodule-router.ts.template`
- current-tab list/detail：`templates/submodule-router-current-tab.ts.template`
- hzero-openTab create/view/edit path：`templates/submodule-router-open-tab-page-modes.ts.template`
- hzero-openTab 新建独立、编辑/详情固定 path 复用：`templates/submodule-router-open-tab-reusable-fixed-path.ts.template` + `templates/open-tab-reusable-fixed-path-best-practice.md`
- dynamic-tab create/view/edit path：`templates/submodule-router-dynamic-tab-page-modes.ts.template`
- 同 pathname 不同 search 独立页签：`templates/submodule-router-dynamic-tab-dws.ts.template`

对应 `config/config.ts` 必须使用 `import route from './router'` 和 `routes: route`。单文件模式下，`config/routes/index.js` 和 `config/routes/<FeatureRoute>.js` 是 not-applicable，不得作为缺失项阻塞。

### split-routes-dir

多路由文件或项目要求拆分时使用 `config/routes/index.js` + `config/routes/<FeatureRoute>.js`。聚合写法、FeatureRoute 基本结构和一级页面/父子路由标准形态统一以 `templates/submodule-config.ts.template` 与对应 router templates 为准；这里不再重复代码示例，只保留后续审查规则。

规则：

- 路由入口必须先判定 `submoduleRouteEntryMode=single-router-ts / split-routes-dir`。仅新增一个路由文件时优先 `single-router-ts`；多路由文件或项目明确采用 `config/routes/**` 聚合时使用 `split-routes-dir`。
- `single-router-ts` 模式下，`config/router.ts` 是唯一路由入口，`config/config.ts` 使用 `import route from './router'` 和 `routes: route`；`config/routes/index.js` 和 FeatureRoute 缺失不是问题。`config/router.ts` 必须按场景选模板：list-only 使用 `submodule-router.ts.template`，current-tab list/detail 使用 `submodule-router-current-tab.ts.template`，普通 HZERO 系统页签 create/view/edit path 参数模式使用 `submodule-router-open-tab-page-modes.ts.template`，新建独立且编辑/详情固定 path 复用使用 `submodule-router-open-tab-reusable-fixed-path.ts.template` 并读取 `open-tab-reusable-fixed-path-best-practice.md`，dynamic-tab create/view/edit path 模式使用 `submodule-router-dynamic-tab-page-modes.ts.template`，同 pathname 不同 search 独立页签使用 `submodule-router-dynamic-tab-dws.ts.template`。
- `split-routes-dir` 模式下，`config/routes/index.js` 聚合 FeatureRoute，`config/config.ts` 使用 `import routes from './routes'` 和 `routes: [...routes]`。
- `config/config.ts` 是 Umi 子模块主配置和 `registerRegex` 接线文件，不是具体路由数组承载文件。新生成或改造路由时，完整 route array 必须写入 `config/router.ts` 或 `config/routes/**`；不得把 `const routes = [...]`、`routes: [{ ... }]`、current-tab 模板或 dynamic-tab 模板内容直接内联到 `config/config.ts`。命中内联时必须回 Implementation 修正为对应 route entry mode。
- 模板占位符只用于模板文件。实际生成的 `config/router.ts`、`config/routes/**` 和 `config/config.ts` 必须直接写确认后的 `path`、`component`、`title`、`registerRegex`、`mode`、`dws` 字符串字面量；不得额外抽 `ROUTE_PREFIX`、`FEATURE_PATH`、`LIST_PATH`、`DETAIL_PATH`、`ROUTE_TITLE`、`COMPONENT_PATH` 等常量/变量再拼接 route 配置。`component` 一旦出现，必须是字符串字面量；禁止常量引用、字符串拼接、带 `${}` 的模板字符串、函数调用或 import 常量。缺事实时回 Design/Task 确认，不用变量承接不确定性。
- `path` 必须来自已确认 route prefix；无法确认时只能 `generatedCandidate` 或 `missing + reason`。
- `split-routes-dir` 模式的子路由必须使用完整绝对路径，例如 `/<module>/requisition/list`、`/<module>/requisition/detail/:id`；不得依赖相对 path 推导。
- `single-router-ts` 模式可按目标项目模式使用父级完整绝对 path + 子级相对 path，例如父级 `/prm/requisition`，子级 `list` / `detail/:id`；也可使用完整绝对子路由，例如 `/prm/requisition/list` 与 `/prm/requisition/detail/:id`，但不得在同一 `router.ts` 中混用无证据的绝对/相对子路由风格。父级 route 与列表子 route 不得使用同一个 path；父级仅作为分组 / 稳定 Tab 边界时不配置 `component`；新生成子模块 route config 不配置任何 `redirect` route；列表子路由必须使用显式 `/list` 或项目确认的等价列表段。若平台菜单仍指向父级 path，必须在设计/任务中记录菜单、navigation 或 openTab 入口直接打开真实 `/list` path，不得用 route `redirect` 兜底，并验证父级 path、列表 path 和详情 path 都可匹配。
- 普通一级页面直接配置 `component`；有列表、详情、新建、编辑等子页面时使用父级 `routes` 嵌套路由。用户选择“当前页打开详情”或设计为 current-tab 时，不得生成列表和详情两个同级顶级 route。
- 父级 route 仅作为分组或稳定 Tab 边界时，不配置 `component`；新生成 route config 不配置 `redirect`；只有父级本身确认为可渲染页面时才配置父级 `component`。
- 新增/生成 route 默认不显式写 `exact`；只有目标项目现有路由模式或明确证据要求时才写。父级 `routes` 容器不得配置 `exact: true`，并且必须验证子路由能真实匹配。
- 有列表页的嵌套路由必须区分父级分组 path 与列表页面 path。禁止生成父级 `/feature` 与列表子路由 `/feature` 同路径结构；也禁止生成任何 route `redirect`，包括父级 `redirect + routes` 和单独叶子 redirect。父子同 path 或 redirect 结构在 HZERO 路由合并后可能导致内容区 404，尤其影响 `/feature/detail/create`、`/feature/detail/view/:id` 和 `/feature/detail/edit/:id`。标准生成路径为父级 `/feature`、列表 `/feature/list`、详情 `/feature/detail/...`，同时同步常量、菜单入口、openTab/path、返回列表路径和验证用 URL。
- `split-routes-dir` 模式的 `component` 使用 `@/pages/<PageName>` 或 `@/pages/<feature>/<page>`；不得为了排查问题改成相对文件路径、父工程 `src/pages` 路径或 hzero-cli `components`。
- `single-router-ts` 模式的 `component` 必须 follow project。新生成子模块页面固定落到 `src/pages`；pages 目录模式可使用 `Requisition/List`、`./Requisition/List`、`@/pages/Requisition/List` 或 `BasicConfig/SalarySubsidyStandard` 这类 Umi 页面引用，不得使用 `../src/pages/Requisition/List` 这类从 route config 文件位置反推的文件系统相对路径。只有改造已存在的 `src/routes/**` 存量页面，且 Target Placement 记录 `pageRoot=src/routes`、`pageRootSource=existing-file/project-evidence/adjacent-module` 与具体证据时，才使用项目别名路径，例如 `@/routes/PrmRequisition/List`。无参考基线、`pageRootSource=asset-baseline/missing/user-confirmed`、缺 Target Placement 或仅用户偏好时，不得生成 `src/routes/**` 页面。完全禁止把 `./routes/PrmRequisition/List` 当作 `src/routes` 页面引用；Umi 会将其解析为 `src/pages/routes/PrmRequisition/List`，导致 `.umi-production/core/routes.ts` 编译时报 `Module not found`。`config/config.ts` 的路由引用路径也必须同步改为 `./router`，不得仍引用 `./routes`。
- `authorized: true` 是开发期/候选访问配置，不等于平台菜单权限已配置。
- 详情页若按设计使用抽屉，不额外生成详情 route。
- 详情页若按设计使用“当前 Tab 页跳转 / `routeOpenMode=menu-current`”，必须读取 `templates/current-tab-menu-reuse-best-practice.md`。不得默认生成会被 HZERO 页签容器识别为新应用内 Tab 的同级独立详情 route，也不得生成两个同级顶级 exact route（列表 route 和详情 route 各自直接带 `component`），也不得只用 `history.push('/detail')` 或只靠父子 `routes` 嵌套声明当前 Tab。默认优先使用父 route + `routes` 嵌套子路由作为路由结构，`single-router-ts` 使用 `submodule-router-current-tab.ts.template`；列表子路由使用 `/list`，新建使用 `/create`，详情/编辑 route 使用 `/detail/view/:id`、`/detail/edit/:id`，`mode: 'route'` 或省略默认 route，并通过固定 `import { openTab } from 'utils/menuTab';` 传入父级菜单 path 或父级 route 作为 `key`，`path` 指向详情路由，例如 `openTab({ key: '/demo/demo-parent', path: '/demo/demo-parent/detail/view/{id}' })`。`/detail/create` 属于违规路径，发现后迁移到 `/create`。新生成详情页主身份和 pageMode 必须来自 route path/params；query/state 只能承载列表筛选、分页、排序、`source`、`returnTo`、详情内子 Tab 或 `navigationToken`，绝不能承载页面主身份、目标详情页主记录 ID、页面模式或 HZERO Tab 唯一身份。`?editFlag=true/false`、`?mode=edit/view`、`?action=create`、`?pageMode=edit&id=...` 命中时必须作为 migration finding 移除，不得保留只读 fallback，也不得由入口 emit。不得为 current-tab 新生成同 pathname query 分流；不得在列表组件执行部分 hooks 后按 query 条件 `return <DetailPage />`。缺少 `parentTabKey` 或 `targetDetailPath` 时必须回 Design/Task 确认；`openTab` import 不属于该类缺口。
- 详情页若需要 HZERO 系统页签，必须明确 `routeOpenMode=hzero-openTab-path-params`、`hzero-openTab-reusable-fixed-path` 或 `dynamic-tab`。`hzero-openTab-path-params` 表示使用普通 route path 参数表达 create/view/edit 页面身份，route 使用 `mode: 'route'` 或省略默认 route；有列表页且存在 create/view/edit 时，必须使用父 route + `routes` 嵌套，并优先套用 `templates/submodule-router-open-tab-page-modes.ts.template`。该模式只能证明 URL 可匹配，不能单独证明详情页签复用；固定 `key` 但不同记录 `path` 不同，在按 path 去重的平台仍可能多开。`hzero-openTab-reusable-fixed-path` 表示新建使用固定 `/create` 独立页签，view/edit 使用固定 `/detail` 复用页签，route 使用 `templates/submodule-router-open-tab-reusable-fixed-path.ts.template`，并按 `templates/open-tab-reusable-fixed-path-best-practice.md` 建立 tab context、标题和保存后跳转链路；记录 id 和 pageMode 不放进可复用详情 path，必须来自 confirmed tab context / navigation state / sessionStorage fallback 或项目等价 wrapper，并验证连续点击不同记录详情页签数量不增加。记录级或 pageMode 级独立页签才使用 `dynamic-tab`：route 必须配置 `mode: 'dynamic'`，`openTab.key` 与 `path` 使用可被 route config 真实匹配的具体路径；view/edit 的 `key/path` 应包含记录 id，例如 `/detail/view/{id}`，create 没有记录 id，`key/path` 只能使用具体 create path，例如 `/create`，不得追加假记录 id 或未注册后缀。有列表页且存在 create/view/edit 时优先套用 `templates/submodule-router-dynamic-tab-page-modes.ts.template`。path 已包含 pageMode 和 record id 时默认不需要 `dws`；create path 不因缺 record id 自动需要 `dws`；只有同 pathname 不同 search 也要独立，或项目明确要求 dynamic route 按 search 拆分时才配置 `dws: true`。`openTab` 复用父级 `key` 属于当前 Tab，不属于独立应用内 Tab。
- HZERO 系统页签标题必须区分 route 静态 `title` 和运行时 `openTab.title`：route `title` 使用稳定中文页面名，例如“采购申请详情”；点击详情、编辑、标记、审批等记录级入口时，若需要在页签上标识具体记录，`openTab.title` 应来自 Contract Check / Route Context 中确认的用户可读业务显示字段，例如 `requisitionNumber`、单据编号、名称或标题。`requisitionHeaderId`、`id`、`headerId`、加密 id、数据库主键或 route param 只能作为 key/path/query 的技术身份，不能默认作为用户可见 tab title；除非 FDS/用户/项目 confirmed baseline 明确要求显示该字段。只有列表 record、API 返回或详情回读合同能提供该 display field 时才写动态标题；缺字段时使用静态 route title 并记录 `tabTitleFallback` / production replacement，不得把技术 ID 当 fallback。
- dws 动态页签模板仅用于 FDS/TDS/用户明确要求同 pathname 不同 search/query 独立页签的场景，优先使用 `templates/submodule-router-dynamic-tab-dws.ts.template`。这里不重复示例代码；只保留审查点：`mode: 'dynamic'`、`dws: true`、`key === path` 且二者都包含用于区分页签的 search。仅有项目旧写法不能启用 dws；新生成详情页仍优先使用 `/detail/:id` path 参数。
- route 文件接入、平台菜单 path、菜单 code、按钮权限码必须分开记录。

## src/routes-config.tsx

`src/routes-config.tsx` 是可选项，不是每次新建子模块的必选项。只有满足以下任一条件时才生成：

- 目标项目相邻子模块已有同类 `routes-config.tsx` 模式。
- 页面需要子模块局部 Choerodon `ConfigProvider`、样式入口或局部包装。
- 用户通过 question 明确选择生成。

question：

```text
是否为新子模块生成 src/routes-config.tsx？
1. 不生成：保持最小骨架，后续确需局部包装再补。
2. 生成局部包装：加入 ConfigProvider 和 index.less 引入，仅作用于子模块。
```

若生成，范式：

```tsx
import React from 'react';
import { ConfigProvider } from 'choerodon-ui';
import './index.less';

export const PageWrapper = () => {
  const PageWrapperComponent = ({ children }: any) => {
    const options = {
      lovTableProps: {
        queryFieldsLimit: 3,
      },
    };
    return <ConfigProvider {...options}>{children}</ConfigProvider>;
  };
  return PageWrapperComponent;
};

export default {};
```

规则：

- 不做全局污染。
- 只放子模块局部配置。
- `index.less` 可在这里引入，保证子模块样式生效。

## Page Pattern

推荐页面目录按 DataSet 数量和共享范围收敛，不强制所有页面都创建 `stores/`。

有参考工程、参考子模块或相似页面时，DataSet 文件落点必须进入 `baselineComparison`，但本文 Page Pattern 仍是主线。若参考写法只是 `List/stores/queryDS.ts`、`Detail/stores/detailDS.ts`、feature 根 `stores/lineDS.ts` 这类目录归组差异，且没有共享运行时 `DataSet` 实例、没有把 mock runtime store 放入页面 `stores/`、没有削弱 transport/field/验证合同，默认按 `merge` 保留为项目目录兼容点；只有能证明该混合落点比本 Page Pattern 更清晰、更可维护或更符合目标工程装载/协作边界，并记录 `superiorityEvidence` 与 `aiDecisionAllowed=yes` 时，才允许该项 `follow-project`。同时记录 `standardBaselineApplied=true`、参考模块 `evidenceQuality`、`adoptedPatternItems[]=directory:dataset-stores-layout`、与本 Page Pattern 的差异、decision 和 reason。若缺参考模块质量评级、只凭搜索命中或无法判断该混合落点是否刻意设计，目录差异只能作为 `unknown-quality` candidate，不能覆盖本节规则。

单页面只有一个 DataSet 时，优先扁平放在页面目录同级，减少无意义目录层级：

```text
src/pages/<feature>/list/
├── index.tsx
├── listDS.ts
└── components/
    └── XxxTable.tsx
```

同一页面有两个及以上 DataSet、主从头行 DataSet，或 DataSet 配套 helper/adapter 较多时，再使用页面级 `stores/` 归组：

```text
src/pages/<feature>/detail/
├── index.tsx
├── stores/
│   ├── headerDS.ts
│   └── lineDS.ts
└── components/
    └── XxxSections.tsx
```

列表和详情共享同一业务资源时，service/baseUrl/action API 应位于 feature 根或 `services/`，而不是挂在某个页面子目录：

```text
src/pages/<feature>/
├── service.ts
├── list/
│   ├── index.tsx
│   └── listDS.ts
└── detail/
    ├── index.tsx
    └── stores/
        ├── headerDS.ts
        └── lineDS.ts
```

列表和详情确实复用 DataSet 字段、transport adapter 或工厂时，可使用 feature 根 `stores/`，但只共享配置/工厂，不共享运行时实例：

```text
src/pages/<feature>/
├── service.ts
├── stores/
│   ├── headerFields.ts
│   └── createHeaderDS.ts
├── list/
│   ├── index.tsx
│   └── listDS.ts
└── detail/
    ├── index.tsx
    └── stores/
        └── lineDS.ts
```

`stores/` 命名边界：

- 页面目录下的 `stores/` 默认只放 Choerodon DataSet 配置/工厂及其局部 adapter，不承载 mock runtime store、全局状态仓库或本地内存数据源。
- 单 DataSet 文件不得为了统一外观强制建 `stores/`；多个 DataSet 或明显扩展场景才建目录。
- Feature 级 `stores/` 只有在列表、详情、弹层或其它页面真实复用 DataSet 字段、transport adapter、工厂函数或字段 helper 时才创建；只是共用 service/baseUrl 不算共用 DataSet，不应因此提升到 feature 根 `stores/`。
- 共享 DataSet 时只能共享字段配置、工厂函数、transport builder、query/response adapter 等无运行时状态的配置；每个页面或组件实例必须调用工厂创建自己的 `DataSet` 实例。
- DataSet 文件应优先导出工厂函数，例如 `createListDS()`、`createHeaderDS()`，避免默认导出全局单例 `new DataSet(...)` 导致多 Tab、多实例、列表详情切换或详情切换记录时状态串扰。
- mock runtime store 应归属 devServer mock handler/plugin 或其同级 mock runtime 文件，并通过 HTTP mock API 被 DataSet/service 访问；不得放入页面 `stores/` 后由页面直接读写。

页面优先使用：

- HZERO `Header` / `Content`。
- `formatterCollections`。
- `PermissionButton`。
- Choerodon UI Pro `DataSet` / `Table`。
- Choerodon UI Pro `Modal.open`，按需求使用业务弹层；Drawer 使用 `Modal.open({ drawer: true, resizable: true, ... })`，普通 Modal 使用 `Modal.open({ ... })`；不要自绘弹层或 JSX Modal/Drawer 常驻渲染。
- Choerodon UI Pro `Form + Output`。

列表页默认：

- `Table + DataSet + filterBar`；`queryBar` 具体写法按 enumProvenance 使用 `TableQueryBarType.filterBar` 等 enum 形态。
- 有关键字/搜索框时开启 `fuzzyQuery`。
- 操作列必须最后一列，固定右侧按 enumProvenance 使用 `ColumnLock.right` 或项目 confirmed 等价 enum 导出。该固定列要求只针对行操作列；普通业务列只有设计或项目基线明确要求时才固定。
- 禁止优先手写查询 Form。

## Mock Request

无真实后端但需要可运行 mock 时：

```text
HZERO devServer middleware mock API
  -> DataSet transport.read / 非 DataSet service-action request 发起 HTTP 请求
  -> mock route 读取 dev-only runtime store
  -> raw response + dataKey/totalKey，或 transformResponse/adapter/helper 归一化
  -> 列表/详情/动作都从同一 runtime store 当前态生成
```

规则：

- mock seed 请求必须走当前前端服务 origin。
- 不走 `API_HOST`。
- mock/demo middleware mount 默认使用 `/_mock/<module>/v1/{organizationId}/...`，`organizationId` 来自运行时租户上下文；service/DataSet 实际请求必须命中当前前端服务 origin + `/_mock/<module>/v1/{organizationId}/...`，不得只把裸 `/_mock/<module>` 作为 service prefix 交给会拼 `API_HOST` 的 request helper；不得使用 `<unconfirmed-gateway-prefix>` 伪装 mock，不得使用 `/api/v1/demo-org` 或硬编码 `demo-org`。
- service/DataSet baseUrl 与 middleware 监听 path 必须同源同路径；一个写 `<unconfirmed-gateway-prefix>/<service>/v1/{organizationId}`、一个写裸 `/_mock` 被拼到远端 `API_HOST`、另一个监听 `/api/v1/demo-org` 时，mock-request 不成立。
- Target Placement 是父工程托管子模块时，mock handler/plugin 应归属 `packages/<module>/dev-mock/`；父工程 `config/config.ts` 顶层 `plugins` 必须显式注册该子模块 plugin，或注册父工程聚合 plugin 后引用子模块 handler/plugin，记录 `parentRootMockPluginRegistration`。子模块独立 `package-start` 默认适用，必须通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父工程同一 plugin，记录 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`；`config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得注册该 plugin。除非用户或目标工程文档明确禁止 package-start，否则不得写 `not-applicable`。子模块 package 配置单独注册、`packages-config.js` package 条目中的 `plugins` 字段都不能作为父工程 mock 生效证据。
- 子模块 mock 文件命名默认使用 `dev-mock/<module>-dev-mock-plugin.js` 和 `dev-mock/<module>-dev-mock.js`，模板分别为 `templates/submodule-dev-mock-plugin.js.template` 和 `templates/submodule-dev-mock.js.template`。生成前必须读取模板，落盘时只替换 `__MODULE_KEY__` 与 `__MODULE_CAMEL__`；`__MODULE_KEY__` 必须替换为真实 module key，`__MODULE_CAMEL__` 必须替换为合法 camelCase/pascalCase 标识片段。handler 文件必须直接 `module.exports = <module>DevMockMiddleware` 导出 middleware 函数，并暴露 `__mockMount = '/_mock/<module>/'`；handler 模板生成物必须保留 `parseMockRequestPath(pathname)`，业务 route 统一从 `organizationId/resourceSegments` 动态分发，不得在实现阶段手写固定租户路径；plugin 必须直接 `require('./<module>-dev-mock')`，并保留模板自检：导出类型校验、`__mockMount` 一致性校验、重复注册跳过/告警、注册日志和缺失 Umi 扩展点时明确报错。不得解构不存在的命名导出，不得调用 `require('./<module>-dev-mock')(api.app)` 或依赖 `api.app`/Express app 实例直接挂载。监听路径必须以 `/_mock/<module>/` 开头。
- 子模块 dev-mock 目录与 `config` 目录平级，不存在时直接新建；旧 `config/<module>-dev-mock*.js` 位置无效，必须迁入 `dev-mock/`。mock 数据量较多、包含多接口 seed、状态流转或头行明细 store 时拆为 `dev-mock/<module>-dev-mock-data.js`、`dev-mock/<module>-dev-mock-store.js` 或等价小模块；只有 1-2 条简单 seed 时允许内联在 handler 中。拆分后 handler 必须显式 require/import data/store，并让列表、详情、保存、状态动作和刷新接口从同一 data/store 读取或写回。列表分页固定按 0-based `page/size` 处理，`page=0` 是第一页，缺省 page=0，禁止 `(page - 1) * size`、`Number(query.page || 1)`、`Number(query.page ?? 1)` 或 fallback 1 造成 `totalElements > 0` 但 `content=[]`；`currentPage/pageSize` 属于无效旧协议，命中时必须迁移，不得建立双协议或归一化分支。
- 子模块 plugin 固定使用 `api.addBeforeMiddlewares(() => [<module>DevMockMiddleware])`；不得生成旧 `api.addBeforeMiddleware` fallback、`api.addBeforeMiddlewares(registerMock)`、`api.addBeforeMiddlewares(<middleware>)`、`api.addBeforeMiddlewares(() => { require(...)(api.app); })` 或只判断属性存在而不判断 `typeof api.addBeforeMiddlewares === 'function'` 的写法。
- 父工程聚合 plugin 可以集中在 `config/dev-mock-plugin.js`，但它只做集成转发，应引用各子模块 mock handler/runtime store；子模块 plugin 仍是推荐归属。
- 不用纯内存 `mock.ts` 冒充 `mock-request`。
- DataSet 列表查询必须有可见 Network 请求。
- 详情若要求 mock request，点击查看也应触发可见 mock request，或明确只消费同源 runtime store。

## Verification

新子模块生成后至少发现并建议以下验证，运行与否按项目证据和用户授权：

```bash
./node_modules/.bin/tsc -p packages/<module-name>/tsconfig.typecheck.json
./node_modules/.bin/cross-env UMI_ENV=prod NODE_OPTIONS="--max_old_space_size=10240" node ./node_modules/umi/bin/umi.js hzero-build --only-build-micro <module-name>
```

Typecheck 只能使用目标包已有且明确 `--noEmit` 的 script，或独立 `tsconfig.typecheck.json` 明确 `noEmit=true`、`emitDeclarationOnly=false`。上文发布 `tsconfig.json` 只用于 build/package，不得通过 CLI 覆盖后用于 typecheck。执行前后必须调用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_typecheck_no_emit.py` 完成配置预检与 `lib/*.d.ts` 快照对比；缺安全 typecheck 入口时记录 `not-run + reason=missing-no-emit-typecheck-entry`，不得自动清理已有发布产物。

子模块路由或微前端元数据变更后的固定验证链路为：

```bash
npm run build:ms -- <module-name>
node scripts/refreshMicroConfig.js
```

其中最终编译命令只能为 `npm run build:ms -- <module-name>`；根工程缺少 `build:ms` script 时记录 `missing-required-build-ms-script` 并回工程接线补齐，不得改用 yarn、pnpm 或其它 build 命令。`refreshMicroConfig.js` 仍以脚本存在或项目文档确认为执行前提。

依赖就绪、build/refresh 已实际运行后，Verification 仍不得重启 dev server、打开浏览器或执行 hard reload；页面运行态闭合只能作为独立 runtime acceptance 或用户手工证据记录。默认 mock demo、目标工程依赖未安装或缺外部运行态证据时，只记录为后续补跑链路，不作为当前强制验证要求，也不得因此调用 Browser Verification question。`node scripts/refreshMicroConfig.js` 只有在脚本存在或项目文档确认时作为已确认命令；未确认时写为候选检查项，不得编造成已执行。实际运行 `npm run build:ms -- <module-name>` 后，验证报告必须检查 `packages/<module>/lib`、`dist`、`.umi`、`.umi-production` 等生成产物是否残留在业务子模块工作区；若出现 `lib/`，只能判定为构建/转译副产物并删除或要求回 Implementation 清理，不得纳入源码提交、Handoff 资产或“页面实现文件”证据。

人工检查：

- `config/packages-config.js` 已注册。
- `config/packages-config.js` / `packages-config.ts` 新增子模块时默认只添加 `{ name: '<module>' }`。不得无来源追加 `initLoad: false`、`registerRegex`、`plugins`、`priority`、`routes` 或其它字段；若 active registry 中同类模块都要求额外字段，必须记录 schema/baseline 证据和字段来源。`registerRegex` 默认属于子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`，不是 packages-config 条目的兜底字段。
- `config/config.ts` 中 `extendParentConfig` 只从 `@hzerojs/plugin-micro` 导入，且在目标前端父工程根目录执行 `node -e "require.resolve('@hzerojs/plugin-micro')"` 成功。
- 新建或接入的包名应按 Node 包名解析：在目标前端父工程根目录执行 `node -e "require.resolve('<module>/package.json')"`；`<module>` 是 `packages/<module>/package.json` 的 `name`，不是目录路径。结果必须分类记录为 `workspaceResolverStatus=passed / failed-missing-dependencies / failed-link-missing / failed-name-mismatch / failed-but-build-passed / not-run`。失败时先检查 workspace/link、根 `package.json` 的 `workspace:*` 依赖、`node_modules/<module>` 和包管理器状态；若缺依赖或 link 未安装，属于环境前置或集成风险，不得先归因为业务页面代码；若 `build:ms -- <module>` 已通过但 resolver 失败，保留 build 通过事实，只把 resolver 写为风险并核对执行目录、package name 和 root dependency；只有 package name、root dependency、workspace 配置或父工程 registry 确实缺失/冲突，才回 scaffold/integration 修复。
- 如可访问插件安装目录，新增或改造子模块后运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_hzerojs_submodule_config.py --root <frontend-root> --module <module>`；该脚本用于机械拦截根应用配置形态、顶层 `plugins`、顶层 `registerRegex`、`packages-config` 条目非法字段和 `config.dev.ts` 错误继承。无法定位插件目录时，不得跳过规则本身，必须记录 `submoduleConfigValidator=not-run + reason` 并按本节人工静态检查。
- `config/config.ts` 的 `registerRegex` 不使用 catch-all。
- `config/config.dev.ts` 存在，或有明确 `not-applicable + reason` 证明该子模块不支持独立 `package-start`。
- `submoduleRouteEntryMode` 已记录。`single-router-ts` 模式检查 `config/router.ts` 存在且 `config/config.ts` 引用 `./router`；`split-routes-dir` 模式检查 `config/routes/index.js` 正常聚合 FeatureRoute 且 `config/config.ts` 引用 `./routes`。
- `config/config.ts` 未内联完整 route array；除 `routes: route` 或 `routes: [...routes]` 接线外，不应出现业务 route 对象、页面 `component`、`mode: 'dynamic'`、`dws` 或 list/detail 子路由结构。
- 路由配置字段使用直接字面量；无额外路径片段/标题/component 变量拼接，无模板占位符残留。
- Umi route 使用标准 `routes` 结构；未为排查问题改成 hzero-cli `components`、自定义 router 或单页面 query switch。
- 一级页面直接配置 `component`；父级分组 route 不配置 `component`；新生成 route config 不配置 `redirect`。`split-routes-dir` 模式嵌套路由子 path 均为完整绝对路径，component 使用 `@/pages/...`；`single-router-ts` 模式按项目证据使用父级绝对 path、子级相对 path 和包内页面相对 component。
- route path 与 `registerRegex` 前缀一致。
- 页面能通过路由访问。
- mock 请求命中前端服务 origin，path 匹配 `/_mock/<module>/v1/{organizationId}/...`。
- 父工程托管子模块下，子模块 mock plugin 已被父工程 `config/config.ts` 顶层 `plugins` 显式注册或被该数组注册的父工程聚合 plugin 引用；默认同时静态核对 `package-start` 插件来源，确认其通过 `extendParentConfig` 继承父 plugin，且子模块 `config/config.ts` / `config/config.dev.ts` 均未重复注册该 plugin；除非用户或目标工程文档明确禁止 package-start，否则不得写 `not-applicable`。middleware 变更后的实际重启服务证据只能来自独立 runtime acceptance 或用户手工证据，Verification 不启动服务，不能只依赖热更新声明运行态闭合。
- package 发布清单可以保留模板默认的 `lib` 和 `config/config.ts`，但必须按模板排除 `.umi`、`.umi-production`、`lib/config/*` 等非业务发布项；实际生成出的 `packages/<module>/lib/`、`dist`、`node_modules`、`.umi`、`.umi-production` 等目录不得被当作页面、DataSet、service、路由证据或 Handoff 资产。若 `build:ms` 后生成 `packages/<module>/lib/`，必须记录为验证副产物并清理或标记未提交，不得写入业务交付源码。
- UI 实现没有超出 FDS/TDS/FBS/Figam/PageSchema 设计依据。

## Rejection Conditions

新建或审查子模块时，以下情况必须阻塞或回退：

- 缺 `package.json`。
- 缺 `tsconfig.json`。
- 缺 `config/config.ts`。
- 缺 `config/config.dev.ts`，且没有明确证据证明该子模块不支持独立 `start/package-start`。
- `package.json` 残留模板占位符、缺 `scripts`、缺必需 HZEROJS 业务子模块 scripts、遗漏 `files` 发布边界、`files` 重复，或把实际生成出的 `.umi/.umi-production/lib/dist/node_modules` 目录作为业务资产提交、页面证据或 Handoff 资产。
- 缺 Umi 路由入口：`single-router-ts` 模式缺 `config/router.ts`，或 `split-routes-dir` 模式缺 `config/routes/index.js` / `config/routes/<FeatureRoute>.js`。
- `config/config.ts` 内联完整业务 route array，或把应属于 `config/router.ts` / `config/routes/**` 的 list/detail/current-tab/dynamic-tab 路由对象直接写入主配置。
- `config/config.ts` 从 `@hzerojs/preset-hzero/lib/util`、`@hzerojs/preset-hzero/lib/*` 或其它深路径导入 `extendParentConfig`，或 `@hzerojs/plugin-micro` 在目标工程不可解析。
- `config/config.ts` 使用根应用配置形态：`import { IConfig } from 'umi'`、`export default { ... } as IConfig`、顶层 `plugins/presets` 注册 `hzero-front` / `@hzerojs/preset-hzero`，或顶层 `registerRegex`。
- 父工程托管场景下，子模块 `config/config.ts` 顶层 `plugins` 注册 dev mock plugin 或其它 Umi plugin；mock plugin 必须由父工程根配置注册，子模块只通过 `extendParentConfig` 继承。
- 实际路由配置中残留模板占位符，或把已确认 path/title/component/registerRegex 抽成变量后再拼接，导致生成结构偏离模板或审查难以确认真实 route。
- 未注册 `config/packages-config.js`，且无明确 not-applicable reason。
- 新增 package registry 条目无来源包含 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段，而不是最小 `{ name: '<module>' }`；或用 packages-config 条目的 `registerRegex` 替代子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`。
- 新子模块默认使用 `registerRegex: '\\/.*'`。
- route prefix 未确认却写成 confirmed route。
- 子模块路由为了排查 404、Tab 或加载问题改成非标准 Umi routes 结构、添加 route `redirect`，或混用 hzero-cli `components`。
- 父级仅作为分组 / 稳定 Tab 边界却配置 `component`，导致父子 route 行为不清。
- `split-routes-dir` 模式嵌套路由子 path 使用相对路径，或子模块页面 component 未使用 `@/pages/...`；`single-router-ts` 模式未按项目证据同步 `config.ts` 的 `./router` 引用、pages-root component 风格和子路由 path 风格；任何模式使用 `../src/pages/...` 或 `./routes/...` 作为 route component。
- 修改子模块路由后未重建目标子模块、未刷新 microConfig、缺外部 dev server restart / hard reload 证据，却声明路由可达。
- mock 数据只走本地函数，不走 requestable mock。
- mock-request 只生成 `dev-mock/<module>-dev-mock*.js` 但未被父工程注册，或 plugin require 的 middleware 导出形态与 handler 文件不一致。
- plugin 直接把 middleware 函数传给 `api.addBeforeMiddlewares`，没有使用 `() => [middleware]` 回调数组形态；或使用 `require('./<module>-dev-mock')(api.app)` / `api.addBeforeMiddlewares(() => { require(...)(api.app); })` 这类 Express app 直接挂载；或缺少 `api.addBeforeMiddleware` 兼容兜底且项目只暴露老接口。
- mock plugin/handler 缺少模板自检机制，不能证明 middleware 导出函数、`__mockMount` 匹配、重复注册保护和 Umi 扩展点可用性。
- mock 模板残留 `__MODULE_KEY__`、`__MODULE_CAMEL__` 或 `__MOCK_MIDDLEWARE_EXPORT__` 占位符；进入 runnable/usable=true 时必须阻塞。
- 页面查询区手写 Form 替代 `Table filterBar`。
- 详情只读字段不用 `Form + Output`。
- 弹层类交互未按需求使用工程标准 Choerodon/HZERO Modal/Drawer/Overlay 组件，而是自绘弹层。

## Minimum Skeleton Without Project Reference

跨项目没有现成子模块时，可按以下最小骨架落地：

```text
packages/<module-name>/
├── package.json
├── tsconfig.json
├── config/config.ts
├── config/config.dev.ts
├── config/router.ts                    # single-router-ts, one route file
# or
├── config/routes/index.js              # split-routes-dir
├── config/routes/<FeatureRoute>.js     # split-routes-dir
├── src/index.less
└── src/pages/<PageName>/index.tsx
```

无项目参考、无可采纳相邻子模块或参考资产不可读时，必须启用 `assetBaselineSource=hzerojs-asset-baseline`，并严格使用内置模板生成子模块骨架，不得自由裁剪结构或只生成 package/config/page 三件套。`package.json` 必须来自 `templates/submodule-package.json.template`；`tsconfig.json` 必须直接复制 `templates/submodule-tsconfig.json.template` 且保持 JSON 等价，`config/config.dev.ts` 必须来自 `templates/submodule-config.dev.ts.template`，`config/config.ts` 必须按 `submoduleRouteEntryMode` 使用 `templates/submodule-config-single-router.ts.template` 或 `templates/submodule-config.ts.template`，路由入口必须使用对应模板/标准结构。最小文件树必须包含 `package.json`、`tsconfig.json`、`config/config.ts`、`config/config.dev.ts`、合法 Umi route entry、子模块基础样式入口 `src/index.less`、`pageRoot=src/pages` / `pageRootSource=asset-baseline` 和默认 `src/pages/<PageName>/index.tsx` 页面根；父工程 active registry 集成和收敛的 `registerRegex` 必须规划或标记 blocked。`src/index.less` 只表示子模块入口基线，不授权业务页面新增局部样式；业务页面样式仍由 Style Necessity Contract 控制。mock-request 命中时必须补 `dev-mock/<module>-dev-mock-plugin.js` 和 `dev-mock/<module>-dev-mock.js`，并规划父工程 `config/config.ts` 顶层 `plugins` 注册或父工程聚合注册；同时记录 `parentMockPluginRegistrationEvidence`、`mockPluginTemplateCompliance`、`mockPluginSelfCheck` 和 `mockPrefixOriginPolicy`。缺父工程注册、插件非模板形态、缺模板自检或 mock prefix 未拼当前 dev server origin 时，无参考模块不得进入 `mock-completed`、`usable=true` 或 runnable handoff。

`src/routes-config.tsx` 仍按可选规则处理，不作为无参考项目的默认必选项。

核心原则：

```text
extendParentConfig
+ routes 聚合
+ hzeroMicro.microConfig.registerRegex 收敛
+ packages-config 注册
+ tsconfig 继承父工程
+ 页面使用 HZERO/Choerodon 标准组件
```

# 工程结构与编码规则前置

## 设计文档必须传递的元数据
- `featureName`、`featureSlug`、`featureRoot`
- `targetProject`、`targetModule`、`pageType`
- `routePath`、`menuPath`、`permissionCodes`
- `fieldMappingStatus`、`apiList`、`backendDependencyMap`
- `directoryPlan`、`codingRules`
- `validationCommands`、`finalCompileCommand`、`unitTestPolicy`

## HZERO/UMI 目录基线
- 父应用页面通常位于 `src/pages/<page-kebab>/`，父应用路由入口是根 `config/config.ts`。
- 微前端子模块页面通常位于 `packages/<module>/src/pages/<page-kebab>/`，子模块路由事实源是 `packages/<module>/config/config.ts`，开发态独立启动配置文件是 `packages/<module>/config/config.dev.ts`。
- 微包声明入口是根 `config/packages-config.js`。
- 新建 `packages/<module>` 子模块时，目录基线必须包含 `package.json`、`tsconfig.json`、`config/config.ts`、`config/config.dev.ts` 和 `src/`。`package.json` 默认使用 `front-hzero-enterprise-process-control` 的 submodule package 模板，必须包含 HZEROJS 业务子模块 scripts；`transpile` 和 `files: lib` 保持发布/转译模板口径，但 Verification 阶段不得直接执行包内 `transpile`，实际生成出的 `lib/` 也不得作为交付源码。`files`、`dependencies`、`peerDependencies`、`volta`、`private`、`main` 等字段按相邻子模块/父工程模板/用户模板证据裁剪补充，无证据时不默认生成依赖相关字段。`files` 不得重复。`config/config.dev.ts` 用于子包独立 `start/package-start`，优先参考相邻子模块或父工程约定；无模板时使用 `front-hzero-enterprise-process-control` 的 submodule config.dev 模板 的空对象导出，不得使用 `extendParentConfig` 或默认展开 `./config`。`tsconfig.json` 应优先参考相邻子模块或父工程约定；无项目模板或用户模板时，直接复制 `front-hzero-enterprise-process-control` 的 `submodule-tsconfig.json.template`，保持 JSON 等价，不自行增删字段，不写 `compilerOptions.paths`，paths alias 继承父工程。不得只创建 package/page/config 而漏掉类型配置或开发态配置。

```jsonc
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "emitDeclarationOnly": true,
    "outDir": "./lib",
    "rootDir": "./src",
    "baseUrl": "./"
  },
  "include": [
    "src"
  ],
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
- 页面目录常见职责是 `index.tsx` 承载页面壳和交互，`<name>DS.ts` / `dataset.ts` 承载 Choerodon DataSet，`service.ts` 承载已确认接口调用；页面局部 `style.less/index.less` 只有在 Style Necessity Contract 确认组件 props 或项目已有 class 不足时才创建或修改。单页面只有一个 DataSet 时优先与 `index.tsx` 同级放置；同一页面有两个及以上 DataSet、头行/主从 DataSet 或配套 adapter/helper 较多时，再使用页面级 `stores/` 目录。列表/详情等多个页面真实复用 DataSet 字段、adapter 或工厂时，可使用 feature 根 `stores/`；但共享的是配置和工厂，不得共享运行时 `DataSet` 实例。`stores/` 只表示 DataSet 配置/工厂归组，不承载 mock runtime store 或全局状态仓库。

## 探索边界
- 目标工程结构应来自用户输入、后端 handoff metadata、目标项目证据、`sdd-workspace/changes/{change-id}/frontend/design/` 中的设计契约，或 `sdd-workspace/changes/{change-id}/frontend/` 中已有前端执行资料。
- 设计阶段不得为了猜测路径重复全仓搜索配置目录。
- `src/.umi/`、`src/.umi-production/`、`packages/<module>/src/.umi/`、`packages/<module>/src/.umi-production/`、`dist/`、`node_modules/`、`lib/` 默认不作为业务目录探索来源，也不得作为新子模块生成、提交或发布清单中的业务资产来源。

## 编码规则前置
- 设计文档只描述编码规则和目录计划，不直接编码。
- API list、config TS、路由配置、权限清单或平台协议位置应明确来源；缺少时列为待确认。
- 最终编译命令找不到时必须写候选命令或待确认，不得伪造。

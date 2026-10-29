# HZEROJS Submodule Design Contract

本文只描述 Frontend Design 阶段的新建/接入 `packages/<module>` 子模块落位合同。子模块骨架生成、父工程写入、Review/Verification 拒收项和构建命令门禁在 `front-hzero-enterprise-process-control` 的 HZEROJS 子模块运行期门禁。

## Applicability
- 用户提到“子模块”“独立子模块”“微前端子包”“packages 模块”。
- 新增或改造 HZEROJS `packages/<module>` 页面。
- 父工程 `src/pages/<module>` 与 `packages/<module>` 落点可能混淆。
- 需要新增父工程注册、微前端 route prefix 或 `registerRegex`。

## Target Placement Contract

Frontend Design 必须输出 `Target Placement Contract`：

| 字段 | 状态 | 说明 |
| --- | --- | --- |
| placementType | new-package / existing-package / parent-src-page / integration-only / unknown | 用户说“子模块/packages/微前端”且未否定时，默认候选为 new-package/existing-package |
| placementIntentSource | user-explicit / user-implicit / FDS / TDS / evidence / generatedCandidate | 判断是否需要 question |
| targetProject | confirmed / missing / conflict | 目标前端父工程 |
| packageName | confirmed / generatedCandidate / missing | `packages/<module>` 包名 |
| packageDir | confirmed / generatedCandidate / missing / not-applicable | 子模块业务代码根 |
| businessDomain | confirmed / generatedCandidate / missing / conflict / needs-confirmation | package 内业务域或功能分区；确认 packageDir 不等于确认 businessDomain |
| pageRoot | src/pages / existing-src-routes / custom / missing / conflict / needs-confirmation | package 内页面根目录；新生成页面固定 `src/pages` |
| pageRootSource | asset-baseline / project-evidence / adjacent-module / existing-file / generatedCandidate / missing | `pageRoot` 来源；`src/routes` 只允许用于改造已存在页面 |
| pageGroup | confirmed / generatedCandidate / missing / conflict / needs-confirmation | package 内页面目录分组，例如 `src/pages/<domain>/<Feature>` |
| pageDir | confirmed / generatedCandidate / missing | 页面/组件/DataSet/service/style 根，例如 `src/pages/<Feature>` |
| routePrefix | confirmed / generatedCandidate / missing / conflict / needs-confirmation | 当前功能主路由前缀，必须与 pageGroup 和菜单分组一致 |
| menuGroup | confirmed / generatedCandidate / missing / not-applicable | 平台菜单归属或业务菜单分组 |
| packageInternalAmbiguity | none / multiple-business-domains / multiple-route-prefixes / multiple-candidates / missing-evidence | package 内部落点是否仍有歧义 |
| submoduleRouteEntryMode | single-router-ts / split-routes-dir / not-applicable / missing | 仅一个路由文件时使用 `config/router.ts`；多路由文件或项目拆分模式使用 `config/routes/index.js` + FeatureRoute |
| routeConfigPath | confirmed / generatedCandidate / missing | 子模块或父工程路由配置 |
| parentRegistrationPath | confirmed / generatedCandidate / missing / not-applicable | 例如 `config/packages-config.js` |
| parentRegistrationEntryPolicy | minimal-name-only / schema-confirmed-extra-fields / missing / conflict / not-applicable | 父工程 package registry 条目默认 `{ name: '<module>' }`；额外字段必须有 active schema / 项目基线 / 用户确认来源 |
| parentRegistrationExtraFieldSource | active-schema / project-baseline / platform-required / user-confirmed / none / not-applicable | `initLoad/registerRegex/plugins/priority/routes` 等额外字段来源；无来源时不得生成 |
| parentRegistrationCandidates | confirmed / generatedCandidate / missing / not-applicable | 所有候选父工程注册入口，例如 `config/packages-config.*`、`.hzerorc.*`、workspace 或 CI/script registry |
| activeRegistryEvidence | confirmed / partial / missing / conflict / not-applicable | 哪些注册入口实际被根配置、脚本或构建读取 |
| registerRegex | confirmed / generatedCandidate / missing / conflict | 必须收敛到已确认 route prefix |
| configDevPath | confirmed / generatedCandidate / not-applicable / missing | 新建 Umi 子模块默认需要 `packages/<module>/config/config.dev.ts` 支持子包独立 `start/package-start`；只有工程证据证明不支持独立启动时才可 not-applicable |
| packageTemplate | project-template / baseline-template / user-template / missing | 新建子模块必须记录 `package.json` 来源；默认基线为 `front-hzero-enterprise-process-control` 的 submodule package 模板 |
| packageRequiredScripts | present / missing / not-applicable | 新建 Umi 业务子模块必须包含 `start`、`build`、`build:ms`、`transpile`、`build:app`；Verification 不直接执行包内 `transpile` |
| packageFilesPolicy | project-trimmed / baseline-trimmed / missing / invalid | `files` 发布边界必须按证据裁剪，排除 `.umi/.umi-production` 等生成产物且不得重复 |
| packageDependencyFieldsSource | adjacent-package / parent-template / workspace-evidence / user-template / none | `dependencies`、`peerDependencies`、`devDependencies`、`resolutions`、`volta`、`private`、`main` 等字段来源；无证据不生成 |
| tsconfigTemplate | project-template / baseline-template / user-template / missing | 新建子模块必须记录 `tsconfig.json` 来源；默认基线为 `front-hzero-enterprise-process-control` 的 submodule tsconfig 模板，生成时直接复制模板 JSON，不自行增删字段，不在子模块内写 `compilerOptions.paths` |
| mockPluginPath | confirmed / generatedCandidate / not-applicable / missing | `queryMode=mock-request` 时默认 `packages/<module>/dev-mock/<module>-dev-mock-plugin.js`，并要求父工程注册或聚合注册 |
| parentRootMockPluginRegistration | parent config/config.ts plugins -> submodule plugin / parent config/config.ts plugins -> aggregator / missing / not-applicable | HZEROJS Umi 父工程托管子模块的父工程启动接线；父工程根 `config/config.ts` 顶层 `plugins` 直接注册子模块 plugin，或注册父工程聚合 plugin |
| packageStartMockPluginSource | parent-config-inherited-by-extendParentConfig / standalone-project-equivalent-root-config / missing / not-applicable | HZEROJS Umi 子模块默认支持 `package-start` / 子包独立启动；`queryMode=mock-request` 时必须通过 `config/config.ts` 的 `extendParentConfig` 继承父工程同一 mock plugin；子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得重复注册同一 mock plugin，只有工程证据证明不支持独立启动时才可 not-applicable |
| parentSrcWritePolicy | registration-only / forbidden / allowed-with-reason / not-applicable | 父工程 `src/**` 写入边界 |
| forbiddenBusinessPaths | confirmed / generatedCandidate / not-applicable | 例如 `src/pages/**` |

## Design Rules
- 用户使用“子模块”“独立子模块”“微前端子包”“packages 模块”且未明确否定时，默认解释为 `packages/<module>` 独立包，不得解释为父工程 `src/pages/<module>` 业务目录。
- `packageDir` 只能确认包级写入边界，不能单独确认功能级落点。目标 package 下存在多个业务目录、多个 route prefix、多个菜单分组或多个相似页面候选时，必须确认 `businessDomain`、`pageRoot`、`pageRootSource`、`pageGroup`、`pageDir`、`routePrefix` 和 `menuGroup`；未确认时 `packageInternalAmbiguity` 不能为 `none`。
- 新生成 Umi 子模块页面根固定是 `src/pages`。`src/routes` 只允许用于改造已存在于 `src/routes/**` 的存量页面，并且必须写 `pageRoot=existing-src-routes`、`pageRootSource=existing-file/project-evidence` 和证据摘要。无参考基线、`pageRootSource=asset-baseline`、缺来源或仅用户偏好时生成 `src/routes/**` 是设计偏差，不得进入 runnable Implementation。
- 只有在用户输入、FDS/TDS、平台菜单、routeConfig 或高置信工程证据能唯一定位业务域时，才允许把包内落点写为 `confirmed`；similarPage、命名相似、最近改动和生成规则只能写 `generatedCandidate / needs-confirmation`。
- 包内落点未确认时必须触发 `Target Placement Confirm` 或输出 `blocked-by-missing-target-placement`；不得因为已确认 `packages/<module>` 就把页面直接落到 package 根或最高置信候选目录。
- `placementType=new-package/existing-package` 时，页面、组件、DataSet、service、style、mock、i18n 等业务文件必须落在 `packageDir` 或其设计确认的子目录；父工程默认只允许 registration/config 集成写入。
- `parentSrcWritePolicy=registration-only/forbidden` 时，父工程 `src/pages/**` 是业务代码禁写路径；只有 `allowed-with-reason` 且设计写明原因、范围和验证方式时才可写入。
- 父工程注册必须先识别 active registry。Design 不能只写一个猜测的 `parentRegistrationPath`；如果根配置、`.hzerorc`、workspace 或构建脚本存在多个候选入口，必须记录每个入口的证据和状态。无法判断哪个入口生效时，`activeRegistryEvidence=partial/missing`，不得声明子模块生产可达。
- 父工程 package registry 条目默认只生成 `{ name: '<module>' }`。`initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段必须有 active schema、项目 confirmed baseline、平台强制要求或用户确认来源，并记录 `parentRegistrationExtraFieldSource`；无来源时不得生成。`registerRegex` 默认记录在子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`，不得用 packages-config 条目字段代替。
- `registerRegex` 必须收敛到已确认 route prefix；不得用 `\\/.*` 作为新子模块默认候选。
- 新建 Umi `packages/<module>` 子模块必须在 Design 中把这些事实决定清楚：`submoduleRouteEntryMode`、实际 route entry、`configDevPath` 是否必需、`packageTemplate`、`packageRequiredScripts`、`packageFilesPolicy`、`packageBuildArtifactPolicy`、`packageDependencyFieldsSource`、`tsconfigTemplate`、`mockPluginPath`。这些字段的具体模板内容、生成细则和运行时拒收项统一以 `front-hzero-enterprise-process-control` 的 HZEROJS 子模块运行期门禁 为准；Design 在这里不重复 runtime 细则，只负责做出可交付的选择并写明来源。
- `queryMode=mock-request` 时，Design 必须规划 mock plugin/handler 的子模块归属：默认 `dev-mock/<module>-dev-mock-plugin.js` + `dev-mock/<module>-dev-mock.js`，记录 `__MODULE_KEY__`、`__MODULE_CAMEL__` 的替换规则、handler 直接导出 middleware 函数、`__mockMount`、plugin 使用 `api.addBeforeMiddlewares(() => [middleware])` 的注册形态，以及 `mockPluginSelfCheck=planned`；并记录 `parentRootMockPluginRegistration` 对应的父工程 `config/config.ts` 显式注册或父工程聚合 plugin 引用方案。`package-start` / 子包独立启动默认适用，必须同步规划 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`，即子模块 `config/config.ts` 通过 `extendParentConfig` 继承父工程同一 plugin；子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得注册同一 plugin。只有工程证据证明不支持独立启动时，才可写 `packageStartMockPluginSource=not-applicable + reason`。没有 mock 需求时写 `mockPluginPath=not-applicable + reason`，不得把 mock 文件列为最小骨架必选项。
- `src/routes-config.tsx` 是可选项。只有相邻模块证据、局部 `ConfigProvider`/样式包装需求或用户确认时才进入目录计划；未确认时写 `not-generated + reason`。
- 后端 TDS、已有父工程路由示例或“最短可运行路径”不能单独把子模块落点降级为父工程 `src/pages`。

## Empty / Missing Reference Mode

目标是 HZEROJS 父工程或 `packages/<module>`，但工程为空、参考资产缺失/不可读，或工程内缺少相邻子模块、同类页面、可采纳 wrapper 时，Frontend Design 必须启用 `hzerojs-asset-baseline.md`，记录 `assetBaselineStatus=active`、`assetBaselineSource=hzerojs-asset-baseline`、`baselineComparison.evidenceQuality=asset-baseline`、`baselineComparison.decision=follow-asset-baseline`。

空项目或缺失参考模块不允许降级为自由实现。Design 必须把 `Submodule Baseline Contract` 标记为 asset baseline，并明确哪些结构来自内置模板、哪些来自项目证据、哪些仍待确认；固定 `pageRoot=src/pages`、`pageRootSource=asset-baseline`，不得把新生成页面根改成 `src/routes`。模板清单、最小骨架和运行时拒收项统一以 `hzerojs-asset-baseline.md` 和 `hzerojs-submodule-runtime-gate.md` 为准。

资产基线不能回答业务和平台问题。Target Placement、Missing Contract、Open Interaction、Import/Export Component Mode、LOV/lookup、附件 bucket/storageCode、导入导出 templateCode、tenantContext、servicePrefix、backend readiness 或 Production Replacement 仍应在同一轮 Contract Check 中分类处理。默认 Mock demo 下，LOV/lookup code、附件 bucket/storage/template、导入导出 templateCode/endpoint、权限码和 locale key 能形成候选时，不作为独立 question 或 runnable demo 阻塞；必须改为 `mockOnly/generatedCandidate/placeholderParameter + Production Replacement`。只有字段/value/bind/endpoint 结构无法形成当前 Mock 候选时，未 resolved 才不得进入 runnable Implementation；production-ready、真实 API/文件/导入导出联调或拒绝默认 Mock 的诉求只进入独立集成与稳定化 advisory，后续生产结论仍要求真实契约 confirmed。

## Baseline Comparison
目标工程证据用于识别项目现状，不等于生成准则。新建或改造 HZEROJS 子模块时，必须记录 `baselineComparison`：

| 场景 | 决策 |
| --- | --- |
| 工程写法更完整、更安全 | follow-project |
| 工程写法只是命名、目录或封装差异，不降低完整性/安全性 | follow-project + difference |
| 工程历史模块缺文件、漏父工程注册、缺路由聚合、`registerRegex` 过宽或构建链路不可验证 | legacy-risk；不得作为新代码默认范式 |
| 工程约定与 baseline 冲突且无法判断是否为刻意设计 | block / needs-confirmation |
| 空 HZEROJS 项目、参考资产缺失或无可采纳参考模块 | follow-asset-baseline，并保留所有未解决 questionGate |

## Output Requirements
- Design 文档必须记录 targetPlacement、directoryPlan、route/menu candidate、parent registration candidates、activeRegistryEvidence、forbidden business paths 和验证候选命令。
- 缺 packageName、businessDomain、pageRoot、pageRootSource、pageGroup、pageDir、routePrefix、targetProject、parentRegistrationPath、parentRegistrationEntryPolicy、registerRegex、Umi 子模块 `submoduleRouteEntryMode`、`configDevPath`、`packageTemplate`、`packageRequiredScripts`、`packageFilesPolicy`、`packageBuildArtifactPolicy`、`packageDependencyFieldsSource` 或 `tsconfigTemplate` 时，不得声明可进入 runnable Implementation；不适用项必须写 `not-applicable + reason`。`queryMode=mock-request` 且缺 `mockPluginPath` 或父工程注册方案时，也不得声明 `usable=true`。
- 后续 Task/Implementation/Review/Verification 必须继承 `front-hzero-enterprise-process-control` 的 HZEROJS 子模块运行期门禁。

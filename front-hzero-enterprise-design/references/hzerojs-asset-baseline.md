# HZEROJS Asset Baseline

用于目标是 HZEROJS 父工程或 `packages/<module>` 子模块，但工程内为空、参考资产缺失、无法读取参考资产，或缺少可采纳相似页面、相邻子模块、项目 wrapper 证据时，给 Frontend Design、Task Breakdown、Implementation 和 Review 提供最低企业前端资产基线。本文只补“形态和边界”，不补业务事实。

统一使用 `assetBaseline*` 合同，覆盖 **空项目** 和 **缺失参考资产 / 无可采纳参考模块** 两类场景；不读取或转换旧字段名。

页面域分层、constants/service/stores/components/Table 的示例写法见 `hzerojs-enterprise-page-composition-example.md`。命中 Empty / Missing Reference Mode 时，Design 和 Task 应把该示例作为 asset-baseline 结构参考；若偏离，必须记录项目证据、相邻模块证据或用户确认。

## 阅读路由
- 判断是否进入无参考 / 缺失参考资产基线时读 `Applicability` 和 `Baseline Decision`。
- 设计和任务拆分页面、子模块、数据链路形态时读 `Required Shape`、`Mock Request Closure` 和 `Question Gate Preservation`。
- 实现、审查或验收无参考模块时读 `No UI Downgrade` 和 `Output Requirements`。

## Applicability

命中以下条件时进入 Empty / Missing Reference Mode：

- 目标工程是 HZEROJS / Umi / hzero-build 前端工程，或用户明确要求新建/接入 `packages/<module>`。
- Explore / Frontend Evidence 已完成目标工程、父注册入口、构建脚本和目录候选的必要扫描，但未找到已确认的 `golden-baseline` 或 `project-compatible` 相似页面。`golden-baseline` 必须满足 `goldenBaselineStatus=confirmed`、合法 `baselineConfirmationSource` 和 `baselineHealthCheck=pass`，不能仅凭搜索命中或相邻页面存在自动成立。
- `similarPageEvidenceQualityStatus=missing / partial`，且缺失原因是“空项目、参考资产缺失、参考资产不可读、无同类页面、无可采纳子模块或无可采纳 wrapper”，不是未探索。
- 当前需求仍需要生成或改造真实业务前端工程，而不是只输出设计草案。

## Baseline Decision

空项目或缺失参考资产不得退化为 non-compliant、local-filter、普通 Button、手写 Form 或业务壳页面。应记录：

| field | value |
| --- | --- |
| assetBaselineStatus | active / not-applicable / blocked；覆盖 empty / missing-reference |
| assetBaselineSource | hzerojs-asset-baseline |
| assetBaselineDecision | follow-asset-baseline |
| similarPageEvidenceQualityStatus | missing + reason=empty-project-no-adoptable-module / missing-reference-no-adoptable-module |
| baselineComparison.evidenceQuality | asset-baseline |
| baselineComparison.decision | follow-asset-baseline |

`asset-baseline` 只能作为缺少项目样板时的标准形态证据。它不等于 `golden-baseline` 项目样板，也不能证明目标工程的 wrapper、LOV、bucket、templateCode、API、菜单或权限已存在。子模块模板正文、最小文件树和运行时拒收项统一以 `front-hzero-enterprise-process-control` 的 HZEROJS 子模块运行期门禁 为准。

## Required Shape

Empty / Missing Reference 基线下，新增 HZEROJS 子模块或页面至少按以下生产形态生成或拆任务：

- 子模块骨架：必须 follow `hzerojs-submodule-runtime-gate.md` 的最小骨架和模板索引。无参考工程不得只生成 `package.json + config/config.ts + 页面目录`，也不得自由省略 `tsconfig.json`、`config/config.dev.ts`、路由入口或父工程注册规划。
- 子模块 config 基线：`config/config.ts` 必须按 `submoduleRouteEntryMode` 使用 `submodule-config-single-router.ts.template` 或 `submodule-config.ts.template`，`extendParentConfig` 只能从 `@hzerojs/plugin-micro` 导入，禁止 `@hzerojs/preset-hzero/lib/util`、`@hzerojs/preset-hzero/lib/*` 或其它深路径。进入 Verify 前必须在目标前端父工程根目录记录 Node resolver 证据：`require.resolve('@hzerojs/plugin-micro')` 必须可解析；`require.resolve('<module>/package.json')` 按 `workspaceResolverStatus` 分类记录，`<module>` 是 `packages/<module>/package.json` 的 `name`。缺依赖/link 未安装或 build 已通过但 resolver 失败时，不得直接归因为业务代码；package name、root dependency、workspace 配置或父工程 registry 确认缺失/冲突时，才回 scaffold/integration 修复。
- 父工程 package registry：必须先识别 active registry，默认只规划 `{ name: '<module>' }`。`initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段必须有 active schema、项目 confirmed baseline、平台强制要求或用户确认来源，并记录 `parentRegistrationEntryPolicy` / `parentRegistrationExtraFieldSource`；无来源不得生成。`registerRegex` 默认在子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex` 中闭合，不得用 packages-config 条目字段替代。
- 页面落点：新生成子模块必须记录 `pageRoot=src/pages`、`pageRootSource=asset-baseline`，固定使用 `src/pages/<PageName>/index.tsx`。`src/routes` 不作为新生成页面的可选落点；只有改造已存在于 `src/routes/**` 的存量页面，且有明确 existing-file / project-evidence 时，才允许继承。无参考基线下直接生成 `src/routes/**` 是资产基线违例，不得标记为 mock-completed、usable=true 或 production-ready。
- 路由基线：列表 + 详情/编辑/新建页面默认使用父 route + `routes` 嵌套，列表子路由使用显式 `/list` 或项目确认等价列表段；父 route 与列表子 route 不得同 path；新生成 route config 不得配置任何 `redirect` route。标准形态为父级 `/<module>/<feature>`、列表 `/<module>/<feature>/list`、详情 `/<module>/<feature>/detail/...`，并同步常量、菜单/openTab 入口、返回列表路径和验证 URL。若菜单或历史入口仍指向父级 path，Design 只能规划菜单/openTab/navigation 直接进入真实列表 path，并把正式平台菜单入口调整写入 Production Replacement / Handoff；不得规划父路由 redirect 到 list。
- 路由模板分流：`config/config.ts` 只负责 `routes: route` 或 `routes: [...routes]` 接线，不承载完整业务 route array。具体路由必须进入 `config/router.ts` 或 `config/routes/**`，并按确认的打开方式选择模板：当前页打开详情使用 `submodule-router-current-tab.ts.template`；普通 HZERO 系统页签使用 `submodule-router-open-tab-page-modes.ts.template`；每条记录或 pageMode 独立页签使用 `submodule-router-dynamic-tab-page-modes.ts.template`；同 pathname 不同 search 独立页签只在用户或项目证据明确时使用 `submodule-router-dynamic-tab-dws.ts.template`。实际 route 字段直接写确认后的字面量，不额外抽路径、标题或 component 变量。
- 路由菜单候选：无参考基线下不得从零追问菜单路径。Design 必须按 `generated-code-conventions.md` 生成 `parentRoutePath/listRoutePath/menuPath/routeTitle/menuGroup` 候选：已有项目父路径时沿用父路径并追加 feature kebab；无父路径但子模块明确时使用 `/<module-kebab>/<feature-kebab>`；列表 + 详情/编辑/新建形态下 `parentRoutePath` 只做分组或稳定 Tab 边界，`listRoutePath` 默认追加 `/list`，`menuPath` 默认等于真实 `listRoutePath`；单页功能才默认 `menuPath` 等于 `routePath`；`routeTitle` 使用业务中文名；`menuGroup` 优先父路径/父菜单，其次模块业务域或模块名，再退到 `<module-kebab>`。候选状态为 `generatedCandidate`，可进入 mock/demo 和候选实现；正式平台菜单父级、菜单 code、菜单标题、角色授权和平台多语言进入 Production Replacement / Handoff。只有候选无法唯一生成、父路径/父菜单冲突、production-ready 或本轮必须完成正式平台菜单挂载时，才触发 `Route Menu Confirm`。
- Route Context / Edit Mode：无参考基线或有项目存量基线时，新建、编辑、查看和详情页面都必须使用内置 path pageMode 表达页面身份：`/create`、`/detail/view/:id`、`/detail/edit/:id`。`/detail/create` 属于违规路径，发现后迁移到 `/create`。页面内部只从 path pageMode 派生语义化 `editable`；`?editFlag=true/false` 属于无效旧链接，必须迁移，不得读取、emit 或作为 UI 编辑态、route 身份、Tab 身份来源。
- Feature-local 分层：本条只在 Empty / Missing Reference Mode 下提供默认页面域形态；已有可采纳参考工程、参考子模块或相似页面时，不得机械套用为资产基线结论，也不得让参考目录直接覆盖内置规则。必须回到 `hzerojs-submodule-runtime-gate.md` 的 Page Pattern 和 `baseline-comparison-rubric.md` 做 `baselineComparison`：内置规则作为最低主线，参考只补充项目命名、目录和局部风格；只有证明参考项比内置规则更完整、更安全或更适合目标工程运行约束时，才允许该项 `follow-project`。资产基线下，业务页面默认使用页面域内分层，不把列表、详情、主从行、导入导出和附件全部塞进单个页面或全局 `src/stores/<feature>DS.ts`。列表/详情/主从页面至少规划 `src/pages/<PageGroup>/stores/queryDS.ts`、`detailDS.ts`，存在行筛选或行表时规划 `lineQueryDS.ts`；存在主从行或附件时分别规划 `components/LineTable.tsx`、`components/<Feature>Attachment.tsx` 或等价页面域组件；导入导出默认直接渲染 `Import` / `ExcelExportPro` 标准组件，只有存在头/行多入口复用、复杂参数收敛或项目 confirmed wrapper 时才规划带 `wrapperJustification` 的页面域动作组件。共享常量放在页面域 `constants.ts`。只有项目证据、相邻模块惯例或用户确认支持全局 store / 单文件页面时，才允许合并，并必须记录 reason 和 replacement 风险。
- 页面骨架：HZERO `Header + Content` 相邻根结构，列表/详情/表单/主从区块按 UI Contract，不自造页面级 Provider 或业务 wrapper 包住整组 `Header + Content`。
- Form label 基线：详情、编辑、新建和只读业务 `Form + Output` 默认必须有用户可见 label。需求/FDS/TDS/Figma/UI Contract 或项目 confirmed baseline 未明确 `labelLayout` 时，设计阶段默认 `labelLayout=horizontal` 和 `labelLayoutSource=default-horizontal-by-design-rule`；不得在业务详情/编辑/新建表单无来源使用 `labelLayout="placeholder"` / `LabelLayout.placeholder` / `labelLayout="none"` / `LabelLayout.none` 隐藏 label。
- 基础信息表单组合与布局基线：当已确认页面存在基础信息 / HeaderForm、设计产物只给出高层结构且未指定列数/容器宽度/跨列/标签/响应式细节、并且原型/Figma、项目 confirmed baseline 与用户未覆盖时，Design 必须同时生成 `Form Composition Contract` 和 `Basic Info Form Layout Contract`，触发 `default-form-layout-by-design-rule`，不得把 DataSet/mode/action 职责留给 Implementation 猜。头行、主从、多 Tab 或复用基础信息区默认 `page-container-plus-presentational-form`：页面容器拥有 DataSet、pageMode、record lifecycle、validation 和页面动作；HeaderForm / DetailForm 只接收 `dataSet`、`mode` 和局部组件参数；DataSet `fields/dynamicProps` 负责字段 metadata、bind 和动态可编辑性。默认布局基线为页面级 `Content` 的 `containerWidthPolicy=content-available`、`xs=1, sm=1, md=2, lg=3`、`lg=3` 列、`labelWidth=120` 和横向标签；短字段初始单列、长值 Lov 可优先评估两列、地址/备注/长文本/富文本/附件优先跨当前整行。可按可用宽度、字段密度、标签/值长度和字段语义记录 `layoutAdjustmentReason` 后调整 `3/2/1` 列、labelWidth、跨度或断点，不需要外部布局证据，也不设字段数自动阈值。审计和后端生成字段的展示时机、跨 mode 策略和 `submitPolicy` 由 Field Visibility Matrix / Field Editability Matrix 决定，不属于默认布局。固定 `max-width` 或居中只能有明确来源。参考页面的对应实现记录为 `reference-code-fact`，作为本默认规则的来源证据；目标页面确认列数变化时，长字段必须使用当前列数全跨，不能保留固定 `colSpan=3`。卡片、摘要头、字段顺序、额外分组和字段可见性均不由本布局基线决定。
- 详情集合基线：无参考基线下必须生成 `Detail Collection Contract`。TDS/MDS/API/DTO 声明为数组或集合的详情字段，表格型详情集合必须使用 Choerodon Pro Table；必须记录 `apiField`、columns、rowKey、`component=Choerodon Pro Table`、`componentSource=builtin-choerodon-table`、字段名来源和 mock 同名字段策略。mock/demo 响应必须使用同一 `apiField`；旧字段别名只能在集中 service/request adapter 中转换，不得进入详情组件。
- 详情/主从覆盖基线：无参考基线下必须生成 `Design Coverage Ledger`，并逐项覆盖 HeaderForm/基本信息字段、字段可编辑性、审计字段、页面级动作、明细 Tabs、明细筛选区、明细工具栏、行操作和保存后 route/URL 行为。TDS/FDS 要求的 `mobile/email` 等可编辑字段不得被详情 Output 或 disabled 表单误锁；`rejectReason/createdByName/lastUpdatedByName` 等展示字段若来自 TDS/FDS/API，必须进入 Field Usage Matrix 和 HeaderForm/基本信息验收。TDS/FDS 要求任一业务明细页签（如“采购申请明细”）或明细筛选时，必须生成 Tabs/TabPane 或项目等价页签结构和 line query DataSet/queryFields，不能直接裸渲染表格并关闭 `queryBar`。
- 弹层尺寸基线：无参考基线下必须生成 `Modal / Drawer / Overlay Contract`。所有业务 Modal / Drawer / Overlay 宽度严格按设计/Figma/PageSchema/项目 confirmed baseline/用户确认；设计未指定宽度时，普通表单 Modal 默认 `size=small / width≈520px 或项目 small 等价值`，详情 Drawer / 高密度只读详情 / 三列及以上 Form 优先使用项目 Drawer 默认尺寸或 confirmed baseline，不强制 small，并记录 readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`。`medium/large/70%/80%/980px` 等宽框只能有明确来源；尺寸必须写在 confirmed 弹层 API 入口（如 `size`、`width`、`drawerWidth/modalSize`），不能只写 `style.width`、内容容器或 CSS class。
- 列表查询基线：无参考基线下仍必须生成或继承 `List Query Contract`。普通管理列表默认使用 Choerodon Pro `Table + DataSet + filterBar` 或项目等价封装；`filterBar` 只表示查询条形态，不等于顶部 fuzzy search，代码形态按 enumProvenance 默认使用 `TableQueryBarType.filterBar`。FDS/TDS/Figma/用户确认出现“搜索框 / 关键字搜索 / 模糊查询 / 顶部快速搜索”时，必须写 `fuzzyQueryRequired=true`、`fuzzyQueryFields`、placeholder、`queryFieldsLimit`、查询/重置/刷新行为，并把 `queryBarProps.fuzzyQuery=true` 和按需 `queryBarProps.fuzzyQueryPlaceholder` 或项目等价写法作为实现验收；`fuzzyQueryFields` 不得生成到 `queryBarProps`。只有项目证据证明不支持时才允许 `unsupported-with-evidence`，且不得支撑 production-ready。
- 数据链路：DataSet-first 或项目确认的 service/DataSet 模式；空项目 / 缺失参考资产基线下，DataSet 管理的 `read/create/update/destroy/submit` 默认 `dataSetTransportMode=request-config-direct`，必须在 `transport.*` 中直接返回 Choerodon DataSet 可消费的 request config，不得 import 或调用业务 service 函数。`transport.read: ({ params }) => queryXxx(id, params)`、`transport.submit: () => saveXxx(...)`、`service/mock + loadData` 都不是可采纳基线。页面级提交、撤回、作废、导入导出等非 DataSet 生命周期动作才允许作为 `runtimeDataEntry.owner=service-action`；`confirmed-hybrid-wrapper` 只允许共享不发请求的 URL/query/payload/response 纯 helper 或项目 request adapter，不得表示 DataSet transport 委托业务 service。mock demo 必须是 HZERO 本地 devServer middleware 暴露的可请求 `/_mock/<module>/v1/{organizationId}/...`，不得用组件内数组、local-filter 或 `service/mock + loadData` 冒充。`queryMode=mock-request` 时必须同时闭合 `parentMockPluginRegistrationEvidence`、`mockPluginTemplateCompliance`、`mockPluginSelfCheck` 和 `mockPrefixOriginPolicy`；无参考模块不能只生成 mock handler 文件、只写裸 `/_mock/<module>` 前缀、缺少模板自检，或用 `api.app` / Express app 直接挂载绕过模板 plugin。
- 契约保真基线：无参考基线下默认 `runtimeFieldPolicy=canonical-only`。Field Usage Matrix 必须记录 `canonicalField/runtimeFieldPolicy/adapterAliasPolicy/forbiddenRuntimeAliases`；旧字段别名只能在集中 service/request adapter 中出现，不得进入页面、DataSet、Table、Form、actionGuard 或 submit payload。按钮、行操作、字段 label、状态文案、确认/通知和区块标题默认 `copyPolicy=exact-source`，近义改写必须有 `copyOverrideSource`。状态动作必须记录 `statusField/statusEnumMap`，不得把设计状态 code/meaning 改成旧模型近义值。
- Choerodon enum 基线：无参考项目证据时，`asset-baseline` 默认采用组件库 enum 风格，不得因为缺项目相似页面而降级为裸字符串或 broad `as any`。Design / Task 必须写 `enumStrategy=asset-baseline-enum`、`enumProvenance.source=asset-baseline-reference`，并按 `hzerojs-enterprise-page-composition-example.md` 和 Choerodon reference 使用 `FieldType`、`DataSetSelection`、`DataToJSON`、`ColumnLock`、`ColumnAlign`、`TableQueryBarType`、`TableEditMode`、`SelectionMode`、`ButtonColor`、`FuncType` 等明确枚举；`DataSetSelection.single/multiple` 只用于 DataSet `selection`，Table `selectionMode` 必须使用 `SelectionMode.rowbox/treebox/click/none/dblclick/mousedown`。只有 DataSet 配置类枚举在用户或项目证据确认 string 风格时才可写 `enumStrategy=dataSet-confirmed-string/project-string-confirmed`。
- TypeScript render 基线：无参考基线下 `typescriptRenderContract=required`。Table columns、renderer、toolbar buttons、table toolbar buttons、Modal.open content、Attachment/ImportExport wrapper props 必须有 typed surface 或类型安全构造；不得把 columns/buttons 写成无类型数组后靠 `as any`、`.filter(Boolean)` 或未类型化 renderer 参数消音。列表表格、明细表格和详情集合表格默认从 `choerodon-ui/pro/lib/table/Column` 导入 `ColumnProps`、`ColumnRenderProps`，并把列定义写成 `useMemo<ColumnProps[]>(...)`、`const columns: ColumnProps[] = ...` 或等价 typed surface；所有自定义 `renderer` 参数默认标注 `ColumnRenderProps`，除非目标项目已确认使用 `RenderProps` / wrapper 专用类型。renderer 参数必须兼容 Choerodon `RenderProps/ColumnRenderProps` 的可选 `value`，不能把 `{ value }` 写成必填参数类型后再靠 `any` 规避。
- Modal lifecycle 基线：无参考基线下使用 `Modal.open` / Drawer / 业务弹层时，必须生成 `modalLifecycleContract=required`，并把 `closeApiSource` 标为 `return-proxy / children-modal-prop / header-closeBtn / static-close / project-wrapper / blocked`。只有目标项目源码、类型声明和项目样例三者至少一类确认后，Implementation 才能调用 `modal.close()`、`Modal.close(key)` 或 wrapper close；缺证据时默认使用组件内置关闭按钮或返回证据补齐，不得猜测返回值。
- DateTime / object render 基线：DataSet 使用 `FieldType.dateTime/date/week/month/year/time` 的字段必须在 Table/Output/自定义 JSX 中有明确展示策略：组件默认展示、项目 confirmed date renderer，或显式格式化为字符串；不得直接返回 `value`、`record.get(dateField)` 或 moment-like 对象作为 React child。`FieldType.object` 集合字段默认按详情集合基线使用 Table/组件展示，不得 JSON stringify 或对象直接渲染。
- i18n 消费基线：无参考项目证据时，仍默认使用 HZERO `intl.get(fullKey).d(fallback)` 和 `formatterCollections` / 项目等价平台 prompt 注册；不得因为空子模块、缺参考页面或平台多语言尚未配置，就把 DataSet `label`、Table column header、Form label、按钮、Modal/Drawer/Tab 标题、notification/confirm、空态和校验提示降级为硬编码中文。缺服务简码、功能英文名或 namespace 时标记 `i18nCoverage=missing/partial` 和 replacement；基础事实足够时按 `generated-code-conventions.md` 生成 `generatedCandidate` key，同轮写入 `platform-locale-keys.json`，默认 status=pending。
- 权限和按钮：业务动作默认进入 Action Entry Matrix 和 Button Semantic Matrix；required 动作使用 `PermissionButton` / HZERO 权限方案或 generatedCandidate 权限码承接，不能普通 Button fallback。
- 状态动作和保存跳转：撤回、提交、作废、删除等状态动作只要在 FDS/TDS/API/status-flow 中存在且入口已确认，必须进入 Status Action Matrix、Action Entry Matrix、Button Semantic Matrix 和 Design Coverage Ledger；不得因 service 已存在但页面按钮未拆验收而漏实现。新建保存后若设计要求留在详情并补齐 `headerId/id` 到 URL、Tab key 或 routeContext，必须写入 `saveRedirectPolicy` 和 Design Coverage Ledger；Implementation 不能只刷新 DataSet 后停留在无主键路由。
- 主数据/枚举/附件：按字段语义分类保留 LOV/lookup/Attachment candidate。缺平台编码时使用 `generatedCandidate/missing`、mock-only options 或 replacement 承接，不得静默降级成普通 `TextField`、普通 `Output` 或 raw UUID。标准业务附件 JSX 默认使用 Choerodon Pro `Attachment`、`Attachment.Dragger` 或项目 confirmed wrapper；常规为 `choerodon-ui/pro` 命名导入，若目标版本证据显示桶入口循环依赖或运行时报 `ReferenceError: Attachment is not defined`，可使用 `choerodon-ui/pro/lib/attachment` 默认导入并记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed`。`components/Attachment` / `hzero-front/lib/components/Attachment` 在无参考基线下按配置对象处理，只允许以 `hzeroAttachmentConfig` 等 config 名传给 `components/RichTextEditor` / `NewRichTextEditor` 的附件配置入口，不得作为 `<Attachment />` 渲染。若项目声称该路径是 wrapper，必须有 exportShape=react-component/confirmed-wrapper 的项目证据。
- 导入导出：required 能力必须生成 HZERO 标准导入组件、`Import`、`ExcelExportPro` 或项目 confirmed wrapper 的候选形态；参数缺失时使用 mock/generatedCandidate 候选常量先支撑标准组件实现，并写入 Contract Check / Verification / Handoff，不能用普通 Button、disabled/no-op、提示入口、本地下载模拟或无来源薄封装。
- 状态动作：提交、撤回、作废、删除等必须生成按钮态、action 入口和 mock/API handler 同源守卫；缺矩阵时阻塞或回设计补齐。

## No UI Downgrade

Empty / Missing Reference Mode 下以下实现直接判为不合格：

- 手写查询 `<Form>` 替代 Choerodon Pro DataSet queryFields / Table 查询形态。
- FDS/TDS/Figma/UI Contract 要求搜索框、关键字或模糊查询，但列表未实现顶部 fuzzy search、未映射 `fuzzyQueryFields`，显式配置 `queryBarProps.fuzzyQuery=false`，或把字段映射误写成 `queryBarProps.fuzzyQueryField/fuzzyQueryFields`。
- 申请人、部门、组织、供应商、物料等主数据字段以普通 `TextField` 实现，且无自由文本来源。
- 附件、文件 UUID、上传/预览/下载字段以普通 `TextField` / `Output raw uuid` 实现。
- `import Attachment from 'components/Attachment'` 或等价默认导入后直接 `<Attachment />` / `<Attachment.Dragger />` 渲染，且没有 exportShape=react-component/confirmed-wrapper 证据；配置对象用法必须命名为 `hzeroAttachmentConfig` 或等价 config 名并只传给富文本组件 API。
- required 导入/导出能力以普通 `Button`、永久 `disabled`、无 `onClick`、no-op、提示弹窗或本地状态模拟实现。
- DataSet `transport.read/create/update/destroy/submit` import 或调用业务 service 函数，例如 `transport.read: ({ params }) => queryXxx(id, params)` 或 `transport.submit: () => saveXxx(...)`。
- `config/config.ts` 内联完整业务 route array，或把 list/detail/current-tab/openTab/dynamic-tab 路由对象直接写入主配置。
- 有列表 + 详情/新建/编辑子页面时生成同级顶级 route，而不是父 route + `routes` 嵌套；设计、任务或 route config 使用任何 `redirect` route，包括父路由 redirect 到 list、父级 `redirect + routes`、同父级 path redirect 子路由或单独叶子 redirect；普通 `hzero-openTab` 误配 `mode: 'dynamic'`；dynamic-tab 复用普通详情 tab key。
- 页面、DataSet、Table、Form、actionGuard 或 submit payload 直接使用旧字段别名，且 UI Contract 未确认 legacy runtime。
- 按钮或行操作把设计原文近义改写，例如“新建”改成“新增行”、“提交审批”改成“提交”，且没有 `copyOverrideSource`。
- 状态 code/meaning 与 `statusEnumMap` 不一致，例如把 `NEW` 改成 `DRAFT`、`IN_APPROVAL` 改成 `SUBMITTED`，且没有集中 adapter 或 legacy runtime 来源。
- 列表/详情 required 行操作缺失，例如设计要求按状态显示提交审批、撤回审批、删除，但实现只给详情/编辑/删除或缺少状态守卫。
- 新生成查看/编辑/新建入口、openTab key/path、保存跳转或 Tab 唯一性使用 `?editFlag=true/false`、`?mode=edit/view`、`?action=create` 表达页面模式，而不是内置 `/create`、`/detail/view/:id`、`/detail/edit/:id`；DataSet 中的 `editFlag` 反向决定页面可编辑态。
- 详情集合字段使用项目只读表格/薄 wrapper、`renderPlainList`、`ul/li`、逗号拼接、JSON stringify 或多字段模板字符串展示，替代 Choerodon Pro Table。
- 详情集合字段、mock 数据或 service 读取与 TDS/MDS/API/DTO 不一致的无来源别名，且没有集中 adapter 证据。
- 业务 Modal / Drawer / Overlay 在设计未指定宽度时生成宽框，或只通过 `style.width`、内容容器、CSS class 控制弹层宽度；普通表单 Modal 无 wrapper 默认 small 证据时缺少 `size=small` / 项目 small 等价配置；详情 Drawer / 高密度详情缺项目默认尺寸或 baseline、readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`。
- `Modal.open` / Drawer 自定义关闭入口缺 `modalLifecycleContract`，或无证据调用 `Modal.open()` 返回值的 `.close()`、静态 `Modal.close(key)`、私有 container close/update API。
- 新建/编辑页使用 mock seed、示例人名、示例部门、历史记录或当前时间预填业务输入字段，且无 UI Contract 默认值来源。
- 详情、编辑、新建或只读业务 Form 无来源使用 `labelLayout="placeholder"` / `LabelLayout.placeholder` / `labelLayout="none"` / `LabelLayout.none`，导致业务字段 label 不可见。
- 父工程 `packages-config` / `hzeroMicro.packages` 新增子模块时无来源追加 `initLoad`、`registerRegex`、`plugins`、`priority`、`routes` 等额外字段，或用 package 条目里的 `registerRegex` 替代子模块 `config/config.ts` 的 `hzeroMicro.microConfig.registerRegex`。
- mock-request 子模块 plugin 使用 `require('./<module>-dev-mock')(api.app)`、`api.addBeforeMiddlewares(() => { require(...)(api.app); })`，或任何依赖 `api.app` / Express app 实例直接挂载的非模板写法；这不符合 `submodule-dev-mock-plugin.js.template`，不得标记为 `mock-completed`、`usable=true` 或 production-ready。
- mock-request 子模块 plugin/handler 缺少模板自检机制，不能证明 middleware 导出函数、`__mockMount` 匹配、重复注册保护和 Umi 扩展点可用性。
- 列表 + 详情/编辑/新建路由中父 route 与列表子 route 使用同一个 path，或通过父 route / 叶子 route `redirect` 到 `/list`，导致列表、详情或新建运行时匹配不稳定。
- Table/Form/Button/Modal/Drawer 等组件 enum-like props 裸写字符串、布尔值或缺 enumProvenance；DataSet enum-like props 裸写字符串且没有 `project-string-confirmed` 证据。
- DataSet `fields/queryFields` 的 `label`、Table column title/header、Form 显式 label、按钮、Modal/Drawer/Tab 标题、notification/confirm、空态或校验提示直接写用户可见中文/英文，且未使用 `intl.get().d()`、未进入 i18nCoverage / platform locale ledger / replacement。
- Table columns、renderer、toolbar buttons、table toolbar buttons 或弹层内容缺 `typescriptRenderContract`，使用 broad `as any/as unknown`、`.filter(Boolean)`、无类型 renderer 参数或未导入 symbol 规避类型问题。
- `FieldType.dateTime/date/week/month/year/time` 字段的 Table renderer、Output renderer 或 JSX 直接返回 moment-like `value` / `record.get(...)` 对象，可能触发 React #31；日期对象必须显式格式化或使用 confirmed renderer。
- 在目标前端工程 `src/**` 或 `packages/**/src/**` 生成 `__implementation-self-check__.md`、`__review*.md`、`__verify*.md` 等流程记录文件。

## Mock Request Closure

无参考模块或资产基线下，`FE-SERVICE-MOCK` / mock-request 任务必须形成完整接入闭环，不能只补 mock 数据文件：

- 子模块 mock 文件必须使用 `front-hzero-enterprise-process-control` 的 submodule dev mock plugin 模板 和 `front-hzero-enterprise-process-control` 的 submodule dev mock handler 模板，生成前读取模板，落盘时只替换模板中实际存在的占位符；替换后必须验证无 `__MODULE_KEY__`、`__MODULE_CAMEL__` 或其它 `__[A-Z0-9_]+__` 占位符残留，并保留 `mockPluginTemplateCompliance` / `mockPluginSelfCheck` 证据，不得手写替代结构。
- `parentRootMockPluginRegistration` / `parentMockPluginRegistrationEvidence` 必须来自父工程 `config/config.ts` 顶层 `plugins` 注册子模块 plugin，或注册父工程聚合 plugin 后由聚合 plugin 引用子模块 handler/plugin；无父工程的独立应用写 `not-applicable + 项目等价根配置入口`。`packages-config.js` package 条目 `plugins` 字段无效。
- HZEROJS Umi `packages/<module>` 子模块默认支持 `package-start` / 子包独立启动；`queryMode=mock-request` 时，除父工程 `config/config.ts` 顶层注册外，还必须确认 `packageStartMockPluginSource=parent-config-inherited-by-extendParentConfig`，即 package-start 通过子模块 `config/config.ts` 的 `extendParentConfig` 继承父工程同一 plugin；子模块 `config/config.ts` 不得新增仅服务 mock 的顶层 `plugins` 注册，`config/config.dev.ts` 不得注册同一 `../dev-mock/<module>-dev-mock-plugin`。只有项目证据明确不支持子包独立启动时，才允许 `packageStartMockPluginSource=not-applicable + reason`。
- `mockPluginTemplateCompliance` 必须证明 plugin 直接 `require('./<module>-dev-mock')`，并通过 `api.addBeforeMiddlewares(() => [middleware])` 注册；不得生成旧 `api.addBeforeMiddleware` fallback。`require('./<module>-dev-mock')(api.app)`、`api.addBeforeMiddlewares(() => { require(...)(api.app); })` 或任何 `api.app` 直接挂载均为 `non-template-invalid`。
- `mockPluginSelfCheck` 必须证明 plugin/handler 保留模板自检：middleware 导出函数、`__mockMount` 匹配、重复注册保护、注册日志和 Umi 扩展点缺失时的明确失败；Design/Task 阶段可写 `planned`，Implementation/Verification/Review/Handoff 阶段必须写 `export-shape-pass+mount-pass+duplicate-guard-pass`、`failed`、`not-run` 或 `not-applicable`。
- `mockPrefixOriginPolicy` 必须是 `current-dev-server-origin`：servicePrefix/DataSet/service mock 分支必须使用业务包本地 `service-prefix.ts.template` 形态，通过模板内本地 SSR guard helper 生成当前 dev server origin + `/_mock/<module>`；不得 import 或复用目标工程 `getCurrentOrigin()` / `currentOrigin` / origin helper。裸 `/_mock/<module>` 只能作为 middleware mount，不得作为默认 service prefix 交给会拼 `API_HOST` 的 request helper。
- File Mapping 必须包含 mock handler、mock plugin、servicePrefix/request helper、DataSet/service 调用文件，以及父工程 `config/config.ts` 或父工程聚合 plugin integration task；缺任一项时只能标 `blocked-by-contract` 或 `blocked-by-design`。
- Verification 必须记录静态 mock validator、父工程 plugin 源码接线和 servicePrefix/helper 对账；Network/HTTP smoke 或 DataSet request 证据只能来自外部 runtime acceptance 或用户手工证据，实际 origin 是当前 dev server，path 匹配 `/_mock/<module>/v1/{organizationId}/...`，并证明父工程 plugin 已生效。

## Question Gate Preservation

资产基线只补形态，不补生产事实。进入 Empty / Missing Reference Mode 后，所有生产、落点、交互或工程接线问题仍必须逐一保留，不得因为基线完整而自动 resolved。Empty / Missing Reference Mode 不是串行流程中的第一步；Design 必须在同一轮 Contract Check 中累积完成资产基线、默认 mock demo 数据链路、真实接口 readiness、production replacement 和全部 questionGate 扫描：

- `Missing Contract Confirm`：影响当前 Mock demo 的必要契约或 Mock 接线冲突未确认；真实前端可调用契约、production-ready 目标或拒绝默认 Mock 只进入后续独立集成 advisory。
- `Frontend Project Confirm`：目标前端工程、父工程、已有 `packages/<module>` 或新建子模块边界仍不唯一。该 gate 只确认工程/package 边界，不确认 package 内功能落点。
- `Target Placement Confirm`：package 内 `businessDomain/pageGroup/pageDir/routePrefix/menuGroup` 仍不唯一。
- `Open Interaction Confirm`：详情打开方式、系统页签、动态页签或浏览器新标签页未确认。
- `Import Component Mode Confirm` / `Export Component Mode Confirm`：需求包含导入/导出能力且组件模式未确认。
- 附件 bucket/storageCode、LOV code、lookup code、templateCode/importCode/export template、tenantContext、servicePrefix、backend readiness、production replacement 范围未确认。默认 mock/demo 下，附件 bucket/storage/template 缺口转为 generatedCandidate/mockOnly/placeholder + replacement，不再单独追问；其它缺口仍按对应 gate 处理。

记录规则：

- Empty / Missing Reference Mode 下影响当前 Mock demo 的待确认项必须拆成独立 `questionGateQueue[]` 项；候选互不依赖时由 Lite / 外层 question owner 在一次 question 工具调用中批量提交，依赖前序答案时才串行；不得把 `Frontend Project Confirm`、`Target Placement Confirm`、`Route Menu Confirm`、`Open Interaction Confirm`、导入导出模式或 `Frontend Design Confirm` 合并为一个问题域或一个答案。production-ready/真实 API 目标不进入当前 question 队列，只记录后续独立集成 advisory。空项目基线候选只属于 Target Placement，不能顺带确认其它问题域。
- `questionGatePreservationStatus=required` 表示基线已启用但仍有未解决门禁。
- `assetBaselineDecision=follow-asset-baseline` 只表示按资产基线补工程形态；若页面存在 DataSet/service/transport/action request，默认写 `mockDemoDecisionStatus=default-mock-demo`、`runtimeDataPathDecision=requestable-demo-mock`、`queryMode=mock-request`。该默认不确认生产 API、真实远端请求、LOV/lookup、权限、附件、导入导出、Target Placement 或 Open Interaction。
- `questionGate.required=true && resolved=false` 或 `questionGateQueue[]` 任一未解决时，不得进入 runnable Implementation、Verify、Handoff 或 DONE。
- `assetBaselineSource=hzerojs-asset-baseline` 可以采用默认 mock demo，但不能把 `generatedCandidate`、真实 API、平台编码或生产契约改成 `confirmed`。

## Output Requirements

Frontend Design / Task Breakdown 至少输出：

| field | 说明 |
| --- | --- |
| assetBaselineStatus | active / not-applicable / blocked + reason；覆盖空项目和缺失参考资产 |
| assetBaselineSource | hzerojs-asset-baseline / not-applicable |
| assetBaselineDecision | follow-asset-baseline / not-applicable |
| questionGatePreservationStatus | required / clear / blocked |
| unresolvedQuestionGates | Missing Contract / Target Placement / Open Interaction / Import Component Mode / Export Component Mode / other |
| pageRoot | src/pages / existing-src-routes / custom；新生成页面固定 src/pages |
| pageRootSource | asset-baseline / project-evidence / adjacent-module / existing-file；src/routes 不允许用于新生成页面 |
| parentRegistrationEntryPolicy | minimal-name-only / schema-confirmed-extra-fields / missing / conflict / not-applicable |
| parentRegistrationExtraFieldSource | active-schema / project-baseline / platform-required / user-confirmed / none / not-applicable |
| listRoutePathPolicy | explicit-list-child / project-equivalent-list-segment / blocked |
| routeContextPolicy | path-pageMode-required / project-confirmed-equivalent / blocked |
| editFlagPolicy | derived-internal-only / blocked |
| formLabelLayoutPolicy | visible-label-required / no-label-confirmed / blocked |
| formCompositionPolicy | page-container-plus-presentational-form / simple-page-co-located-with-reason / blocked；页面容器、Form 组件、DataSet、mode、validation/action 和 readonly 策略必须可追溯 |
| detailCollectionContract | pass / partial / missing / blocked / not-applicable；数组/集合字段必须含 apiField、columns、rowKey、component、mock 同名字段策略 |
| drawerModalContract | pass / partial / missing / blocked / not-applicable；普通表单 Modal 未指定宽度默认 size=small；详情 Drawer / 高密度详情记录项目默认尺寸或 baseline、readabilityRisk、Form columns/colSpan 和 valueOverflowPolicy；宽度配置入口必须有 API 证据 |
| uiContractDowngradeAllowed | no |
| mockOnlyDataTransport | default-mock-demo / blocked |
| mockPluginSelfCheck | planned / export-shape-pass+mount-pass+duplicate-guard-pass / failed / not-run / not-applicable |
| dataSetTransportMode | request-config-direct / not-applicable / blocked |
| runtimeDataEntryOwnerPolicy | dataset-transport / service-action / confirmed-hybrid-wrapper / blocked |
| confirmedHybridWrapperPolicy | shared-helper-or-request-adapter-only / not-applicable / blocked |
| fieldRuntimePolicy | canonical-only / blocked |
| forbiddenRuntimeAliases | list / none |
| detailRegionCoverage | pass / partial / missing / blocked / not-applicable；详情/主从页必须覆盖 Header/基本信息 required 字段、Form owner DataSet/record、Tabs、明细筛选、详情动作和保存后 route 主键 |
| ownerDataSetOrRecordPolicy | confirmed / missing / conflict / not-applicable；详情/编辑/新建 Form 字段必须有 owner DataSet 或 record 来源 |
| statusEnumMapStatus | pass / partial / missing / conflict / not-applicable |
| copyPolicyDefault | exact-source |
| contractFidelityCheck | required / not-applicable；scope=fields/buttons/status/row-actions/i18n-copy |
| i18nConsumptionPolicy | intl-get-required / project-i18n-confirmed / blocked |
| i18nCoverage | pass / partial / missing / blocked / not-applicable |
| platformLocaleKeys | confirmed / pending / mixed / none / not-collected；逐 key 记录 defaultMessage、platformSource 和 evidence |
| enumStrategy | asset-baseline-enum / dataSet-confirmed-string / project-enum-confirmed / blocked |
| enumProvenanceSource | asset-baseline-reference / project-evidence / adjacent-module / user-confirmed / missing |
| typescriptRenderContract | required / confirmed / blocked |
| modalLifecycleContract | 按 `schema-checklist.md` / `frontend-compliance-manifest.md` 值域填写 |
| closeApiSource | 按 `schema-checklist.md` / `schema-field-contract-gates.md` 值域填写 |
| dateTimeRenderContract | required / confirmed / blocked / not-applicable |
| attachmentImportPolicy | pro-attachment-jsx / confirmed-wrapper / hzero-attachment-config-for-rich-text / blocked |
| attachmentImportExportShape | react-component / static-member / confirmed-wrapper / config-object / missing |

Implementation 必须把这些字段继承到 `taskAcceptanceScan` 或 `design-deviation-report`。若代码结果违反 No UI Downgrade，或缺少 `enumStrategy` / `typescriptRenderContract` 的 required 结论，当前任务只能是 `partial-needs-rework`、`blocked-needs-rework` 或 `blocked`，不得标 `mock-completed`、`usable=true`、`Implementation Complete` 或 checklist `[x]`。

详情/主从页命中 `detailRegionCoverage=partial/missing/blocked`、`ownerDataSetOrRecordPolicy=missing/conflict`，或违反 `GCSQ-DETAIL-REGION-001` / `GCSQ-FORM-DS-001` 时，同样只能是 `partial-needs-rework`、`blocked-needs-rework` 或 `blocked`；不得因为列表页可运行、service 已存在或 DataSet refresh 成功而标记详情实现完成。

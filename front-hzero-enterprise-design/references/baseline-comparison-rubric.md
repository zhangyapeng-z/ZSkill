# Baseline Comparison Rubric

用途：当目标工程现状、相邻页面写法或历史子模块范式与当前标准规则不一致时，用一套轻量准则判断采用工程写法、标准范式、合并方案还是阻塞确认。本文用于 Explore、Frontend Design、Task Breakdown 和 Review，不替代具体业务契约。

## 目录

- Core Rule
- Evidence Quality Levels
- Golden Baseline Confirmation
- Reference Module Decision
- Superiority Decision and Question Gate

## Core Rule

工程证据用于识别事实，不自动成为生成准则。标准范式用于提供最低完整性、安全性和可验证性边界。生成或修改真实业务前端工程前，必须选择不破坏项目运行、且不复制历史缺陷的方案。

相似页面、历史模块和搜索命中的代码必须先评级，再决定是否采用。未评级代码只能证明“项目中存在这种写法”，不能证明“新代码应该这么写”。

所有新增/改造真实业务前端工程的 comparison 都必须先记录 `standardBaselineApplied=true`，表示已加载内置标准基线作为最低规范尺。`standardBaselineApplied` 不等于 `asset-baseline`，也不表示启用 `hzerojs-asset-baseline`。有参考子模块、相似页面或项目 wrapper 时，仍先用标准基线做比较，再按 `golden-baseline / project-compatible / legacy-risk / anti-pattern / unknown-quality` 决定 `follow-project / merge / follow-baseline / block`。只有无可采纳参考模块、参考资产缺失/不可读或空项目时，才允许记录 `assetBaselineSource=hzerojs-asset-baseline` 和 `decision=follow-asset-baseline`。

AI 不得凭主观偏好、文件数量、相似命名或“项目里这样写过”判定参考项优于内置规则。`follow-project` 必须有可复核证据；证据不足时默认 `merge / follow-baseline`，若会影响关键行为则写 `block + confirmationNeeded=yes`。

## Evidence Quality Levels

| quality | 判定条件 | 可采纳范围 |
| --- | --- | --- |
| `golden-baseline` | 用户、Frontend Design、项目 owner 或明确基线文档指定的好样板；Review/Verification 无明显阻塞项 | 可作为同类页面的优先写法来源，但仍不能替代当前 feature 的字段、接口、权限、LOV/lookup、附件或导入导出契约 |
| `project-compatible` | 相似页面能证明项目组件、import 路径、路由聚合、request helper 或 wrapper 存在，且未命中本表 anti-pattern | 可确认工程能力和局部项目风格；需要与标准范式合并 |
| `asset-baseline` | 目标 HZEROJS 项目为空、参考资产缺失/不可读，或缺少可采纳相似页面，但已按 `hzerojs-asset-baseline.md` 选择资产基线 | 只能提供标准形态和最低门禁；不能替代项目 wrapper、平台编码、API、LOV/lookup、附件、导入导出或用户确认 |
| `legacy-risk` | 相似页面可运行但存在老写法、缺验证、缺 mock/request 证据、过度封装、假按钮、`as any`、本地 options、无来源 Provider 等问题 | 只能作为兼容性或迁移风险记录，不得复制为新代码默认范式 |
| `anti-pattern` | 命中明确拒收项，或 Review/用户反馈证明该写法不可用、不可维护或违反 HZERO/Choerodon 规范 | 只能作为反例；Implementation 必须规避或修复 |
| `unknown-quality` | 只通过搜索命中、命名相似、最近改动或未评估目录发现 | 只能作为 candidate，不得覆盖标准规则 |

## Golden Baseline Confirmation

`golden-baseline` 不能由搜索命中、文件数量、最近修改、命名相似或模型主观判断自动确认。必须同时满足：

- `baselineConfirmationSource` 为 `user-explicit / owner-doc / design-confirmed-from-owner` 之一；`none / search-only / model-inferred` 不允许标记为 golden。
- `baselineConfirmationText` 记录用户原话、项目 owner 说明、基线文档路径或 Frontend Design 中的确认依据。
- `baselineScope` 明确为 `package / page-pattern / route-pattern / DataSet-pattern / wrapper-pattern / other`，不得用一个 golden 页面覆盖所有工程模式。
- `baselineHealthCheck=pass`，且 Review/Verification 未发现会影响该模式复用的 blocker；若只有局部通过，最多为 `project-compatible`。
- `goldenBaselineStatus=confirmed`；未确认、证据冲突或健康检查失败时分别写 `not-confirmed / conflict / rejected`。

`golden-baseline` 只确认工程模式和局部项目风格，不确认当前 feature 的业务事实。API、字段、权限码、菜单、LOV/lookup、附件 bucket/storageCode、导入导出模板、Target Placement、Open Interaction、tenantContext、servicePrefix 和 backend readiness 仍必须由当前 feature 契约确认。默认 mock/demo 是内置决策，只记录 `mockDemoDecisionStatus=default-mock-demo`、`queryMode=mock-request` 和 replacement，不作为 golden baseline 授权项。

## Reference Module Decision

有参考子模块或相似页面时，决策顺序固定为：

1. 记录 `standardBaselineApplied=true`，加载标准基线作为最低门禁。
2. 对参考子模块做 `evidenceQuality` 评级。
3. `golden-baseline` 且适用范围一致时可 `follow-project`。
4. `project-compatible` 时默认 `merge`：保留项目兼容点，同时用标准基线补齐完整性、安全性和可验证性。
5. `legacy-risk / anti-pattern / unknown-quality` 不得进入默认生成范式，只能 `follow-baseline / block`，或作为 `rejectedPatternItems`。
6. 只有无可采纳参考时，才进入 `follow-asset-baseline`。

参考子模块必须先通过 `Reference Module Quality Gate`，再允许进入 Design / Task / Implementation：

- 每个参考子模块必须记录 `evidenceQuality`、`qualityBasis`、`contaminationStatus`、`adoptedPatternItems`、`rejectedPatternItems`、`blockedPatternReuse`、`downstreamPolicy` 和 `decision`。
- 未评级参考默认 `unknown-quality`，只能 `locate-only / reject-template`，不得成为 UI、route、DataSet、service、mock、provider、wrapper、i18n 或 permission 的实现模板。
- `qualityBasis=no-issue-found / scan-only` 只表示机械扫描证据，不能自动升级为 owner 确认；只有 `owner-confirmed / user-confirmed / design-confirmed` 才能支撑 `golden-baseline`。
- `legacy-risk / anti-pattern / unknown-quality` 不得有 `adoptedPatternItems`；若已有产物采纳了这些模式，Task 必须阻塞 runnable implementation，Review 必须形成 finding，Handoff 必须降级。
- `project-compatible + qualityBasis=no-issue-found` 只能在 `adoptedPatternItems[]` 中授权 `directory / style` 等低风险局部模式；route、DataSet、service、mock、provider、wrapper、i18n、permission 等关键实现区必须 `require-owner-confirmation / follow-baseline / reject-template / locate-only`，不得仅凭扫描未命中变成全量模板授权。低风险局部模式默认是对内置规则的补充，decision 应优先写 `merge`；只有证据证明参考项优于内置规则时，才允许对应项 `follow-project`。
- DataSet 文件落点和 `stores/` 目录归组可作为 `directory:dataset-stores-layout` 低风险目录模式采纳，前提是仅改变文件组织，不改变 DataSet transport、fields/queryFields、queryDataSet、Form/Table 绑定、mock/runtime store 或运行时实例边界。该采纳默认是 `merge`：保留内置 DataSet 运行语义和验证门禁，只兼容项目目录归组；只有能证明参考落点在目标工程中更清晰、更可维护或更符合装载/协作边界，并记录 `superiorityEvidence=runtime-required / repeated-healthy-reference / pure-helper-or-directory-boundary` 与 `aiDecisionAllowed=yes` 时，才可写 `follow-project`。若参考模块同时引入 `transport` 调 service、共享 `new DataSet(...)` 实例、页面 `stores/` 承载 mock runtime store、字段别名漂移或 `loadData/local-filter` 成功路径，则不再是目录模式，必须按 DataSet / mock / field contract 关键实现区评级和处理。
- Open Interaction 的用户可见选项集合不得由参考子模块或相似页面决定。参考子模块中的 Drawer/Modal/抽屉/弹窗只能作为 `rejectedPatternItems`、冲突证据或明确弹层来源的复核证据；当当前 FDS/用户输入写的是“点击跳转至新建页面 / 点击跳转至编辑页面 / 跳转至对应数据的编辑页面 / 跳转到详情页面”时，参考子模块只能补 route helper、path、key、title 或验证方式候选，不得把弹层形态加入 question。
- 可访问参考模块源码时，应优先运行只读机械扫描 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_reference_module_quality.py --root <reference-module-root>` 或等价入口，作为 `scanReport` 证据。该扫描只能支撑质量评级，不确认当前 feature 的业务契约。
- `decision=merge` 只表示“项目兼容点 + 标准基线补齐”的组合策略；不能把参考模块中的 local-filter、`as any`、薄封装、无来源 Provider、旧 mock、权限 fallback 或字段别名带入新实现。

## Superiority Decision and Question Gate

更优判定先由 AI 基于证据做门槛判断，但 AI 只能在证据可复核时自判。以下任一证据成立，才允许把单个参考项从 `merge` 升级为 `follow-project`：

- 参考项补足了目标工程必需的运行约束，而内置默认会破坏 workspace、alias、micro frontend 装载、父工程注册、package-start、构建脚本或已确认平台接线。
- 参考项通过对应 owner gate、validator、typecheck/build/browser/network 证据，且内置默认无法通过或会降低可验证性。
- 参考项只抽取纯 helper、路径常量、类型安全 adapter 或目录协作边界，能减少重复但不隐藏 contract、不改变 runtime behavior。
- 多个健康参考模块一致采用该项，且 quality gate 未命中 anti-pattern；关键区仍需要 owner/user/design-confirmed 证据。

以下情况 AI 不得自判为更优，默认 `merge / follow-baseline`；若会影响关键行为、关键链路或内置硬规则，则写 `block + confirmationNeeded=yes`：

- 只能证明“项目里这样写过”，不能证明质量、优势或运行必要性。
- 只是目录、命名、import 风格、文件分组或局部封装差异，且未证明优于内置规则。
- 涉及 route、DataSet transport、service、mock、permission、wrapper、Provider、i18n、tenantContext、production transport 等关键实现区。
- 参考模块只通过搜索命中、未运行 quality gate，或 quality basis 只是 `scan-only / no-issue-found` 且没有 owner 确认。
- 参考写法与内置硬规则冲突，但无法证明这是目标工程刻意设计或运行约束。

question gate 只处理高价值决策，不得把所有低风险差异都交给用户。命中以下任一条件时，Design / Task 必须输出独立 `questionGateQueue[]` 项，记录 `decision=block`、`confirmationNeeded=yes`，并阻塞 runnable Implementation：

- AI 无法证明参考项是否优于内置规则，但采纳会改变运行行为、目录边界、接口链路、权限链路或 mock/production 数据链路。
- 参考项与内置硬规则冲突，但可能来自目标工程真实约束。
- 关键实现区需要 `owner-confirmed / user-confirmed / design-confirmed` 才能从 `merge` 升级为 `follow-project` 或 `golden-baseline`。
- 采纳参考项会影响后续验证命令、父工程接线、平台配置、权限码、菜单、LOV/lookup、附件、导入导出或 production replacement 范围。

question 输出必须只确认一个问题域，并记录 `questionReason=superiority-uncertain / critical-conflict / owner-confirmation-required / runtime-impact`。若用户不确认或证据仍不足，保持 `merge` 或 `follow-baseline`，不得自动升级为 `follow-project`。

## Anti-pattern Evidence

相似页面出现以下写法时，默认降级为 `legacy-risk` 或 `anti-pattern`，不得作为正向模板：

- `UrlHistoryProvider`、`HistoryProvider`、`ConfigProvider`、自定义 Context Provider 或业务 wrapper 无 UI Contract / 项目证据却包裹整组 HZERO `Header + Content`。
- 为单一 HZERO/C7N 组件新增无来源薄封装、`*Adapter`、`runtimeAdapters`、`buttonProps`、`t()` 等，导致权限、i18n、导入导出、request 或组件 API provenance 被隐藏。
- `PermissionButton || Button`、普通 `Button` fallback、required 权限按钮未通过 `front-hzero-permission-button`。
- required 导入/导出缺 `ImportExportEntryProof`，或入口不是 HZERO 标准组件 / 项目 confirmed wrapper。
- `new DataSet({ ... } as any)`、`columns as any`、`queryBar as any`、`Component as any` 或其它整段 props/API 逃逸。
- 本地数组 options 替代已确认 lookup/value-set/Lov 主数据；或用相似页面字段猜当前 feature 的值集、LOV、bucket、templateCode。
- 缺 `queryMode`，无 requestable mock seed，也无 production transport 证据，却把 DataSet/service 写成可运行链路。
- `loadData`、模块内存数组、service/mock、local-filter 被包装成 mock-request 或 production-ready。
- 父工程托管子模块的 mock plugin 只在子模块内生成，父工程 `config/config.ts` 顶层 `plugins` 未注册子模块 plugin 或聚合 plugin；或缺少默认 package-start 下子模块 `config/config.ts` 的 `extendParentConfig` 继承证据且无不支持证据。
- mock plugin 使用 `require('./<module>-dev-mock')(api.app)`、`api.addBeforeMiddlewares(() => { require(...)(api.app); })`、直接传 middleware、`api.addBeforeMiddlewares(registerMock)` 等非 `submodule-dev-mock-plugin.js.template` 形态。
- mock plugin/handler 缺少模板自检机制，不能证明 middleware 导出函数、`__mockMount` 匹配、重复注册保护和 Umi 扩展点可用性。
- `config/config.ts` 内联完整业务 route array，或把 list/detail/current-tab/openTab/dynamic-tab 路由对象直接写入主配置。
- 有列表 + 详情/新建/编辑子页面时生成同级顶级 route，而不是父 route + `routes` 嵌套；设计或 route config 使用任何 `redirect` route，包括父路由 redirect 到 list、父级 `redirect + routes`、同父级 path redirect 子路由或单独叶子 redirect；普通 `hzero-openTab` 误配 `mode: 'dynamic'`；dynamic-tab 复用普通详情 tab key。
- 用 `?editFlag=true/false`、`?mode=edit/view`、`?action=create`、query/state 或 DataSet `editFlag` 表达页面模式、详情 ID、openTab key/path 或 HZERO Tab 唯一身份。
- 详情、编辑或新建页父组件创建了 `headerDs/detailDs` 等 owner DataSet，但 `HeaderForm/BasicInfoForm/DetailForm` 未接收或 `<Form>` 未绑定 `dataSet/record`；Form 字段只靠同名局部状态、列表 DataSet 或 payload helper 证明，导致详情字段空值。
- 列表、详情、DataSet、mock/API response 或 submit payload 使用近义字段名且无集中 adapter，例如列表 `requisitionNum/applicantDeptName/applyDate`，详情使用 `requisitionNumber/deptName/applyTime`，却没有 Field Usage Matrix / adapterAliasPolicy 对账。
- 详情页漏 required 头字段、基本信息展示字段或编辑字段，例如联系方式、邮箱、驳回/拒绝原因、创建人/更新人显示字段；或把业务主数据编辑字段降级为普通 `TextField/Output` 显示字段。
- 设计或 TDS 要求详情 Tabs、明细页签或行筛选，但实现直接裸渲染明细 Table、关闭 `queryBar`、缺 lineQueryDS/queryFields，或无法按物料类别、金额区间等 required 条件筛选。
- 状态矩阵/API/FDS/TDS 存在详情撤回、取消、作废、删除等业务动作，但相似页面只在 service 中有方法、页面 Header/toolbar 无动作入口或无权限/状态守卫。
- 新建保存后设计要求留在详情并补齐 `headerId/id` 到 URL、Tab key 或 routeContext，但相似页面只刷新 DataSet 或停留在 `/detail/create`。
- 主从/行保存 service path 漏父主键 path segment，或 resourcePath 与 TDS/API 模板不一致，例如应为 `/{headerId}/lines/save` 却实现成 `/headers/lines/save`。

## Decision Values

| decision | 适用条件 | 后续动作 |
| --- | --- | --- |
| `follow-project` | 工程写法更完整、更安全，或经 owner gate 证明比内置规则更适合目标工程运行约束，且不降低门禁 | 沿用该参考项，记录证据路径、优于内置规则的理由和保留的内置门禁 |
| `follow-baseline` | 工程写法缺失关键结构、安全性差或不可验证，标准范式可直接补齐且不破坏项目 | 按标准范式生成或修正 |
| `follow-asset-baseline` | HZEROJS 空项目、参考资产缺失/不可读或无可采纳相似页面，已启用 `hzerojs-asset-baseline` | 按资产基线生成生产形态；继续保留所有未解决 questionGate，不得把 generatedCandidate/unknown 升级为 confirmed |
| `merge` | 工程写法有项目兼容性，或只是项目封装/命名/目录差异且不降低门禁，但未证明优于内置规则 | 保留项目兼容点，同时以内置规则补齐标准门禁 |
| `block` | 无法判断工程写法是否刻意设计，或补齐会影响运行/权限/构建 | 阻塞并写 `confirmationNeeded=yes` |
| `not-applicable` | 当前不涉及目标业务前端工程或对应规则不适用 | 写 reason，不做 comparison 结论扩展 |

## Rubric

| 维度 | 检查问题 | legacy-risk 示例 | 推荐决策 |
| --- | --- | --- | --- |
| 完整性 | 是否覆盖 package、tsconfig、config、routes、父工程注册、页面目录、mock seed、验证命令 | 漏 `tsconfig.json`、漏 `packages-config`、漏 `routes/index.js` | follow-baseline / merge |
| 安全性 | 是否存在 catch-all route、权限绕过、租户硬编码、mock 冒充真实接口、native HTTP 未确认 | `registerRegex='\\/.*'`、硬编码 tenantId、local-filter 冒充 mock-request | follow-baseline / block |
| 可验证性 | 是否能通过 lint/typecheck/build/browser/network 或至少形成候选命令 | 无 package script、无可定位 route、mock 不可请求 | merge / block |
| 工程兼容性 | 标准范式是否会破坏 workspace、alias、runtime、构建脚本或既有封装 | 项目使用自定义 route 聚合/helper，但证据完整 | follow-project / merge |
| UI 一致性 | 是否复用项目组件和 Choerodon/HZERO 标准模式 | 手写查询 Form、自绘 Modal/Drawer/Overlay、div/grid 详情 | follow-baseline / merge |
| 详情区域覆盖 | 是否覆盖 Detail Contract / Design Coverage Ledger 的 Header 字段、Form owner DataSet/record、Tabs、明细筛选、详情动作和保存后 route 主键 | HeaderForm 未绑定 DataSet、required 字段未展示、裸 Table 替代 required Tab、`queryBar=\"none\"`、撤回入口缺失、保存后仍在 create URL | follow-baseline / block |
| 数据链路 | queryMode、transport、response shape、mock/runtime store 是否一致 | service/mock + loadData 冒充 request、PageResponse 直接接错 transport | follow-baseline / block |
| 用户确认 | 冲突是否需要产品/平台/项目 owner 决策 | 不确定是否必须生成 `routes-config.tsx`、不确定 route prefix | block |

## Empty / Missing Reference Fallback

当 `similarPageEvidenceQualityStatus=missing` 的原因是 HZEROJS 空项目、参考资产缺失/不可读、无同类页面或无可采纳子模块时，不得把缺少样板解释为允许 non-compliant 或自由生成。Design 应记录 `assetBaselineStatus=active`、`assetBaselineSource=hzerojs-asset-baseline`、`evidenceQuality=asset-baseline`、`decision=follow-asset-baseline`，并引用 `hzerojs-asset-baseline.md`。

资产基线只补工程形态和最低质量门禁，不补业务事实。`follow-asset-baseline` 不是一个会先完成再进入下一类降级判断的串行阶段，也不是允许跳过后续扫描的短路条件。Design 必须在同一轮 Contract Check 中继续判定并累积以下门禁：Target Placement、Missing Contract、默认 Mock demo 决策、Open Interaction、Import/Export Component Mode、附件 bucket/storageCode、LOV/lookup code、templateCode、tenantContext、servicePrefix、backend readiness 和 Production Replacement。默认 Mock demo 决策本身不进入 questionGateQueue；LOV/lookup code、附件 bucket/storage/template、导入导出 templateCode/endpoint、权限码和 locale key 能形成候选时，不得进入 questionGateQueue，也不得阻塞 runnable demo，必须转为 generatedCandidate/mockOnly/placeholder + Production Replacement，生产结论仍保持 partial/missing。只有字段/value/bind/endpoint 结构无法形成当前 Mock 候选时，未 resolved 才保留 `questionGate.required=true` 或 `questionGateQueue[]` 并阻塞当前 runnable Implementation；production-ready、真实联调或拒绝默认 Mock 的诉求只进入后续 advisory。

## Required Output

`baselineComparison` 至少包含：

| field | 说明 |
| --- | --- |
| area | submodule-structure / route-registerRegex / routes-config / UI-component-pattern / mock-request / production-transport / tenant-context / other |
| projectEvidence | 工程证据路径、相邻页面或用户输入 |
| standardBaselineApplied | true / false；真实业务前端工程 comparison 默认 true |
| evidenceQuality | golden-baseline / project-compatible / asset-baseline / legacy-risk / anti-pattern / unknown-quality |
| goldenBaselineStatus | confirmed / not-confirmed / rejected / conflict / not-applicable |
| baselineConfirmationSource | user-explicit / owner-doc / design-confirmed-from-owner / none / not-applicable |
| baselineConfirmationText | 用户原话、owner 文档路径、设计确认依据或 not-applicable |
| baselineScope | package / page-pattern / route-pattern / DataSet-pattern / wrapper-pattern / other / not-applicable |
| baselineHealthCheck | pass / partial / failed / not-run / not-applicable |
| baselineRule | 对应 reference/template/rule |
| detailRegionCoverage | pass / partial / missing / blocked / not-applicable；真实详情/主从 comparison 默认必须对账 Header 字段、Form 绑定、Tabs、明细筛选、详情动作和保存 route |
| ownerDataSetOrRecordPolicy | confirmed / missing / conflict / not-applicable；详情/编辑/新建 Form 字段必须说明 owner DataSet 或 record 来源 |
| difference | 差异摘要 |
| decision | follow-project / follow-baseline / follow-asset-baseline / merge / block / not-applicable |
| reason | 决策原因 |
| superiorityEvidence | none / runtime-required / validator-proven / owner-confirmed / repeated-healthy-reference / pure-helper-or-directory-boundary；`follow-project` 不得为 none |
| aiDecisionAllowed | yes / no；只有证据可复核且不命中 question gate 时才允许 yes |
| questionReason | superiority-uncertain / critical-conflict / owner-confirmation-required / runtime-impact / not-applicable |
| legacyRisk | yes / no |
| confirmationNeeded | yes / no |

## Blocking Defaults

以下情况默认不得进入 runnable implementation：

- 目标业务前端工程实现却没有 `engineeringExplorationRequired=yes` 和对应 E1/E2/E3 证据。
- 新建/接入子模块缺 E3 evidence 或缺 baselineComparison。
- HZEROJS 空项目、参考资产缺失/不可读或缺可采纳相似页面，但未启用 `hzerojs-asset-baseline`，或启用后把 unresolved questionGate 当成 resolved。
- 工程历史写法存在 catch-all `registerRegex`，并被复制到新子模块。
- 工程历史写法漏父工程注册、路由聚合或 tsconfig，并被当作新建默认骨架。
- local-filter、service/mock 或内存数组被声明为 mock-request。
- 父工程托管子模块 mock-request 缺父工程 `config/config.ts` 顶层 plugin 注册、缺 package-start 子模块 `config/config.ts` 的 `extendParentConfig` 继承证据且无不支持证据，或 mock plugin 命中 `api.app` 直接挂载 / 非模板形态。
- 父工程托管子模块 mock-request 缺 `mockPluginSelfCheck`，或自检结果为 `failed/not-run` 却声明 `mock-completed`、`usable=true`。
- 真实 API production-transport 缺 serviceRequestContract、tenantContext 或 response shape 映射。
- 详情/主从页 comparison 缺 `detailRegionCoverage`，或已发现 required 头字段、Form owner DataSet/record、required Tabs、明细筛选、详情状态动作、保存后 route 主键任一缺口却仍采用相似页面为正向模板。
- 相似页面命中 `legacy-risk` / `anti-pattern`，但未输出 baselineComparison 决策就被复制到新实现。
- 未评级或 unknown-quality 相似页面覆盖了标准 HZERO/Choerodon 规则。
- 无法判断工程约定是否刻意设计，但仍生成真实工程代码。

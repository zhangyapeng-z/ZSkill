# Schema Runtime Gates

用途：承接 `templates/schema-checklist.md` 中运行时门禁的长规则，包括并发一致性、路径放置、Target Placement、mock/runtime、合规汇合和最终状态判定。本文是 runtime gate 事实源，`schema-checklist.md` 只保留检查入口、关键条件和回退动作。

## 阅读路由
- 需要做 task-status / changedFiles / shared-file-locks 一致性检查时读 `Concurrency And Status Gates`。
- 需要判断 Target Placement、Submodule Page Root 或 backfill 是否闭合时读 `Placement Gates`。
- 需要判断 mock/demo、replacement、production compliance 是否可汇合时读 `Runtime And Compliance Gates`。
- 需要判断 `production-ready / conditional / blocked` 最终状态时读 `Merge Status Gates`。

## Concurrency And Status Gates

`schema-checklist.md` 中以下项的细则以本节和 `frontend-concurrency-control.md` 为准：

- `parallel-slices` 与 Task List
- `integrationTaskId`
- `shared-file-locks`
- changedFiles 一致性
- Task Status Update Gate
- changedFiles 来源校验
- Process Artifact Placement
- Review 映射
- Verify 映射
- Handoff 汇总

最低要求：

- 并行 slice、共享文件锁、integration task 和 changedFiles 来源必须互相可追溯。
- 非 Implementation 阶段不得写业务代码。
- 流程记录文件不得落进业务源码目录。
- `task-status.md`、Review、Verify、Handoff 对 changedFiles 和状态台账的结论不能互相冲突。

## Placement Gates

`schema-checklist.md` 中以下项的细则以本节、`frontend-write-scope-control.md`、`hzerojs-submodule-runtime-gate.md` 和前端设计侧 target placement 资产为准：

- Target Placement
- Submodule Page Root
- Target Placement Backfill
- 工程探索等级
- Baseline Comparison
- Similar Page Quality
- Enterprise Page Composition
- No-Reference Default Slices
- No-Reference Master-detail Closure

最低要求：

- 新增/改造页面、子模块和业务 changedFiles 的物理落点必须与确认过的 `targetPlacement` 一致。
- 无参考基线时，默认仍以 `src/pages` 为空项目基线，不能靠 TDS/FDS 或自然语言“确认当前落位”放行 `src/routes`。
- Target Placement 缺资产时，只允许 backfill，不允许继续 runnable Implementation。

## Runtime And Compliance Gates

`schema-checklist.md` 中以下项的细则以本节、`front-hzero-mock-request`、`backend-api-readiness-for-frontend.md`、`hzero-choerodon-production-compliance-gate.md`、`frontend-compliance-manifest.md` 和对应专项 reference 为准：

- Question Gate
- UI Contract
- UI Source Priority
- Figma 429 Persistence
- Frontend ID Runtime Contract
- Field Usage Matrix
- Field Editability
- Field Visibility
- Empty / Derived Field UX
- Action Entry Matrix
- HZERO Page Layout / Scroll
- Component API Provenance
- Enum Provenance
- Generated Code Static Quality Gate
- Frontend Compliance Manifest
- Blocked Placeholder Gate
- Manual Checklist
- Mock Request Gate
- Mock To Production Switch
- Runtime Data Entry Drift
- HZERO Choerodon Production Compliance
- Backend API Readiness
- Readiness Checklist
- Production Replacement Confirm
- Write Scope Confirm
- Service Request Contract
- Tenant Context
- Route Menu Confirm
- Route Open Mode
- Open Interaction
- Route Context / Edit Mode
- Lessons Learned

最低要求：

- 对用户可见的阻塞原因必须收敛到 6 个一级 gate：`question-gate`、`target-and-write-scope`、`contract-readiness`、`validator-required`、`review-blocking`、`verification-failed`。C7N、mock、i18n、submodule、LOV、附件、导入导出等具体 ruleId 只作为上述 gate 的 evidence / validator detail / replacement item，不得各自升级成独立流程阻塞标题。
- `contract-readiness` 只阻塞影响 route/menu、写入落点、真实 API、租户上下文、生产可达、组件可实例化或数据提交安全的核心契约。LOV/lookup、附件、导入导出、权限、i18n、通用组件等只缺业务编码、平台参数、bucket/storage/template、templateCode、lovCode、lookupCode、permissionCode、locale key 或运行验证时，默认生成 `generatedCandidate` / `mockOnly` / `placeholderParameter` 并写入 replacement / handoff risk；不得阻塞 Task / Implementation / Review / Handoff，也不得声明 production-ready。
- 组件级降级只能降级缺失参数或生产闭合状态，不得降级组件形态。required LOV/lookup 不得退化为普通 TextField，required 附件不得退化为普通按钮/静态列表/Upload 空壳，required 导入导出不得退化为普通 Button/request，required 权限动作不得退化为普通 Button。LOV、Attachment、Import/Export 和 HZERO 通用组件的标准坐标默认是内置能力；缺相似页面、缺项目 wrapper 或缺本地样例不构成阻塞。只有目标工程依赖/版本/编译证据明确否定标准组件可导入或可实例化，且没有 confirmed wrapper，或字段/value/bind 形态无法生成候选，或实现会产生 disabled/no-op/local-filter/inline mock 成功路径时，才进入一级 gate 阻塞。
- `verification-failed` 只表示本轮已纳入验证计划且已实际执行的 validator、typecheck、build/compile 失败；页面运行态不属于普通 Verification 执行项，只能来自外部 runtime acceptance 或用户手工证据。未执行、缺依赖、缺运行态目标、默认 mock demo 未要求页面运行态闭合，或只是缺运行态证据时，不得写成 `verification-failed`；只能记录 `not-run / unknown / handoff risk`，并通过 `buildable/reachable/usable` 和 `manualVerificationRequired/frontendServiceNotice` 表达未验证事实。专项测试不是默认阻塞项，只有用户、任务目标或主流程明确要求并实际执行失败时才进入本 gate。
- checklist 不重复展开专项规则，直接引用 owning reference。
- 只要命中 mock/demo、replacement、route/menu confirm、route open mode、tenant context、attachment、import/export、compliance manifest 等专项门禁，就必须由对应 reference 或 manifest 提供证据。
- user-question、replacement、blocked 和 not-applicable 必须有稳定来源，不能用自然语言兜底。
- 新增/改造页面的 routePath、menuPath、routeTitle、routePrefix 或 menuGroup 必须来自用户确认、平台菜单/routeConfig 证据，或 `generated-code-conventions.md` 的唯一候选生成规则。规则候选只能写 `generatedCandidate`，可进入 mock/demo 和候选实现，并必须进入平台菜单/标题 replacement；production confirmed 必须来自用户或平台/routeConfig 证据。候选无法唯一生成、存在多个父路径/父菜单冲突、目标要求 production-ready 或本轮必须完成正式平台菜单挂载时，`questionGate.template=Route Menu Confirm` 且未 resolved，不得进入 Task / Implementation。
- 前端工程、父工程、已有 `packages/<module>` 或新建子模块边界不唯一时，必须使用 `Frontend Project Confirm`；package 内 `businessDomain/pageRoot/pageGroup/pageDir/routePrefix/menuGroup` 不唯一时，必须使用 `Target Placement Confirm`。两者同时适用且候选互不依赖时，必须在 `questionGateQueue[]` 中作为两个独立 gate 保留，并在一次 question 调用中批量展示；只有功能落点候选依赖工程/package 答案时才串行调用。任何把工程/package 边界和 package 内功能落点合并成一个问题或一个答案的阶段结果都按 `questionGateQueue.invalid` 处理，不得进入 Task / Implementation。
- 新增/改造页面的详情打开方式、Tab 行为和相关 route 字段按三态处理：用户/FDS/Figma/PageSchema 明确 current-tab、Drawer、Modal、具体系统页签、记录级页签或浏览器页签时为 `explicit-source`，直接记录 confirmed/sourceRef；普通 `demo-slice / minimum-codable` 的 route-page/list-detail 无冲突且只有内置 current-tab 安全候选时为 `default-safe-current-tab`，写 `routeOpenMode=menu-current generatedCandidate`、`detailViewInteractionMap=current-tab-page resolved-by-policy`，允许进入 Task/Implementation并保留 production replacement；只有多个合理候选、来源冲突、production-ready 行为冻结或含糊“新标签页”时为 `ambiguous-or-conflict`，必须使用 `Open Interaction Confirm`。Question 候选仍按输入来源过滤：无弹层证据不得展示 Drawer/Modal；弹层候选最多一个 `抽屉打开`；明确 Modal 直接记录 Modal Contract。current-tab 固定使用 `/create`、`/detail/view/:id`、`/detail/edit/:id`，不得生成 `/<feature>/edit/:id`、`/detail/create` 或 query pageMode。
- 当前 FDS/用户输入写明“点击跳转至新建页面 / 点击跳转至编辑页面 / 跳转至对应数据的编辑页面 / 跳转到详情页面”时，先识别为 route-page 页面跳转语义；普通 demo 无其它 Tab 语义或冲突时可按 `default-safe-current-tab` 自动闭合。参考子模块、相似页面、工程 evidence、routeConfig 或 `openTab`/`mode: dynamic` 只作为内部实现候选，不能把默认 current-tab 自动升级为独立/动态页签，也不能关闭真正的 `ambiguous-new-tab` question。同类参考模块存在可采纳且覆盖当前 question 全部入口的 Drawer 证据时，可额外生成唯一一个 `抽屉打开` 候选；Modal/弹窗仍不得由参考模块生成选项。
- Open Interaction 的路由/页签类选项默认全部展示：`当前菜单页签内打开`、`新开一个系统页签`、`每条记录新开独立系统页签`、`浏览器新标签页`。不得因为当前资料暂缺记录 id、业务单据 id、业务标题、`dws/queryStateKey` 或同 route 多实例证据而隐藏 `每条记录新开独立系统页签`；缺口写入选项描述和记录要求，选择后先保持 `generatedCandidate/needs-confirmation`，补齐后才可 confirmed。其它选项如存在特殊要求、适用例外或后续确认要求，也必须写进对应选项描述；缺失时按 `missing-option-description` 或 `hidden-special-requirement` 处理。
- Open Interaction question 调用前增加 payload runtime gate：`questionGateQueue[]` 必须携带 Design 生成的完整 `questionToolPayload`，consumer 只能原样转发。`ambiguous-new-tab` 必须满足 `optionSetSource=builtin-open-interaction-template`、固定三个新标签页业务选项，以及 `allowFdsChange=true` 时的当前菜单页签变更选项。无参考 Drawer 候选时 `referenceEvidenceInfluence=none`；有可采纳参考 Drawer 候选时必须是 `drawer-option-only`，并同时具备 `overlayEvidence=reference-drawer`、覆盖全部入口的 `referenceDrawerEvidence` 和 `drawerOptionChangesFds=true`。缺 payload、选项集合漂移、技术术语泄漏、Drawer 证据不足或 consumer 重写时，写 `openInteractionPayloadValidation=failed`、`reason=missing-payload/reference-evidence-leak/technical-term-leak/option-set-drift/reference-drawer-evidence-invalid`；`parallelGroupStarted=false` 时留在同一 Design closeout 修正，`parallelGroupStarted=true` 时判定 `parallel-baseline-invalidated`，禁止调用 question 或回普通 Design。
- `Route Menu Confirm` 与 `Open Interaction Confirm` 同时适用且候选互不依赖时，必须在 `questionGateQueue[]` 中作为两个独立 gate 保留，并在一次 question 调用中批量展示；只有打开方式候选依赖 route/menu 答案时才串行调用。`Route Menu Confirm` 不得关闭 `routeOpenMode/detailViewInteractionMap`；`Open Interaction Confirm` 不得关闭 `routePath/menuPath/routeTitle/routePrefix/menuGroup`。任何把路径菜单和详情打开方式合并成一个问题或一个答案的阶段结果都按 `questionGateQueue.invalid` 处理，不得进入 Task / Implementation。

## Merge Status Gates

`schema-checklist.md` 中最终 `handoffStatus` 的主决策值为 `production-ready / conditional / blocked`。输入出现其它交付状态时按 `invalid-stage-result` 返回原 owning stage，不做状态映射；mock/demo 是否已证明可演示必须读取 `deliveryTarget`、`mock.queryMode`、`verification.buildable`、`verification.reachable`、`verification.usable`、`manualVerificationRequired` 和 `frontendServiceNotice`。

状态判定顺序固定为：先处理同一前端子流程可补齐的内部阶段证据和自动修复链，再判断是否可 `conditional`，最后才判断最终 `blocked`。已进入阶段的 required Review / Verification / Handoff evidence、validator result contract、repairDispatch、task-status、Compliance Manifest、replacement checklist 或 owning-agent trace 缺失，属于 invalid early return / premature handoff，不是合法最终交付状态。默认 `demo-slice` 的外部 browser/runtime/Network evidence 缺失、`reachable/usable=unknown`、`manualVerificationRequired=true`、后端 readiness partial/missing、production replacement pending、production-only 参数待登记和可选 validator `not-applicable/not-run + reason` 均优先进入 `conditional`。只有重新诊断命中 Terminal Block Whitelist，证明当前可运行路径、安全或核心契约无法闭合，才允许最终 `blocked`；repair budget 和 timebox 不是判定条件。

Required owning-agent evidence 是进入状态判定前的硬前提。页面交付、`demo-slice`、存在 Feature Root 或需要状态回写的 `regular-change` 中，Task / Implementation / Review / Verification / Handoff 任一已进入阶段都必须有对应 owning agent 的真实调用、非空结果、canonical artifact 或结构化 blocker。`frontend-task-agent` 空返回、Task artifacts 缺失、Review/Verification/Handoff 只有 primary 自查、或 required artifact 由 primary self-direct 补写，均判为 `invalid-stage-self-direct` / `invalid-task-empty-return`；这类问题不允许直接转成 `conditional` 或最终 `blocked`，必须先回同一前端子流程的 owning stage 补真实结果。`direct-no-task` 只豁免小范围、无 Feature Root、无共享契约、无状态回写的 `regular-change` Task artifact，不豁免已进入 Review / Verification / Handoff 的 owning-agent 证据。`repair-fast-lane` 不属于 direct-no-task：它允许复用已有 Feature Root 的 Task artifact 而不重新进入 TASK，但当前 `frontendAutoRunId` 必须真实调用 Implementation、Review 和 Verification owner，`flowControl` 必须证明 targetFilesPreflight、最多 2 个既有文件、无共享锁、无新风险域和全部 contract delta=false，Verification 只运行 V0/V1；满足后才可 `flowCutoff=after-verification`。不得进入 Task / Final Review / Artifact，也不得声明 Handoff ready / production-ready / DONE；历史同名顶层字段不做兼容读取。

### production-ready

至少同时满足：

- question gate 已闭合
- `contractStatus=ready`
- `reviewResult=pass`
- `verification.buildable/reachable/usable=true`
- `writeScopeAudit=pass/not-applicable`
- targetPlacement、baselineComparison 和关键 contract 字段已闭合
- `productionCompliance.complianceState=production-compliant`
- `productionCompliance.manifest` 全部适用 gate 为 `pass/not-applicable`
- `blockers=[]`
- replacement 已 closed 或 not-applicable

### mock/demo verification facts

mock/demo 路径是否“可演示”不再映射为独立最终状态，至少由以下事实判断：

- question gate 已闭合
- 默认 mock/demo 决策和 mock 接线状态明确
- `reviewResult=pass`
- `verification.buildable/reachable/usable=true`
- replacement checklist required-ready
- `done=false`
- 若 `mock.queryMode=mock-request`，则 mock gate 已闭合
- 命中 HZERO + Choerodon 门禁时，`productionCompliance.manifest` 不存在 failed/blocked gate

### conditional

允许存在 mock/demo 或常规交付目标，但 build、reachable 或 usable 证据未全部闭合；Handoff 必须记录未验证项、`manualVerificationRequired`、`frontendServiceNotice`、下一步和 `done=false`。仅因目标前端工程未安装依赖导致依赖型验证 `not-run + blocked-by-missing-dependencies` 时，使用 `verification.environmentNotice` 记录环境前置；默认 `demo-slice` / mock demo 仅缺外部页面运行态证据且用户未要求 production-ready 或完整验收时，不触发用户确认，直接以 `conditional` 汇总并提示用户手动启动前端服务自测。两者都不得写 DONE 或 production-ready。

`conditional` 不是失败态，也不是关闭态。它可以表达：mock/demo 已生成但页面运行态未验证、目标工程依赖或 workspace resolver 证据未闭合、production replacement pending、production-only 平台资产待登记，或后端代码完成但运行环境尚未验证。`conditional` 必须 `done=false`。Lite 汇合读取到 `contracts.backendApiReadiness.status=closed + implementationStatus=completed + runtimeAvailability=verified` 且 `mock.queryMode=mock-request/partial/unknown` 或 `contracts.productionReplacementTrigger=pending/triggered` 时，按 Mock demo 正常汇合并允许继续 FSS / 通用资产；记录 `ready-for-independent-integration`、明确 nextStage 和 production replacement advisory，不得调度 replacement / cleanup slice、恢复同一 `frontendAutoRunId` 或设置 Mock 开关。仅 `implementationStatus=completed + runtimeAvailability=unknown/not-run` 时保持 Mock 并记录 `implementation-complete-runtime-unverified + waiting-backend-integration`；两种状态都不得触发真实 transport。

### blocked

出现以下任一项时成立：

- 阻塞 finding 未关闭，且重新诊断已命中 Terminal Block Whitelist
- 已实际执行的验证失败，且自动修复已止损、需要用户决策或存在外层 gate
- 影响当前可运行路径、安全或数据提交的核心契约缺失，且需要外层决策
- 关键目标路径本身缺失或冲突，无法通过补 reason 或内部证据链闭合
- `task-status.md` 与实际状态因 dirty/conflict、越界写入或状态源冲突而无法在同一前端子流程调和
- 无 runnable 目标；此时必须写 `progressionDecision.blockedReason=non-runnable-target`

仅缺 required 内部结果字段、artifact path、trace、状态回写或汇总一致性时，不满足上述 `blocked` 条件；这是 invalid early return，必须先在同一前端子流程修正。仅缺外部运行态证据、依赖环境、production-only 平台参数或待替换项时也不满足上述 `blocked` 条件，按 `conditional` 处理。

### Invalid Stage Result

`code-only`、legacy demo label 和顶层 `non-runnable` 均不是合法汇合目标。命中时必须写 `invalid-stage-result` 并回原 owning stage 重新生成 canonical 结果；不得映射为 `blocked / conditional` 后继续下游。

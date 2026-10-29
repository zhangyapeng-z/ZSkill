# 前端交付复盘与资产补强规则

用于在人工测试、Review 或用户反馈证明“实现和设计/任务没有完全对齐”时，反向补强公共规则资产、设计模板、任务模板和实现规则。

## 阅读路由

- 手测、Review 或用户反馈暴露实现与设计/任务不一致时，读 `触发条件`、`复盘输出必须回答` 和 `设计和任务补强要求`。
- 页面区域、DataSet-first、未验证表述等复盘共性问题，读对应同名章节。
- 调查前端编排耗时、设计续跑、自动返工、空返回、fix package 目标文件错位或 mock-request 路径遗漏时，只读 `耗时与返工防护`。

## 触发条件
- 页面区域缺失：查询区、工具栏、操作列、Header、详情主表、明细表、附件区等任一实现遗漏。
- 设计文档与实现/用户反馈冲突，例如设计写了无证据的摘要区、额外卡片或页面说明。
- 任务验收过粗，只写“操作列齐全”“表格齐全”，未在 `Contract Acceptance`、`UI Acceptance`、`Verification Acceptance` 中逐项列按钮、筛选、编辑态、权限和查询模式。
- 代码能生成但不能用，例如组件 props 不属于该组件标准能力、DataSet 查询链路未闭合、刷新后状态丢失。
- Review 文档多次漂移，说明 blocker 细节被多份文档重复维护。

## 复盘输出必须回答
1. 设计本身有没有问题：是否存在无 Figma/PageSchema/业务证据支撑的区域或遗漏的交互。
2. 任务拆分有没有问题：`Contract Acceptance`、`UI Acceptance`、`Verification Acceptance` 是否能逐项验证页面区域、按钮、权限、DataSet/query、编辑态。
3. 代码不可用的直接原因：组件 API 用错、状态源不稳定、mock/request 边界不清、页面区域漏实现等。
4. 补强落点：记录公共规则或模板缺口，避免同类问题再次发生。

## 单一事实源原则
- blocker 细节、changedFiles 和残余风险只能有一个主记录。
- Review、task-status、handoff 文档只引用 blockerId，不重复改写 blocker 名称和 changedFiles 明细。
- 若发现文档漂移，优先补规则，减少重复维护，而不是继续在多份文档中同步长描述。

## 页面区域 checklist
新增企业页面或主从页面的设计和任务必须逐项列出以下区域，不得只写“页面齐全”：

### 列表页
- 查询区：字段逐项列出。
- 页面工具栏：新建、导出、批量动作等逐项列出。
- 表格列：主字段、状态字段、金额/日期字段逐项列出。
- 行操作列：详情、编辑、提交、撤回、取消、删除等逐项列出。
- 权限：查看、编辑、保存、删除、导出等动作必须拆独立 candidate/confirmed 权限；不得用详情权限代替编辑权限。

### 详情/主从页
- 页面 Header / 页面级按钮区。
- 基本信息 Form。
- 附件/上传/占位区；缺协议时只能占位并进入替换清单。
- 明细表上方筛选区。
- 明细表工具栏按钮区：新建、保存、删除、导出等逐项列出。
- 明细表行操作列：编辑、删除等逐项列出；默认是否编辑态必须明确。
- 编辑态来源：URL、状态守卫、用户动作三者的优先级必须冻结。

## Choerodon DataSet-first 强制规则
- Table 的查询关系应由 DataSet 建模：`queryFields` 或主 DataSet 的 `queryDataSet`。
- 不得把 `queryDataSet` 当作 Table 层业务查询 props 使用。
- 不得用 Table 层 `onQuery/onReset` 兜 DataSet 查询主链路；若项目组件确有自定义扩展，必须给出本项目证据。
- Table 层只负责渲染入口，例如 `dataSet`、`queryBar`、`buttons`、`columns`、`editMode` 等项目已确认 props。
- mock/demo 若发现 `loadData/local-filter`、`src/utils/mock.ts`、模块内存数组或组件内 seed/filter，必须标记为 blocking cleanup/rework，不得作为新生成目标、降级分支或待替换保留项；若用户要求“走 mock request”，应建 DataSet transport mock 或项目可访问 mock API。

## 设计和任务补强要求
- 技术设计必须显式写出“不实现”的区域，尤其是 Figma/PageSchema 未确认的摘要区、统计卡片、附件上传等。
- 任务验收必须拆为 `Contract Acceptance`、`UI Acceptance`、`Verification Acceptance`，且能人工逐项打勾；不能只写“操作区齐全”“行表齐全”。
- Review 发现实现遗漏时，应同时判断设计/任务是否也有缺陷；若有，必须记录公共模板或 reference 的补强项。

## 未验证表述
- 未运行 build/browser 时，只能写 `not-run`、`unknown` 或 `未证明 runnable`。
- 人工查看代码只能证明“静态代码层面存在/不存在”，不能证明页面可见或交互可用。

## 耗时与返工防护

复盘发现耗时异常通常不是单一实现复杂，而是设计确认往返、子 agent 空返回、修复包目标文件错位、validator 固定路径未前置进入任务，或并发 slice 后集成证据不足。后续前端流程必须把这些情况作为可观测门禁处理。

### 全链路优化优先级

| 优先级 | 优化项 | 执行口径 |
| --- | --- | --- |
| P0 | Design Input Preflight | 先判定 standardPageProfile、落位、queryMode、打开方式、导入导出模式、fieldMatrixSource 和 replacement profile；能标准承接的直接写 autoResolution |
| P0 | targetFiles preflight | Review 修复包生成、primary repairDispatch 和 Implementation 写码前三处一致检查 targetFiles |
| P0 | narrow fix 空转止损 | 小修复 5 分钟无 patch/验证/blocker 即重派更窄任务或止损 |
| P0 | integrationContractSmoke | 并发 slice 后由 integration task 输出消费证明、shared drift 和孤立产物，不让 Review 承担完整集成追踪 |
| P1 | Review targeted budget | targeted-blocking 默认 15 分钟，超时输出 cost anomaly、已确认 findings 和未覆盖项 |
| P1 | mock-request path precheck | Task Breakdown 前置 dev-mock、servicePrefix、父工程 plugin、package-start 和 validator target |
| P1 | Design standard profile | HZEROJS 子模块 + 主从 + mock-request + 导入导出/附件使用标准骨架和 replacement draft |
| P2 | validator 化 known blockers | 使用 `validate_frontend_integration_contract_smoke.py` 将孤立组件、导入导出/附件未消费、状态码/权限码漂移等稳定问题沉淀为静态 validator |

### Design 耗时防护

- Frontend Design 必须先输出 `designInputPreflight`，再展开完整字段、按钮、路由、附件、导入导出和 replacement 矩阵；缺本节时不得进入 Task Breakdown。
- 命中 `standardPageProfile=HZEROJS_SUBMODULE_MASTER_DETAIL_MOCK_REQUEST` 时，默认使用 HZEROJS 子模块、mock-request、主从页面、标准附件、标准导入导出和 production replacement 草案骨架；不得重新从空白模板推导每个章节。
- `minimum-codable + default-mock-demo` 下，导入/导出默认 `designAutoResolution=standard-import-export-direct`，参数缺口写 generatedCandidate / replacement；只有 production-complete、项目 wrapper/custom 外壳冲突、用户拒绝标准入口或参数结构无法形成候选时才提问。
- `routeOpenMode/detailViewInteractionMap` 不做无证据默认。用户、FDS/TDS/需求明确语义或明确 Drawer/Modal/弹层证据可关闭；其它情况合并到一个 Open Interaction question，不得对每个入口零散提问。未明确弹层时不得把 Drawer/Modal/弹窗/抽屉加入选项；普通 route / 编辑页 / 详情页的当前页候选必须写 `当前菜单页签内打开` 并使用 `/create`、`/detail/view/:id`、`/detail/edit/:id` 内置 route 模板。
- MDS/API 可解析字段应先生成字段矩阵骨架，并标记 `fieldMatrixDerivationStatus=generated-from-MDS-API / mixed / manual / missing`；missing 阻塞 runnable design，mixed/manual 必须说明人工补充范围。
- production replacement 草案默认使用 `productionReplacementDraftProfile=standard-mock-demo`；只列本轮命中的 route/menu、API、permission、LOV、attachment、import/export、mock-store 等替换项，不展开无关生产验收长清单。

### 子 agent 空转超时

- narrow fix / mechanical fix / validator evidence fix 等小修复任务，调度输入必须写明 `narrowFix=true`、`maxTargetFiles`、`sourceResultPath`、`targetFiles`、`completionCriteria` 和 `internalRepairReturnRequired=true`；空返回或不可信结果只回 primary 重建 owner input，不生成 terminal blocked。
- 小修复只允许读取 source result、task-status / task-breakdown 摘要和 `targetFiles` 对应文件；额外探索必须有 `deltaExploreReason`，否则返回 `internal-repair-required + reason=blocked-by-narrow-fix-scope`，由 primary 在同一 run 重建更窄输入、补 backfill 或重诊断。
- 子 agent 完成读取定位后，若 5 分钟 wall time 内没有产生 `apply_patch`、验证命令、`task-status-updates` proposal 或结构化 `blocked` 结果，primary 必须把该调用标记为 `subagent-stalled-or-empty-return`，停止等待并在同一会话重新派发更窄任务或形成 internal checkpoint；不得直接返回外层阻塞，除非 session/transport 不可恢复或重新诊断命中 Terminal Block Whitelist。
- `agentDispatchTrace.telemetry` 应记录 `agentDurationMs`、`firstActionLatencyMs`、`toolCallCount`、`patchCount`、`validationCommandCount`、`outputChars` 和 `stallStatus`。数值采集不到时省略该数值，并在成本报告写 `costGovernanceStatus=unverified + reason`；不得用字符串占位，也不得把空返回包装成 completed。
- 任一阶段 `agentDurationMs > 600000` 且 `patchCount <= 1`，或 `firstActionLatencyMs > 300000` 且无结构化 blocker，必须在阶段结果中写 `costAnomaly=low-output-long-wall-time`，并进入 targeted retry / stop-loss 判断。

### Review 耗时分账与扫描预算

- Review 父级调度耗时必须拆成 `queueWaitMs / owningReviewMs / reportWriteMs / fixPackageBuildMs / fixPackageHandoffMs / implementationFixMs / recheckMs`，不得只用父级 wall time 评价 `frontend-review-agent` 本身。
- 前置 Review 默认 `reviewMode=targeted-blocking`，只扫描 changedFiles、touched task、required acceptance、mock/request、route/permission、DataSet/service 和适用 validator；不得因为首次 Review 就自动全量读完整设计、完整任务、全部源码和 Handoff。
- 并发 slice 后的页面组合入口和共享合同漂移必须由串行 integration task 先输出 `integrationContractSmoke`。存在 smoke manifest / validator 结果时，Review 优先使用 `reviewMode=integration-contract-review`，只复核该证据、scope fingerprint 和抽查 changedFiles；若缺 `consumerProof`、存在 `unconsumedArtifacts` 或 `sharedContractDrift`，直接回 integration task，不得在 Review 内扩大成完整集成追踪。validator 已通过且 scope fingerprint 匹配时，Review 不重复执行同一批静态扫描。
- `targeted-blocking` 超过 15 分钟、读取无关文件超过 8 个、或 `readOutputChars` 明显大于 changedFiles/acceptance 所需范围时，必须写 `reviewCostAnomaly=targeted-review-over-budget`，并把后续动作收敛为 findings-first + fix package / backfill package。
- `full-scan` 只能由明确失效原因触发：`changed-files-expanded`、`contract-changed`、`task-mapping-changed`、`new-risk-domain`、`source-review-missing`、`user-requested-full-review`。缺失效原因时必须降级为 `integration-contract-review`、`targeted-blocking`、`fix-package-recheck` 或 `reuse-existing-review`。
- `fix-package-recheck` 必须按 `rootCause.riskDomains` 和修复包的 `affectedStaticGateScan.rulesChecked/rulesHit` 收敛，只检查原 finding、targetFiles/changedFiles、completionCriteria、风险域相关静态规则和是否出现新风险域；不得固定重扫附件、导入导出、i18n、renderer、row-actions 或完整页面区域。
- Review 报告落盘和 task-status 回写应使用 blockerId / findingId 引用，不复制长 finding 正文到多处；写报告超过 5 分钟时，应先输出结构化 findings 和修复包，再做简版落盘。
- Review 生成修复包后，父级应立即切到 Implementation；不得在 Review 父级继续等待修复执行或复查完成。修复包执行、复查和 Review 本体必须分别记时。

### recommendedFixPackage targetFiles 预检

Review 生成自动修复包前、primary 创建 `repairDispatch` 前、Implementation 写代码前，都必须执行同一套 targetFiles preflight：

| 检查项 | 通过条件 | 失败动作 |
| --- | --- | --- |
| existsOrCreateAllowed | 每个 `targetFiles` 已存在，或在 Task File Mapping / changedFilesPlan 中标为本轮允许新建 | 不得进入 Implementation；回 Review 修正修复包或回 Task Breakdown 补写入范围 |
| inWriteScope | 文件位于当前 feature/page/package 的允许写入范围，且不是只读参考、锁定共享文件或目标工程外路径 | 输出 `progressionDecision.backfillPackage.targetStage=TASK_BREAKDOWN` 或 Write Scope Confirm |
| matchesPlacement | 文件路径与 Target Placement / `packageDir` / `pageRoot` 一致；不得指向旧目录、历史 `src/routes/**` 或已被 File Mapping 禁写的父工程业务路径 | 修复包 `autoFixEligible=false`，回 Task Breakdown 修正 targetFiles |
| enoughForRootCause | `targetFiles` 能覆盖 `rootCause.affectedFiles`、可定位缺口和 completionCriteria；不会要求 Implementation 自行发现其它文件 | `targetFilesEnough=false`，不得自动返工 |
| noNewRiskDomain | 不新增 route/DataSet/service/权限/i18n/附件/导入导出能力，不扩大 changedFiles，不改变 Design/Task/Contract | 改写为 backfill / 用户确认，不进入自动修复 |

预检通过时，必须在 Review 报告和 repairDispatch 中写：

```text
targetFilesPreflight:
  status: pass
  checkedFiles: []
  writeScopeSource: File Mapping / changedFilesPlan / direct-no-task
  placementSource: Target Placement Contract / packageDir / pageRoot
  rejectedFiles: []
```

预检失败时，不得调度 `frontend-implementation-agent`；fallback 模式也不得调度 `frontend-general-agent -> frontend-implementation-agent`。必须写 `targetFilesPreflight.status=failed`、`rejectedFiles[]`、`failureReason` 和 `requiredBackfill`。

### mock-request 路径合同预检

Task Breakdown 阶段一旦 `queryMode=mock-request`、`runtimeDataPathDecision=requestable-demo-mock`、默认 mock demo 或任务包含 mock handler/plugin、servicePrefix、DataSet/service mock request，必须先做 `mockRequestPathContractPrecheck`，再放行 Implementation。

必查路径：

| 路径/文件 | 任务要求 |
| --- | --- |
| `packages/<module>/dev-mock/**` | 子模块 mock handler/plugin 必须进入 File Mapping、changedFilesPlan 和 validator target；不得落到业务 `src/**/mock` 或旧 `mock/` 目录 |
| `packages/<module>/src/utils/servicePrefix.ts` | 当 service/DataSet 需要统一 mock / production prefix 时必须进入 File Mapping；不需要时写 `not-applicable + reason` |
| 父工程 `config/config.ts` 或确认的聚合 plugin 文件 | 父工程托管 mock-request 必须有顶层 plugin 注册/聚合任务和源码验证点 |
| 子模块 `config/config.ts` | package-start 默认必须通过 `extendParentConfig` 继承父工程 mock plugin；不适用必须有项目证据 |
| mock validator target | `FE-VALIDATE-MOCK` 的 `validatorTarget` 必须指向 `<frontend-root>/packages/<package>`，并带 `--root <frontend-root> --package-dir packages/<package>` |

缺任一路径映射时，Execution gate 必须 failed，`Can Enter Implementation=no + mock-request-path-contract-missing`。Task agent 应在当前 closeout 自动补齐；补不齐才回 Design / Task backfill，不得先进入 Implementation 后迁移路径。

### integration contract smoke validator

并发 slice、shared-first lane 或串行 integration task 完成后，如已生成 `integrationContractSmoke` manifest，应运行：

```bash
${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_integration_contract_smoke.py --root <frontend-root-or-packageDir> --manifest <integration-contract-smoke.json>
```

该 validator 覆盖三类稳定 Review finding：

| 检查域 | 机械校验 | 失败动作 |
| --- | --- | --- |
| required artifact consumption | `requiredArtifacts[].file` 必须存在，并被声明的 `consumers[].file` import 且在 JSX / action wiring 中实际使用 | 回 integration task 补页面接线或修正 manifest；不得进入 Review |
| required capability entry | `capabilityEntries[]` 中 required 的 `import/export/attachment/lineTable/lineExport` 等能力必须在 consumer surface 命中正向入口 token | 回 Implementation / integration task 补入口；不得以组件文件存在当作已完成 |
| shared contract drift | `sharedContractFreeze` 中声明的状态码、权限码必须覆盖扫描文件内匹配 pattern 的 literal | 回 Design / Task 更新并重新冻结 shared contract，或删除漂移 literal |

命中 `hzero_integration_artifact_unconsumed`、`hzero_integration_capability_entry_missing`、`hzero_integration_status_code_drift` 或 `hzero_integration_permission_code_drift` 时，Review 应优先生成 integration finding / backfill package，而不是扩大为全量追踪扫描。

### Review finding 分级返工

Review finding 必须分成三类并决定返工口径：

| 类型 | 例子 | 处理 |
| --- | --- | --- |
| mechanical | 缺 `Modal.confirm`、缺 loading guard、locale key 漏登记、validator evidence 字段漏填、task-status 文案一致性 | 允许 narrow fix；必须带 targetFiles preflight |
| behavioral | 保存链路丢数据、详情/列表状态不同源、明细持久化不闭合、mock request 读写不同源 | 合并 fix package，按 `fix-package-recheck` 复查 |
| contract | API shape、路由权限、附件/导入导出生产参数、Target Placement 或 UI Contract 缺失 | 不生成 recommendedFixPackage；回 Design / Task / Contract / 用户确认 |

同一 `repairPlanFingerprint` 只允许一次 targeted repair 和一次窄复查。复查仍失败时返回 root-cause refinement checkpoint，保留稳定 `repairAttemptKey`、递增 `repairDiagnosisRevision` 并生成新 fingerprint 后继续；不得启动完整 Review 判断“能不能再修”，也不得用无诊断变化的 Implementation 原样探索。repair budget/timebox 不得形成 terminal blocker。

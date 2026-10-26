# 转换评估参考

## 目标
每次 Figma/设计稿转企业前端页面后，用统一清单评估转换质量，避免输出看似完整但事实不足或难以演进的代码。

## 设计读取检查
- 是否记录原始 Figma URL、`fileKey` 和标准化 `nodeId`。
- 是否记录 Framelink `get_figma_data` 是否成功、输入是 JSON、Framelink JSON wrapper 还是 YAML-like、是否使用具体 selection link。
- 是否按需调用或评估 `download_figma_images`，并记录图片/SVG 下载状态。
- 是否说明读取成功、失败或降级原因。
- 是否区分 Figma、截图、PRD、用户输入和项目源码证据。
- 是否没有根据页面名称臆造精确布局。

## PageSchema 检查
- `source` 是否包含 `mcpTool`、`selectionUrl`、`rawInputFormat`、`rootNodeName`、`imageRefs`、`styleEvidence` 和 `componentEvidence`（适用时）。
- 是否识别页面类型：list / form / formWithTable / detail / masterDetail / treeList / dashboard / uploadImport / componentShowcase / unknown。
- 是否识别主要区块：header、tabs、card、form、filterBar、toolbar、table、modal、drawer。
- 是否把字段、列、操作标记为 confirmed / inferred / missing。
- 是否忽略无意义 Figma 包裹层和 auto layout 噪音。
- 是否没有把 Figma 层级树直接当成前端 DOM 树。

## 占位文案检查
- `Label` 不得当作真实字段 label 或字段名。
- `Button` 不得当作最终按钮文案或权限动作。
- `Table title` 不得当作真实列名。
- `Table text` 不得当作 mock data 写入业务代码。
- `Please enter` 只能作为输入框候选 placeholder 证据。

## 组件映射检查
- 是否先查项目自定义组件，再降级到 HZERO 或 Choerodon。
- 是否确认自定义组件 import、props、事件和数据源后才生成调用代码。
- HZERO 页面是否先确认容器、路由、菜单权限、i18n 和 service/model 边界。
- Choerodon 页面是否 DataSet-first，并明确 Form/Table/queryFields/filterBar 边界。
- 表格是否从 Figma 纵向列 frame 转置为前端 columns。

## UI Contract seeds 检查
- 是否输出 UI 设计回读表，逐项标明列表、筛选、按钮、详情区块、字段顺序和交互入口来自 Figma/PageSchema 哪个区域。
- 是否为列表页输出 `DataSet + Table + filterBar` seed 和 enumProvenance；关键字/模糊搜索是否输出 `fuzzyQuery` 候选。
- 是否输出 QueryFields Schema 候选：组件类型、是否多选、是否允许清空、默认展示字段和 `queryFieldsLimit` 候选。
- 是否输出表格字段顺序和操作列 seed；行操作列是否要求最后一列且 `ColumnLock.right`，并禁止 `lock=true` / `lock: 'right'`。普通业务列不得因该操作列规则被强制固定，只有设计或项目基线明确要求时才输出固定列 seed。
- 是否输出详情只读 `Form + Output` seed；数组详情区块是否输出 Table seed；是否禁止无依据摘要头和 `div/grid` 详情。
- 是否输出 Modal / Drawer / Popover / Dropdown 等 overlay 的 mask、z-index、portal、不透明背景和关闭后无遮挡 seed；是否把层级穿透标为 blocking 风险。
- 是否输出 HZERO route/menu/PermissionButton/i18n/platform 能力边界，并保持未确认项为 `generatedCandidate`、`inferred` 或 `missing`。
- 若涉及 demo，是否输出 `mock-request` seed，且没有把 `service/mock + loadData` 伪装成 mock-request。

## 事实边界检查
- 是否没有编造接口 URL、HTTP method、参数、响应结构。
- 是否没有编造 route path、menu code、permission code。
- 是否没有编造 `lovCode`、`lookupCode`、bucket、templateCode。
- 是否没有编造组件 props、events、默认值。
- 缺失事实是否进入待确认项，而不是 runnable-looking 占位代码。

## 代码生成检查
- 是否只生成证据足够的代码。
- 缺接口时是否只生成 PageSchema、UI Contract seeds、组件映射说明和待确认清单。
- 是否最小化改动并匹配项目既有风格。
- 是否避免绝对定位复刻 Figma。
- 是否定义桌面和移动端的基础响应式行为。
- 是否禁止手写查询 Form、自绘 Drawer/Modal、`div/grid` 详情、行操作列 `lock=true` 和 local-filter 伪装 mock-request 进入下游实现建议。

## 验证检查
- 是否先发现项目已有 scripts 和执行目录。
- 是否运行可行的 lint、typecheck/tsc、test、build。
- 是否按 `references/visual-verification.md` 记录视觉基准、实现截图、可接受差异和未验证差异。
- 未运行验证时是否说明原因。
- 是否区分工具验证结果、大模型静态审查和未验证项。

## 样例沉淀策略
- 只沉淀实际读取过的 Figma 样例。
- 每个样例必须记录 `fileKey`、`nodeId`、Framelink 输入格式（JSON / Framelink JSON wrapper / YAML-like）、可确认事实、不可确认事实和 PageSchema 摘要。
- 不为覆盖场景而编造“列表页、详情页、上传页”等样例。
- 后续真实样例优先补充：纯查询列表页、新增/编辑弹窗页、详情页、主从表页、上传/附件页。

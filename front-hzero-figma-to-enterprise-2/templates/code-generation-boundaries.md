# 代码生成边界模板

## 使用前提
1. 已读取 Figma 或设计证据。
2. 已形成 PageSchema。
3. 已区分 confirmed / inferred / missing。
4. 已确认或标记目标技术栈：custom / HZERO / Choerodon / HZERO + Choerodon。
5. 已输出 UI 设计回读表和 UI Contract seeds；未输出时只能停留在 PageSchema / 映射分析，不进入实现建议。

## 路线 A：HZERO 页面映射方案

适用场景：
1. 页面属于 HZEROJS 工程。
2. 需要路由、菜单权限、i18n、Permission、service/model 或 HZERO 页面容器。
3. Figma 提供的是页面视觉结构，业务协议尚未全部确认。

可生成：
1. 页面容器映射：Header/Content/PageHeaderWrapper 或项目已确认容器。
2. 页面区域结构：header、tabs、card、form、filterBar、table。
3. 静态标题和临时文案清单，待接 i18n。
4. 权限按钮结构，但不生成未确认权限码。
5. service/model 文件位置建议，但不生成未确认接口请求。
6. `componentShowcase` 只能生成 HZERO/项目封装组件映射表或组件文档说明，不生成业务 route/service/model。
7. UI Contract seeds：页面容器、route/menu、permission、i18n、platform 能力和 Choerodon 内容区责任分界。

不可生成：
1. 未确认 route path、菜单编码、权限码的可运行实现；设计文档中可以按规则输出 `generatedCandidate`，但必须标明来源、状态和确认人。
2. 未确认 service URL、HTTP method、参数和响应结构。
3. 未确认 bucket、templateCode、lovCode、lookupCode。

交接到专项：
1. 路由/菜单/Tab：`front-hzero-route`。
2. 页面容器、i18n、权限、service/model：`front-hzero-enterprise-page`。
3. HZERO + Choerodon DataSet：先 `front-hzero-enterprise-page`，再 `front-hzero-choerodon-ui`。
4. PageSchema 到 HZERO 的中间输出先使用 `templates/hzero-mapping-output.md`。

## 路线 B：Choerodon DataSet + Form + Table 映射方案

适用场景：
1. 目标页面明确使用 Choerodon UI / Pro。
2. 页面包含表单、表格、查询、筛选、弹窗、抽屉或 Lov/Attachment。
3. 字段和接口可确认；若缺少字段或接口契约，只输出 PageSchema、组件映射和待确认清单，不生成结构骨架，也不把非 runnable 结构作为用户可选交付。

可生成：
1. DataSet 划分建议：主 DataSet、明细 DataSet、queryFields/queryDataSet。
2. Form/Table/Card/Tabs 的结构映射建议；列表页默认建议 `Table + filterBar` 语义，并把 `queryBar` 代码形态交给 enumProvenance。
3. 已确认字段的 DataSet `fields`。
4. 已确认查询字段的 `queryFields`。
5. 未确认字段以待确认清单输出，不写入 runnable-looking 代码。
6. `componentShowcase` 只能生成组件映射表或组件文档页骨架，不生成业务 DataSet 页面。
7. UI Contract seeds：QueryFields Schema、`fuzzyQuery` 候选、操作列 `ColumnLock.right`、详情 `Form + Output`、overlay 层级规则和 mock-request 边界。

不可生成：
1. 未确认 `transport.read/create/update/destroy/submit`。
2. 未确认 `lovCode`、`lookupCode`、附件标识/bucket 的可运行实现；设计文档中可以输出候选值或待确认项。
3. 仅由 Figma 占位 `Label` 推导出的字段名。
4. 手写查询 Form、自绘 Drawer/Modal、`div/grid` 详情、`lock=true`、local-filter 伪装 mock-request。

交接到专项：
1. DataSet 建模、Form、Table、Lov、Attachment：`front-hzero-choerodon-ui`。
2. HZERO 工程中的 Choerodon 页面：先 HZERO 边界，再 Choerodon 实现。
3. PageSchema 到 Choerodon 的中间输出先使用 `templates/choerodon-mapping-output.md`。

## 路线 C：项目自定义组件映射方案

适用场景：
1. 项目已有业务封装组件。
2. 自定义组件 API 可从源码确认。
3. Figma 结构可映射到现有 PageHeader、Card、SearchForm、Table、DrawerForm 等抽象。

可生成：
1. 已确认自定义组件的 import 和基础组合。
2. PageSchema 到组件 props 的映射说明。
3. 静态结构和样式微调。
4. 接口缺失时仅输出映射说明、待确认项和暂停补契约建议，不生成业务页面骨架或请求。

不可生成：
1. 未确认组件 props、事件、render hook 或 children 约定。
2. 未确认组件内部是否已处理权限、i18n、loading、分页。
3. 未确认项目全局状态、hooks 或 model 约定。

发现顺序：
1. 先查相似页面。
2. 再查共享组件目录。
3. 再查页面容器/权限/i18n/请求封装。
4. 最后决定是否降级到 HZERO 或 Choerodon 标准模式。

## 最小安全输出
证据不足时输出以下内容即可，不继续编码：
1. PageSchema。
2. 三条路线的推荐优先级。
3. UI Contract seeds 或未生成原因。
4. 可直接生成与不可生成范围。
5. 阻塞待确认项。
6. 下一步验证计划。

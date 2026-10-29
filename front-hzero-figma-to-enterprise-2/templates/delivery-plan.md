# 交付计划模板

## 设计输入
1. 来源：Figma / 截图 / PRD / 混合。
2. 可确认内容：页面结构、文案、主要组件、资源。
3. 不可确认内容：接口、权限、字段真实类型、组件 API。

## PageSchema 摘要
1. 页面类型：list / form / formWithTable / detail / masterDetail / treeList / dashboard / uploadImport / componentShowcase。
2. 区块：header、search、filterBar、toolbar、card、table、form、modal、drawer 等。
3. 字段和操作：区分 confirmed / inferred / missing。

## 技术映射
1. 目标技术栈：custom / HZERO / Choerodon / HZERO + Choerodon。
2. 组件映射优先级：项目自定义组件 → HZERO → Choerodon UI / Pro → 原生兜底。
3. 数据层：service/model 或 DataSet，列出需要确认的协议。
4. 工程集成：路由、权限、i18n、样式、资源。
5. UI Contract seeds：列表、筛选、表格、详情、overlay、权限按钮、mock/demo 和 HZERO 平台边界必须输出推荐组件、必须规则、禁止反模式、下游 owner。

## 执行计划
1. 确认目标模块和相似页面。
2. 读取 Figma 节点并生成 PageSchema。
3. 确认字段、接口、权限和组件 API。
4. 补齐 UI Contract、字段/接口/权限契约和目标工程证据。
5. 进入默认 mock-request demo 或真实契约实现路径。
6. 运行项目验证命令。

## formWithTable 补充计划
1. 先拆主表单区和明细表格区。
2. 主表单区确认字段名、必填、字段类型和提交协议。
3. 明细表格区确认列字段、分页/排序、筛选条件、行操作和批量操作。
4. 若目标是 Choerodon，优先拆为主 DataSet + 明细 DataSet。
5. 若目标是 HZERO，先确认页面容器、路由权限和 i18n，再接 DataSet 或 service/model。

## Choerodon 补充计划
1. 先按 `templates/choerodon-mapping-output.md` 输出 PageSchema 到 DataSet/Form/Table 的映射。
2. `list` 页面拆为列表 DataSet、filterBar、queryFields/queryDataSet、enumProvenance 和 Table columns；关键字/模糊搜索输出 `fuzzyQuery` 候选。
3. `form` 页面拆为表单 DataSet 和 Form 字段。
4. `detail` 页面拆为 `Form + Output` 只读字段、数组 Table 和附件/关联区块。
5. `modal/drawer/overlay` 页面拆为弹层 DataSet、Form、生命周期和层级穿透检查待确认项。
6. `componentShowcase` 只输出组件/状态/变体映射表，不生成业务 DataSet 页面。

## HZERO 补充计划
1. 先按 `templates/hzero-mapping-output.md` 输出 PageSchema 到页面容器、权限、i18n 和数据层的映射。
2. `list` 页面确认 Header/Content、查询区、工具栏、表格、权限按钮和 service/model 或 DataSet 路线。
3. `formWithTable` 页面先确认 HZERO 页面容器和权限边界，再决定内容区使用 service/model 还是 Choerodon DataSet。
4. `uploadImport` 页面只列上传/导入/导出平台协议待确认项，不生成 bucket、templateCode、endpoint。
5. `componentShowcase` 只输出 HZERO/项目封装组件候选映射，不生成业务 route、permission 或 service/model。

## 待确认项
1. 接口契约。
2. 字段名和字段类型。
3. 权限码和菜单入口。
4. LOV / 值集 / 附件协议。
5. 自定义组件 API。
6. Figma 中占位文案对应的真实业务文案。

## 验证标准
1. 编译、lint、typecheck 或项目已有验证命令通过。
2. 页面结构与设计主要区块一致。
3. 表单、查询、表格、弹窗或抽屉主要交互可用。
4. 无虚构接口、权限、值集、LOV 或上传协议。
5. 下游实现必须回读 UI Contract seeds；未覆盖 `filterBar`、`fuzzyQuery`、`ColumnLock.right`、`Form + Output`、overlay 层级和 mock-request seed 时，不能宣称设计已完整落地。

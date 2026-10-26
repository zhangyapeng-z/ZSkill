# Figma 到企业前端 - 领域细节

## 阅读路由
- Figma 到企业前端 其它不归入阶段的领域细节、交叉引用或 proof 结构命中时读取。

## 组件映射优先级
1. 项目自定义业务组件：如 `BizTable`、`BizSearchForm`、`BizDrawerForm`、封装的上传/附件/LOV/权限按钮等。必须从项目源码确认名称和 API。
2. HZERO 页面与业务模式：页面容器、i18n、权限按钮、service/model、上传导入导出、值集/LOV、HZERO + Choerodon DataSet 边界。
3. Choerodon UI / Pro：业务表单、表格、查询、提交、校验、Lov、Attachment、Modal/Drawer 优先 `choerodon-ui/pro` 和 DataSet-first。
4. 原生 HTML/CSS：只用于纯布局、装饰、无业务状态的视觉表达，不能承载业务协议。

## 降级策略
- 无法读取 Figma：只基于用户提供的描述/截图做页面模式分析，不臆造精确布局。
- Framelink MCP 返回结果过大或目标不清：要求用户提供更精确的 frame/group selection link，或按页面区域拆分读取；仍不足时输出 PageSchema 和缺口。
- 无字段/接口契约：只生成 PageSchema、组件映射、UI Contract seeds 和待确认清单，不生成结构骨架或真实请求。
- 无项目自定义组件证据：降级到 HZERO 或 Choerodon 标准模式，并标注可替换点。
- 视觉结构复杂但业务不明确：先输出 `PageSchema` 和 question gate / 待确认契约，不直接编码；需要用户选择时必须调用 question 或返回主流程 question gate。
- Figma 组件文本是通用占位，如 `Label`、`Button`、`Table title`、`Table text` 时，只能确认结构和控件类型；不得把这些占位文案当成业务字段名或最终按钮文案。

## PageSchema 自动提取
- 当拿到 Framelink `get_figma_data` JSON、Figma API JSON 或工具展示的 YAML-like 文本时，可先运行 `scripts/extract-page-schema.js` 生成 PageSchema 草案。
- 脚本结果只是结构初稿，必须再用本 skill 的 references 和真实项目证据复核。
- JSON 输入置信度高于 YAML-like 文本；YAML-like 文本只能生成低置信结构草案，仍应优先保存 Framelink 原始 JSON。
- 原始 JSON、PageSchema 和 UI Contract seeds 应保存到 `sdd-workspace/changes/{change-id}/frontend/figma-cache/`，后续同 link/node 优先复用缓存。

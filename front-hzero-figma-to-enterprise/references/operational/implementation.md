# Figma 到企业前端 - 实现与工程证据

## 阅读路由
- Figma 到企业前端 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## 本地资源
按需查本目录资源；不要外显内部路径。Figma 缓存和前端产物位置遵循 `references/figma-cache-and-frontend.md`。

核心 reference 路由：
- 读取与缓存：`references/url-parsing.md`、`references/figma-mcp-workflow.md`、`references/framelink-output-shape.md`、`references/figma-cache-and-frontend.md`。
- 分析与映射：`references/design-analysis.md`、`references/component-mapping.md`、`references/custom-component-discovery.md`、`references/integration-boundaries.md`。
- 组件映射门禁：`references/component-mapping-guardrails.md`，用于输出 UI 设计回读表、UI Contract seeds、禁止反模式和下游 owner。
- 质量与验证：`references/conversion-evaluation.md`、`references/visual-verification.md`。

模板路由：
- PageSchema：`templates/page-schema.md`、`templates/page-schema-output.md`。
- 映射输出：`templates/hzero-mapping-output.md`、`templates/choerodon-mapping-output.md`、`templates/code-generation-boundaries.md`、`templates/delivery-plan.md`。
- 业务页面不得生成骨架模板；Figma 输入只产出 PageSchema、映射输出、UI Contract seeds、待确认项和下游 owner。

脚本路由：
- 已取得 Framelink JSON、Figma API JSON 或 YAML-like 文本时，可运行 `scripts/extract-page-schema.js` 生成 PageSchema 草案。

`references/samples/*` 是按样例类型拆分的二级 reference。只有在用户明确要求对照既有 Figma 样例、沉淀新样例，或当前节点与已收录样例高度相关时才读取；普通设计转代码任务优先查工作流、设计分析、组件映射和回归边界资料。需要样例时只读最小匹配文件：
- 表单展示：`references/samples/form-showcase.md`。
- 表格展示：`references/samples/table-showcase.md`。
- 导航、查询和反馈：`references/samples/navigation-query-feedback.md`。
- 数据展示和选择器：`references/samples/data-display-selector.md`。

## 工作流程
1. 输入识别：确认是否有 Figma URL、`fileKey`、`node-id`、截图或 PRD；有 URL 时按 `references/url-parsing.md` 解析 `fileKey` 和 `node-id`。
2. 产物目录优先：按 `references/figma-cache-and-frontend.md` 先读取 `sdd-workspace/changes/{change-id}/frontend/index.md`、`handoff/artifact-index.md` 和 `figma-cache/**/{readme.md,page-schema.json,ui-contract-seeds.json,ui-contract-seeds.md,assets-manifest.json}`，从已有产物判断是否存在同 `fileKey + nodeId` 的可复用 PageSchema、UI Contract seeds、资源清单或 partial 读取结果。
3. 缓存判定：缓存可用且设计未变时复用缓存，输出 `cache-only` 或 `confirmed-from-cache`，减少 Figma 链接获取；缓存缺区域时只补读缺失区域，不重复读取已缓存节点。
4. Framelink 读取：无缓存、缓存失效、link/node 变化、readme 标记 stale、用户说明设计已变，或下游需要缓存中缺失的区域/资源时，能使用 Framelink Figma MCP 才按 `references/figma-mcp-workflow.md` 调用 `get_figma_data`；需要导出图片或 SVG 时再调用 `download_figma_images`。
5. 缓存写入：读取后写入 `figma-source.json`、`page-schema.json`、`ui-contract-seeds.json` 或 `ui-contract-seeds.md`、`assets-manifest.json` 或缓存说明，并同步 `sdd-workspace/changes/{change-id}/frontend/index.md` 的 figma-cache source、Current Stage 和 Open Items；短答未写入时标注 `Figma 缓存状态：未写入`。
6. 降级读取：不能使用 Framelink MCP 时说明原因，并只基于用户给出的截图/文字做有限分析，不臆造精确尺寸、组件实例或资产。
7. 页面分析：识别页面类型、布局区域、查询区、工具栏、表格、表单、弹窗、抽屉、详情、上传、导航和空/错误状态。
8. 生成 `PageSchema`：先输出中间结构，标记 confirmed / inferred / missing，避免把视觉猜测当业务事实。
9. 技术栈分流：根据项目上下文和用户目标选择自定义组件、HZERO 页面、Choerodon UI / Pro 或组合路径。
10. 组件映射：按优先级映射视觉节点；无法确认的组件、字段类型和协议必须进入待确认项。
11. UI Contract seeds：按 `references/component-mapping-guardrails.md` 生成区域级 seeds，写清推荐组件、必须遵守规则、禁止反模式、下游 owner 和 open contracts。
12. 工程集成边界：结合设计 handoff metadata 和最小项目证据确认候选目录、路由、权限、i18n、service/model、DataSet、样式方案和资源路径；未确认项必须保留 missing / 待确认。
13. 生成交付：默认输出 PageSchema、UI 设计回读表、UI Contract seeds、组件映射说明、待确认清单和验证规划；即使证据充足，也只生成可交接的设计证据和片段，不直接完成完整业务实现。
14. 交接收尾：输出返回 `frontend-auto-agent` 的 handoff metadata、仍缺业务契约和建议验证方式；不在本 skill 内执行完整 lint/typecheck/build/browser 验证。

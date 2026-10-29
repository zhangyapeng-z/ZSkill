# Figma 到企业前端 - 设计与契约

## 阅读路由
- Figma 到企业前端 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 设计交接策略
- 生成设计交接材料前先判断目标路线：HZERO、Choerodon DataSet 或项目自定义组件。
- HZERO 路线只输出页面容器、i18n、权限和数据层边界；Choerodon 路线只输出 DataSet/Form/Table/组件映射；自定义组件路线先确认组件 API。
- 任一路线默认只输出 PageSchema、边界、UI Contract seeds、组件映射说明和待确认项，不生成 runnable-looking 业务代码。
- 用户要求完整实现时，先返回 `frontend-auto-agent` 交接建议；由主 agent 完成 Contract Check、Frontend Design、Task Breakdown、Implementation、Review、Verification、Final Review 和 Handoff。

## 事实确认契约
- Figma 只能确认视觉结构、可见文案、尺寸、颜色、层级、组件名/组件属性、变量、资源引用和部分组件形态，不能单独确认接口、权限、字段业务类型、后端协议或值集编码。
- 字段类型可以根据视觉先标记为 `candidateType`，但生成真实 DataSet field 或表单控件前，必须确认来源：PRD、接口契约、相似页面、后端 DTO 或用户明确输入。
- 具体组件 props、事件、默认值必须来自项目源码、对应 skill references、官方文档或用户明确约束。
- 缺少接口契约时，不输出 runnable-looking `transport`、service 请求或占位 API。
- Framelink Figma MCP 输出的 YAML/JSON 是设计语义、布局、样式和组件线索，不是本项目最终代码；落地时必须改写为项目约定组件、样式和数据模式。
- Figma 设计系统展示节点只能沉淀组件、状态和变体映射，不能直接当作业务页面生成。

## 目标
把 Figma 或其他设计证据转成企业前端可交接方案：先抽象为页面中间结构，再按项目自定义组件、HZERO 页面规范和 Choerodon UI / Pro 规则生成 PageSchema、组件映射、边界说明和设计交接材料。完整业务实现、真实接口接入、路由权限落地和验证闭环必须回到 `frontend-auto-agent`。

负责：
- 判断设计输入是否足够用于页面生成。
- 从 Figma MCP、Figma 节点或截图/PRD 中识别页面模式、区块、字段、表格、操作、弹窗和资产。
- 生成或校验 `PageSchema` 中间结构。
- 按 `sdd-workspace/changes/{change-id}/frontend/figma-cache/` 缓存 Figma 原始读取结果、PageSchema、UI Contract seeds 和资源清单，避免重复读取。
- `sdd-workspace/changes/{change-id}/frontend/` 位于当前 SDD 项目根目录下，不位于目标前端工程内部或目标前端工程平级外部目录。
- 定义组件映射优先级：项目自定义组件 → HZERO 标准页面/自定义封装 → Choerodon UI / Pro → 原生 HTML/CSS 兜底。
- 约束 DataSet、HZERO 路由权限、i18n、service/model、样式、资源和 UI Contract seeds 边界。
- 给出低打扰追问、降级输出、验证和交付清单。

不负责：
- 编造接口、字段业务含义、权限码、路由、`lovCode`、`lookupCode`、上传协议或组件 API。
- 把 Figma 视觉节点直接像素级硬编码成难以演进的页面。
- 直接生成 production runnable 页面、真实 service/helper、真实 DataSet transport、路由配置、权限配置或上传导出协议代码。
- 替代 `frontend-auto-agent` 做完整业务实现、任务拆解、验证闭环或交付收口。

## UI 来源优先级
- UI 显示布局的权威顺序：用户明确确认 > Figma/PageSchema confirmed > 目标工程同类页面基线 > FDS 中的 UI 描述 > 后端 TDS 前端提示。适用范围包括页面布局、区块顺序、视觉层级、按钮区域、列表/表单/详情/弹层形态、字段显示顺序、密度和响应式视觉约束。
- 业务与契约的权威顺序：用户明确确认 > FDS/TDS/API/DTO/权限/平台协议 > 目标工程业务证据 > Figma 可见文案。适用范围包括业务能力、字段语义、接口、状态流转、权限、route/menu、LOV/lookup、附件/导入导出协议和生产请求契约。
- Figma/PageSchema 可以约束 UI 如何显示，但不能删除 FDS/TDS 已确认的业务能力；FDS/TDS 可以约束数据和业务，但不能在无前端复核时覆盖 Figma confirmed 的布局。
- 当 Figma 与 FDS/TDS 发生冲突时，不得静默合并。必须输出 `uiBusinessConflicts`，分别写清 `layoutAuthority`、`businessAuthority`、`conflictResolution` 和是否需要 question gate。
- 仅 UI 呈现冲突且业务能力完整覆盖时，可按 Figma/PageSchema 布局继续；业务能力、字段语义、权限或接口受到影响时，必须标记 `missing/conflict` 并交由主流程确认。

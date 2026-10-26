# Framelink Figma MCP 工作流参考

## 目标
把 Framelink Figma MCP 的原始输出转为企业前端可用证据：先用 `get_figma_data` 获取目标节点的描述性设计数据，必要时用 `download_figma_images` 导出图片/SVG，再进入 PageSchema、组件映射和代码生成。

本项目默认使用 Framelink Figma MCP，而不是 Figma 官方 MCP。不要假设存在 `get_design_context`、`get_screenshot`、`get_metadata`、`get_variable_defs` 或 `get_code_connect_map` 这些官方 MCP 工具。

## 必需调用顺序
0. 产物缓存检查：请求 Framelink 前，先读取 `sdd-workspace/changes/{change-id}/frontend/index.md`、`handoff/artifact-index.md` 和 `figma-cache/**/{readme.md,page-schema.json,ui-contract-seeds.json,ui-contract-seeds.md,assets-manifest.json}`。已有同 `fileKey + nodeId` 可用缓存时，优先复用 PageSchema、UI Contract seeds 和资源清单，输出 `cache-only` 或 `confirmed-from-cache`，不调用 Framelink。
1. `get_figma_data`：仅在缓存缺失、缓存失效、设计变更或需要补读缺失区域时读取目标 frame/group/node 的结构化设计数据。必须优先使用用户提供的 selection link，避免读取整个文件。
2. 分析返回数据：按 `references/framelink-output-shape.md` 识别页面、区块、组件实例、组件属性、样式、布局、图片引用和重复结构。
3. `download_figma_images`：仅当节点包含需要落地且缓存中没有的图片、SVG、复杂 icon 或位图资源时调用；不要为纯组件库图标或可由项目组件表达的元素下载资源。
4. 项目源码确认：在生成代码前搜索项目自定义组件、HZERO 页面模式、Choerodon DataSet/Pro 组件和样式 token。

如果 Framelink 工具不可用，只能基于截图/PRD/用户文字降级分析，并必须说明缺少结构化 Figma 证据。

## 证据分级
- `confirmed`：来自 Framelink `get_figma_data`、`download_figma_images`、项目源码、PRD/API 契约或用户明确输入。
- `inferred`：来自视觉形态、组件命名、样式名、重复结构、设计系统样例或相似页面推断。
- `missing`：生成真实业务代码前必须补齐的字段、接口、权限、值集、LOV、上传协议或组件 API。

PageSchema、组件映射和交付说明都应保留这个分级。

## get_figma_data 使用规则
- Framelink 通常返回描述性 YAML/JSON，保留布局、样式名、组件属性、嵌套组件和去重信息；它不是可直接复制的业务代码。
- 保留有业务意义的层级：页面、区块、表单组、筛选区、工具栏、表格、弹窗、抽屉、状态。
- 消除无业务意义的层级：auto layout 包裹、背景 frame、装饰 vector、组件内部私有层、重复 placeholder。
- 对节点名、组件实例名、样式名和组件属性做语义提取，例如按钮主次、输入状态、必填、禁用、选中、表格单元格类型。
- 设计系统展示节点应沉淀为组件类型、状态和变体映射，不应直接生成业务页面。

## 图片和 SVG 下载规则
- Framelink 的 `download_figma_images` 可导出 Figma 文件中的图片或 icon 节点；只在资源确实需要落地时使用。
- 资源落地前先确认项目资源目录和命名规范。
- 装饰图标优先映射项目图标库；无法映射且 Framelink 可导出 SVG 时再下载静态资源。
- 不把包含业务数据的截图作为页面内容。
- 若用户环境禁用了 image download 工具，应说明限制，并把资源列为待处理项。

## 大节点处理
- Framelink 官方建议复制具体 frame/group selection link；复杂页面应按区域读取，避免一次拉取整个文件。
- 按页面区域拆分读取：Header、Search/Form、Toolbar、Table、Modal/Drawer、Detail、Upload。
- 多个 frame 代表多状态或多页面时，分别生成 PageSchema，不要混为一个页面。
- 对重复列表/表格，只抽取结构和少量样例，不把所有重复层逐一转为 DOM。
- 如果返回数据仍过大或目标不清，要求更精确的 Figma selection link，而不是凭文件名或页面名继续猜。

## 429 / rate limit 处理
- Framelink / Figma MCP 的错误格式可能不统一，必须先做错误归一化，再写入产物。只要满足下列任一条件，都统一判定为 `figmaFetchStatus=rate-limited-429`、`figmaFetchErrorCode=429`：
  - HTTP status / statusCode / response.status 为 `429`。
  - error code / error.status / error.response.status / tool result code 为 `429`。
  - 异常 message、stderr、tool output、JSON error body 中包含 `rate limit`、`rate-limited`、`too many requests`、`quota exceeded`、`429`、`Too Many Requests` 等限流语义。
  - 工具返回空数据、partial 数据或失败包装，但错误摘要中出现上述限流语义。
- 归一化时必须保留原始错误摘要，不把工具特定格式丢掉。产物字段至少记录：`rawErrorShape`、`rawErrorExcerpt`、`normalizedReason=rate-limit`、`figmaFetchStatus=rate-limited-429`、`figmaFetchErrorCode=429`。
- 如果工具只返回空数据、空异常、无 status 且无可识别错误文本，必须统一判定为 `figmaFetchStatus=failed`、`figmaFetchErrorCode=unknown`、`rawErrorShape=empty-response / unknown`、`normalizedReason=unknown`，并输出 retryPlan 或要求用户提供更精确 selection link；不得把空失败当成 Figma confirmed 或 cache valid。
- 先查 `sdd-workspace/changes/{change-id}/frontend/figma-cache/` 是否已有同 fileKey/nodeId 的可用缓存；有缓存时优先输出 `cache-only` 或 partial PageSchema，不重复拉取。
- 不要连续重复请求同一个大节点超过 2 次。第二次仍失败时，改为按 Header、Search/Form、Toolbar、Table、Modal/Drawer、Detail、Upload 等区域分批读取，或要求用户提供更精确 selection link。
- 输出 retryPlan：失败节点、已尝试次数、分批区域、建议等待时间、下一次继续条件、已缓存的 partial 证据。
- 已成功读取的区域必须先缓存；后续恢复时从未完成区域继续，不从头读取整个文件。

## 视觉验证衔接
- Framelink 没有独立 `get_screenshot` 流程时，按 `references/visual-verification.md` 建立视觉基准。
- 复杂页面至少保留 Figma selection link、Framelink data 摘要、必要下载资源和本地实现截图。
- 未完成视觉对比时，交付结果只能声明结构/工程验证完成，不能声称已达到 1:1 视觉一致。

## 与官方 Figma MCP 的区别
- Framelink 主要工具是 `get_figma_data` 和 `download_figma_images`。
- Framelink 输出偏描述性数据，常为 YAML/JSON；不要期待官方 MCP 的 React + Tailwind 代码输出。
- Framelink 会尽量保留样式名、组件属性、嵌套组件和去重信息；这些可以用于组件映射，但仍需用项目源码确认真实 API。
- 若当前环境同时安装多个 Figma MCP，优先使用用户配置的 Framelink；只有用户明确要求，才按其他 MCP 的工具名调整流程。

## 交付前检查
- 是否记录 Figma URL、`fileKey`、标准化 `nodeId` 和读取方式。
- 是否调用了 Framelink `get_figma_data`，或说明缺失原因。
- 是否把占位文案保留为结构证据，而不是业务字段、按钮或列名。
- 是否按需调用 `download_figma_images`，或说明无需下载/工具不可用。
- 是否按 `visual-verification.md` 完成视觉基准和实现截图检查，或说明未完成原因。
- 是否先确认项目组件 API，再生成组件调用。
- 是否避免编造 route、permission、service、DataSet transport、lookupCode、lovCode、bucket 和 templateCode。
- 是否运行可行的 lint、typecheck、test、build 或页面打开验证。

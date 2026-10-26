# Figma URL 解析参考

## 支持的 URL 形态
- `https://www.figma.com/design/<fileKey>/<fileName>?node-id=2-2282`
- `https://www.figma.com/file/<fileKey>/<fileName>?node-id=2%3A2282`
- `https://www.figma.com/proto/<fileKey>/<fileName>?node-id=2-2282`

## 解析规则
- `fileKey`：从 `/design/`、`/file/` 或 `/proto/` 后的第一段路径提取。
- `node-id`：优先从查询参数 `node-id` 提取。
- `node-id` 中的 `-` 需要转换为 `:`，例如 `2-2282` 转为 `2:2282`。
- URL 编码的 `node-id=2%3A2282` 需要解码为 `2:2282`。
- 深层 instance node 可能包含分号路径，例如 `I5666:180910;1:10515;1:10336`，必须作为单个 node id 保留。
- `t=`、`m=`、`type=` 等参数只用于 Figma 展示状态，不参与节点读取。

## 降级规则
- 有 `fileKey` 但无 `node-id`：不要默认读取整个文件；需要用户选择目标 Frame 时必须通过 question 或返回主流程 question gate；只有用户明确允许时才能读取文件顶层并再通过 question 确认目标节点。
- URL 无法解析 `fileKey`：说明链接格式不足，要求用户提供 Figma 原始链接或 `fileKey`。
- `node-id` 解析后读取失败：说明可能是权限、节点不存在、节点类型不适合或链接不是设计文件节点；不要根据文件名臆造布局。
- 用户只给截图：跳过 Figma 工具读取，只做有限 PageSchema 推断，并把精确尺寸、组件实例和资源列为未确认。

## 输出记录
分析结果中应记录：
- 原始 URL。
- `fileKey`。
- 标准化后的 `nodeId`。
- 读取方式：Figma 工具 / 截图 / PRD / 混合。
- 读取失败原因或降级原因。

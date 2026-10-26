# Framelink 输出结构参考

## 目标
把 Framelink `get_figma_data` 返回的描述性 JSON/YAML-like 数据稳定转成 PageSchema 证据。Framelink 输出不是业务代码，也不是接口契约；它是视觉、布局、组件、样式和资源线索。

## 常见顶层形态
Framelink 输出可能是以下形态之一：

```json
{
  "metadata": {
    "name": "H-ZERO-流光蓝-preview",
    "fileKey": "bH0YIuDvb0xQ3wdaoEm6iF",
    "nodeId": "103:14686"
  },
  "data": [
    {
      "type": "text",
      "text": "metadata:\n  name: ...\nnodes:\n  - id: 103:14686\n    name: 表格\n    type: FRAME"
    }
  ]
}
```

```json
{
  "name": "Page title",
  "type": "FRAME",
  "children": []
}
```

```json
{
  "nodes": [
    {
      "id": "2:2282",
      "name": "中台表单",
      "type": "FRAME",
      "children": []
    }
  ]
}
```

```yaml
name: 中台表单
type: FRAME
children:
  - name: Header
    type: FRAME
  - name: 表单 / 类型=文本输入框
    type: INSTANCE
```

优先保存 JSON 或 Framelink JSON wrapper；YAML-like 文本可以用于低置信草案，但不要把解析结果当作完整 Figma 树。

## 有用字段
- `id`：Figma node id，可作为证据引用，不等于业务字段名。
- `name`：节点名、组件名或图层名，可用于识别页面区域、组件类型和设计系统变体。
- `type`：节点类型，如 `FRAME`、`GROUP`、`INSTANCE`、`TEXT`、`RECTANGLE`、`VECTOR`。
- `text` / `characters`：可见文案。占位文案必须按占位规则处理。
- `children`：子节点。用于识别区块、表单组、表格、弹窗、重复结构。
- `componentProperties` / `properties`：组件属性，如状态、类型、大小、必填、禁用、选中。
- `styles` / `style`：颜色、字体、字号、边框、阴影等视觉证据。
- `layout` / `absoluteBoundingBox` / `size`：布局、尺寸和间距线索。
- `fills` / `imageRef` / `imageHash` / `svg`：资源线索，必要时衔接 `download_figma_images`。

## PageSchema 提取路径
1. 顶层 frame/group 名称 → `page.name` 候选；如果是 `Page title` 等占位，则 evidence 为 `inferred`。
2. 大区块名称 → `regions`：Header、Search、FilterBar、Toolbar、Table、Form、Card、Tabs、Modal、Drawer、Upload。
3. `INSTANCE` + 表单/输入/筛选/选择/日期/上传关键词 → `FieldSchema` 候选。
4. `表头`、`Table title`、列 frame、重复单元格 → `ColumnSchema` 候选，必须转置为 columns。
5. 按钮组件、icon button、文本按钮 → `ActionSchema` 候选，权限和行为默认为 `missing`。
6. 图片/SVG 引用 → `integration.assets` 候选；只有实际下载或项目已有资源确认后才标为 `confirmed`。
7. 若节点含 `表格展示`、`基础`、`行内编辑`、`树形`、`拖拽`、`禁用行` 等规格分组，优先识别为 `componentShowcase`，用于组件映射回归，不当作业务列表页。

## 置信度规则
- JSON 且包含 `children`、`type`、`name`：可生成 medium 置信 PageSchema。
- Framelink JSON wrapper 且内嵌文本包含 `nodes:`：可生成 medium 置信 PageSchema，并记录 `rawInputFormat: framelinkJsonWrapper`。
- JSON 只包含扁平文本或节点摘要：只能生成 low/medium 置信 PageSchema。
- YAML-like 文本：只能生成 low 置信 PageSchema，除非人工复核并补充结构。
- 文件级链接或无目标 node：不要生成高置信结构；要求具体 selection link。

## 低置信 YAML-like 处理
当只能拿到 YAML-like 文本时：
- 可以抽取出现频繁的节点名、文本和组件关键词。
- 可以识别明显的 `Header`、`Table`、`Form`、`Button`、`Modal` 等区域。
- 不要保留精确层级、尺寸、样式 token 或资源路径为 confirmed。
- 输出必须提示“建议保存 Framelink 原始 JSON 后重跑脚本”。

## 常见误读
- 节点名包含业务词，不代表字段名、接口名、权限码或 i18n key。
- `componentProperties.required=true` 或 `必输=true` 只是 required 候选，不能单独生成最终校验。
- `imageRef` 只是资源引用线索，不代表资源已经可用于项目。
- 设计系统示例中的所有状态都不是业务状态机。

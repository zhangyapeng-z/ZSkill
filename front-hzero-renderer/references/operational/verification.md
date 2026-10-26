# Renderer - 验证与运行态

## 阅读路由
- Renderer 验证、构建、浏览器检查、运行态判定或输出检查时读取。

## Verification Checklist
- 状态标签通过 `TagRender` 渲染，有文本、颜色符合状态矩阵或项目候选，空值按项目规则展示为空或 fallback。
- 日期、时间、数字格式与字段类型和后端语义一致。
- 操作列通过 `c7nOperatorRender` / `operatorRender` 或已记录 project-override helper 渲染，按钮数量、overflow 入口和空 operators 表现符合标准或项目扩展；行操作权限、状态和二次确认专项验证仍由 `front-hzero-choerodon-ui` 的 row-actions scenario reference 承担。

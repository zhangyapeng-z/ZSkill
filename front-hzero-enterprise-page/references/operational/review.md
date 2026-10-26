# 企业页面 - 审查与反模式

## 阅读路由
- 企业页面 Review、自查、反模式、finding 或合规判断时读取。

## 反模式
- 用户可见文案硬编码。
- 权限编码随意写死且不跟 route path 关联。
- 请求协议写在点击事件中。
- HZERO DataSet 页面脱离 HZERO 页面容器、路由和权限规范。
- 把 HZERO render helper 当 React 组件使用，例如 `<TagRender status={...} />`、`<c7nOperatorRender ... />`。
- 编造 bucket、templateCode、接口路径、租户规则、权限 code、字段、路由或本地 helper。
- 编造 previewUrl、文件预览 token、转换服务、支持文件类型或跨域策略。
- 在计划或评审文本中输出可复制的内部占位 token；应改成自然语言待确认项。

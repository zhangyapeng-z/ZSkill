# Figma 到企业前端 - 审查与反模式

## 阅读路由
- Figma 到企业前端 Review、自查、反模式、finding 或合规判断时读取。

## 反模式
- 只看截图、不调用 Framelink `get_figma_data` 就开始实现。
- 把 Framelink 返回的层级数据逐层硬翻成 HZERO 或 Choerodon DOM。
- 直接把 Figma frame 逐层翻译成大量绝对定位 `div`。
- 根据按钮文案编造权限码或接口动作。
- 根据下拉视觉编造 `lookupCode` 或 `lovCode`。
- 未确认项目封装组件 API 就生成调用代码。
- HZERO 页面跳过路由、菜单权限、i18n 和页面容器。
- Choerodon 页面跳过 DataSet-first，改用散乱本地状态承载查询、提交和校验。

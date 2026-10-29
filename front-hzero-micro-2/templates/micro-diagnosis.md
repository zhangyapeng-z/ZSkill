# 微前端诊断输出模板

## 问题阶段
- public url / 构建产物路径 / 远程元数据 / 运行时 `mfRemotes` / 远程访问路径 / 路由匹配 / 运行时加载
- 具体场景：remoteEntry 404 / 子模块白屏 / registerRegex 不匹配 / 跨模块组件加载失败 / 部署后 chunk 异常

## 已知信息
- 子模块：
- 路由前缀：
- 目标包名：
- exposed key / 组件：
- `PACKAGE_PUBLIC_URL`：
- 构建产物路径：
- 远程访问路径：
- `microConfig` 目标包地址：
- 运行时 `window.mfRemotes` 地址：
- Network 失败 URL：

## 优先检查项
- 
- 当前最可能阶段：
- 需要先排除的非微前端因素：菜单权限 / 路由配置 / 页面运行时报错

## 远程元数据与运行时检查
- `microConfig.json`：
- `window.mfRemotes`：
- `remoteEntry.js` 实际 URL 来源：`microConfig` / `window.mfRemotes` / 部署产物说明 / Network
- `remoteEntry.js` 访问结果：
- `mfExposes`：
- `registerRegex`：
- 构建产物路径：
- 远程访问路径：
- public url、构建产物路径、远程访问路径是否分别确认：

## 验证方式
- 
- Network：
- Console：
- 路由命中：
- 首屏加载影响：

## 待确认项
- 
- 包名 / 路由前缀：
- public url：
- 构建产物路径：
- 远程访问路径：
- `microConfig` 远程地址：
- `window.mfRemotes` 运行时地址：
- Network 失败 URL：
- 暴露组件协议：

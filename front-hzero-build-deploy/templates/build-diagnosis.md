# 前端构建与产物加载诊断输出模板

## 问题阶段
- 本地开发 / 父模块构建 / 子模块/子包编译 / public url / 构建产物路径 / 远程元数据 / 远程访问 / 运行时 `mfRemotes` / 运行时加载 / 增量构建

## 已知信息
- 包管理器：
- 项目 scripts：
- 执行目录：
- 目标包名：
- 编译范围：父模块 / 单个子模块 / 全部子模块
- routes/config/registerRegex 是否变更：
- 子模块构建命令：
- microConfig 刷新命令：
- dev server 是否重启：
- 浏览器是否 hard reload：
- `PACKAGE_PUBLIC_URL`：
- 构建产物路径：
- 远程访问路径：
- `microConfig` 目标包地址：
- 运行时 `window.mfRemotes` 地址：
- Network 失败 URL：

## 优先检查项
- 

## 推荐命令或配置检查
- 

## 远程元数据与产物检查
- `packages/microConfig.json`：
- 目标包 `remoteEntry.js` 构建产物：
- `remoteEntry.js` 实际 URL 来源：`microConfig` / `window.mfRemotes` / 部署产物说明 / Network
- `remoteEntry.js` 访问结果：
- public url、构建产物路径、远程访问路径是否分别确认：

## 验证方式
- 

## 待确认项
- 
- public url：
- 构建产物路径：
- 远程访问路径：
- `microConfig` 远程地址：
- `window.mfRemotes` 运行时地址：
- Network 失败 URL：

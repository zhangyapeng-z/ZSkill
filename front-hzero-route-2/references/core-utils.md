# HZERO Route Core Utils

HZERO front core 中常见路由工具包括 `gotoPage`、`getRoutes`、`getMicroModuleInfoList`、`getMicroModuleInfo`、`isSpecialRouter`。
完整工具分组和跨域边界由 `front-hzero-enterprise-page` 负责；本文件只保留路由域的使用约束。

## 使用边界
- 使用前确认目标项目 `utils/utils` alias、文件和 export 存在；不要复制 core 源码路径到业务 import。
- `gotoPage(pathname, search)` 是普通 dva/router 跳转候选，不能替代 HZERO `openTab`、dynamic Tab 或菜单数据契约。
- `getRoutes(path, routerData)` 可作为读取已加载 route 子项的候选工具，但不能证明新 route/menu 已注册。
- `getMicroModuleInfo(microModule)` 可用于判断目标微前端模块是否存在，不能证明 `remoteEntry`、chunk、registerRegex 或菜单权限正确。
- `isSpecialRouter` 可用于识别基于 `PUBLIC_URL` 前缀的 `/pub`、`/public`、`/private`、`/link`、`/iframe`、`/pure-pub` 等特殊路由候选；特殊访问模式仍需项目路由和布局证据确认。
- `resolveRequire(module)` 只用于处理 `require` / dynamic import 的 default 导出差异；不能用来吞掉模块路径错误。
- `getMenuId()` 可能依赖 `window._hzero_currentMenuId`，只可作为运行态菜单上下文候选，不能证明平台菜单已配置。

## 禁止项
- 用 `gotoPage` 或 route helper 掩盖 menu path、route path、权限、Tab、registerRegex 或子模块加载配置错误。
- 用 core utils 的存在证明业务路由、菜单、权限码或远程访问路径存在。
- 未确认 alias/export 就写 `import { gotoPage } from 'utils/utils'`。
- 因 `getMicroModuleInfo` 返回存在就宣称微前端生产可用；仍必须验证 microConfig、remoteEntry、chunk、公网路径和 registerRegex。

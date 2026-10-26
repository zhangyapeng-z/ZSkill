# 企业页面 - 设计与契约

## 阅读路由
- 企业页面 设计、契约冻结、question gate、事实确认或资源选择时读取。

## 事实确认契约
- 仅依赖自身说明和本地 `references/` 给出安全流程、硬规则、输出结构和不确定性处理。
- 本地 references 是模式和候选事实，不等同于目标项目契约。
- 输出具体页面代码、service/model、权限配置、DataSet transport、上传/导入/导出参数、LOV/值集编码或接口结构前，必须先从项目源码、用户提供的契约或明确文档确认；确认不了就列为待确认项。能够按规范生成的候选编码必须标为 `generatedCandidate`，不能伪装成 confirmed。
- 权限 code 是契约事实。required 业务动作缺 confirmed 权限码时，不得降级为普通按钮；若 route path、action 清单和项目权限编码规则足够，应生成 `generatedCandidate permissionCode`，继续使用 `front-hzero-permission-button` 的固定 `ButtonPermission`，并标明生产权限码仍需菜单/权限资产登记或确认。只有 action 清单、route/menu 命名空间或编码规则不足时才阻塞确认；不得仅凭按钮文案静默编造 action，也不得把候选权限码写成 confirmed。
- 权限按钮组件入口、Provider 入参、`codeList` / `permissionList` 契约、旧组件禁用和按钮 type 规则统一由 `front-hzero-permission-button` 负责；页面 skill 不得被相似页面旧写法覆盖。
- 相似 HZERO 页面只能作为容器、import、formatter、布局和组件组合的项目模式证据，不能证明新业务路由、菜单、权限码、字段名、i18n key、service/helper、接口或附件标识字段。
- 不得用 `mock`、`demo` 前缀把从页面名推导出的字段、路由、权限码、i18n key、service/helper 或附件标识字段写成 confirmed；默认 mock demo 下可生成可请求演示链路，但候选字段、路由、权限码、i18n、service/helper 和附件标识必须标为 `generatedCandidate/mockOnly` 并进入 production replacement。
- “按常规先写”“后面我再改”“你先按经验来”不是字段、接口、权限或路由 confirmed 契约。契约缺失但候选生成基础事实足够时，应输出 generatedCandidate 并保留确认/登记边界；基础事实不足或 mock 接线无法闭合时不得新增页面目录、路由配置、service/model、DataSet 字段、本地业务数据、本地查询/保存 helper 或 PermissionButton code。required 权限动作不得退化成普通按钮绕开权限。
- HZERO render helper 是契约事实。`TagRender`、`enableRender`、`dateRender`、`operatorRender`、`c7nOperatorRender` 等 `utils/renderer` helper 的 import、签名和调用形态由 `front-hzero-renderer` 负责；不得把普通 helper 当 React 组件使用。

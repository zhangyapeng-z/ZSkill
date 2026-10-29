# 权限按钮 - 审查与反模式

## 阅读路由
- 权限按钮 Review、自查、反模式、finding 或合规判断时读取。

## Review Findings
至少 major：
- required 动作使用普通 `Button`。
- required 动作未使用固定 `ButtonPermission`。
- required 动作只因权限码、平台登记或 `permissionList` 参数未 confirmed，就退回普通 `Button`、隐藏入口、disabled/no-op、合同占位或本地 wrapper。
- 从 `components/Permission` 直接 `import { ButtonPermission }`，而不是 `import { Button as ButtonPermission }`。
- 使用 `@common/components/PermissionButton`、业务/模块前缀包装的 `*PermissionButton`、本地 wrapper 或 fallback。
- Header / PageHeader / Toolbar / 表格上方工具栏 / 表单普通按钮 / 详情页非表格按钮误套行操作 `type="text"`，且无 UI Contract、固定组件 API 或明确 project-override 来源。
- 行操作误用 `type="c7n-pro"`。
- `funcType`、`ButtonColor` 等旧 props 无证据迁移。
- 仅因按钮间距、对齐或视觉统一，把 Button Contract 未判定为 required 的普通 `Button` 改成 `ButtonPermission`。

blocking：
- 权限按钮运行时异常。
- 固定权限按钮 import shape 错误导致组件为 `undefined`，触发 React #130 / 元素类型无效白屏。
- 权限判断失效或总是可见/总是隐藏。
- `permissionList` / `codeList` 契约错配。
- `permissionList` 使用字符串数组、权限码常量数组、缺 `code/type` 的对象数组，或 `ButtonPermission` 在 prm/PermissionProvider 读取 `permissionList` 的场景使用 `codeList`，导致权限检查失效或 `undefined.replace` 运行时异常。
- 导入/导出标准组件的 required 权限被错误迁移到顶层 `permissionList`、本地薄封装或普通 `ButtonPermission` 外壳，导致标准组件按钮权限不生效。
- required 权限绕过后仍声明 production-ready。
- 权限参数缺口被当成组件生成阻塞，导致 required 动作不可达或只展示“权限待确认 / replacement / 仅保留权限合同”等用户可见内部文案。

## Handoff Closeout
- 交付摘要应记录固定 `ButtonPermission` 动作清单、confirmed / generatedCandidate / missing 权限码状态、仍需平台登记或确认的权限项。
- 未验证 Provider 契约、按钮可见性、禁用态或权限隐藏风险必须进入 Handoff 风险或 replacement。

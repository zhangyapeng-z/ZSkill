# 权限按钮 - 实现与工程证据

## 阅读路由
- 权限按钮 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## Position Rules
- required 动作进入实现时，缺 confirmed 权限码只影响参数状态，不影响固定组件生成；应生成 `generatedCandidate permissionCode`，并以 `permissionList={[{ code: permissionCode, type: 'button', meaning }]}` 形态继续渲染固定 `ButtonPermission`。不得把 `permissionList` 写成字符串数组，也不得默认使用 `codeList`；`codeList` 仅限目标源码和 Provider 均 confirmed 的项目特例。
- Table 行操作列，包括列表页操作列、详情页明细表、子表行操作列：`ButtonPermission` 默认必须使用 `type="text"`。
- Header、PageHeader、Toolbar、表格上方工具栏、表单普通按钮、详情页非表格按钮：不得继承行操作 `type="text"`；普通权限按钮默认优先使用 `type="c7n-pro"`，除非 UI Contract、固定组件 API 或明确 project-override 另有来源。
- 上一条不适用于标准导入/导出组件的内置触发按钮；其按钮样式通过 `buttonProps` / `otherButtonProps` 传入，并按 `front-hzero-import-export` 已确认组件合同执行。
- `color`、`type` 等 Button props 必须按固定组件 API 和项目 enum/string 风格确认；不要照搬旧 Pro Button 的 `funcType` / `ButtonColor`。
- 视觉修复不得改变 Button Contract。按钮间距、对齐、高度或外观不一致时，先检查所在 Header/Toolbar/Table `buttons` 的实际 DOM、组件 props、className 和 CSS 命中；只有 Button Contract 已判定 `permissionRequirement=required` 时才把普通 `Button` 改为固定 `ButtonPermission`。
- 不得因为权限码、平台登记或 Provider runtime 未验证，把 required 动作改成普通 `Button`、隐藏入口、永久 disabled/no-op、tooltip 占位、合同 `<div>` 或本地 wrapper。Provider 契约无法判定时回 Design/Task 或标记 blocked；仅参数未确认时继续生成固定组件和 `permissionList` 对象数组，并记录 replacement / handoff risk。

# 权限按钮 - 设计与契约

## 阅读路由
- 权限按钮 设计、契约冻结、question gate、事实确认或资源选择时读取。

## Button Contract
每个业务按钮先判定：
- `permissionRequirement=required`：必须使用固定 `ButtonPermission`，即使权限码只是 `generatedCandidate`。
- `permissionRequirement=not-applicable`：必须有 FDS/TDS、用户确认或项目基线 reason，可使用普通 `Button`。
- `permissionRequirement=unknown`：先回到 Design/Task 补 Button Contract，不得误报 production-ready。

缺 confirmed 权限码不是降级普通 `Button` 的理由。若 route path、action 清单和编码规则足够，使用 `generatedCandidate permissionCode` 并保留平台登记/确认项；若只有权限码、`permissionList` 候选值或平台登记证据缺失，不得把 `permissionRequirement=required` 改成普通 `Button`、disabled/no-op、占位入口或隐藏 required 动作。只有缺少固定权限组件来源、Provider 契约无法判定、动作来源未确认或无法形成候选编码基础事实时，才回 Contract Check / Design 补契约。

`ButtonPermission` 不是样式统一工具。不得因为按钮间距、垂直对齐、外观不一致或相邻按钮使用了权限组件，就把 Button Contract 未判定为 required 的普通按钮改成 `ButtonPermission`；这类视觉问题应回到所在 toolbar/Table buttons 的 DOM、组件 props 和局部样式合同处理。

## Contract
实现或审查必须确认：
- `ButtonPermission` 的源码或类型声明。
- `PermissionProvider` / `context.permission.check` 的入参字段；HZERO/prm 默认按 `permissionList` 对象数组处理。
- 权限码数组结构、字段名和 `meaning/type` 要求。
- Button props 透传边界，例如是否支持 `color`、`type`。

默认权限载荷必须是 `permissionList={[{ code: PERMISSION_CODE, type: 'button', meaning: '...' }]}` 或等价对象数组；不得生成 `permissionList={[PERMISSION_CODE]}`、`permissionList={['hzero.xxx.action']}`、`permissionList={[{ permissionCode }]}`、缺 `code/type` 的数组，或把 `codeList={[PERMISSION_CODE]}` 传给固定 `ButtonPermission`。`codeList` 只有在目标组件源码、类型声明和 Provider 入参都确认消费 `codeList` 时才可作为项目特例，并必须记录 evidence；prm 包或 `PermissionProvider` 读取 `permissionList` 的场景不得使用 `codeList`。旧组件 props 不得无证据迁移到固定组件，包括 `funcType`、`ButtonColor`、旧版字符串数组 `permissionList` 形态等。

导入/导出标准组件自带按钮时，权限绑定和按钮形态归 `front-hzero-import-export` 的组件 props 合同处理：导入使用 `buttonProps.permissionList`，导出使用 `otherButtonProps.permissionList`；头部/页面级导入导出默认使用 `ButtonColor.primary`、`type="c7n-pro"` 或 confirmed wrapper 页面级按钮形态，只有行内导入/导出、链接态入口或 UI Contract 明确弱按钮时才允许 `type="text"` 并记录来源。不要为了套用 `ButtonPermission` 再包一层 `HeaderImportAction` / `HeaderExportAction` / 本地权限按钮封装；也不要把标准组件的按钮配置 props 误判为本 skill 禁止的旧权限按钮入口。

## Fixed Import
HZERO/C7N required 权限按钮固定使用：

```ts
import { Button as ButtonPermission } from 'components/Permission';
```

禁止用以下入口替代：
- `import { ButtonPermission } from 'components/Permission'`，该模块导出 `Button` 而不是 `ButtonPermission`，会让组件为 `undefined` 并触发 React #130 白屏。
- `@common/components/PermissionButton`
- 业务/模块前缀包装的 `*PermissionButton` 薄封装
- `PermissionButton || Button` fallback
- required 业务动作直接使用普通 `Button`
- 只因相似页面存在旧写法而采用本地 wrapper

`components/Permission` 的 `Button as ButtonPermission` 是固定标准坐标，不作为项目证据探索项处理。实现、审查和验证只检查是否按该坐标消费；不得输出“目标缺导出”“待确认 importPath”或切换旧组件 / 项目 wrapper。

## Generated Candidate Boundary
- required 动作缺 confirmed 权限码时，优先按 route path、菜单/页面 code、action 名称和项目权限编码规则生成 `generatedCandidate permissionCode`。
- generatedCandidate 权限码必须进入 Button Contract、Compliance Manifest、Verification 和 Handoff / 平台登记项；生产状态保持 partial，不得声明权限资产 confirmed。
- generatedCandidate 权限码不影响组件形态：代码仍必须使用固定 `ButtonPermission`，并填入 `permissionList` 对象数组；`codeList` 仅限目标源码和 Provider 均 confirmed 的项目特例。
- 不得把权限码缺口展示成页面文案，例如“权限码待确认”“replacement”“仅保留权限合同”；这些只能出现在设计/交付产物中。

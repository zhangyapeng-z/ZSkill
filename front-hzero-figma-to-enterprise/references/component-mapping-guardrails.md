# Figma 组件映射门禁

## 目标
把 Figma / 截图 / PRD 中识别出的视觉结构，提前转成 HZERO 与 Choerodon 可继承的 UI Contract seeds。Figma 阶段只生成候选和约束，不确认接口、字段名、权限码、route、组件 API 或生产可运行实现。

## 使用位置
- PageSchema 形成后、输出 HZERO / Choerodon 映射前必须执行。
- 输出给 `frontend-design-agent`、`frontend-task-agent` 或 `frontend-auto-agent` 的 handoff 中必须携带 `uiContractSeeds`。
- 若 Figma 证据不足，只能输出 `candidate` 或 `missing`，不得把视觉推断写成 `confirmed`。

## UI Contract Seeds Schema
```ts
type UIContractSeed = {
  regionId: string;
  sourceEvidence: 'figma' | 'screenshot' | 'prd' | 'prototype' | 'mixed';
  evidenceState: 'confirmed' | 'inferred' | 'missing';
  layoutAuthority: 'user-confirmed' | 'figma-pageschema' | 'project-baseline' | 'fds-ui' | 'backend-tds-hint' | 'missing' | 'not-applicable';
  businessAuthority: 'user-confirmed' | 'fds-tds-api' | 'project-business-evidence' | 'figma-visible-copy' | 'missing' | 'not-applicable';
  conflictResolution: 'none' | 'figma-layout-business-covered' | 'business-contract-overrides-visual-copy' | 'needs-question' | 'blocked' | 'not-applicable';
  targetStack: 'hzero' | 'choerodon' | 'hzero-choerodon' | 'custom' | 'unknown';
  recommendedComponent: string;
  requiredRules: string[];
  forbiddenPatterns: string[];
  downstreamOwner: 'frontend-design-agent' | 'frontend-auto-agent' | 'user-confirmation';
  openContracts: string[];
};
```

## 来源优先级
- UI 显示布局使用 `layoutAuthority` 判定，优先级为用户明确确认 > Figma/PageSchema confirmed > 目标工程同类页面基线 > FDS UI 描述 > 后端 TDS 前端提示。
- 业务契约使用 `businessAuthority` 判定，优先级为用户明确确认 > FDS/TDS/API/DTO/权限/平台协议 > 目标工程业务证据 > Figma 可见文案。
- 若 Figma 与 FDS/TDS/API 不一致，seed 必须记录 `conflictResolution`。仅视觉呈现冲突且业务能力完整覆盖时可写 `figma-layout-business-covered`；字段语义、接口、权限、route/menu 或验收受影响时写 `needs-question` 或 `blocked`。
- 不允许用 FDS/TDS 的描述性 UI 文案覆盖 confirmed Figma 布局，也不允许用 Figma 文案推导生产字段、权限或接口。

## Choerodon 映射硬规则
- `list` 或包含表格查询的页面：默认生成 `DataSet + Table + filterBar` 候选，并要求下游按 enumProvenance 选择 `TableQueryBarType.filterBar` 等 enum 形态；除非项目证据证明当前工程不支持。
- Figma 出现“搜索框 / 关键字搜索 / 模糊查询 / 模糊搜索”时，输出 `queryBarProps.fuzzyQuery=true` 候选；参数名仍为 `missing`，等待接口或业务契约确认。
- 查询字段必须输出 QueryFields Schema 候选：label、candidateType、组件候选、是否多选、是否允许清空、默认展示状态和 `queryFieldsLimit` 候选。
- 表格列必须输出字段顺序映射候选。操作列必须作为最后一列，右侧固定使用 `ColumnLock.right`；禁止输出 `lock: true` / `lock: 'right'`。
- 详情只读字段默认映射为 `Form + Output`；数组型详情区块映射为 `Table`；不得建议 `div/grid` 手写只读详情。
- 弹框、抽屉、Popover、Dropdown 等 overlay 必须输出层级规则：mask / z-index / portal / 不透明背景 / 关闭后无遮挡；页面 Header、固定表头、固定列或列表内容穿透到 overlay 上方属于 blocking 风险。
- 弹框和抽屉优先输出项目既有 `Modal.open({ ... })` / `Modal.open({ drawer: true, resizable: true, ... })` 或项目封装候选；未查到工程证据前只标 `candidate`，不得确认 JSX Modal 或自绘 Drawer。
- 业务按钮候选必须记录 `front-hzero-permission-button` 固定 `ButtonPermission`；权限码保持 `missing`，不得改用项目权限按钮封装或旧 PermissionButton。

## HZERO 映射硬规则
- Figma 页面结构只能生成 HZERO 页面容器、i18n 文案清单、权限动作清单和平台能力候选；不得推导 route path、menu code、permission code、model namespace 或 service 函数。
- HZERO + Choerodon 页面必须先输出 HZERO 边界：页面容器、route/menu 状态、权限按钮位置、i18n namespace 状态、平台能力边界；再输出 Choerodon 内容区候选。
- route prefix、菜单 path、菜单 code、按钮 code、`templateCode`、`customizedCode` 和 i18n namespace 未确认时只能标 `generatedCandidate` 或 `missing`，不得标 `confirmed`。
- 上传、导入、导出、附件、LOV、lookup、文件预览只能输出平台能力候选和待确认协议，不得从 Figma 文案编造 `bucket`、`templateCode`、`lovCode`、`lookupCode` 或 endpoint。

## Mock / Demo 边界
- Figma 阶段不能把“页面可展示”当作 mock-request 契约。
- 若建议 demo 或临时契约，列表/查询型 demo 默认输出 `queryMode=mock-request` 候选。
- 若目标工程存在 `public/` 或等价静态资源目录，必须提示可创建 requestable seed JSON；“没有现成 mock 文件”不能直接降级为 `local-filter`。
- `service/mock + loadData`、模块内存数组、`src/utils/mock.ts` 或组件内 filter 必须作为 blocking cleanup 记录，不能作为实现候选，也不能标成 `mock-request`。
- 下游 Verification 必须记录 mock request 的 URL、method、query/body、origin 和 DataSet transport 或项目 request adapter 证据。

## 输出要求
Figma handoff 必须包含：
1. UI 设计回读表：列表、筛选、按钮、详情区块、字段顺序和交互入口分别来自 Figma/PageSchema 哪个区域。
2. UI Contract Seeds：每个主要区域至少一条 seed，说明推荐组件、layoutAuthority、businessAuthority、conflictResolution、必须遵守规则、禁止反模式和下游 owner。
3. Component Contract Gaps：字段名、接口、权限、route、LOV/lookup、Attachment、组件 API、mock-request 证据缺口。
4. Anti-pattern Warnings：命中或潜在命中的手写查询 Form、自绘 Drawer/Modal、`div/grid` 详情、`lock=true`、local-filter 伪装 mock-request 等风险。

## 交接规则
- Choerodon 相关 seed 必须交给 `frontend-design-agent` 形成 DataSet/component Contract，并由下游阶段 owner 显式继承。
- HZERO route/menu/permission/runtime 相关 seed 必须交给 `frontend-design-agent` 形成对应 Contract，并由下游阶段 owner 显式继承。
- 完整页面交付必须回到 `frontend-auto-agent`，由 Contract Check、Frontend Design、Task Breakdown、Implementation、Review、Verification 和 Handoff 继续闭环。

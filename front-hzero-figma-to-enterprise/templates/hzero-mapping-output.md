# HZERO 映射输出模板

## 使用场景
用于 PageSchema 已形成，目标技术栈为 HZEROJS 企业页面、HZERO + Choerodon DataSet 或项目 HZERO 封装组件，需要把 Figma 设计结构转成 HZERO 页面容器、权限、i18n、数据层和平台能力边界。

## 输入摘要
1. PageSchema 类型：`list` / `form` / `formWithTable` / `detail` / `treeList` / `uploadImport` / `modal` / `drawer` / `componentShowcase` / `unknown`。
2. 主要区域：header、toolbar、search/filterBar、form、table、tabs、modal、drawer、upload。
3. 证据状态：confirmed / inferred / missing。
4. Framelink 证据：组件证据、图片/SVG 证据、占位文案、组件展示节点。

## 映射总则
1. HZERO 拥有工程位置、路由、菜单权限、页面容器、i18n、权限按钮和平台协议边界。
2. HZERO + Choerodon 页面必须先确定 HZERO 容器和权限边界，再交给 Choerodon DataSet/Form/Table 实现内容区。
3. 不从 Figma 页面标题、按钮文案或组件名推导 route path、menu code、permission code、service 函数、model namespace 或 i18n key。
4. 上传、导入、导出、附件、值集、LOV 和文件预览只输出候选能力和待确认项，不写 bucket、templateCode、lookupCode、lovCode、endpoint 或租户规则。
5. 项目已有页面容器、权限按钮、表格封装、筛选条或上传封装优先于通用 HZERO/Choerodon 候选。
6. HZERO 映射必须输出 UI Contract seeds，明确 route/menu/permission/i18n/platform 能力是 `confirmed`、`generatedCandidate`、`inferred` 还是 `missing`。
7. HZERO + Choerodon 页面必须把 HZERO 边界 seed 和 Choerodon 内容区 seed 分开输出，避免 route/permission 与 DataSet/Form/Table 责任混在一起。
8. UI 显示布局以 Figma/PageSchema confirmed 优先；业务契约以 FDS/TDS/API/用户确认优先。冲突必须输出 `uiBusinessConflicts`，不得从 Figma 反推 route/menu/permission 或让后端 TDS 覆盖 Figma 布局。

## Page Type 映射
| PageSchema 类型 | HZERO 页面方案 | 数据层建议 | 输出边界 |
| --- | --- | --- | --- |
| `list` | `Header + Content` 或 `PageHeaderWrapper` + 查询区 + 表格 + 工具栏 | service/model 或 HZERO + Choerodon DataSet | 缺接口时不写 service/model 或 DataSet transport |
| `form` | 页面容器 + 表单区 + 底部/顶部操作 | service/model 或 DataSet 表单 | 缺字段契约时只输出字段候选和 i18n 文案清单 |
| `formWithTable` | 页面容器 + 主表单 + 明细表格 + 页签/卡片 | 主数据层 + 明细数据层；可交给 Choerodon DataSet | 缺主从协议时不写提交/分页/行操作代码 |
| `detail` | 页面容器 + 只读详情 + 操作区 + 关联表格/附件 | 读取 service/model 或 readonly DataSet | 缺读取接口时只输出详情区域结构 |
| `treeList` | 页面容器 + 左树右表/树表 | 树接口或 DataSet tree，字段待确认 | 不从视觉树推导 id/parent/children 字段 |
| `uploadImport` | 页面容器 + 上传/导入/导出/结果区 | HZERO 平台上传/导入导出协议 | 不写 bucket、UUID、templateCode、endpoint |
| `modal` / `drawer` | HZERO 页面动作触发弹窗/抽屉 | 弹层 service/model 或 DataSet | 打开来源、权限、提交和刷新策略待确认 |
| `componentShowcase` | 组件/状态映射表或组件文档页 | 无业务数据层 | 不生成业务页面、权限码或 service/model |

## 输出结构
```md
## HZERO 映射结论
- 页面类型：
- 推荐路线：HZERO service/model / HZERO + Choerodon DataSet / 项目自定义 HZERO 封装
- 是否可生成代码：可生成 / 仅映射说明 / 暂停补契约

## 页面容器
- 候选容器：Header + Content / PageHeaderWrapper / 项目封装
- 证据：相似页面 / 项目源码 / 待确认
- PageSchema 区域映射：header、content、card、tabs、table、modal、drawer
- UI 来源优先级：layoutAuthority / businessAuthority / conflictResolution

## UI Contract Seeds
| PageSchema 区域 | 推荐 HZERO / HZERO+Choerodon 候选 | layoutAuthority | businessAuthority | conflictResolution | 必须规则 | 禁止反模式 | 下游 owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| page/container | Header + Content / PageHeaderWrapper / 项目封装 | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / needs-question / blocked | 页面容器、目录、模块边界必须由项目证据确认 | Figma title 推导 route 或目录 | frontend-design-agent |
| route/menu | route prefix / menu path / menu code 候选 | not-applicable | fds-tds-api / project-business-evidence / missing | none / needs-question / blocked | 未确认只能 generatedCandidate 或 missing | 宣称 confirmed、registerRegex catch-all | frontend-design-agent |
| permission/actions | PermissionButton / Permission / 项目权限封装 | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / needs-question / blocked | 菜单权限和按钮权限分开记录 | 按钮文案生成权限码、菜单权限等同按钮权限 | frontend-design-agent |
| i18n/text | 文案清单 + i18n namespace 候选 | figma-pageschema / missing | fds-tds-api / project-business-evidence / missing | none / business-contract-overrides-visual-copy / needs-question | key/namespace 遵循项目证据 | 从 Figma 占位文案批量生成真实 key | frontend-design-agent |
| content/table/form | HZERO 边界 + Choerodon DataSet/Form/Table | figma-pageschema / project-baseline / missing | fds-tds-api / missing | none / figma-layout-business-covered / needs-question | HZERO 负责容器/权限/i18n，Choerodon 负责内容组件事实 | 一个组件混管 route、权限、DataSet、UI 状态 | frontend-design-agent |
| platform | upload/import/export/LOV/lookup/Attachment 候选 | figma-pageschema / missing | fds-tds-api / missing | none / needs-question / blocked | 协议、bucket、templateCode、lovCode 等待确认 | 从视觉图标编造平台协议 | frontend-design-agent |

## i18n 与文案
| Figma 文案 | 用途 | i18n 状态 | 待确认 |
| --- | --- | --- | --- |
|  | 页面标题/按钮/表头/提示 | confirmed/inferred/missing | i18n namespace/key |

## 权限映射
| Figma 操作 | HZERO 权限候选 | 证据状态 | 待确认 |
| --- | --- | --- | --- |
| 主按钮/工具栏按钮/行操作 | `front-hzero-permission-button` 固定 `ButtonPermission` | missing | route path、menu code、button action code、平台配置状态 |

## 数据层边界
- service/model 路线：
  - service 文件：待确认
  - model namespace/effects：待确认
  - request URL/method/params/response：待确认
- HZERO + Choerodon DataSet 路线：
  - HZERO 负责：容器、路由、权限、i18n、平台协议
  - Choerodon 负责：DataSet、Form/Table、Lov/Attachment 组件事实

## 平台能力
- 上传/附件：
- 导入/导出：
- 值集/LOV：
- 文件预览/外部集成：
```

## 可生成范围
可生成：
1. HZERO 页面容器、布局区域和页面壳层的映射说明。
2. PageSchema 区域到 Header/Content/Card/Tabs/Form/Table/Modal/Drawer 的结构映射。
3. 文案清单和 i18n 待确认项。
4. 权限动作清单和 permission 待确认项。
5. service/model 或 DataSet 的边界说明。
6. UI Contract seeds 和 HZERO/Choerodon 责任分界。

暂不生成：
1. 未确认 route path、menu code、permission code。
2. 未确认 i18n namespace/key。
3. 未确认 service URL、method、params、response、model namespace/effects。
4. 未确认 bucket、UUID、templateCode、lookupCode、lovCode。
5. 从 Figma 占位文案推导的字段名、权限动作或接口函数名。
6. 未经 HZERO route/menu/permission/i18n 证据确认的生产可运行注册。

## componentShowcase 输出
当 PageSchema 类型为 `componentShowcase`：
1. 输出 Figma 组件/状态/变体到 HZERO 或项目封装组件候选的映射表。
2. 优先搜索项目是否已有表格、查询、表单、上传、弹窗、Tag、Tabs、Tree、步骤条等封装。
3. 不生成业务 route、permission、service/model 或 DataSet。
4. 可建议沉淀到 `references/component-mapping.md`，作为后续业务页面映射依据。

## 交接到 front-hzero-enterprise-page
后续由 `front-hzero-enterprise-page` skill 确认：
1. 页面目录、路由和菜单权限。
2. `Header + Content`、`PageHeaderWrapper` 或项目页面容器。
3. `intl.get().d()`、`formatterCollections` 和 i18n namespace。
4. `front-hzero-permission-button` 固定 `ButtonPermission`，并确认权限码入参契约。
5. request/service/model、上传/导入/导出、值集/LOV 和平台协议。

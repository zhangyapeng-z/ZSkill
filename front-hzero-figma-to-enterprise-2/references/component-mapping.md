# 组件映射参考

## 目录
- 映射原则
- 组件映射优先级
- 常见 Figma 到组件候选
- 展示节点规则
- 表格转置规则

## 映射原则
- 优先映射到已有业务抽象，不重复造轮子。
- 先确认组件 API，再生成调用代码。
- 视觉相似不等于业务等价；字段协议和数据来源必须单独确认。
- 复杂页面先生成 PageSchema，再映射组件。
- Figma 只产出组件候选和置信边界；最终组件调用必须再经过项目自定义组件/HZERO/Choerodon 的组件决策。
- PageSchema 形成后必须按 `component-mapping-guardrails.md` 生成 UI Contract seeds，避免下游只拿到泛化的组件候选。

## 组件映射优先级
1. 项目自定义组件：先从项目源码确认名称、导入路径、props、事件、children/render hook、数据源、权限、i18n、loading、分页和上传等内置能力。
2. HZERO 页面/封装：页面容器、国际化、权限、service/model、上传/导入/导出和值集/LOV 都必须回到 HZERO 平台契约。
3. Choerodon UI / Pro：业务表单、表格、查询、提交、Lov、Attachment、Modal/Drawer 优先 `choerodon-ui/pro` 和 DataSet-first。
4. 原生 HTML/CSS：只用于纯布局、装饰、说明文本、分隔线和图标占位，不能承载业务协议。

项目自定义组件优先搜索：
- `BizTable`、`CommonTable`、`SearchTable`、`ProTableWrapper`。
- `SearchForm`、`QueryForm`、`AdvancedSearch`、`FilterPanel`。
- `DrawerForm`、`ModalForm`、`DetailPanel`、`PageContent`。
- `PermissionButton`、`AuthorizedButton`、`ImportButton`、`ExportButton`、`AttachmentPanel`。

## 常见 Figma 到组件候选
| Figma 形态 | 候选组件 | 必须确认 |
| --- | --- | --- |
| 主按钮/次按钮 | HZERO Permission/Button 或 Choerodon Button | 权限、动作、loading |
| 查询输入 | TextField / 自定义查询组件 | 字段名、接口参数 |
| 下拉 | Select / SelectBox | lookupCode/options 来源 |
| 对象选择 | Lov / 自定义 Lov | lovCode、返回对象、bind |
| 日期范围 | DatePicker range / 自定义日期范围 | 参数名、格式、时区 |
| 表格 | Table / 自定义 Table | columns、分页、排序、操作列 |
| 弹窗 | Modal / ModalProvider | 打开来源、提交和关闭生命周期 |
| 抽屉 | Drawer / 自定义 DrawerForm | 宽度、提交、详情/编辑模式 |
| 附件 | Attachment / 自定义附件组件 | bucket、UUID、权限、提交粒度 |

## UI Contract seeds
组件映射输出不能只写“候选组件”。每个主要区域必须补一条 seed：
- 推荐组件：项目自定义组件、HZERO 封装或 Choerodon Pro 组件候选。
- 必须规则：例如 `Table + filterBar` 语义、`fuzzyQuery` 候选、行操作列右锁定、`Form + Output`、overlay 层级规则、PermissionButton 边界；涉及 `queryBar/lock/labelLayout/color/funcType` 等组件 enum-like props 时必须输出 enumProvenance，并由下游选择 `TableQueryBarType.*`、`ColumnLock.*`、`LabelLayout.*`、`ButtonColor.*`、`FuncType.*` 等 enum。普通业务列只有在 Figma/PageSchema、UI Contract 或项目 confirmed baseline 明确要求固定时才输出固定列 seed。
- 禁止反模式：手写查询 Form、自绘 Drawer/Modal、`div/grid` 详情、行操作列用 `lock=true` 冒充右锁定、local-filter 伪装 mock-request。
- 下游 owner：`frontend-design-agent`、`frontend-auto-agent` 或用户确认；实现、审查和验证由对应阶段 owning agent 承接。
- open contracts：字段名、接口、权限、route、LOV/lookup、Attachment、mock-request 证据等缺口。

Figma 或截图只能把 seed 标为 `candidate` / `inferred` / `missing`，不能因为视觉形态相似就标为 HZERO 或 Choerodon API `confirmed`。

候选到实现的判定：
- confirmed：项目已有组件 API、HZERO 平台契约或 Choerodon 组件事实已确认，可生成调用代码。
- candidate：只由视觉形态、组件名或 PageSchema 推得，只能输出映射建议和待确认项。
- rejected：视觉相似但业务语义不匹配，或会绕过 DataSet、权限、上传协议、页面容器、项目封装。

设计转代码输出组件映射时，应包含推荐组件、候选原因、需要确认的 API/协议、被排除组件及原因。不要把 candidate 写成可运行 import 或 props。

## 展示节点规则
- 设计系统、组件规范、showcase 节点不能直接当作业务页面；它们只提供组件族、视觉状态和布局候选。
- `Label`、`Button`、`Table title`、`Table text`、`字段一`、`操作1` 等展示文案不能生成字段名、权限动作、接口参数或 i18n key。
- required、disabled、hover、selected、error、success 等视觉状态只能作为候选状态；真实校验、禁用规则、业务枚举和错误码必须由业务契约确认。
- 表单/查询/选择器展示节点可以确认控件候选，不确认 field name、lookupCode、lovCode、options 来源、返回对象或提交值结构。
- 导航、步骤条、面包屑、分页器和菜单展示节点不能推导 route path、menu code、permission code、分页协议或流程状态机。
- 数据展示、Tag、Tree、Tabs、Collapse、Statistic、Card、List 等展示节点不能推导数据来源、业务状态码、跳转路径或权限策略。
- 反馈、通知、气泡确认、Modal/Drawer 展示节点只能确认结构和视觉候选；触发时机、确认/取消事件、权限、接口和刷新策略必须另行确认。
- Modal、Drawer、Popover、Dropdown 等 overlay 展示节点必须额外记录层级 seed：mask、z-index、portal、不透明背景和关闭后无遮挡；Header、固定表头、固定列或列表内容穿透到 overlay 上方属于 blocking 风险。
- 上传、图片、文件列表和 Attachment 展示节点只能确认组件候选；bucket、UUID 字段、上传 action、预览/下载协议和提交粒度必须另行确认。

## 表格转置规则
- 如果 Figma 表格由多个列 frame 组成，且每列包含 `表头` + 多个 `表格内容`，生成代码时必须转为横向 `columns` 数组。
- 列标题为 `Table title` 时，只能生成占位列摘要，不生成真实 `name`。
- 重复 `Table text` 只能用于判断行高、密度和列数，不作为 mock data 写入业务代码。
- 工具栏 icon 按钮只确认操作位存在；刷新、设置、更多等动作必须从 icon 名称、组件名和项目约定共同确认。
- 行内编辑、树形、拖拽、禁用行、排序和筛选只能作为能力候选；字段、保存协议、树结构、排序/筛选参数和操作权限必须由接口或项目证据确认。

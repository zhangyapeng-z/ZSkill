# PageSchema 输出模板

## 设计证据
1. 来源：Figma / 截图 / PRD / 混合。
2. MCP 工具：Framelink / Figma API / 手工 / 未确认。
3. `selectionUrl`：如果适用。
4. `fileKey`：如果适用。
5. `nodeId`：如果适用，使用标准 `2:2282` 格式。
6. 输入格式：JSON / Framelink JSON wrapper / YAML-like / 截图 / 文本。
7. 读取状态：成功 / 失败 / 降级。
8. `figmaFetchStatus`：success / partial / rate-limited-429 / permission-denied / node-not-found / failed / cache-only / not-applicable。
9. `figmaFetchError`：code / message / attemptedCount / retryAfter。
10. `figmaRetryPlan`：是否需要重试、分批目标、建议等待时间、是否可用缓存继续。
11. `figmaPartialCoverage`：已读取节点、未读取节点、覆盖说明。
12. `figmaErrorNormalization`：rawErrorShape / rawErrorExcerpt / normalizedReason；429 限流必须统一 normalizedReason=rate-limit。

## 结构识别
1. 页面类型：`list` / `form` / `formWithTable` / `detail` / `masterDetail` / `treeList` / `dashboard` / `uploadImport` / `componentShowcase` / `unknown`。
2. 布局：`singleColumn` / `twoColumn` / `multiColumnForm` / `sidebarContent` / `fLayout` / `tabs` / `steps` / `unknown`。
3. 主要区块：header、listHeader、list、listItem、contentCard、emptyPage、tabs、card、form、filterBar、table、modal、drawer。
4. 置信度：high / medium / low。

## PageSchema
```ts
const pageSchema = {
  source: {
    type: 'figma',
    mcpTool: 'framelink',
    selectionUrl: '<figma-selection-url>',
    fileKey: '<fileKey>',
    nodeId: '<nodeId>',
    rawInputFormat: 'json',
    fetchStatus: 'success',
    fetchErrorCode: 'not-applicable',
    fetchErrorMessage: '',
    rawErrorShape: 'not-applicable',
    rawErrorExcerpt: '',
    normalizedReason: 'not-applicable',
    cacheStatus: 'new',
    retryPlan: {
      required: false,
      reason: '',
      attemptedCount: 0,
      nextRetryAfter: '',
      splitTargets: [],
      canContinueFromCache: false,
    },
    partialCoverage: {
      readNodes: [],
      missingNodes: [],
      coverageNote: '',
    },
    evidenceNotes: [],
    imageRefs: [],
    styleEvidence: [],
    componentEvidence: [],
  },
  page: {
    name: '<confirmed or placeholder title>',
    type: 'formWithTable',
    layout: 'tabs',
    confidence: 'high',
  },
  regions: [],
  integration: {
    targetStack: 'unknown',
    route: 'missing',
    permission: 'missing',
    i18n: 'missing',
    dataContract: 'missing',
    assets: 'missing',
  },
  uiSourcePriority: {
    layoutAuthority: 'figma-pageschema',
    businessAuthority: 'missing',
    conflictPolicy: 'do-not-silent-merge',
    uiBusinessConflicts: [],
  },
  uiContractSeeds: [],
  openQuestions: [],
};
```

## UI 设计回读表
| PageSchema 区域 | Figma / 设计证据 | 下游 UI 契约种子 | layoutAuthority | businessAuthority | conflictResolution | 证据状态 | 待确认 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| list/filterBar/table/detail/overlay/actions |  |  | figma-pageschema / project-baseline / fds-ui / missing | fds-tds-api / user-confirmed / missing | none / figma-layout-business-covered / needs-question / blocked | confirmed/inferred/missing |  |

## 组件映射
1. 项目自定义组件候选：列出已从源码确认的组件；未确认则写“未确认”。
2. HZERO 映射：页面容器、权限、i18n、service/model 边界。
3. Choerodon 映射：DataSet、Form、Table、queryFields/filterBar、Modal/Drawer。
4. 原生兜底：只列纯布局和装饰部分。

## UI Contract Seeds
每个主要区域必须按 `references/component-mapping-guardrails.md` 输出 seed：

```ts
const uiContractSeeds = [
  {
    regionId: '<region-id>',
    sourceEvidence: 'figma',
    evidenceState: 'inferred',
    layoutAuthority: 'figma-pageschema',
    businessAuthority: 'missing',
    conflictResolution: 'none',
    targetStack: 'hzero-choerodon',
    recommendedComponent: '<recommended component candidate>',
    requiredRules: [],
    forbiddenPatterns: [],
    downstreamOwner: 'frontend-design-agent',
    openContracts: [],
  },
];
```

来源优先级：
1. UI 显示布局：用户明确确认 > Figma/PageSchema confirmed > 目标工程同类页面基线 > FDS UI 描述 > 后端 TDS 前端提示。
2. 业务契约：用户明确确认 > FDS/TDS/API/DTO/权限/平台协议 > 目标工程业务证据 > Figma 可见文案。
3. Figma 与 FDS/TDS/API 冲突时必须写入 `uiBusinessConflicts`，不得静默合并。

常见 seed：
1. 列表查询：`DataSet + Table + filterBar`；关键字/模糊搜索出现时追加 `queryBarProps.fuzzyQuery=true` 候选，并记录 enumProvenance 以决定 `TableQueryBarType.filterBar` 等 enum 形态。
2. 查询字段：输出 QueryFields Schema 候选，包含组件类型、是否多选、是否允许清空、默认展示状态和 `queryFieldsLimit` 候选。
3. 表格列：输出字段顺序候选；操作列最后一列且 `ColumnLock.right`；禁止 `lock: true` / `lock: 'right'`。
4. 详情只读：单对象字段 `Form + Output`；数组字段 `Table`；禁止 `div/grid` 手写详情。
5. F 型布局：顶部 Header/ListHeader、左侧 List、右侧 ListItem/ContentCard/EmptyPage；下游必须引用 `front-hzero-enterprise-page` 的 f-layout scenario reference，并记录 `_LOCATED_DATA_`、列表折叠/宽度、详情保存后刷新定位和滚动吸附候选。
6. overlay：Modal / Drawer / Popover / Dropdown 必须包含 mask、z-index、portal、不透明背景和关闭后无遮挡检查；层级穿透标为 blocking 风险。
7. HZERO：route、menu、permission、i18n、platform 能力只输出候选或缺口，不从 Figma 推导真实编码。
8. mock/demo：列表/查询 demo 必须是 `queryMode=mock-request`；`service/mock + loadData`、模块内存数组、`src/utils/mock.ts` 或组件内 filter 必须标为 blocking cleanup，不作为降级实现。

## Framelink 证据
1. `get_figma_data`：记录是否读取、目标节点是否精确、是否存在过大或截断风险。
2. `download_figma_images`：记录是否需要下载图片/SVG、下载状态和项目资源落地状态。
3. 样式证据：列出可确认的颜色、字号、间距、圆角、阴影；未映射到项目 token 前保持 inferred。
4. 组件证据：列出 Figma 组件名/属性和项目组件映射状态。
5. 429 限流证据：必须记录 `figmaFetchStatus=rate-limited-429`、`figmaFetchErrorCode=429`、`rawErrorShape`、`rawErrorExcerpt`、`normalizedReason=rate-limit`、已尝试次数、是否命中缓存、已读取/未读取节点和 retryPlan；该状态必须写入 `figma-cache/readme.md`、`page-schema.json` 和 `frontend/index.md`。

## 可生成范围
1. 可直接生成：已确认结构、静态布局、非业务装饰、PageSchema。
2. 仅映射说明：缺接口但结构明确的表单、表格、卡片、Tab，只输出 PageSchema / UI Contract seeds / 待确认项。
3. 暂不生成：真实接口、权限码、字段名、LOV/值集、上传协议、组件 API 未确认部分。

## 待确认项
1. 目标技术栈和目标模块路径。
2. 字段清单、字段名、字段类型和校验规则。
3. 接口契约、分页/排序/筛选协议。
4. 权限码、菜单入口、i18n key。
5. 项目自定义组件 API。

## 验证方式
1. 结构验证：PageSchema 是否覆盖主要区块。
2. 规则验证：是否忽略占位文案、是否转置表格、是否未编造协议。
3. 视觉验证：按 `references/visual-verification.md` 建立视觉基准、截取本地实现图并记录差异。
4. 工程验证：发现项目 scripts 后运行 lint、typecheck/tsc、test、build 中可行命令。

# PageSchema 模板

这份模板用于把 Figma、截图、PRD 或原型整理成可交接的页面结构证据。下面的英文类型名是代码字段，保留不翻译；填写说明和结论应使用易懂中文。PageSchema 只能证明视觉结构和交互线索，不能替代真实接口、字段、权限或组件 API 契约。

```ts
type EvidenceState = 'confirmed' | 'inferred' | 'missing';
type FigmaFetchStatus = 'success' | 'partial' | 'rate-limited-429' | 'permission-denied' | 'node-not-found' | 'failed' | 'cache-only' | 'not-applicable';

type PageSchema = {
  source: {
    type: 'figma' | 'screenshot' | 'prd' | 'prototype' | 'mixed';
    mcpTool?: 'framelink' | 'figma-api' | 'manual' | 'unknown';
    selectionUrl?: string;
    fileKey?: string;
    nodeId?: string;
    rootNodeName?: string;
    rawInputFormat?: 'json' | 'framelinkJsonWrapper' | 'yamlLike' | 'screenshot' | 'text' | 'unknown';
    fetchStatus?: FigmaFetchStatus;
    fetchErrorCode?: '429' | '403' | '404' | 'timeout' | 'unknown' | 'not-applicable';
    fetchErrorMessage?: string;
    rawErrorShape?: 'http-status' | 'json-error' | 'tool-exception' | 'stderr-text' | 'empty-with-message' | 'empty-response' | 'unknown' | 'not-applicable';
    rawErrorExcerpt?: string;
    normalizedReason?: 'rate-limit' | 'permission' | 'not-found' | 'timeout' | 'parse-failed' | 'unknown' | 'not-applicable';
    cacheStatus?: 'new' | 'updated' | 'reused' | 'missing' | 'not-written';
    retryPlan?: {
      required: boolean;
      reason?: string;
      attemptedCount?: number;
      nextRetryAfter?: string;
      splitTargets?: string[];
      canContinueFromCache?: boolean;
    };
    partialCoverage?: {
      readNodes?: string[];
      missingNodes?: string[];
      coverageNote?: string;
    };
    evidenceNotes: string[];
    imageRefs?: Array<{
      nodeId?: string;
      name?: string;
      type: 'image' | 'svg' | 'icon' | 'unknown';
      status: 'downloaded' | 'referenced' | 'missing';
      path?: string;
      notes?: string[];
    }>;
    styleEvidence?: Array<{
      name: string;
      value?: string;
      evidence: EvidenceState;
      notes?: string[];
    }>;
    componentEvidence?: Array<{
      figmaName: string;
      componentType?: string;
      mappedTo?: string;
      evidence: EvidenceState;
      notes?: string[];
    }>;
  };
  page: {
    name: string;
    type: 'list' | 'form' | 'formWithTable' | 'detail' | 'masterDetail' | 'treeList' | 'dashboard' | 'uploadImport' | 'componentShowcase' | 'unknown';
    layout: 'singleColumn' | 'twoColumn' | 'multiColumnForm' | 'sidebarContent' | 'fLayout' | 'tabs' | 'steps' | 'unknown';
    confidence: 'high' | 'medium' | 'low';
  };
  regions: Array<{
    id: string;
    type: 'header' | 'search' | 'filterBar' | 'toolbar' | 'table' | 'form' | 'detail' | 'modal' | 'drawer' | 'tabs' | 'tree' | 'upload' | 'card' | 'listHeader' | 'list' | 'listItem' | 'contentCard' | 'emptyPage' | 'custom';
    title?: string;
    evidence: EvidenceState;
    fields?: FieldSchema[];
    actions?: ActionSchema[];
    columns?: ColumnSchema[];
    children?: PageSchema['regions'];
  }>;
  integration: {
    targetStack: 'custom' | 'hzero' | 'choerodon' | 'hzero-choerodon' | 'unknown';
    route?: EvidenceState;
    permission?: EvidenceState;
    i18n?: EvidenceState;
    dataContract?: EvidenceState;
    assets?: EvidenceState;
  };
  uiContractSeeds: UIContractSeed[];
  openQuestions: string[];
};

type FieldSchema = {
  label: string;
  name?: string;
  candidateType?: 'string' | 'number' | 'currency' | 'date' | 'dateTime' | 'dateRange' | 'lookup' | 'lov' | 'boolean' | 'attachment' | 'upload' | 'unknown';
  required?: boolean;
  layout?: 'verticalCompact' | 'horizontal' | 'inline' | 'unknown';
  evidence: EvidenceState;
  notes?: string[];
};

type ColumnSchema = FieldSchema & {
  sortable?: boolean;
  filterable?: boolean;
  operation?: boolean;
};

type ActionSchema = {
  label: string;
  role: 'primary' | 'secondary' | 'danger' | 'link' | 'icon' | 'unknown';
  scope: 'page' | 'toolbar' | 'row' | 'form' | 'modal' | 'drawer';
  permission?: EvidenceState;
  behavior?: EvidenceState;
  notes?: string[];
};

type UIContractSeed = {
  regionId: string;
  sourceEvidence: 'figma' | 'screenshot' | 'prd' | 'prototype' | 'mixed';
  evidenceState: EvidenceState;
  targetStack: 'hzero' | 'choerodon' | 'hzero-choerodon' | 'custom' | 'unknown';
  recommendedComponent: string;
  requiredRules: string[];
  forbiddenPatterns: string[];
  downstreamOwner: 'frontend-design-agent' | 'frontend-auto-agent' | 'user-confirmation';
  openContracts: string[];
};
```

## 输出规则
- `name` 可来自 Figma 文案或用户输入；无法确认时使用页面用途描述，不要编造业务实体。
- 字段 `name` 只有在接口、源码或用户明确字段清单确认时填写；否则只填 `label` 和 `candidateType`。
- `source.mcpTool` 使用 Framelink 时填 `framelink`；无法确定时填 `unknown`。
- Figma API / Framelink 命中 429 限流时，`source.fetchStatus` 必须写 `rate-limited-429`，`fetchErrorCode=429`，并填写 `rawErrorShape`、`rawErrorExcerpt`、`normalizedReason=rate-limit`、`retryPlan`、`cacheStatus` 和 `partialCoverage`；不得写 `confirmed`。429 可来自 status code、error body、异常 message 或工具文本输出，不要求工具返回标准 HTTP 响应。
- Figma 工具空失败时，`source.fetchStatus` 必须写 `failed`，`fetchErrorCode=unknown`，`rawErrorShape=empty-response / unknown`，`normalizedReason=unknown`，并填写 `retryPlan`；不得写 `confirmed` 或 `confirmed-from-cache`，除非另有可用缓存证据。
- 当 `source.rawInputFormat` 为 `framelinkJsonWrapper` 时，表示 JSON 的 `data[].text` 内包含 Framelink YAML-like 工具文本；可以生成中等置信度草案，但仍应保留原文件用于回归。
- 当 `source.rawInputFormat` 为 `yamlLike` 时，`page.confidence` 通常只能是 `low`，除非人工补充了结构证据。
- `source.imageRefs` 只记录资源证据和下载状态，不代表资产已经按项目规范落地。
- `source.styleEvidence` 和 `componentEvidence` 只能作为映射线索；真实 token、组件 import 和 props 仍需项目源码确认。
- Figma 占位文案 `Label`、`Button`、`Table title`、`Table text` 不得进入最终业务字段名；只能作为结构证据。
- `uiContractSeeds` 必须按 `references/component-mapping-guardrails.md` 输出。它们是下游设计、任务、实现、审查和验证的约束种子，不是 Figma 阶段确认了组件 API。
- 列表、筛选、表格操作列、详情只读区块、弹框/抽屉/overlay、权限按钮和 mock/demo 至少应各自形成 seed 或明确说明不适用。
- 顶部查询 + 左侧列表 + 右侧详情的 F 型布局必须设置 `page.layout='fLayout'`，并至少输出 `header/listHeader/list/listItem` 区域；右侧详情分组应输出 `contentCard` seed，空态应输出 `emptyPage` seed 或明确不适用。
- `openQuestions` 只列阻塞代码落地的问题，避免把所有细节都变成追问。

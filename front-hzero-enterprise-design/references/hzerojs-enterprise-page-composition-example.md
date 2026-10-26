# HZEROJS Enterprise Page Composition Example

用途：当目标 HZEROJS 子模块缺少可采纳参考模块、参考资产不可读，或相邻模块质量未知时，给 Frontend Design、Task Breakdown、Implementation 和 Review 提供页面域分层示例。本文是结构和边界示例，不确认业务事实。

## 阅读路由
- 需要确定无参考基线时的默认目录结构时读 `File Shape`。
- 需要判断哪些常量应集中收口时读 `constants.ts Boundary`。
- 需要判断 DataSet、页面、组件和 service 的分层边界时按章节顺序继续阅读。

## File Shape

无参考基线下，列表 + 详情 + 头行主从 + 附件 + 导入导出页面默认使用页面域分层：

```text
src/pages/<PageGroup>/
  constants.ts
  index.less # optional; only when Style Necessity Contract confirms local style is required
  stores/
    queryDS.ts
    detailDS.ts
    lineQueryDS.ts
  components/
    LineTable.tsx
    <Feature>Attachment.tsx
    ImportExportActions.tsx # optional; only for multi-entry or wrapperJustification
  List/index.tsx
  Detail/index.tsx
src/services/<feature>Service.ts
src/utils/servicePrefix.ts
platform-locale-keys.json
```

不要在无项目证据时退化为：

```text
src/stores/<feature>DS.ts
src/pages/<PageGroup>/List/index.tsx
src/pages/<PageGroup>/Detail/index.tsx
```

这种形态会把列表查询、详情头、行、状态动作、附件、导入导出和 mock 候选压到少数文件里，降低替换真实 API、Review 和 Handoff 的可控性。

## constants.ts Boundary

`constants.ts` 承接可审查的业务边界：route、prompt、权限码、lookup/lov 候选、状态集合、状态守卫和契约保真元数据。页面不直接散落这些字符串。

```ts
export const FEATURE_ROUTE = '/prm/requisitions';
export const FEATURE_PROMPT = 'hspd.prm.requisition';

export const FIELD_RUNTIME_POLICY = {
  mode: 'canonical-only',
  forbiddenRuntimeAliases: ['requisitionNum', 'approvalStatus', 'applicantDeptName'],
  adapterAliasPolicy: 'service-request-adapter-only',
} as const;

export const OVERLAY_SIZE_CONTRACT = {
  defaultSize: 'small',
  defaultWidth: 520,
  source: 'asset-baseline',
  wideSizePolicy: 'design-or-confirmed-baseline-only',
} as const;

export const DETAIL_COLLECTIONS = {
  lineList: {
    apiField: 'lineList',
    component: 'Choerodon Pro Table',
    rowKey: 'requisitionLineId',
    mockFieldPolicy: 'same-api-field',
    aliasPolicy: 'none',
  },
} as const;

export const PERMISSION_CODES = {
  query: 'prm.requisition.query',
  create: 'prm.requisition.create',
  update: 'prm.requisition.update',
  delete: 'prm.requisition.delete',
  submit: 'prm.requisition.submit',
  withdraw: 'prm.requisition.withdraw',
  import: 'prm.requisition.import',
  export: 'prm.requisition.export',
};

export const LOOKUP_CODES = {
  authorizationStatus: 'HSPD.PRM.APPROVAL_STATUS',
  purchaseType: 'HSPD.PRM.PURCHASE_TYPE',
  urgency: 'HSPD.PRM.URGENCY',
};

export const AUTHORIZATION_STATUS = {
  NEW: 'NEW',
  IN_APPROVAL: 'IN_APPROVAL',
  APPROVED: 'APPROVED',
  REJECTED: 'REJECTED',
  CANCELLED: 'CANCELLED',
} as const;

export const STATUS_ENUM_MAP = {
  authorizationStatus: [
    { code: AUTHORIZATION_STATUS.NEW, meaning: '新建', color: 'default', source: 'FDS/TDS/API' },
    { code: AUTHORIZATION_STATUS.IN_APPROVAL, meaning: '审批中', color: 'processing', source: 'FDS/TDS/API' },
    { code: AUTHORIZATION_STATUS.APPROVED, meaning: '已审批', color: 'success', source: 'FDS/TDS/API' },
    { code: AUTHORIZATION_STATUS.REJECTED, meaning: '已拒绝', color: 'error', source: 'FDS/TDS/API' },
    { code: AUTHORIZATION_STATUS.CANCELLED, meaning: '已取消', color: 'default', source: 'FDS/TDS/API' },
  ],
} as const;

export const LOV_CODES = {
  applicant: 'HSPD.PRM.APPLICANT', // generatedCandidate until platform confirmed
  dept: 'HSPD.PRM.DEPT',
  itemCategory: 'HSPD.PRM.ITEM_CATEGORY',
  item: 'HSPD.PRM.ITEM',
};

const DELETE_ALLOWED_STATUS = new Set<string>([AUTHORIZATION_STATUS.NEW, AUTHORIZATION_STATUS.CANCELLED]);
const SUBMIT_ALLOWED_STATUS = new Set<string>([AUTHORIZATION_STATUS.NEW, AUTHORIZATION_STATUS.REJECTED]);

export const canDelete = (status?: string) => DELETE_ALLOWED_STATUS.has(String(status));
export const canSubmit = (status?: string) => SUBMIT_ALLOWED_STATUS.has(String(status));
export const canWithdraw = (status?: string) => status === AUTHORIZATION_STATUS.IN_APPROVAL;
```

规则：
- 权限码、lookup/lov code 可以是 `generatedCandidate`，但必须集中并进入 replacement；不能散落在按钮和 DataSet 中。
- `FEATURE_PROMPT` / `preCode` 是 i18n namespace 候选。空子模块或无参考页面也必须用 ``intl.get(`${FEATURE_PROMPT}.model.<field>`).d('<fallback>')`` 消费用户可见文案，并同步登记到 `platform-locale-keys.json`；平台未配置时标记 pending，已有 `/hpfm/prompt` 或平台导出证据时标记 confirmed。不要新增局部 `intlPrefix` / `t()` helper 隐藏 key 来源。
- `FIELD_RUNTIME_POLICY` 只是示例形态；实际字段必须来自 FDS/TDS/API/MDS。无参考基线默认 `canonical-only`，旧字段别名只能在 service/request adapter 中转换，不能进入页面、DataSet、Table、Form、guard 或 payload。
- `OVERLAY_SIZE_CONTRACT` 是无参考基线的弹层默认。业务 Modal / Drawer / Overlay 设计未指定宽度时，普通表单 Modal 使用 `size=small` 或项目 small 等价值；详情 Drawer / 高密度只读详情 / 三列及以上 Form 使用项目 Drawer 默认尺寸或 confirmed baseline，并记录 readabilityRisk、Form columns/colSpan 和 `valueOverflowPolicy`；宽框只能来自设计/Figma/PageSchema/项目 confirmed baseline/用户确认。
- `DETAIL_COLLECTIONS` 是无参考基线的详情集合默认。表格型数组/集合字段必须使用 API/MDS `apiField`，mock 同名返回，用 Choerodon Pro Table 展示；旧字段别名只能在 service/request adapter 集中转换。
- `STATUS_ENUM_MAP` 必须继承设计/API 状态全集。状态守卫必须同时用于按钮显隐和 action handler；不能只在 UI 层隐藏，也不能把设计状态值改成旧模型近义值。
- 按钮和行操作文案默认 exact-source。代码中的用户可见文案必须能追溯到 Button Semantic Matrix 的 `sourceText/copyPolicy/copyOverrideSource`；不得把“新建”自行改成“新增行”、把“提交审批”自行改成“提交”。
- 本地 options 只能用于 mock/demo 或 generatedCandidate，不得把主数据语义降级为普通 `TextField`。

## DataSet Boundary

列表查询、详情头、行表应拆成独立 DataSet 配置。主数据字段保留 object + bind，枚举字段保留 lookup/valueSet，附件字段保留 attachment contract。

```ts
import { DataSet } from 'choerodon-ui/pro';
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';

export const queryDS = () => ({
  autoCreate: true,
  fields: [
    {
      name: 'requisitionNumber',
      type: FieldType.string,
      label: intl.get(`${FEATURE_PROMPT}.model.requisitionNumber`).d('申请编号'),
    },
    {
      name: 'applicantObj',
      type: FieldType.object,
      label: intl.get(`${FEATURE_PROMPT}.model.applicantId`).d('申请人'),
      lovCode: LOV_CODES.applicant,
      textField: 'realName',
      valueField: 'id',
      ignore: 'always',
    },
    { name: 'applicantId', type: FieldType.string, bind: 'applicantObj.id' },
    { name: 'applicantName', type: FieldType.string, bind: 'applicantObj.realName' },
    {
      name: 'authorizationStatus',
      type: FieldType.string,
      lookupCode: LOOKUP_CODES.authorizationStatus,
    },
  ],
});
```

```ts
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';

export const lineDS = () => ({
  primaryKey: 'requisitionLineId',
  fields: [
    {
      name: 'itemCategoryObj',
      type: FieldType.object,
      lovCode: LOV_CODES.itemCategory,
      textField: 'itemCategoryName',
      valueField: 'itemCategoryId',
      ignore: 'always',
    },
    { name: 'itemCategoryId', type: FieldType.string, bind: 'itemCategoryObj.itemCategoryId', required: true },
    { name: 'itemCategoryName', type: FieldType.string, bind: 'itemCategoryObj.itemCategoryName' },
    {
      name: 'itemObj',
      type: FieldType.object,
      lovCode: LOV_CODES.item,
      textField: 'itemName',
      valueField: 'itemId',
      ignore: 'always',
      // Only when LOV Lookup Binding Contract confirms:
      // paramName=itemCategoryId, paramSourceField=itemCategoryId, emptyValueBehavior, cascadeClearPolicy.
      dynamicProps: { lovPara: ({ record }) => ({ itemCategoryId: record.get('itemCategoryId') }) },
    },
    { name: 'itemId', type: FieldType.string, bind: 'itemObj.itemId', required: true },
    { name: 'itemName', type: FieldType.string, bind: 'itemObj.itemName' },
    { name: 'quantity', type: FieldType.number, required: true },
    { name: 'unitPrice', type: FieldType.number, required: true },
    { name: 'lineAmount', type: FieldType.number },
  ],
});
```

规则：
- DataSet、Table、Form 和 submit payload 的字段名默认使用 `canonicalField`。若后端或旧页面存在旧别名，只能由 service/request adapter 做集中转换，并在 Field Usage Matrix 记录 `adapterAliasPolicy` 和 `forbiddenRuntimeAliases`。
- 上例中的 `dynamicProps.lovPara` 只表示已确认参数契约后的形态；缺 `paramName/paramSourceField/sourceTiming/emptyValueBehavior/cascadeClearPolicy/confirmedSource` 时，不生成猜测型 `lovPara`，只保留 object LOV + bind 候选并进入 replacement。
- `applicantId/deptId/itemId/itemCategoryId/supplierId/customerId/organizationId` 等主数据字段默认是 `lovCandidate`；没有 confirmed lovCode 时仍保留 object/bind 或 generatedCandidate，不降级为普通输入。
- `authorizationStatus/purchaseType/urgency/source/channel` 等枚举字段默认是 lookup/valueSet；没有平台 code 时记录 generatedCandidate/mock-only options，不把状态数组散落页面。
- 详情只读展示使用 `*Name/*Meaning/displayField`；不得只展示 raw id/code/uuid。

## Service Boundary

service 是页面级业务 action adapter，承接 ID runtime、mock/real prefix 切换、request shape 和 action 语义。页面只调用语义函数。
DataSet 生命周期内的 read/create/update/destroy/submit 不是页面 action：DataSet 文件必须在 `transport` 中直接返回 request config，不得 import 或调用 service 函数。

```ts
const normalizeId = (id: string | number) => String(id);

export function saveRequisition(payload: { header: any; lineList: any[] }) {
  const headerId = payload?.header?.requisitionHeaderId;
  return request(
    buildApiPath(headerId ? `/prm-requisition-headers/${normalizeId(headerId)}` : '/prm-requisition-headers'),
    {
      method: headerId ? 'PUT' : 'POST',
      body: payload,
    }
  );
}

export function deleteRequisitionHeaders(headerIds: Array<string | number>) {
  return request(buildApiPath('/prm-requisition-headers/batch-delete'), {
    method: 'DELETE',
    body: { headerIds: headerIds.map(normalizeId) },
  });
}
```

规则：
- 页面不得直接拼 request URL 或散落 `request(...)`，除非任务明确是 service 层。
- 上一条只约束页面组件，不授权 DataSet 调 service。`transport.read: ({ params }) => queryRequisitionLines(id, params)`、`transport.submit: () => saveRequisition(...)` 等写法是 legacy/anti-pattern，新生成代码一律禁止。
- 如需复用路径、prefix、分页参数或响应字段，只能抽 `buildApiPath`、`buildQueryParams`、`adaptPageResponse`、`buildSubmitPayload` 这类纯 helper；service action 和 DataSet transport 可共享 helper，但不能互相调用。
- save/create/update、delete/batch-delete、submit/withdraw/cancel 必须分别保留业务语义函数。
- ID-like 字段统一 `String(id)`，不得 `Number(id)`。

## Master-detail Mode Example

头行页在无参考基线下，必须先选清楚明细读取和删除模式，而不是一边生成 `lineQueryDS.ts`，一边继续页面内手工 `loadData/normalizeLines`。

```ts
export const MASTER_DETAIL_CONTRACT = {
  lineDataMode: 'line-query-transport',
  lineQueryDataSet: 'required',
  lineReadSource: 'line-query-api',
  lineRefreshPolicy: 'line-query-refresh',
  saveGranularity: 'line-separate',
  lineDeleteMode: 'service-delete',
  handPayloadPolicy: 'shared-payload-builder',
} as const;
```

也允许：

```ts
export const MASTER_DETAIL_CONTRACT = {
  lineDataMode: 'embedded-local-lines',
  lineQueryDataSet: 'forbidden',
  lineReadSource: 'detail-response',
  lineRefreshPolicy: 'header-refresh',
  saveGranularity: 'header-cascade-lines',
  lineDeleteMode: 'replace-all-on-save',
  handPayloadPolicy: 'shared-payload-builder',
} as const;
```

规则：
- `lineDataMode='line-query-transport'` 时，明细表必须真正使用 `queryDataSet/transport`；不能只留一个未接入的 `lineQueryDS.ts`。
- `lineDeleteMode='replace-all-on-save'` 时，删除 persisted line 必须作为整体保存覆盖语义的一部分记录下来；不能写成“看起来只是本地删掉一行”。
- `generatedCandidate-normalizer` 只能作为 mock/demo 过渡，不应成为 production 默认写法。

## Line Query Example

```ts
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';

export const lineQueryDS = () => ({
  autoCreate: true,
  fields: [
    {
      name: 'itemCategoryObj',
      type: FieldType.object,
      lovCode: LOV_CODES.itemCategory,
      textField: 'itemCategoryName',
      valueField: 'itemCategoryId',
      ignore: 'always',
    },
    { name: 'itemCategoryId', type: FieldType.string, bind: 'itemCategoryObj.itemCategoryId' },
  ],
});

export const lineListDS = (headerIdGetter: () => string | undefined) => ({
  primaryKey: 'requisitionLineId',
  queryDataSet: new DataSet(lineQueryDS()),
  transport: {
    read: ({ data }) => ({
      url: buildApiPath(`/prm-requisition-headers/${String(headerIdGetter())}/lines`),
      method: 'GET',
      data,
    }),
  },
});
```

规则：
- `headerIdGetter()` 为空时，明细查询入口应 `hidden / disabled-with-reason / blocked`，而不是拼 `__empty__`、fake id 或 fake URL。
- 明细查询 DataSet 和明细表 refresh policy 必须成对出现；否则 Review 无法判定 query line contract 是否闭合。

## Status Action Matrix

无参考基线下，状态动作不要散落在按钮、页面函数和 mock handler 里。设计和实现都至少要能落成一张最小矩阵。

```ts
export const STATUS_ACTIONS = {
  submit: {
    sourceStatus: ['NEW', 'REJECTED'],
    targetStatus: 'IN_APPROVAL',
    permissionCode: PERMISSION_CODES.submit,
  },
  withdraw: {
    sourceStatus: ['IN_APPROVAL'],
    targetStatus: 'WITHDRAWN',
    permissionCode: PERMISSION_CODES.withdraw,
  },
  remove: {
    sourceStatus: ['NEW', 'CANCELLED'],
    targetStatus: 'DELETED',
    permissionCode: PERMISSION_CODES.delete,
  },
};

export const canRunStatusAction = (action: keyof typeof STATUS_ACTIONS, status?: string) =>
  STATUS_ACTIONS[action].sourceStatus.includes(String(status));
```

```ts
export async function handleSubmit(record) {
  if (!canRunStatusAction('submit', record?.get('authorizationStatus'))) {
    notification.warning({ message: '当前状态不允许提交' });
    return;
  }

  await submitRequisition(record.get('requisitionHeaderId'));
  await queryDS.query();
}
```

规则：
- 至少记录 `sourceStatus / targetStatus / permissionCode / uiGuard / serviceAction / refreshTarget`。
- UI 按钮、action 入口、mock handler 三处必须复用同一套状态来源。
- 页面 Header 的导航取消/返回不能复用业务状态动作矩阵。

## Attachment Wrapper Example

附件能力默认封装成页面域组件，不把 bucket/storage/template 直接写进页面。

```tsx
import { Attachment } from 'choerodon-ui/pro';

type AttachmentProps = {
  dataSet: DataSet;
  readOnly?: boolean;
  fieldName?: string;
  bucketName: string;
  attachmentUUIDField?: string;
};

export default function RequisitionAttachment({
  dataSet,
  readOnly = false,
  fieldName = 'attachmentUuid',
  bucketName,
  attachmentUUIDField = 'attachmentUuid',
}: AttachmentProps) {
  return (
    <Attachment
      dataSet={dataSet}
      mode={readOnly ? 'view' : 'edit'}
      bucketName={bucketName}
      attachmentUUID={dataSet.current?.get(attachmentUUIDField)}
      name={fieldName}
    />
  );
}
```

规则：
- 页面只传 contract/config，不内联 `ATTACHMENT_DEMO_BUCKET`、`ATTACHMENT_DEMO_STORAGE`。
- `bucket/storage/template` 未确认时进入 `constants.ts generatedCandidate` 或 replacement，不进入页面 JSX。
- 只读/编辑态策略收敛在 wrapper，不散落在多个页面分支。
- `Attachment` 常规用 `choerodon-ui/pro` 命名导入；若目标版本证据显示桶入口循环依赖或运行时报 `ReferenceError: Attachment is not defined`，可用 `choerodon-ui/pro/lib/attachment` 默认导入并记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed`；也可用项目 confirmed wrapper。不得用 `components/Attachment` 默认导入配置对象后直接 JSX 渲染。

## Import / Export Entry Example

导入导出默认直接渲染标准组件。只有同时存在头/行多入口、复杂参数收敛、跨页面复用或项目 confirmed wrapper 时，才创建 `ImportExportActions.tsx` 等页面域组件；单个导入或单个导出按钮不得为转发 props、改名标准组件或隐藏权限/模板候选而新增薄封装。

```tsx
<Import
  templateCode={IMPORT_TEMPLATE_CODE}
  buttonProps={{
    type: 'text',
    permissionList: [{ code: PERMISSIONS.import, type: 'button', meaning: '导入数据' }],
  }}
/>

<ExcelExportPro
  requestUrl={exportUrl}
  queryParams={() => queryDS.current?.toData() || {}}
  otherButtonProps={{
    type: 'text',
    permissionList: [{ code: PERMISSIONS.export, type: 'button', meaning: '导出数据' }],
  }}
/>
```

规则：
- 头导出、行导出、头导入、行导入分开建模，不混 template、URL、parentId。
- 关闭导入弹层后的 refresh target 必须显式，例如 `queryDS.query()` 或 `detailDS.query()`。
- 缺失 templateCode、权限码、tenantContext 或 query params 时，用 `generatedCandidate/missing/replacement` 承接，不降级成普通按钮。
- `headerId` 未确认时，行导入/行导出应 `hidden / disabled-with-reason / blocked`，不是构造 `__empty__` URL 继续渲染。
- 权限随标准组件按钮 props 传入：导入使用 `buttonProps.permissionList`，导出使用 `otherButtonProps.permissionList`。顶层 `permissionList`、无证据 `funcType` 和 `HeaderImportAction` / `HeaderExportAction` 薄封装不是默认范式。

## Attachment Candidate Example

附件 contract 未闭合时，应把候选值集中到 constants 或 wrapper props，而不是页面里直接 `process.env.*`。

```ts
export const ATTACHMENT_CONTRACT = {
  fieldName: 'attachmentUuid',
  bucketName: 'HSPD.PRM.GENERATED_BUCKET',
  bucketDirectory: 'prm',
  storageCode: 'HSPD.PRM.GENERATED_STORAGE',
  contractValueStatus: 'generatedCandidate',
  generatedCandidateCarrier: 'constants',
} as const;
```

```tsx
<RequisitionAttachment
  dataSet={detailDS}
  readOnly={!editable}
  fieldName={ATTACHMENT_CONTRACT.fieldName}
  bucketName={ATTACHMENT_CONTRACT.bucketName}
/>
```

规则：
- `process.env.BUCKET_NAME`、`ATTACHMENT_DEMO_BUCKET`、raw uuid 展示不能直接出现在页面业务组件中。
- 候选值允许存在，但必须通过 constants/wrapper/replacement 承接，并在 Review/Handoff 中可追踪。

## Component Boundary

复杂能力用页面域组件封装，页面只负责编排。

业务弹层由触发方使用 `Modal.open` 或 confirmed wrapper 打开。无参考基线下，普通表单 Modal 设计未指定宽度时必须显式使用 small 默认或继承 wrapper 默认 small 证据；详情 Drawer / 高密度详情记录项目默认尺寸或 baseline、readabilityRisk 和长值展示策略；不要只给内容容器写 `style.width`。

```tsx
import { ColumnProps, ColumnRenderProps } from 'choerodon-ui/pro/lib/table/Column';

const buildRowOperators = (record: Record) => {
  const viewTitle = intl.get(`${FEATURE_PROMPT}.button.view`).d('查看');
  const operators = [
    {
      key: 'view',
      ele: (
        <PermissionButton
          type="text"
          permissionList={[{ code: PERMISSION.view, type: 'button' }]}
          onClick={() => handleView(record)}
        >
          {viewTitle}
        </PermissionButton>
      ),
      len: 2,
      title: viewTitle,
    },
  ];

  return operators;
};

const handleView = (record: Record) => {
  Modal.open({
    drawer: true,
    resizable: true,
    size: OVERLAY_SIZE_CONTRACT.defaultSize,
    title: intl.get(`${FEATURE_PROMPT}.view.title.detail`).d('详情'),
    children: <RequisitionDetailContent recordId={String(record.get('requisitionHeaderId'))} />,
  });
};

const columns: ColumnProps[] = [
  // ...business columns
  {
    name: 'operator',
    width: 120,
    lock: ColumnLock.right,
    renderer: ({ record }: ColumnRenderProps) =>
      c7nOperatorRender(buildRowOperators(record), record, { limit: 3 }),
  },
];
```

```tsx
Modal.open({
  drawer: true,
  resizable: true,
  size: OVERLAY_SIZE_CONTRACT.defaultSize,
  title: intl.get(`${FEATURE_PROMPT}.view.title.detail`).d('详情'),
  children: <RequisitionDetailContent recordId={recordId} />,
});
```

详情集合内容由 Choerodon Pro Table 承载，字段名来自 `DETAIL_COLLECTIONS.<section>.apiField`，不在内容组件中读取别名或拼接文本。

```text
components/LineTable.tsx
  - line columns
  - row action and table buttons
  - c7nOperatorRender
  - LineExportButton

components/<Feature>Attachment.tsx
  - Attachment/project wrapper
  - readOnly policy
  - bucket/storage generatedCandidate or replacement marker

components/ImportExportActions.tsx # optional only when wrapperJustification exists
  - Import direct entry or confirmed wrapper
  - ExcelExportPro direct entry or confirmed current wrapper
  - multi-entry templateCode/export URL/query param adapter
```

页面不得内联 demo bucket、demo storage、template、mock-only upload action：

```ts
// bad in page component
const ATTACHMENT_DEMO_BUCKET = 'demo-bucket';
const ATTACHMENT_DEMO_STORAGE = 'DEMO_STORAGE';
```

正确做法：
- demo 值进入 mock config、generatedCandidate constants 或 production replacement；
- 页面组件接收 contract/config，不展示或硬编码 demo 事实；
- Handoff / replacement 记录 bucket/storage/template 未闭合。

## Table Boundary

HZERO + Choerodon 列表和明细表默认保留企业表格能力：

```tsx
import { TableQueryBarType } from 'choerodon-ui/pro/lib/table/enum';

<Table
  dataSet={listDS}
  columns={columns}
  buttons={buttons}
  queryBar={TableQueryBarType.filterBar}
  customizedCode="PRM.REQUISITION.HEADER.TABLE"
  customizable
  columnDraggable
/>
```

规则：
- 列表页和可配置明细表默认规划稳定 `customizedCode`，与 feature/page code 绑定。
- 空参考项目或 `assetBaselineSource=hzerojs-asset-baseline` 下，Table `columns` 默认使用 `ColumnProps[]` typed surface，自定义 `renderer` 默认使用 `ColumnRenderProps` 参数；不要让示例退化成无类型 `const columns = [...]`。
- 上述 enum import 表示组件 props 的默认代码形态；Table/Form/Button 等组件 enum props 即使目标项目存在历史字符串风格，也不得作为新增实现形态。DataSet 配置类枚举若目标项目已确认字符串风格且 tsc 可通过，可按 enumProvenance 记录项目证据后使用字符串。
- 多动作操作列默认右锁定并使用 `c7nOperatorRender`；行操作按钮使用 `PermissionButton type="text"`。
- 没有可见 actions 时隐藏操作列，不保留空列。
- 若项目证据显示不支持 `customizable/columnDraggable/customizedCode`，记录 `not-applicable + reason`。

## Review Failure Examples

以下在无参考基线下至少是 major；影响可运行、替换或生产声明时 blocking：

- `src/stores/<feature>DS.ts` 聚合 Query/List/Header/Line 全部 DataSet，且没有项目证据或用户确认。
- 主数据字段用普通 `TextField`，没有自由文本来源。
- required 附件、导入、导出内联到页面大组件，且 demo 参数写在页面里。
- 权限码、状态守卫、LOV/lookup 候选散落在页面。
- `ATTACHMENT_DEMO_*`、`PRM_STATUS_OPTIONS`、`canSubmit/canWithdraw`、`request(...)`、templateCode 或 export URL 直接写在页面组件，而不是进 `constants.ts`、service 或页面域 wrapper。
- `lineQueryDS.ts` 已生成但 Detail/LineTable 未接入；或 persisted line 删除只做 `lineDS.delete()`，没有 `lineDeleteMode` / `persistedLineDeletePolicy`。
- 行导入/行导出/行查询在 headerId 缺失时使用 `__empty__`、fake id、fake path 或其它伪 URL。
- Table 缺稳定 `customizedCode/customizable/columnDraggable` 且没有 not-applicable reason。
- mock/demo 常量进入用户可见 UI 或业务页面，未写 production replacement。

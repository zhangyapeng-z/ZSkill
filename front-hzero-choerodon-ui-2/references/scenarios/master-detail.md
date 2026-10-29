# Master Detail Scenario

## 阅读路由

- Active owner: `front-hzero-choerodon-ui`.
- Related owner: `front-hzero-enterprise-page` owns page layout and route context.
- 触发词：头行明细、主从、header-line、master-detail、明细表保存、头行事务、关联键。

## Scope

头行主从是 DataSet / Table / Form 与企业页面组合场景，不再作为独立 active skill。明细 DataSet、保存粒度、关联键、dataToJSON、事务边界归 `front-hzero-choerodon-ui`；页面布局、route/menu、Header/Content 和定位交互归 `front-hzero-enterprise-page`。

## Stage Routing

- Design：确认主记录、明细集合、关联键、保存粒度、API 事务和新增/编辑/删除状态。
- Implementation：按 DataSet-first 方案实现主从关系，不得用手工 payload 绕过 masterDetailDataContract。
- Review：检查保存粒度、明细脏数据、关联键、删除语义、local-filter 和 mock/真实 API 差异。
- Verification：验证新增、编辑、删除、保存、刷新、错误提示和事务失败回滚。

## Minimal Implementation Shape

```ts
const headerDS = new DataSet({
  primaryKey: 'headerId',
  fields: [{ name: 'headerId', type: FieldType.string }],
  children: {
    lines: new DataSet({
      primaryKey: 'lineId',
      fields: [
        { name: 'lineId', type: FieldType.string },
        { name: 'headerId', type: FieldType.string },
      ],
    }),
  },
  transport: {
    read: ({ dataSet }) => ({
      url: `/v1/{organizationId}/example/${dataSet.current?.get('headerId')}`,
      method: 'GET',
    }),
    submit: ({ data }) => ({
      url: '/v1/{organizationId}/example',
      method: 'POST',
      data: data[0],
    }),
  },
});

const payload = headerDS.current?.toData();
const lines = headerDS.current?.getField('lines');
```

详情页使用独立行 DataSet 时，必须让行表查询链路被实际激活：

```ts
const lineDS = new DataSet({
  primaryKey: 'lineId',
  autoQuery: Boolean(headerId),
  transport: {
    read: ({ params }) => ({
      url: `/v1/{organizationId}/example/${headerId}/lines`,
      method: 'GET',
      query: params,
    }),
  },
  fields: [
    { name: 'lineId', type: FieldType.string },
    { name: 'headerId', type: FieldType.string },
  ],
});

await Promise.all([headerDS.query(), lineDS.query()]);
```

## Rejection Anchors

- 必须记录 `masterDetailDataContract`：主记录、明细集合、关联键、保存粒度、删除语义和事务边界。
- 不得把头 DataSet 和行 DataSet 合并成单个全局 DS，也不得用手工 payload 绕过 DataSet 状态和 `dataToJSON` / `toData()` 策略。
- 明细集合字段必须使用 FDS/TDS/API/MDS 原始字段名；别名 shape 或双字段读取必须标记 contract conflict / migrationRequired，不得进入新实现。
- 只读详情集合仍优先使用 Choerodon Pro Table；不得用原生 table 或薄 wrapper 替代表格合同。
- 独立行 DataSet 绑定到详情 Table 且存在 `transport.read` 时，必须有查询激活证据：`autoQuery: Boolean(parentId/headerId)`，或在父 ID ready、详情主记录切换、保存/提交后的 reload 中显式调用 `lineDs.query()` / 项目 confirmed 等价刷新。只有 `<Table dataSet={lineDs}>` 和 `transport.read` 不证明明细会加载；缺激活时按 `HZC-LINE-DATASET-ACTIVATION-001` 拒收。
- 行 DataSet 的 `parentId/headerId` 必须来自 route params / routeContext、头 DataSet current record、保存响应主键或已确认 tab context；不得用 `'1001'`、`1`、`demo-org`、`__empty__`、placeholder uuid、环境常量或 fallback 默认值硬编码父记录身份。父 ID 未就绪时应 hidden / blocked / no-query，并在生成主键后刷新。
- 新建页父 ID 未生成时，行 DataSet 可以不首查，但保存生成父 ID 后必须补齐 parentId 并刷新头/行，或证明头详情 read 返回的 children 已同步进同一个子 DataSet。

## Owner Source

新增规则只写入本 reference、Choerodon UI owner references 或 enterprise page owner references。

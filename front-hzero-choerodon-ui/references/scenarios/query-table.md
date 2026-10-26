# Query Table Scenario

## 阅读路由

- Active owner: `front-hzero-choerodon-ui`.
- 触发词：查询表格、queryFields、queryDataSet、filterBar、DataSet query、列表分页、查询条件。

## Scope

查询表格是 Choerodon UI / DataSet 场景，不再作为独立 active skill。DataSet-first、Table/Form、queryFields、filterBar、transport 和静态反模式归 `front-hzero-choerodon-ui`；页面 Header、权限、i18n 和 route/menu 归 `front-hzero-enterprise-page`。

## Stage Routing

- Design：确认 queryFields、queryDataSet、transport.read、分页、默认条件和字段来源。
- Implementation：使用 Choerodon Pro Table / DataSet，不得用外部 Form、自建查询栏或 local-filter 伪查询替代。
- Review：检查 filterBar、transport、字段映射、mock request 兼容和 C7N validator 规则。
- Verification：验证查询触发、清空/重置、分页、mock/真实 transport 和可见结果。

## Minimal Implementation Shape

```tsx
import { useMemo } from 'react';
import { DataSet, Table } from 'choerodon-ui/pro';
import type { ColumnProps } from 'choerodon-ui/pro/lib/table/Column';
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';
import { TableQueryBarType } from 'choerodon-ui/pro/lib/table/enum';

export default function QueryList() {
  const queryDS = useMemo(
    () =>
      new DataSet({
        autoCreate: true,
        fields: [{ name: 'keyword', type: FieldType.string }],
      }),
    []
  );
  const tableDS = useMemo(
    () =>
      new DataSet({
        primaryKey: 'id',
        queryDataSet: queryDS,
        transport: {
          read: ({ data, params }) => ({
            url: '/v1/{organizationId}/example/list',
            method: 'GET',
            query: { ...data, ...params },
          }),
        },
        fields: [
          { name: 'id', type: FieldType.string },
          { name: 'name', type: FieldType.string },
        ],
      }),
    [queryDS]
  );
  const columns = useMemo<ColumnProps[]>(
    () => [
      { name: 'id', minWidth: 120 },
      { name: 'name', minWidth: 180 },
    ],
    []
  );

  return (
    <Table
      dataSet={tableDS}
      columns={columns}
      queryBar={TableQueryBarType.filterBar}
      queryFieldsLimit={3}
      style={{ minHeight: 320 }}
    />
  );
}
```

## Rejection Anchors

- 查询需求存在时，不得省略 `queryDataSet`、`queryFields` 或 `filterBar`，除非 UI Contract 明确 `queryAreaPolicy=none-by-design + sourceRef/reason`。
- 顶部 fuzzy search 只允许在 `queryBarProps` 中配置 `fuzzyQuery` 和已确认的 `fuzzyQueryPlaceholder`；不得生成 `queryBarProps.fuzzyQueryField` / `queryBarProps.fuzzyQueryFields`，字段映射必须回到 QueryDS/queryFields 和 UI Contract `fuzzyQueryFields`。
- `queryBarProps` 不得出现无 Choerodon typed surface 或项目 wrapper 证据的自造参数，例如 `searchFieldName`、`keywordField`、`fuzzySearchField`；命中 `c7n_table_querybarprops_unknown_prop` 必须回实现修复。
- 不得用外部 Form、React state local-filter、`loadData()` 或前端内存筛选替代 DataSet `transport.read`。
- Table `columns[].name` 必须绑定主 DataSet `fields`；`queryFields` 不能替代表格列字段元数据。
- 新增或重构的资产基线 Choerodon Pro Table 默认以 `columns={columns}` 传入 `useMemo<ColumnProps[]>` 的列配置；不要把常规业务列写成 `<Table> <Column /> </Table>` 子节点。列配置集中后才能稳定处理 `editable`、权限动作、renderer、`ColumnLock.right` 和列宽策略。
- 只有目标工程 wrapper、递归/运行时动态列，或已确认的组件版本兼容约束确实要求 JSX 子列时才允许偏离；代码近邻必须同时记录 `tableColumnComposition=jsx-children`、`sourceRef` 和 reason。`sourceRef` 必须是相对当前 validator root 可读取的源码路径。仅因旧页面使用 `<Column>` 不是有效来源。
- 页面工具栏动作不得误放入 Table `buttons`，除非 Button Semantic Matrix 确认为 table-toolbar。

## Owner Source

新增规则只写入本 reference 或 Choerodon UI owner references。

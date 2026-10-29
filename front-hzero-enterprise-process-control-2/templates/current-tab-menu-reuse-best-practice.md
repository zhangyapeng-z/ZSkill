# HZERO Current Tab Menu Reuse Best Practice

## Use When

- 用户已通过 `Open Interaction Confirm` 选择“当前页打开详情”或“复用当前菜单页签”。
- Design / Task 已确认 `routeOpenMode=menu-current` 或 `detailViewInteractionMap=current-tab-page`。
- 已确认 `parentTabKey`、`targetDetailPath`、`navigationApi`、`routeMode=route/omitted-default-route`。

## Required Contract

| Field | Required value |
| --- | --- |
| `parentTabKey` | 父级菜单 path、父级 route 或项目确认的父 Tab key，例如 `/prm/requisition` |
| `listPath` | 真实列表 path，例如 `/prm/requisition/list` |
| `targetDetailPath` | 真实详情 path，例如 `/prm/requisition/detail/view/:requisitionHeaderId` |
| `navigationApi` | 固定 `import { openTab } from 'utils/menuTab';`，且传入父级 `key` 与目标 `path`；它是项目级基础能力，不形成页面级缺口 |
| `routeMode` | `mode: 'route'` 或省略默认 route；不得是 `mode: 'dynamic'` |
| `pageIdentity` | 新建、查看、编辑和记录 id 来自 path params，不来自 query/search |

## Route Config Pattern

父 route 是稳定 HZERO Tab 边界，只做分组；列表、创建、查看、编辑是子路由。

```ts
const routes = [
  {
    path: '/prm/requisition',
    authorized: true,
    title: '采购申请管理',
    routes: [
      {
        path: '/prm/requisition/list',
        component: 'PrmRequisition/List',
        authorized: true,
        title: '采购申请管理',
      },
      {
        path: '/prm/requisition/create',
        component: 'PrmRequisition/Detail',
        authorized: true,
        title: '采购申请新建',
        mode: 'route',
      },
      {
        path: '/prm/requisition/detail/view/:requisitionHeaderId',
        component: 'PrmRequisition/Detail',
        authorized: true,
        title: '采购申请详情',
        mode: 'route',
      },
      {
        path: '/prm/requisition/detail/edit/:requisitionHeaderId',
        component: 'PrmRequisition/Detail',
        authorized: true,
        title: '采购申请编辑',
        mode: 'route',
      },
    ],
  },
];
```

### Route Config Rejections

- 不得给父 route 配 `redirect: '/prm/requisition/list'`。
- 不得让父 route 和列表子 route 使用同一个 path。
- 不得把列表、详情、编辑、新建生成成同级顶级 route 后声明 current-tab。
- 不得给 current-tab 详情 route 配 `mode: 'dynamic'` 或 `dws: true`。
- 不得把完整 route array 内联到 `config/config.ts`。

## List Page Navigation

列表行操作必须用父级 key 复用当前菜单页签，path 指向目标详情 route。

```ts
const PARENT_TAB_KEY = '/prm/requisition';
const LIST_PATH = '/prm/requisition/list';

function navigateInCurrentMenu(path: string, title: string) {
  openTab({
    key: PARENT_TAB_KEY,
    path,
    title,
    closable: true,
  });
}

function handleCreate() {
  navigateInCurrentMenu('/prm/requisition/create', '采购申请新建');
}

function handleView(record) {
  const id = String(record.get('requisitionHeaderId'));
  navigateInCurrentMenu(`/prm/requisition/detail/view/${id}`, '采购申请详情');
}

function handleEdit(record) {
  const id = String(record.get('requisitionHeaderId'));
  navigateInCurrentMenu(`/prm/requisition/detail/edit/${id}`, '采购申请编辑');
}
```

`history.push` 只允许用于列表筛选、分页、排序、来源、返回路径或详情内子 Tab 等辅助状态同步。不能用 `history.push('/prm/requisition/detail')` 证明复用当前菜单页签。

## Detail Page Route Context

详情页必须从 path params 派生页面模式和主记录 id。

```ts
function useRequisitionRouteContext(params) {
  const pageMode = params.requisitionHeaderId
    ? params.location?.pathname?.includes('/detail/edit/')
      ? 'edit'
      : 'view'
    : 'create';

  return {
    pageMode,
    requisitionHeaderId: params.requisitionHeaderId ? String(params.requisitionHeaderId) : undefined,
    isCreate: pageMode === 'create',
    editable: pageMode === 'create' || pageMode === 'edit',
  };
}
```

项目可使用 confirmed route context wrapper，但必须保持同一原则：主身份来自 path params，query/search 只作为辅助状态。

## React Hooks Boundary

不要在同一个组件执行一部分 hooks 后再按 query 或 route 状态提前 `return <DetailPage />`。这会导致同一组件前后 render 的 hooks 数量不一致，生产环境常见表现是 `Minified React error #300`。

错误形态：

```tsx
function ListPage() {
  const listDS = useMemo(() => new DataSet(...), []);
  const location = useLocation();

  if (new URLSearchParams(location.search).get('pageMode')) {
    return <DetailPage />;
  }

  const tableColumns = useMemo(() => [...], []);
  return <Table dataSet={listDS} columns={tableColumns} />;
}
```

正确形态：

```tsx
export default function ListPage() {
  return <RequisitionList />;
}

function RequisitionList() {
  const listDS = useMemo(() => new DataSet(...), []);
  const tableColumns = useMemo(() => [...], []);

  return <Table dataSet={listDS} columns={tableColumns} />;
}
```

如果当前路由真的需要在同一页面 shell 内切换多个视图，外层 shell 不应在执行业务 hooks 后分流；每个分支组件应拥有自己的完整 hooks 序列。但 AI 新生成 current-tab 详情默认不采用同 pathname query 分流。

## Verification

current-tab 不能只用 typecheck 或代码静态检查判定通过。必须记录：

- 点击详情/编辑/新建前后的 `window.tabsAction.getTabs()` 数量。
- active tab key 是否仍为 `parentTabKey` 或项目确认的等价父 key。
- URL pathname 是否进入真实详情 route，且 search 不承载 pageMode 或主记录 id。
- route config 中详情 route 是否为 `mode=route/omitted-default-route`。
- 点击不同记录详情/编辑时，应用内 Tab 数量不增加，页面内容更新为目标记录。

未运行浏览器或手工页签检查时，验证结果只能写 `not-run + reason`，不得写 `passed`、`usable=true` 或 `production-ready`。

## PRM Failure Pattern To Reject

以下连续修复路径是反例，后续任务命中任一步都应回到本最佳实践：

1. 用父 route `redirect` 到 `/list` 解决列表入口。
2. 移除 `mode: 'dynamic'` 后仅改成 `history.push('/detail')`。
3. 把路由收敛成 `/list?pageMode=edit&requisitionHeaderId=...`。
4. 在列表组件执行部分 hooks 后按 query 提前 `return <DetailPage />`，触发 React #300。

正确修复应从 route config、导航 API、route context 和验证证据一起闭合。

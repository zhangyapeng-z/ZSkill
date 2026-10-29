# HZERO openTab Reusable Fixed Path Best Practice

## 适用场景

- 用户确认使用 HZERO 系统内页签，不使用浏览器新标签页。
- 新建页需要保留独立草稿页签。
- 查看/编辑已有记录只允许复用一个详情页签。
- 运行时已确认固定 `openTab.key` 但不同 `path` 仍会开多个页签，或项目选择按固定 `path` 控制复用。

## Route Contract

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
        path: '/prm/requisition/detail',
        component: 'PrmRequisition/Detail',
        authorized: true,
        title: '采购申请详情',
        mode: 'route',
      },
    ],
  },
];

export default routes;
```

## Navigation Contract

```ts
type PageMode = 'create' | 'edit' | 'view';

const LIST_TAB_PATH = '/prm/requisition/list';
const CREATE_TAB_PATH = '/prm/requisition/create';
const DETAIL_TAB_PATH = '/prm/requisition/detail';
const DETAIL_CONTEXT_KEY = 'prm.requisition.detailContext';
const DETAIL_CONTEXT_EVENT = 'prm-requisition-detail-context-change';

const titleMap: Record<PageMode, string> = {
  create: '采购申请新建',
  edit: '采购申请编辑',
  view: '采购申请详情',
};

function writeDetailContext(context: { pageMode: PageMode; requisitionHeaderId?: string; tabTitle?: string }) {
  sessionStorage.setItem(DETAIL_CONTEXT_KEY, JSON.stringify(context));
  window.dispatchEvent(new CustomEvent(DETAIL_CONTEXT_EVENT, { detail: context }));
}

function openRequisition(pageMode: PageMode, requisitionHeaderId?: string, requisitionNumber?: string) {
  if (pageMode === 'create') {
    writeDetailContext({ pageMode: 'create' });
    openTab({
      key: CREATE_TAB_PATH,
      path: CREATE_TAB_PATH,
      title: titleMap.create,
      closable: true,
    });
    return;
  }

  const tabTitle = requisitionNumber || titleMap[pageMode];
  writeDetailContext({ pageMode, requisitionHeaderId, tabTitle });
  openTab({
    key: DETAIL_TAB_PATH,
    path: DETAIL_TAB_PATH,
    title: tabTitle,
    closable: true,
  });
}
```

规则：`titleMap` 是 route/pageMode fallback；记录级标题只能使用已确认的业务显示字段，例如 `requisitionNumber` 或名称。`requisitionHeaderId`、`id`、`headerId`、加密 id 和数据库主键只用于上下文、key/path 或请求参数，不得作为用户可见页签标题的默认值。

## Detail Context Contract

```ts
function readDetailContext() {
  const raw = sessionStorage.getItem(DETAIL_CONTEXT_KEY);
  if (!raw) {
    return undefined;
  }
  try {
    return JSON.parse(raw) as { pageMode: PageMode; requisitionHeaderId?: string; tabTitle?: string };
  } catch {
    return undefined;
  }
}

function useDetailContext(pathname: string) {
  const [context, setContext] = useState(() => {
    if (pathname === CREATE_TAB_PATH) {
      return { pageMode: 'create' as const };
    }
    return readDetailContext();
  });

  useEffect(() => {
    const refresh = () => {
      setContext(pathname === CREATE_TAB_PATH ? { pageMode: 'create' } : readDetailContext());
    };

    window.addEventListener(DETAIL_CONTEXT_EVENT, refresh);
    window.addEventListener('focus', refresh);
    window.addEventListener('storage', refresh);
    return () => {
      window.removeEventListener(DETAIL_CONTEXT_EVENT, refresh);
      window.removeEventListener('focus', refresh);
      window.removeEventListener('storage', refresh);
    };
  }, [pathname]);

  return context;
}
```

## Save Redirect Contract

```ts
async function handleSave() {
  const saved = await saveRequisition();
  const tabTitle = saved.requisitionNumber || '采购申请编辑';

  writeDetailContext({
    pageMode: 'edit',
    requisitionHeaderId: String(saved.requisitionHeaderId),
    tabTitle,
  });

  closeTab(CREATE_TAB_PATH);
  openTab({
    key: DETAIL_TAB_PATH,
    path: DETAIL_TAB_PATH,
    title: tabTitle,
    closable: true,
  });
}
```

## Verification

- 点击新建后只打开 `/prm/requisition/create`，标题为 `采购申请新建`。
- 新建保存后关闭 create 页签，并打开或激活 `/prm/requisition/detail`，标题优先使用保存结果中的业务显示字段，否则为 `采购申请编辑`。
- 连续点击不同记录的查看/编辑，`/prm/requisition/detail` 页签数量不增加，内容刷新为最新上下文；若有业务显示字段，页签标题同步为该字段，否则回退为静态中文标题。
- 直接刷新 `/prm/requisition/detail` 时，若上下文不存在，页面必须显示可恢复提示并提供返回列表动作；不得读取旧 route/query fallback，也不得静默展示旧记录。
- runtime route check 必须验证 `/list`、`/create`、`/detail` 都能匹配真实 component，父级 route 不通过 `redirect` 兜底。

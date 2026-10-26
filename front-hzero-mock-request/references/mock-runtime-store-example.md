# Mock Runtime Store Example

用途：给 mock-request 场景提供一个最小但完整的运行态示例，覆盖列表、详情、保存、删除、提交、撤回和头行同步。本文只说明结构和守卫方式，不确认具体业务状态值、报错文案或真实 API 契约。

## 阅读路由
- 需要确定 runtime store 最小结构时读 `Runtime Store Shape`。
- 需要判断列表、详情、动作是否共享同一份运行态数据时读 `List And Detail` 及后续章节。
- 需要给 Implementation / Review / Verify 提供 mock 状态动作闭环样例时按全文顺序阅读。

## Runtime Store Shape

mock-request 有状态页面必须由同一个 dev-only runtime store 维护 header 和 line 数据，列表查询、详情读取和状态动作都从这里读写。

示例中的姓名、物料、编号等展示值属于 `demoGeneratedValue`，只用于 devServer mock response 可读性；不得声明为业务事实、生产默认值或后端样例来源，也不得回填到 create/edit/copy 表单默认输入。

```js
const store = {
  headerSeq: 1000,
  lineSeq: 5000,
  headers: [
    {
      requisitionHeaderId: '1001',
      requisitionNum: 'PRM202406240001',
      organizationId: '1',
      authorizationStatus: 'NEW',
      applicantId: '3001',
      applicantName: '张三',
    },
  ],
  linesByHeaderId: {
    '1001': [
      {
        requisitionLineId: '5001',
        requisitionHeaderId: '1001',
        itemId: 'M1001',
        itemName: '测试物料',
        quantity: 2,
      },
    ],
  },
};

function normalizeId(id) {
  return String(id);
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function findHeader(id) {
  return store.headers.find((item) => item.requisitionHeaderId === normalizeId(id));
}

function getLines(headerId) {
  return clone(store.linesByHeaderId[normalizeId(headerId)] || []);
}

function toNonNegativeInteger(value, fallback) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? Math.floor(parsed) : fallback;
}

function parsePagination(query = {}) {
  const page = toNonNegativeInteger(query.page, 0);
  const size = toNonNegativeInteger(query.size, 10);

  return {
    page,
    size: size > 0 ? size : 10,
  };
}
```

规则：
- header、line、状态动作和分页查询必须共享同一个 store。
- ID-like 字段统一 `String(id)`；不得在 mock runtime 中转成 number。
- 列表查询、详情读取和保存回写后刷新必须读到同一份当前态；不能一套 seed 数据给列表，另一套内存对象给详情或动作。

## List And Detail

分页和详情读取都应从 runtime store 取数，而不是组件内数组过滤。

```js
function queryHeaders(query = {}) {
  const { page, size } = parsePagination(query);
  const { requisitionNum, authorizationStatus } = query;
  const filtered = store.headers.filter((item) => {
    const matchNum = !requisitionNum || item.requisitionNum.includes(requisitionNum);
    const matchStatus = !authorizationStatus || item.authorizationStatus === authorizationStatus;
    return matchNum && matchStatus;
  });

  const start = page * size;
  const content = filtered.slice(start, start + size);

  return {
    content: clone(content),
    totalElements: filtered.length,
    size,
    number: page,
  };
}

function getDetail(headerId) {
  const header = findHeader(headerId);

  if (!header) {
    return null;
  }

  return {
    ...clone(header),
    lineList: getLines(headerId),
  };
}
```

规则：
- 分页接口必须返回 `content / totalElements / size / number`。
- `page` 按 0-based 处理，缺省为 0；只接受 `page/size`，不得读取 `currentPage/pageSize`。
- 详情响应中的 `lineList` 与列表中的 header 必须来自同一 store。
- Query、Reset、Refresh、Action 后重查都必须走 HTTP mock API，不得靠页面本地数组兜底。
- handler 层必须消费 `getDetail()` 的 `null` 并返回明确 not-found，不得把 `null/undefined` 继续传给 `enrich*` 或响应组装。

```js
function sendNotFound(res) {
  return sendJson(res, 404, { message: '数据不存在' });
}

function handleDetailQuery(req, res, headerId) {
  const detail = getDetail(headerId);

  if (!detail) {
    return sendNotFound(res);
  }

  return sendJson(res, 200, detail);
}

function handleLineQuery(req, res, headerId) {
  const header = findHeader(headerId);

  if (!header) {
    return sendNotFound(res);
  }

  return sendJson(res, 200, {
    content: getLines(headerId),
    totalElements: getLines(headerId).length,
    size: getLines(headerId).length,
    number: 0,
  });
}
```

规则：
- `find* / get* / lookup*` 后必须先判空，再访问字段、读取明细或调用 `enrich*`。
- 明细查询缺少父 header 时必须返回 not-found；不能返回 `200 + []` 掩盖错误。
- `enrichHeader(findHeader(id))`、无判空的 `return enrichHeader(header)`、判空前读取 `header.lineList` 都是运行时崩溃风险。

## Save

保存动作必须同时处理 header 和 line，并写回 store。

```js
function saveDetail(payload) {
  const header = payload?.header || {};
  const inputLines = Array.isArray(payload?.lineList) ? payload.lineList : [];
  const headerId = header.requisitionHeaderId
    ? normalizeId(header.requisitionHeaderId)
    : String(++store.headerSeq);

  const nextHeader = {
    ...header,
    requisitionHeaderId: headerId,
    authorizationStatus: header.authorizationStatus || 'NEW',
  };

  const lineList = inputLines.map((line) => ({
    ...line,
    requisitionHeaderId: headerId,
    requisitionLineId: line.requisitionLineId ? normalizeId(line.requisitionLineId) : String(++store.lineSeq),
  }));

  const index = store.headers.findIndex((item) => item.requisitionHeaderId === headerId);

  if (index >= 0) {
    store.headers[index] = nextHeader;
  } else {
    store.headers.unshift(nextHeader);
  }

  store.linesByHeaderId[headerId] = lineList;
  return getDetail(headerId);
}
```

规则：
- 保存后详情重查、列表刷新和行表刷新必须都读取到新状态。
- 行数据应在 save 时与 header 统一归档，不得留在页面局部 state 作为事实源。

## Delete And Status Actions

业务状态动作必须二次校验当前态。UI 按钮守卫和 handler 校验要同源，但 handler 仍要再次检查。

```js
const STATUS_GUARDS = {
  submit: ['NEW', 'REJECTED'],
  withdraw: ['IN_APPROVAL'],
  delete: ['NEW', 'CANCELLED'],
};

function assertTransition(action, currentStatus) {
  const allowed = STATUS_GUARDS[action] || [];

  if (!allowed.includes(currentStatus)) {
    return {
      ok: false,
      message: '当前状态不允许执行该操作',
    };
  }

  return { ok: true };
}

function submitHeader(headerId) {
  const current = findHeader(headerId);
  if (!current) return { statusCode: 404, body: { message: '数据不存在' } };

  const result = assertTransition('submit', current.authorizationStatus);
  if (!result.ok) return { statusCode: 400, body: { message: result.message } };

  current.authorizationStatus = 'IN_APPROVAL';
  return { statusCode: 200, body: getDetail(headerId) };
}

function withdrawHeader(headerId) {
  const current = findHeader(headerId);
  if (!current) return { statusCode: 404, body: { message: '数据不存在' } };

  const result = assertTransition('withdraw', current.authorizationStatus);
  if (!result.ok) return { statusCode: 400, body: { message: result.message } };

  current.authorizationStatus = 'WITHDRAWN';
  return { statusCode: 200, body: getDetail(headerId) };
}

function deleteHeaders(headerIds) {
  const normalizedIds = (headerIds || []).map(normalizeId);

  normalizedIds.forEach((headerId) => {
    const current = findHeader(headerId);
    if (!current) {
      return;
    }

    const result = assertTransition('delete', current.authorizationStatus);
    if (!result.ok) {
      throw new Error(result.message);
    }

    store.headers = store.headers.filter((item) => item.requisitionHeaderId !== headerId);
    delete store.linesByHeaderId[headerId];
  });

  return { failed: false };
}
```

规则：
- handler 必须从 runtime store 读取当前状态；不能只信任前端传来的旧状态。
- 删除、提交、撤回、作废、复制等动作都要有允许源状态。
- header 删除时 line store 也要同步清理。

## Anti-Patterns

以下都不应作为 mock-request 正常实现：

- 页面组件内 `const list = [...]` 后本地 filter/pagination。
- `save/delete/submit` 只改页面 state，不改 middleware runtime store。
- 列表、详情、状态动作各自维护不同数据源。
- 只在按钮 disabled/hidden 上做状态限制，handler 无条件成功。
- 用 `statusMeaning`、`authorizationStatusMeaning` 之类展示字段判断状态机。
- 生成 `ATTACHMENT_DEMO_*`、`MOCK_*`、template/bucket/storage 常量并直接写入页面组件。

# Row Actions Scenario

## 阅读路由

- Active owner: `front-hzero-choerodon-ui`.
- Related owner: `front-hzero-renderer` owns `c7nOperatorRender` / `operatorRender` helper contract.
- 触发词：操作列、行操作、批量操作、actions、operator、查看、编辑、删除、预览、下载、lock right、更多菜单。

## Scope

行操作是 Choerodon Pro Table 场景，不再作为独立 active skill。Table 列定义、操作列位置、宽度、右锁定、Button type 和 DataSet record 归 `front-hzero-choerodon-ui`；renderer helper 的 import、签名、payload 和调用形态仍归 `front-hzero-renderer`；权限码和按钮权限归 `front-hzero-permission-button`。

## Stage Routing

- Design：确认动作清单、权限、状态守卫、二次确认、批量操作、异步 loading / pending 策略和 renderer helper 策略。
- Implementation：操作列必须作为最后一列并使用正确右锁定；多动作优先使用 owner 确认的 helper；调用接口的动作必须有 loading / pending 过渡和重复点击保护。
- Review：检查 `fixed` / `lock=true` 误用、缺少 `title`、裸按钮数组、权限复用、空操作列、破坏性动作缺确认、接口动作缺 loading / 重复点击保护。
- Verification：验证动作可见性、权限隐藏/禁用、更多菜单、二次确认、接口动作 loading / pending 和关键状态守卫。

## Implementation Skeleton

多动作 HZERO + Choerodon Pro Table 操作列默认使用标准 helper，不因相似页面存在裸按钮或 `command` 函数而降级：

```tsx
import { Button as ButtonPermission } from 'components/Permission';
import { ColumnLock } from 'choerodon-ui/pro/lib/table/enum';
import { c7nOperatorRender } from 'utils/renderer';

const ACTION_VISIBLE_LIMIT = 3;

const buildPermission = (action) => [{ code: permission(action), type: 'button' }];

const operationColumn = {
  name: 'operation',
  header: intl.get('hzero.common.button.action').d('操作'),
  width: 220,
  lock: ColumnLock.right,
  renderer: ({ record }) => {
    const operators = [];

    if (canView(record)) {
      const title = intl.get(`${promptCode}.button.detail`).d('详情');
      operators.push({
        key: 'detail',
        ele: (
          <ButtonPermission
            type="text"
            permissionList={buildPermission('detail')}
            onClick={() => handleView(record)}
          >
            {title}
          </ButtonPermission>
        ),
        len: 2,
        title,
      });
    }

    if (canEdit(record)) {
      const title = intl.get(`${promptCode}.button.edit`).d('编辑');
      operators.push({
        key: 'edit',
        ele: (
          <ButtonPermission
            type="text"
            permissionList={buildPermission('edit')}
            onClick={() => handleEdit(record)}
          >
            {title}
          </ButtonPermission>
        ),
        len: 2,
        title,
      });
    }

    return operators.length ? c7nOperatorRender(operators, record, { limit: ACTION_VISIBLE_LIMIT }) : null;
  },
};
```

替换时必须保持这些锚点：
- import 坐标默认是 `components/Permission` 和 `utils/renderer`；目标项目已确认别名或 wrapper 时记录 `project-override` 证据。
- `operators` item 默认使用 `{ key, ele, len, title }`，`ele` 必须是 helper 可渲染的行操作 ReactNode。required 权限动作默认使用 `ButtonPermission type="text"`、项目 confirmed 权限按钮或确认组件包裹后的 ReactNode；`not-applicable` 且有来源 reason 的动作可使用 C7N `Button type="text"`、链接态按钮或项目 confirmed row-action 控件。不得把 `ele` 写成 `intl.get(...).d(...)`、字符串或文案变量；`title` 与按钮文案同源，`len` 覆盖可见文案宽度。
- required 权限必须放在 `ele` 内的按钮组件上；`c7nOperatorRender` options 默认只传 `{ limit }` 或项目 confirmed overflow 配置，不用 `{ permissionList: ... }` 替代行按钮权限。
- 动态动作先按 `visibleWhen` 过滤不可见项，再传给 `c7nOperatorRender` / `operatorRender`。来源写“启用/禁用/置灰/可点击”时不得过滤隐藏，应保留行操作并按 `enabledWhen` 置灰；来源写“显示/隐藏/仅显示”时才控制 `visibleWhen`。
- 业务置灰动作必须有用户可理解的禁用原因。行操作默认通过 Tooltip、`title`、项目 confirmed disabled wrapper 或等价轻量提示暴露 `disabledReasonSource`；删除、撤回、提交、作废等状态动作不允许只灰掉且无原因。
- 操作列位于最后一列，右锁定使用 `ColumnLock.right` 或项目 confirmed 等价 enum；`lock: 'right'`、`fixed: 'right'` 和只配置 `width` 均不能证明右锁定。
- 行操作权限按钮使用 `ButtonPermission type="text"`；Header / Toolbar / 页面级按钮不得套用行操作样式。
- 删除、撤回、取消、作废等破坏性动作必须有项目确认的二次确认或 UI Contract 豁免；删除默认不得豁免。确认弹窗取消时不得触发请求、状态变更或 loading；确认后才执行接口动作。
- 所有调用接口、DataSet `query/submit/delete`、service request 或 mock request 的行/批量动作必须有 loading / pending 过渡和重复点击保护。行级接口动作默认使用当前 record 的 row-level pending key；批量动作默认使用 batch-level pending key；handler 入口必须先判断 pending 并阻断重复触发，请求分支使用 `try/finally` 或等价机制释放 pending。不得只在成功分支清理 loading，也不得让取消确认进入 loading。
- 删除类动作必须先确认再设置 loading 和发请求；`onClick` 只能打开确认或执行本地未保存草稿移除，不能直接调用删除接口。`Popconfirm.onConfirm`、`Modal.confirm.onOk` 或 confirmed wrapper 的确认回调才承载真实 delete/remove request。
- 批量动作按钮若依赖 DataSet 选中行、Table selection 或 `dataSet.selected`，必须通过 `select/unSelect/selectAll/unSelectAll/load/reset` 等事件、React state 或项目 confirmed wrapper 触发按钮态重算；只在 render 中读取 `selected.length` 且选中变化不会刷新 React 的实现不得声明通过。
- 当前行无可见动作时返回 `null`；整页无任何可见行动作时不追加空操作列。

## Rejection Anchors

- 多动作操作列在 `renderer`、`render` 或 `command` 中直接返回 Button / ButtonPermission 数组、Fragment、链接列表或自建更多 Drawer / Modal。
- `column.command` 写成函数形态承载业务动作，或 `command` 返回 ReactNode。
- 把裸 JSX 元素数组传给 helper，例如 `c7nOperatorRender([<Button />], record, options)`，导致缺少 `action.ele`。
- 把按钮文案传给 `ele`，例如 `ele: intl.get(...).d('详情')`、`ele: '详情'` 或 `ele: detailText`，而不是把文案放进行操作按钮 children。
- required 权限动作把 `permissionList` 只放到 `c7nOperatorRender(..., options)`，但 `ele` 内没有 `ButtonPermission` / confirmed 权限按钮。
- 为修复按钮不显示而删除 helper、改回 raw Fragment 或按钮数组。
- 缺少稳定 `key`、缺少 `title`、`title` 与 `ele` 文案不同源、`len` 与文案宽度明显不匹配。
- 用提高 `limit` 或展示全部动作来掩盖按钮截断，且无 UI Contract 或用户确认。
- 行操作列误用 Header / Toolbar 的 `type="c7n-pro"`，或 Header / Toolbar 误用行操作的 `type="text"`。
- UI 隐藏了动作但 handler 没有二次状态守卫。
- FDS/UI Contract 只要求“启用/禁用/置灰”的动作被实现成条件隐藏，或 disabled 后无禁用原因/hover/title/project wrapper 提示。
- 批量按钮依赖 `dataSet.selected` / Table selection 却没有 selection 事件桥接或等价 React state，导致选中/取消选中后按钮态不刷新。
- 调用接口的行/批量动作没有 loading / pending 过渡、缺少重复点击保护、loading 只在成功分支释放，或取消确认后进入 loading。
- 删除、撤回、取消、作废等破坏性动作在 `onClick` 中直接发请求，未通过 `Popconfirm`、`Modal.confirm` 或 confirmed wrapper 的确认回调执行。

## Owner Source

新增规则只写入本 reference、Choerodon UI owner references 或 `front-hzero-renderer`。

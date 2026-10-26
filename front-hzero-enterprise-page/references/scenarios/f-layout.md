# F Layout Scenario

## 阅读路由

- Active owner: `front-hzero-enterprise-page`.
- 触发词：F 型布局、左列表右详情、ListHeader、ListItem、ContentCard、EmptyPage、`_LOCATED_DATA_`、TabsAdsorptionContainer、吸附详情。

## Scope

F 型布局是企业页面布局场景，不再作为独立 skill 承担 active owner。页面结构、Header/Content、i18n、route/menu、权限和 HZERO 页面协议归 `front-hzero-enterprise-page`；详情集合中的 DataSet / Table / Form 规则归 `front-hzero-choerodon-ui`；头行明细事务同时读取 master-detail scenario。

## Stage Routing

- Design：确认左侧列表、右侧详情、选中项定位、空态、保存后刷新和路由上下文。
- Implementation：按企业页面 Header/Content 和 Choerodon 组件规则实现，不得用自建布局绕过标准页面结构。
- Review：检查布局状态、选中项恢复、空态、权限入口、i18n 和 `rejectedPatternItems`。
- Verification：验证首屏、列表选择、详情切换、保存后定位和空态。

## Minimal Implementation Shape

```tsx
<Header title={intl.get('example.title').d('示例页面')} />
<Content>
  <TabsAdsorptionContainer>
    <ListHeader />
    <div className="hzero-f-layout">
      <List dataSet={listDS}>
        {record => (
          <ListItem
            key={record.get('id')}
            selected={record.get('id') === locatedDataId}
            onClick={() => setLocatedData(record.toData())}
          />
        )}
      </List>
      {locatedData ? <ContentCard /> : <EmptyPage />}
    </div>
  </TabsAdsorptionContainer>
</Content>
```

## Rejection Anchors

- 必须记录 `_LOCATED_DATA_` 或等价选中项定位策略、列表折叠/宽度、空态和保存后刷新定位。
- 不得用无 Header/Content 边界的自建双栏布局替代 HZERO 企业页面结构。
- 右侧详情命中表单、表格或头行明细时，必须同步触发 `front-hzero-choerodon-ui` 的 `master-detail` 或相关 Table/DataSet 规则。
- 保存后不得丢失当前选中项；不能验证时必须进入 Verification / Handoff 风险。

## Owner Source

新增规则只写入本 reference 或对应核心 owner reference。

# Customization Scenario

## 阅读路由

- Active owner: `front-hzero-enterprise-page`.
- 触发词：二开、客制化、route override、priority、租户定制、主题字体、headScripts、标准包覆盖。

## Scope

客制化是 HZERO 企业页面和运行时边界场景，不再作为常规阶段独立 skill。页面覆盖、route override、权限/i18n 影响、租户差异和标准包覆盖归 `front-hzero-enterprise-page`；构建、部署和产物加载差异归 `front-hzero-build-deploy`。

## Stage Routing

- Design：确认覆盖目标、优先级、租户/组织上下文和不可影响的标准能力。
- Implementation：只在 confirmed customization scope 内修改，不得用薄 wrapper 隐藏标准组件合同。
- Review：检查 route override、priority、标准包覆盖、i18n/permission 和 dependency drift。
- Verification：验证目标租户/路由/页面入口，未验证租户差异必须进入 handoff risk。

## Minimal Implementation Shape

```ts
export const customizationRoute = {
  path: '/example/custom',
  component: './routes/Example/Custom',
  authorized: true,
  priority: 20,
  tenantScope: ['confirmedTenantId'],
};

export const customizationManifest = {
  overrideTarget: '/example/standard',
  overrideSource: 'user-confirmed / route-config evidence',
  affectedPermissions: ['example.custom.view'],
  replacementRisk: 'standard-package-upgrade-review-required',
};
```

## Rejection Anchors

- 必须记录 `overrideTarget`、`priority`、租户/组织范围、权限/i18n 影响和标准包升级风险。
- 不得用普通页面 wrapper、薄 adapter 或复制标准页面代码隐藏 route override / 标准包覆盖边界。
- 未确认租户差异、客户化资源隔离或 route 优先级时，不得声明 production-ready。
- 构建产物、资源加载或 remote/chunk 差异命中时，必须同步 `front-hzero-build-deploy`。

## Owner Source

新增规则只写入本 reference 或对应核心 owner reference。

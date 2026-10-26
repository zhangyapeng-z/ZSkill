# Choerodon 配置参考

## 事实边界
本文件只记录常见配置决策中可直接影响作用域、默认值和局部配置判断的事实。

如果这里没有覆盖某个配置事实，不要编造字段、默认值或协议行为。应视为未确认，并要求提供用户输入、官方资料或项目证据。

## 全局 Configure
文档示例：

```tsx
import { configure, getConfig } from 'choerodon-ui';

configure({ prefixCls: 'c7n' });
const prefixCls = getConfig('prefixCls');
```

全局 `configure` 只应用于项目级行为。对于页面局部或模块局部行为，如果项目源码支持，应优先使用局部 wrapper 或 provider 模式。

`getConfig(key)` 读取的是全局 `configure` 值，不会读取 `ConfigProvider` 的局部上下文。

## ConfigProvider 与局部配置
- `ConfigProvider` 提供基于 React context 的局部作用域配置。
- 它可以包裹整个应用、某个模块或局部子树。
- 它的 API 与全局配置保持一致，但应主要用于局部作用域行为。
- 函数组件应使用 `useConfig` 读取局部配置。
- 类组件可使用 ConfigContext。
- DataSet 不是 React 组件；它不会自动接收 `ConfigProvider` context。
- 当需要局部配置时，函数组件可通过 `useDataSet` 创建 DataSet。
- 类组件在需要时可传入 `{ getConfig: this.context.getConfig }` 作为 DataSet 构造上下文。

优先级通常是：
1. 组件库默认值
2. `configure`
3. `ConfigProvider`
4. 组件 props

如果项目存在 UED/theme 层，部分优先级可能变化。没有项目证据时，不要断言最终优先级。

## 常见全局配置领域
配置通常覆盖：
- Prefixes: `prefixCls`, `proPrefixCls`, `iconfontPrefix`.
- Lookup/Lov: `lookupUrl`, `lookupAxiosConfig`, lookup batch config, `lovDefineUrl`, `lovQueryUrl`, Lov table/modal/query behavior.
- DataSet defaults: `autoCount`, `dataKey`, `totalKey`, `countKey`, `statusKey`, `tlsKey`, status mapping, default `transport`, feedback, pagination generation.
- Form defaults: label layout/alignment, colon, required mark, validation display, help display.
- Table defaults: `queryBar`, virtual behavior, border, row height, row/column behavior, personalization/customization, pagination.
- Modal/Drawer defaults: mask closable, keyboard, resizable, movable, section border, auto focus, drawer animation and layout.
- Select/input defaults: search behavior, trigger, option filtering, autocomplete, length warnings.
- Attachment can also be configured globally.

从枚举事实迁入的配置相关 enum/type 事实：
- `choerodon-ui/lib/configure/interface`：`InputSuffixCompName` 可包含 `TextField`、`SecretField`、`UrlField`、`Password`、`TextArea`、`IntlField`、`EmailField`、`NumberField`、`Currency`、`DatePicker`、`Cascader`、`Select`、`AutoComplete`、`Lov`、`TreeSelect`、`ColorPicker`、`IconPicker`。
- `choerodon-ui/pro/lib/core/enum`：`Tooltip.none`、`always`、`overflow`；`WaitType.throttle`、`debounce`；`FieldFocusMode.checked`、`focus`。
- Choerodon dataset/pro locale context 中存在 locale 枚举覆盖（`Lang`，例如 `zh_CN`、`en_US`、`ja_JP`），但普通页面工作不应枚举全部 locale；应使用项目 i18n 配置或已确认的 locale 需求。

高频默认项：
- 基础：`prefixCls`、`proPrefixCls`、`iconfontPrefix`、`icons`、`ripple`、`axios`、`renderEmpty`
- lookup/select：`lookupCache`、`lookupUrl`、`lookupAxiosConfig`、`lookupAxiosMethod`、`lookupBatchAxiosConfig`、`useLookupBatch`、`selectSearchable`、`selectBoxSearchable`、`selectTrigger`、`defaultActiveFirstOption`
- Lov：`lovDefineUrl`、`lovDefineAxiosConfig`、`lovDefineBatchAxiosConfig`、`useLovDefineBatch`、`lovQueryUrl`、`lovQueryAxiosConfig`、`lovTableProps`、`lovModalProps`、`lovAutoSelectSingle`、`lovNoCache`、`lovQueryBar`、`lovQueryBarProps`
- DataSet：`autoCount`、`dataKey`、`totalKey`、`countKey`、`statusKey`、`tlsKey`、`status`、`generatePageQuery`、`feedback`、`transport`、`strictPageSize`、`cacheRecords`、`confirm`
- Form/Field：`labelLayout`、`labelAlign`、`labelWidth`、`useColon`、`requiredMarkAlign`、`showValidation`、`showHelp`、`showLengthInfo`、`valueChangeAction`
- Table：`queryBar`、`queryBarProps`、`tableVirtual`、`tableVirtualCell`、`tableBorder`、`tableRowHeight`、`tableButtonProps`、`tableColumnResizable`、`tableColumnHideable`、`tableColumnDraggable`、`customizable`
- Modal/Drawer：mask、keyboard、resizable、movable、section border、auto focus 以及 drawer 专属默认项
- DynamicFilterBar：`tableFilterAdapter`、`tableFilterSearchText`、`tableFilterSuffix`

## 配置规则
- 不要为了修一个页面问题就新增项目级 `configure`。
- 在新增默认配置前，先检查现有 app 或 module 配置。
- HZERO 项目可能有自己的 runtime/layout/config 边界；应用级放置应优先遵循 HZERO skill。
- 不要在全局 lookup/lov/attachment/transport 配置里编造后端 URL。

决策指引：
- 项目级行为：`configure`
- 模块/子树行为：`ConfigProvider`
- 单个组件实例：组件 props
- DataSet 需要局部配置：`useDataSet` 或 DataSet 构造上下文
- 跨页共享的 Lov/lookup/Attachment 后端协议：通常属于全局配置，但前提是契约已确认

## 需要确认的未定项
- 这次变更是全局、模块局部还是页面局部。
- 现有 configure 位置和项目约定。
- 后端 lookup/lov/transport/attachment 协议。
- 该设置是否由 HZERO runtime config 接管。

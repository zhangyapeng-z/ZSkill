# 自定义组件发现参考

## 目标
在 Figma 转代码前，先发现项目是否已有业务封装组件，避免直接落到 HZERO/Choerodon 标准组件或手写 HTML。

## 搜索入口
优先在目标前端工程中搜索：
- 页面目录中的相似业务页面。
- `components/`、`common/`、`shared/`、`layouts/`、`containers/`。
- `routes`、`pages`、`modules`、`packages` 下的局部封装。
- HZERO 项目的 `src/components`、`src/utils`、`src/services`、`models`、`routes-config`。

## 页面容器
候选命名：
- `PageHeader`、`PageHeaderWrapper`、`Header`、`Content`。
- `PageContainer`、`ContentWrapper`、`CardPage`、`SectionCard`。
- `BasicLayout`、`DetailLayout`、`FormPage`、`ListPage`。

确认点：
- 是否内置 breadcrumb、title、back、extra actions。
- 是否接 i18n、权限或 loading。
- 是否要求特定 children 结构。

## 表单封装
候选命名：
- `BizForm`、`BaseForm`、`SearchForm`、`QueryForm`、`CompactForm`。
- `FormItem`、`FieldItem`、`FormSection`、`EditableForm`。
- `ModalForm`、`DrawerForm`、`DetailForm`。

确认点：
- 数据源是 DataSet、Form instance、props 还是 model。
- 字段配置是否支持 label、required、type、options、lov、lookup。
- 是否内置校验、提交、只读态和布局列数。

## 表格和筛选条封装
候选命名：
- `BizTable`、`BaseTable`、`SearchTable`、`ListTable`、`ProTableWrapper`。
- `FilterBar`、`DynamicFilter`、`AdvancedSearch`、`TableFilter`。
- `Toolbar`、`TableToolbar`、`ActionBar`、`BatchActions`。

确认点：
- 分页、排序、筛选协议由谁处理。
- columns 配置格式和 action render 约定。
- 是否支持行选择、批量操作、刷新、列设置。
- 是否已经封装 keyword search、默认筛选、添加筛选。

## 权限按钮
候选命名：
- `PermissionButton`、`AuthorizedButton`、`AuthButton`、`ButtonPermission`。
- HZERO `Permission`、`permissionList` 相关封装。

确认点：
- 权限码来源：route path、permissionList、menu code 或后端返回。
- 无权限时隐藏、禁用还是降级展示。
- loading、confirm、danger、icon 是否内置。

## i18n 和请求封装
候选命名：
- `intl.get`、`formatterCollections`、`useIntl`、`formatMessage`。
- `request`、`axios` wrapper、`service`、`model`、`effects`。

确认点：
- 文案 key 命名规则。
- service 文件目录和 model namespace。
- 请求是否自动注入 tenantId、organizationId、prefix、headers。

## 发现输出
每次发现后输出：
1. 已确认可用的自定义组件。
2. import 路径和 API 证据位置。
3. 可映射 PageSchema 区块。
4. 仍需确认的 props、事件或数据协议。
5. 如果未发现，说明降级路线：HZERO 标准模式或 Choerodon 标准模式。

## 反模式
- 只按组件名字相似就直接使用。
- 未确认 props 就生成调用代码。
- 已有项目封装仍手写通用 Table/Form。
- 不查相似页面，直接从 Figma 生成全新结构。

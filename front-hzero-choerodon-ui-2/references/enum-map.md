# Choerodon Enum Map Reference

## 阅读路由
- 判断本文件能否作为 confirmed 项目证据前读 `用途` 和 `状态策略`。
- DataSet 枚举候选读 `DataSet`。
- Table 枚举候选读 `Table`。
- Form、Field 和组件枚举候选读 `Form And Field`、`Components`。
- 遇到重名枚举、导入歧义或禁止用法时读 `重名与歧义` 和 `禁止项`。

## 用途
本文件是 Choerodon / Choerodon UI Pro / DataSet 枚举与导入路径的集中 fallback reference，用于：

- 构建或评估 Evidence 中的 `Choerodon Enum Import Map`。
- 识别 DataSet、Table、Form、Button、Lov、Attachment 等枚举型 props 的候选枚举域。
- 处理 `ColumnAlign`、`ButtonType`、`ViewMode`、`TableQueryBarType` 等重名枚举的导入歧义。

本文件不是目标项目证据。仅命中本文件时，状态只能是 `generatedCandidate / fallback / missing`，不得标记为项目 `confirmed`。生产实现仍优先使用 Evidence enum import map 或目标项目 import 证据；组件 props 不使用项目字符串风格，DataSet 配置类枚举只有同一目标工程健康证据时才允许 confirmed-string 策略。

## 状态策略
| 证据来源 | 允许状态 | 生成策略 |
| --- | --- | --- |
| 目标项目同类代码已有稳定 enum import | confirmed | 按项目 import 生成 |
| 目标项目同类 DataSet 配置稳定使用字符串，且本 reference 支持 | dataSet-confirmed-string / rejected | 只有同一目标工程健康 DataSet 样例才能作为 confirmed-string；若样例伴随 `as any`、无类型 renderer、enum/string 混用或被 baseline comparison 判为 legacy-risk，必须写入 `rejectedPatternItems`，不得形成字符串策略；组件 props 字符串不得作为新增实现形态 |
| 目标项目 mixed | needs-decision | Design / Task 选择单一策略并写 reason |
| 只有本 reference 命中 | generatedCandidate / fallback | 可进入设计候选，不得作为 production confirmed |
| 无项目证据且本 reference 未覆盖 | missing | 阻塞或回 Explore / Choerodon 专项补证据 |

## DataSet
常见 import：

- `choerodon-ui/pro/lib/data-set/enum`
- 目标项目若从其它 DataSet enum re-export 导入，只能记录为历史兼容/冲突证据；不得沿用为生成坐标，也不得用 project-confirmed evidence 覆盖内置标准坐标。若 `choerodon-ui/pro/lib/data-set/enum` 在目标版本不可用，必须 blocked 并回 Choerodon owner 专项确认。
- `DataSet` 运行时类可以从 `choerodon-ui/pro` 命名导入，但 `FieldType`、`DataSetSelection`、`DataToJSON`、`DataSetEvents` 等 DataSet enum 不得从 `choerodon-ui/pro` 聚合入口导入。`import { DataSet, FieldType } from 'choerodon-ui/pro'` 会在部分 HZEROJS/Choerodon 版本中得到 `FieldType === undefined`，字段写 `FieldType.string` 时触发 `Cannot read properties of undefined (reading 'string')`。命中 `HZC-DATASET-ENUM-IMPORT-001` / `c7n_dataset_enum_invalid_import_source`，至少 major；页面启动已崩溃或仍声明 usable=true / production-ready 时 blocking。

`choerodon-ui/pro/lib/data-set/enum` 常见成员：

| enum | 常见成员 |
| --- | --- |
| FieldType | auto, boolean, number, currency, string, date, dateTime, week, month, year, time, quarter, object, intl, email, url, color, json, attachment, secret, reactNode, bigNumber |
| DataSetSelection | single, multiple |
| DataToJSON | dirty, selected, all, normal, dirty-field, dirty-self, selected-self, all-self, normal-self, dirty-field-self |
| RecordStatus | delete, update, add, sync |
| RecordCachedType | selected, delete, update, add |
| DataSetEvents | query, beforeLoad, load, loadFailed, submit, submitSuccess, submitFailed, select, unSelect, batchSelect, batchUnSelect, selectAllPage, unSelectAllPage, update, fieldChange, export, create, beforeRemove, remove, beforeDelete, reset, validate, validateSelf |
| DataSetStatus | loading, submitting, ready |
| ExportMode | server, client |
| SortOrder | asc, desc |
| FieldIgnore | always, clean, never |
| FieldTrim | both, left, right, none |
| FieldFormat | uppercase, lowercase, capitalize |
| CheckedStrategy | SHOW_ALL, SHOW_PARENT, SHOW_CHILD |
| DateMode | time, dateTime, week, date, month, quarter, year, decade |
| NumberRoundMode | round, floor, ceil |

`DataSetSelection.single/multiple` 只用于 `new DataSet({ selection: DataSetSelection.multiple })` 这类 DataSet 配置，不得用于 Table JSX 的 `selectionMode`。

空项目、缺参考子模块、`assetBaselineSource=hzerojs-asset-baseline` 或 `enumStrategy=asset-baseline-enum` 时，DataSet 字段类型默认生成对应 `FieldType.*` 枚举成员：

```ts
import { FieldType } from 'choerodon-ui/pro/lib/data-set/enum';

const listDs = new DataSet({
  fields: [
    { name: 'applyTimeTo', type: FieldType.date },
    { name: 'authorizationStatus', type: FieldType.string },
    { name: 'amount', type: FieldType.number },
    { name: 'enabledFlag', type: FieldType.boolean },
    { name: 'approvalTime', type: FieldType.dateTime },
    { name: 'applicant', type: FieldType.object },
  ],
});
```

不得为了安抚 TypeScript 或模型输出习惯写 `type: '<fieldType>' as const`。这类任意 DataSet 字段类型字符串加 TS assertion 的写法仍是裸 enum-like 字符串，不是 enum provenance，也不能作为 asset/fallback baseline 的 confirmed 代码形态。

兼容 re-export `choerodon-ui/dataset/enum` 常见成员：

| enum | 常见成员 |
| --- | --- |
| ColumnAlign | left, center, right |
| TimeUnit | hour, minute, second, a |
| LovFieldType | INT, TEXT, DATE, DATETIME, POPUP, SELECT, HREF, PICTURE, IMG, PERCENT |

## Table
常见 import：

- `choerodon-ui/pro/lib/table/enum`
- `choerodon-ui/pro/lib/performance-table/enum`
- 目标项目若使用包装层 re-export，应优先沿用项目 import。

`choerodon-ui/pro/lib/table/enum` 常见成员：

| enum | 常见成员 |
| --- | --- |
| TableMode | list, tree |
| TableEditMode | cell, inline |
| TableQueryBarType | normal, bar, none, advancedBar, professionalBar, filterBar, comboBar |
| TableButtonType | add, delete, remove, save, query, reset, expandAll, collapseAll, export |
| TableCommandType | edit, delete |
| ColumnLock | left, right |
| ColumnAlign | left, center, right |
| DragColumnAlign | left, right |
| RowBoxPlacement | start, end |
| SelectionMode | rowbox, treebox, click, none, dblclick, mousedown |
| TablePaginationPosition | top, bottom, both |
| TableHeightType | auto, fixed, flex |
| TableAutoHeightType | maxHeight, minHeight |
| ScrollPosition | left, right, both, middle |
| HighLightRowType | click, focus |
| GroupType | header, column, row, none |
| SortRangeOption | currentDataSort, allDataSort |

Table `selectionMode` 必须导入并使用 `SelectionMode`，例如：

```tsx
import { SelectionMode } from 'choerodon-ui/pro/lib/table/enum';

<Table selectionMode={SelectionMode.rowbox} />;
```

`SelectionMode.rowbox/treebox/click/none/dblclick/mousedown` 描述 Table 交互选择方式；它不是 DataSet 的单选/多选配置。禁止写 `selectionMode={DataSetSelection.multiple}`、`selectionMode={DataSetSelection.single}` 或 `selectionMode="rowbox"`。

PerformanceTable 的 `TableQueryBarType` 可能来自 `choerodon-ui/pro/lib/performance-table/enum`，不要与普通 Pro Table 混用。

## Form And Field
常见 import：

- `choerodon-ui/pro/lib/form/enum`
- `choerodon-ui/pro/lib/field/enum`
- `choerodon-ui/pro/lib/text-field/enum`
- `choerodon-ui/pro/lib/text-area/enum`
- `choerodon-ui/pro/lib/trigger-field/enum`
- `choerodon-ui/pro/lib/intl-field/enum`

常见成员：

| import | enum / member |
| --- | --- |
| `choerodon-ui/pro/lib/form/enum` | LabelAlign: left, center, right |
| `choerodon-ui/pro/lib/form/enum` | LabelLayout: horizontal, vertical, placeholder, float, none |
| `choerodon-ui/pro/lib/form/enum` | FormLayout: table, none |
| `choerodon-ui/pro/lib/form/enum` | ResponsiveKeys: xs, sm, md, lg, xl, xxl |
| `choerodon-ui/pro/lib/form/enum` | ShowValidation: tooltip, newLine |
| `choerodon-ui/pro/lib/form/enum` | SpacingType: around, between, evenly |
| `choerodon-ui/pro/lib/form/enum` | RequiredMarkAlign: left, right |
| `choerodon-ui/pro/lib/field/enum` | ShowHelp: tooltip, newLine, label, none |
| `choerodon-ui/pro/lib/text-field/enum` | ValueChangeAction: blur, input |
| `choerodon-ui/pro/lib/text-field/enum` | GroupItemCategory: before, after, help, input |
| `choerodon-ui/pro/lib/text-area/enum` | ResizeType: both, vertical, horizontal, none |
| `choerodon-ui/pro/lib/trigger-field/enum` | TriggerViewMode: popup, drawer, modal |
| `choerodon-ui/pro/lib/intl-field/enum` | IntlType: singleLine, multipleLine |

## Components
Pro 组件常见 import：

| import | enum / member |
| --- | --- |
| `choerodon-ui/pro/lib/button/enum` | ButtonColor: default, primary, secondary, gray, blue, red, green, yellow, purple, dark |
| `choerodon-ui/pro/lib/button/enum` | FuncType: flat, raised, link |
| `choerodon-ui/pro/lib/button/enum` | ButtonType: button, submit, reset |
| `choerodon-ui/pro/lib/button/enum` | IconPlacementType: start, end |
| `choerodon-ui/pro/lib/attachment/Attachment` | AttachmentButtonType: download, remove, history |
| `choerodon-ui/pro/lib/attachment/Attachment` | AttachmentListType: text, picture, picture-card |
| `choerodon-ui/pro/lib/lov/enum` | ViewMode: default, button |
| `choerodon-ui/pro/lib/lov/enum` | PrefixRule: start, end, include |
| `choerodon-ui/pro/lib/lov/enum` | SearchAction: blur, input |
| `choerodon-ui/pro/lib/lov/enum` | SelectionsPosition: side, below |
| `choerodon-ui/pro/lib/lov/enum` | PopupSearchMode: single, multiple |
| `choerodon-ui/pro/lib/dropdown/enum` | Placements: bottomLeft, bottomCenter, bottomRight, topLeft, topCenter, topRight |
| `choerodon-ui/pro/lib/date-picker/enum` | TimeUnit: hour, minute, second, a |
| `choerodon-ui/pro/lib/radio/enum` | ViewMode: box, button |
| `choerodon-ui/pro/lib/color-picker/enum` | ViewMode: default, button |
| `choerodon-ui/pro/lib/core/enum` | Tooltip: none, always, overflow |
| `choerodon-ui/pro/lib/core/enum` | WaitType: throttle, debounce |
| `choerodon-ui/pro/lib/core/enum` | FieldFocusMode: checked, focus |

基础组件兜底常见 import：

| import | enum / member |
| --- | --- |
| `choerodon-ui/lib/button/Button` | ButtonType: default, primary, ghost, dashed, danger |
| `choerodon-ui/lib/button/Button` | ButtonFuncType: raised, flat |
| `choerodon-ui/lib/button/Button` | ButtonHTMLType: submit, button, reset |
| `choerodon-ui/lib/tabs/enum` | TabsType: line, card, editable-card, second-level |
| `choerodon-ui/lib/tabs/enum` | TabsPosition: top, bottom, left, right |
| `choerodon-ui/lib/dropdown/enum` | Placements: bottomLeft, bottomCenter, bottomRight, topLeft, topCenter, topRight |
| `choerodon-ui/lib/select/enum` | SelectMode: default, multiple, tags, combobox |
| `choerodon-ui/lib/form/enum` | FormLayout: horizontal, inline, vertical |
| `choerodon-ui/lib/form/enum` | FormItemValidateStatus: success, warning, error, validating |
| `choerodon-ui/lib/table/enum` | TableAutoHeightType: maxHeight, minHeight |

基础组件只在项目明确使用基础 `choerodon-ui`、Pro 不适用或纯展示/布局场景下作为候选；业务表单、表格、查询、附件、弹窗默认仍是 Pro-first。

## 重名与歧义
| 名称 | 风险 | 处理 |
| --- | --- | --- |
| ColumnAlign | DataSet、Table、PerformanceTable 可能都有相近语义 | 按实际组件域导入，不能跨域复用 |
| ButtonType | Pro 中常指 HTML button kind，基础 Button 中常指视觉类型 | 根据组件来源区分，禁止只按名称导入 |
| ViewMode | Lov、Radio、ColorPicker、Board、DatePicker 等多域重名 | 必须写明组件域和 importPath |
| TableQueryBarType | 普通 Pro Table 与 PerformanceTable 导入不同 | 以实际 Table 组件为准 |
| Placements | Pro Dropdown 与基础 Dropdown 均存在 | 按组件来源导入 |
| Size / FormLayout | 基础组件与 Pro 组件语义可能不同 | 不跨组件体系混用 |

## 禁止项
- 不得用 `lock: true` 或 `lock: 'right'` 表示右锁定；使用项目确认的 `ColumnLock.right` 或等价 enum 导出。
- 不得在同一 feature 混用等价字符串和枚举，除非 Design/Task 明确选择并说明原因。
- 不得把本文件中的 importPath 直接写成项目 confirmed。
- 不得把弱类型相邻页面的字符串字面量写法升级为 `project-string-confirmed`；这类证据只能写入 `rejectedPatternItems` 并形成 migration finding。
- 不得用 `as any`、未导入命名空间或静态子组件猜测绕过 enum/API 证据。
- 不得用枚举知识替代业务字段、接口、权限、LOV/lookup、附件 bucket 或上传协议契约。

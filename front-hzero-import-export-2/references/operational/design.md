# 导入导出 - 设计与契约

## Standard Coordinates
| capability | component | importPath | exportShape | mode |
| --- | --- | --- | --- | --- |
| import | Import | components/Import | default | drawer-component |
| export | ExcelExportPro | components/ExcelExportPro | default | pro-component |

以上坐标固定写 `importSource=builtin-standard`、`status=confirmed`、`implementationPolicy=use-standard-import`。目标工程缺相似页面或 wrapper 不影响该结论。

## Design Contract
- `importComponentMode`：`drawer-component / project-wrapper / missing / not-applicable`。
- `exportComponentMode`：`pro-component / project-wrapper / missing / blocked / not-applicable`。
- `project-wrapper` 只允许 confirmed wrapper，且必须证明内部使用当前标准组件并保留权限、租户、请求、结果反馈和关闭刷新能力。
- `CommonImport/Route`、旧 `ExcelExport` 或内部使用旧组件的 wrapper 必须写 `migrationRequired=true`，不得成为 question 选项或实现模式。
- 普通 demo/minimum-codable 直接 `designAutoResolution=standard-import-export-direct`，不触发组件版本问题。
- 只有 current wrapper/custom 外壳冲突、用户拒绝标准入口或参数结构无法实例化时才触发 question；选项只能是标准组件与 confirmed current wrapper。

## Import Flow Contract
- component/importPath/wrapperEvidence
- templateCode/importCode、uploadEndpoint、request params 与 param placement
- template download、result handling、error detail download、closeRefreshPolicy
- tenantContext、permissionCode、status/source

## Export Request Contract
- component/importPath/wrapperEvidence
- endpoint/method/queryParams/body/selectedRows/fileName/fileType
- query/export 参数分流、templateCode、async/result handling
- tenantContext、permissionCode、status/source

业务参数缺失时生成模块级 generatedCandidate 并进入 Contract Check、Verification 和 Handoff replacement；不得改成普通 Button、Upload、自建 Modal/Drawer、静态链接或旧组件。

# 导入导出 - 领域合同

```text
ImportExportContract
  capability: import / export
  mode: drawer-component / pro-component / project-wrapper / not-applicable
  component: Import / ExcelExportPro / confirmed-current-wrapper
  importPath:
  wrapperEvidence:
  templateCode:
  endpoint:
  method:
  requestParams:
  tenantContext:
  permissionCode:
  resultHandling:
  closeRefreshPolicy:
  status: confirmed / generatedCandidate / partial / missing / conflict / not-applicable
```

`CommonImport/Route`、旧 `ExcelExport` 和旧 wrapper 不属于合同枚举，只能进入 migration finding。

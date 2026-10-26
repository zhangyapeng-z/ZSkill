# 企业页面交付检查清单

## 检查顺序
1. 模块位置、路由和菜单访问模式。
2. 页面容器：`Header + Content` 或 `PageHeaderWrapper`。
3. 国际化和页面入口 `formatterCollections`。
4. 权限按钮、权限列和 `components/Permission`。
5. 数据层：request/service/model 或 DataSet transport。
6. 上传、导入、导出、文件预览等专项能力。

## 检查点
- 用户可见文案是否使用 `intl.get().d()`。
- 是否避免新增局部 `t()` / namespace helper 包装 i18n key；若存在，是否有项目 confirmed golden-baseline 证据，且记录 `goldenBaselineStatus=confirmed` 与合法 `baselineConfirmationSource`。
- 权限 code 是否与 route path 和语义动作关联。
- 权限按钮是否符合 `front-hzero-permission-button`；是否避免旧入口、薄封装、fallback 和普通 Button 绕过 required 权限。
- 请求协议是否集中在 service/model 或 DataSet transport。
- DataSet 页面是否仍符合 HZERO 页面容器和权限规范；`Header + Content` 是否为 Fragment 下相邻根节点，业务 wrapper 是否只位于 `Content` 内部。
- 是否避免无来源 `UrlHistoryProvider`、`HistoryProvider`、`ConfigProvider` 或自定义 Provider 包裹整组 `Header + Content`。
- required 导入/导出是否存在 `ImportExportEntryProof`；入口是否为 HZERO 标准组件或项目 confirmed wrapper，component/importPath、template/request、tenantContext、permission、`buttonPermissionPlacement`、runtimeStatus 和 replacement 是否可追溯。
- mock/demo 页面是否声明查询模式、`mock-request` 数据链路、状态守卫、header+line 校验和本地 options；如需运行态状态源，只能位于 requestable mock endpoint / adapter 背后，UI/DataSet 层必须通过 request/transport 访问。
- 是否维护完整 production replacement checklist：route/menu、权限、API、字段、i18n、LOV/lookup、附件、导入导出、mock options、mock-runtime-path；`dev-mock/**` 可以保留，清单只检查是否仍连入 production success path。
- 验证结论是否区分 build、typecheck、dev/browser/manual；build 通过不得替代 typecheck 或浏览器验证。

## 常见风险
- 页面容器缺失。
- 业务 `<div className="*-detail/*-page">` 包住整组 `Header + Content`，破坏 HZERO `.page-content` 滚动语义。
- 无来源 Provider 包住 `Header + Content`，或从 legacy 相似页面复制 Provider。
- 单组件过度封装：无来源薄封装、`runtimeAdapters`、`buttonProps`、权限按钮 fallback、`t()`。
- 导入导出缺 `ImportExportEntryProof`，入口不是 HZERO 标准组件 / 项目 confirmed wrapper，或权限未放入导入 `buttonProps.permissionList` / 导出 `otherButtonProps.permissionList` / confirmed wrapper 合同。
- 权限编码随意写死。
- 上传/导出协议编造 bucket、UUID、templateCode。

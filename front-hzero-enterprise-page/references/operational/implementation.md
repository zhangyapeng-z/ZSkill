# 企业页面 - 实现与工程证据

## 阅读路由
- 企业页面 编码、修复、排障、工程证据确认或具体实现规则命中时读取。

## 本地资源
按需查本目录资源；不要外显内部路径。
- 新增、修改、审查或设计 HZERO 企业页面：优先使用 `references/schema-packets.md` 中的 `EnterprisePageContract`。
- 页面容器、service/model、DataSet 边界和平台契约模式：`references/patterns.md`。
- 常见页面结构和交付组合：`references/common-patterns.md`。
- HZERO renderer/helper 调用形态：`front-hzero-renderer`。
- HZERO import alias、helper import 和 `compilerOptions.paths` 证据：`references/tsconfig-paths.md`。
- 新建 HZEROJS `packages/<module>` 子模块时，必须继承企业前端规则中的 HZEROJS 子模块最佳范式；至少覆盖 package、tsconfig、config/config.ts、config/config.dev.ts、config/routes/index.js、父工程 packages-config 注册、registerRegex 收敛、routes-config 可选确认和子模块验证。
- HZERO core utils、`getEnvConfig`、token、附件、租户、路由、分页和响应工具边界：`references/core-utils.md`。
- i18n、Permission 和 request/model 待确认表达：`references/i18n-permission-request.md`。
- 权限按钮固定入口、Provider 入参和旧组件反模式：`front-hzero-permission-button`。
- 上传、附件和文件预览协议边界使用 `front-hzero-attachment`；导入/导出模式确认、实现、审查和验证细节使用 `front-hzero-import-export`；`ChunkUploader` 分片上传和 `NewRichTextEditor` 新版富文本使用 `front-hzero-common-components`；设计阶段 question 文案仍以 `front-hzero-enterprise-design` 的 question gate 模板 为事实源。
- 值集和 LOV 边界：`references/value-set-lov.md`。
- mock/demo 与生产契约替换边界：`references/mock-contract-boundary.md`。
- 页面交付自检：`references/page-delivery-checklist.md`。
- 需要稳定页面方案输出时使用模板：`templates/page-design.md`。

## 工作流程
1. 确认页面所在子模块、路由和菜单访问模式。
2. 选择页面容器：`Header + Content` 或 `PageHeaderWrapper`。
3. 规划国际化：`intl.get().d()` 与 `formatterCollections`。
4. 规划权限：按钮权限码、Button Contract 和 `front-hzero-permission-button` 固定入口契约。
5. 规划数据层：request/service/model 或 DataSet `transport`。
6. 如涉及上传、附件或文件预览，标注 bucket、UUID、preview URL、token/header、文件类型、接口协议等待确认项；如涉及导入或导出，只标注页面入口、权限、tenantContext 和待确认的专项规则链接，不在页面规则内展开实现细节。
7. 如涉及 Choerodon 组件，先固定 HZERO 页面容器、权限、i18n 和平台协议边界，再交给 Choerodon 的组件决策；不要在 HZERO 页面层凭视觉或经验直接生成未确认的组件 props。
8. 使用 HZERO `utils/renderer` / `hzero-front/lib/utils/renderer` 时，转 `front-hzero-renderer` 确认 helper 导出、函数签名和 JSX 组件化误用边界。
9. 按 `EnterprisePageContract` 输出页面契约、DataSet/Choerodon 边界、平台契约替换清单和验证点；无代码方案中用自然语言描述待确认项，不暴露 `<confirmed...>` 这类占位 token。
10. 页面开发或修改完成后，先按项目证据发现验证命令；依赖就绪且有低成本命令证据时运行最小 lint/typecheck，缺依赖或成本边界未接受时写 `not-run + reason`。开发态不发现、不列出 dev server/HMR/browser 启动命令，不启动或复用 dev server，不打开浏览器；只写前端服务提示：`请进入目标前端工程，按项目 README/团队约定手动启动前端服务后自测页面`。若用户当前请求或上游要求页面运行态闭合，只返回主流程安排独立 runtime acceptance 或记录用户手工证据，不在本页面 implementation 规则内执行。涉及 HZERO 子模块产物、构建配置或发布判断时，再发现目标子模块 build/compile 或对应 HZERO 构建验证；若编译耗时较长，默认列为未验证/建议补跑，用户要求完整验收、产物验证、production-ready 或发布判断时再运行。

HZERO 子模块/页面同时涉及 Choerodon DataSet、查询、表格、编辑弹窗、PermissionButton 和 Attachment/上传时，必须返回 primary / `frontend-auto-agent` 进入完整页面交付链路。编码前至少确认或列为阻塞待确认：子模块路径、路由/菜单入口、按钮权限码、页面容器、i18n namespace、字段清单、接口契约、附件标识字段和上传协议。

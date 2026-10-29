# Frontend Standard Import Coordinates

## Scope

本文件是企业前端生成代码时的标准 import 坐标索引。Design / Task / Implementation 生成 `Component Import / API Provenance` 或代码 import 前，必须先查本表；Review / Verify 发现路径漂移时，也按本表和对应 owner skill 追责。

本表只固化已经由 owner reference 明确的 `builtin-standard` 坐标、固定 helper 或标准入口。用户或 owner reference 明确为固定规则的坐标不是候选项，不进入项目 wrapper 探索，也不存在“目标工程不可解析后再 blocked/fallback”的分支；实现只按标准坐标生成，审查和验证只检查是否偏离。目标工程证据只用于三类情况：

- 证明存在健康的 project wrapper / project override，并且不削弱 owner 规则。
- 证明当前目标版本与本表坐标冲突，需要按 owner skill 的 conflict / blocked / deepImportStatus 分支处理。
- 补充业务参数、权限码、bucket/template、request helper 兼容性或 runtime 验证这类非 import 坐标事实。

目标工程缺少相似页面、缺 import 样例或缺 wrapper 证据时，不得把本表 `builtin-standard` 行降级为 `missing`、`generatedCandidate`、`use-generatedCandidate-with-verification` 或本地薄 wrapper。

## Coordinate Table

| symbol | defaultImportPath | exportShape | ownerSkill | coordinateStatus | implementationPolicy | overridePolicy | validatorRule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Header` / `Content` | `components/Page` | named | `front-hzero-enterprise-page` | builtin-standard | `use-standard-import` | 禁止 `components/Page/Header`、`components/Page/Content`、`hzero-front/lib/components/Page/*`；只有目标工程证明子路径仍统一到同一 MF shared runtime 时才允许例外 | `hzero_front_deep_import_bypasses_mf_shared` |
| `BackBtn` | `components/Page` 或项目 confirmed back navigation entry | named / confirmed wrapper | `front-hzero-enterprise-page` | builtin-standard / project-confirmed | `use-standard-import` / `use-confirmed-import` | 禁止默认使用 `components/Page/BackBtn`、`hzero-front/lib/components/Page/BackBtn`；无 confirmed wrapper 时优先从 Page barrel 或回合同确认 | `hzero_front_deep_import_bypasses_mf_shared` |
| `intl` | `utils/intl` | default | `front-hzero-enterprise-page` | builtin-standard | `use-standard-import` | 禁止 `hzero-front/lib/utils/intl/intl` | `hzero_front_deep_import_bypasses_mf_shared` |
| `formatterCollections` | `utils/intl/formatterCollections` | default | `front-hzero-enterprise-page` | builtin-standard | `use-standard-import` | 禁止 `import { formatterCollections } from 'utils/intl'`、`@common/components/lang/index`、`components/lang` 以及任意 `xxx({ code: [...] })(...)` 项目 wrapper；不要为 formatterCollections 做项目 wrapper 探索 | `hzero_intl_formatter_collections_named_import_invalid` / `hzero_intl_formatter_collections_legacy_lang_invalid` / `hzero_intl_formatter_collections_nonstandard_entry_invalid` |
| `notification` | `utils/notification` | default | `front-hzero-enterprise-page` | builtin-standard | `use-standard-import` | 禁止 `hzero-front/lib/utils/notification` | `hzero_front_deep_import_bypasses_mf_shared` |
| `request` | `utils/request` | default | `front-hzero-enterprise-design` | HZERO baseline | `use-standard-import` when no project conflict | 目标工程已有 confirmed request helper 时沿用；不得新造 request helper 或默认 native HTTP | `GCSQ-REQ-001` |
| `getResponse` | `utils/utils` | named | `front-hzero-enterprise-page` | HZERO baseline | `use-standard-import` for non-DataSet service actions when no project conflict | DataSet read 不强制使用；项目明确覆盖或冲突时按 response handling contract 处理，不向用户询问标准坐标 | response handling contract |
| `getCurrentOrganizationId` | `utils/utils` | named | `front-hzero-enterprise-design` | HZERO baseline | `use-standard-import` when tenantContext applies | 目标工程已有 confirmed tenant resolver 时沿用；不得用 `getUserOrganizationId` 替代当前租户 | tenantContext gate |
| `openTab` | `utils/menuTab` | named | `front-hzero-route` | builtin-standard | `use-standard-import` | 固定使用 `import { openTab } from 'utils/menuTab';`；它是项目级基础能力，不存在页面级 import 缺口、路由回退或用户确认分支。若该入口导致编译/运行失败，按整个前端项目不可用的构建/运行时故障处理；不得猜测其它 import、改用 `history.push` 或 `window.open` | route/openTab contract |
| `DataSet` | `choerodon-ui/pro` | named | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | 本地 `options` DataSet 必须顶层静态导入；禁止动态 require 构造 | `c7n_dataset_options_dynamic_require_dataset` |
| `Table` / `Form` / `Button` / `Modal` / `Tabs` / `Lov` / `Select` | `choerodon-ui/pro` | named | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | 业务组件默认 Pro-first；基础 `choerodon-ui` 只用于纯展示/布局或 Pro 不覆盖且有来源 | C7N component API rules |
| `Tabs.TabPane` | `choerodon-ui/pro` 的 `Tabs` | static-member | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | 禁止 `import { TabPane } from 'choerodon-ui/pro'`、`choerodon-ui/pro/lib/tab-pane`；使用 `<Tabs.TabPane>` 或 confirmed `const TabPane = Tabs.TabPane` | TabPane anti-pattern |
| `DataSetProps` | `choerodon-ui/pro/lib/data-set/DataSet` | named | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | 禁止从 `choerodon-ui/pro`、`choerodon-ui/dataset/data-set/DataSet`、`choerodon-ui/pro/lib/data-set/enum` 或任意 enum re-export 路径导入 | `c7n_dataset_props_invalid_import_source` |
| `ColumnProps` / `ColumnRenderProps` | `choerodon-ui/pro/lib/table/Column` | named | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | 空项目 / asset baseline / typed surface 场景必须使用；项目 confirmed wrapper 类型可覆盖 | `c7n_asset_baseline_table_columns_missing_typed_surface` |
| `FieldType` / `DataSetSelection` / `DataSetEvents` / common DataSet enums | `choerodon-ui/pro/lib/data-set/enum` | named | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | 禁止从 `choerodon-ui/pro` 聚合入口导入；禁止把 `choerodon-ui/dataset/enum`、`choerodon-ui/dataset/data-set/enum` 等兼容 re-export 作为生成坐标；`DataSetSelection.single/multiple` 只用于 DataSet `selection`，不得用于 Table `selectionMode`；目标工程旧写法只能作为历史兼容/冲突证据，不能覆盖内置规则，若标准坐标不可用则 blocked 并回 Choerodon owner 专项确认 | `c7n_dataset_enum_invalid_import_source` / `c7n_dataset_enum_nonstandard_import_source` / `c7n_table_selection_mode_wrong_enum_domain` / enum provenance rules |
| `SelectionMode` / common Table enums | `choerodon-ui/pro/lib/table/enum` | named | `front-hzero-choerodon-ui` | builtin-standard | `use-standard-import` | Table `selectionMode` 固定使用 `SelectionMode.rowbox/treebox/click/none/dblclick/mousedown`；禁止裸字符串和 `DataSetSelection.single/multiple`。其它 Table props 按 `TableQueryBarType`、`TableEditMode`、`ColumnLock`、`ColumnAlign` 等精确 enum 域生成 | `c7n_enum_like_string_without_provenance_*` / `c7n_table_selection_mode_wrong_enum_domain` |
| `ButtonPermission` | `components/Permission` | named alias: `Button as ButtonPermission` | `front-hzero-permission-button` | builtin-standard | `use-standard-import` | 禁止 `import { ButtonPermission } from 'components/Permission'`、`components/PermissionButton`、`@common/components/PermissionButton`、本地 `*PermissionButton` 薄封装、`PermissionButton || Button` fallback；不探索项目封装，不输出目标缺导出分支 | `hzero_permission_button_import_shape_invalid` / `hzero_permission_button_legacy_entry_invalid` |
| `Import` | `components/Import` | default | `front-hzero-import-export` | builtin-standard | `use-standard-import` | confirmed wrapper 才能覆盖；不得用普通 Button、Upload、自建 Modal/Drawer 或 `HeaderImportAction` 假 wrapper 替代 | `hzero_import_*` / `GCSQ-IX-001` |
| `ExcelExportPro` | `components/ExcelExportPro` | default | `front-hzero-import-export` | builtin-standard | `use-standard-import` | 新版导出默认；confirmed wrapper 才能覆盖 | `hzero_export_*` / `GCSQ-IX-001` |
| `TagRender` / `enableRender` / `yesOrNoRender` / `dateRender` / `dateTimeRender` / `numberRender` | `utils/renderer` | named | `front-hzero-renderer` | builtin-standard | `use-standard-import` | 项目 renderer module confirmed 时可覆盖；不得 JSX 化 helper | renderer helper rules |
| `operatorRender` / `c7nOperatorRender` | `utils/renderer` | named | `front-hzero-renderer` | builtin-standard | `use-standard-import` | 缺 import/export 时修复或阻塞，不降级为 Fragment / naked buttons；payload 必须是 action object | `GCSQ-RENDER-001` |
| `Attachment` / `Attachment.Dragger` | `choerodon-ui/pro` | named + static member | `front-hzero-attachment` | builtin-standard | `use-standard-import` | 若目标版本证据显示桶入口循环依赖或 `ReferenceError: Attachment is not defined`，记录 `barrelImportStatus=unsafe / deepImportStatus=confirmed` 后允许 `import Attachment from 'choerodon-ui/pro/lib/attachment'`；confirmed wrapper 可覆盖 | attachment rules |
| `ChunkUploader` | `components/ChunkUploader` | default / project component evidence | `front-hzero-common-components` | builtin-standard / version-gated | `use-standard-import` when component required | 缺 bucket/upload 参数不影响保留标准组件；依赖/版本证据否定时 blocked 或 wrapper | common component rules |
| `NewRichTextEditor` / `RichTextViewer` | `components/NewRichTextEditor` / `components/RichTextViewer` | default / project component evidence | `front-hzero-common-components` | builtin-standard / version-gated | `use-standard-import` when component required | 不归入 Choerodon rich-text；缺协议参数写 generatedCandidate / replacement | common component rules |

## Consumption Rules

- Design / Contract Check 必须把命中本表的行写入 `Component Import / API Provenance`，字段至少包含 `symbol`、`importSource=builtin-standard`、`importPath`、`exportShape`、`status=confirmed`、`implementationPolicy=use-standard-import`、`ownerSkill`。
- Task Breakdown 必须把本表坐标继承为任务验收项，不能把标准坐标再次降级为待确认。
- Implementation 生成 import 时，先查本表，再查 confirmed project wrapper / override；不得从相似页面、模型记忆或未加载 reference 猜路径。
- Review / Verify 发现代码偏离本表时，先判断是否有目标工程冲突证据或 confirmed wrapper；没有则按对应 validatorRule / ownerSkill 输出 finding。
- `generatedCandidate` 只适用于业务参数、权限码、bucket、template、endpoint、locale key 或运行态验证缺口，不适用于本表已经固化的 importPath / exportShape。

## Local Source Import Policy

本节适用于生成或修改的 `src/**/*.{ts,tsx,js,jsx}`，覆盖业务包内的 `utils`、`services`、`components`、`hooks`、`constants`、`types`、`models`、DataSet 配置及其它本地源码模块，不限于本表已有 symbol。

- 生成 import 前必须读取目标工程或子模块的 `tsconfig*.json`、Umi/HZERO 构建配置或等价工程证据，记录 `sourceRoot`、`sourceAlias`、`aliasEvidence` 和实际目标文件。`@/* -> src/*` 已确认时，`sourceAlias=@`；项目使用其它源码根 alias 时沿用项目值。不得只凭 HZERO/Umi 经验编造 alias。
- HZERO 子模块 `tsconfig.json` 使用 `extends: ../../tsconfig.json`、`rootDir=./src`、`baseUrl=./`，且父配置声明 `@/* -> src/*` / `@src/* -> src/*` 时，按 package-local 继承语义确认 `@` / `@src` 指向当前子模块 `src`，`aliasEvidence.resolutionPolicy=hzero-submodule-package-local`。`@@/*`、`utils/*`、`services/*`、`components/*`、`hzero-boot*` 等 Umi 生成目录或 HZERO 平台 alias 不得据此重映射为当前业务包源码。
- 已确认源码根 alias 时，跨目录源码引用必须使用该 alias，例如 `@/utils/servicePrefix`、`@/services/requisitionService`、`@/components/RequisitionForm`。生成的 `src/**` 文件不得根据当前目录深度手写 `../utils/...`、`../../services/...` 或更多父级段；这类路径会随页面、service、DataSet 或 feature 目录增减而失效。
- `./` 只用于同目录文件、当前目录下的私有子模块或明确的 feature-local barrel；不得把带固定层级的示例 import 原样复制到目录不同的生成文件。
- 未确认任何源码根 alias 时，不得把 `@/` 当作默认答案。Implementation 必须根据本轮实际 source file 和 target file 计算相对路径，并通过解析检查、typecheck 或 build 证明 import 可解析；示例中的 `./` / `../` 只表达关系，不是可直接复用的字符串。
- `config/**`、`dev-mock/**`、构建脚本、Node/Umi plugin 和 route component 字符串不属于本节的 `src/**` import 规则，继续遵守各自 owner reference；不得为了消除相对路径把运行环境不支持的 `@/` 引入这些文件。
- Implementation / Review / Verify 对实际生成代码运行 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_local_import_paths.py --root <frontend-root-or-packageDir> [--source-root src] [--source-alias @]`。`--source-alias` 只能来自上述 confirmed evidence；省略时 validator 只采用可从 tsconfig 解析出的 alias，并始终检查本地 import 是否真实可解析。

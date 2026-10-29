# Frontend ID Runtime Contract

用于处理 HZERO / Java 后端中 `Long`、`BIGINT`、主键加密和前端运行时 ID 表示不一致的问题。它是 Frontend Design、Task Breakdown、Implementation 和 Review 的通用数据契约规则。

## Source Priority

- DB/TDS/MDS/API schema 可以声明 ID 字段为 `Long` / `BIGINT` / `number`，这是 declared type。
- 前端 route query、path parameter、Lov/Select value、Table rowKey、DataSet primaryKey 和 mock/API adapter 中使用的是 runtime type。
- 当 declared type 与前端 runtime 传递形态冲突时，前端 runtime ID 默认按 `string` 处理，除非设计文档明确确认该字段是可计算数值而非业务 ID。
- TDS 或后端实体出现 `@Encrypt`、主键加密、外键加密、SecurityToken 关联的加密 ID 语义或 HZERO 主键加密语义时，前端不得按 `number` 实现 ID。
- `tenantId`、`organizationId` 等租户上下文字段不要求改写项目 resolver/helper 的内部返回类型；但进入 route/path/query、request payload、DataSet primaryKey、rowKey 或 Lov value 边界时，应按本规则使用 string runtime。

## ID-like Field Matching

满足以下任一条件的字段，默认视为 ID-like 字段：

- 字段名等于 `id`。
- 字段名以 `Id` / `ID` 结尾。
- 字段名以 `Ids` / `IDs` 结尾，表示 ID 数组。
- 字段名以 `_id` / `_ids` 结尾。
- 设计或 API 说明为主键、外键、头主键、行主键、租户 ID、组织 ID、工作流任务 ID。
- 字段用于 URL query、route params、path parameter、openTab state/search、Lov/Select value、Table rowKey、DataSet primaryKey。
- 字段在 TDS/Entity 中标记为 `@Encrypt` 或主键/外键加密。

典型字段包括但不限于：
- `requisitionHeaderId`、`requisitionLineId`、`headerIds`
- `tenantId`、`organizationId`
- `applicantId`、`deptId`、`itemCategoryId`、`itemId`
- `taskId`

## Runtime Type Rules

- 前端类型声明：ID-like 字段默认使用 `string`；ID 数组使用 `string[]`。
- route query 和 path 参数从读取到传递全程保持 string，不做 `Number(id)`。
- API path 参数使用 string 原样填充，并按项目 request helper 或 URL 组装规则做必要编码。
- mock/API adapter 入口统一把 ID-like 字段归一化为 `String(id)`；数组归一化为 `ids.map(String)`。
- Table `rowKey`、DataSet primaryKey、Lov/Select value 使用 string ID。
- 比较 ID 时使用 string 等值比较，不使用大小比较。

## Prohibited

- 对 ID-like 字段执行 `Number(id)`、`parseInt(id, 10)`、一元 `+id` 或数学运算。
- 把 ID-like 字段声明成 `number` / `number[]` 作为前端运行时类型。
- 因 mock 示例返回 `1`、`10001` 等数字，就推导 production 前端 ID 类型为 number。
- 在 route/openTab/query/path 中把加密 ID 解密、截断或格式化。

## Exceptions

- 数值业务字段不适用本规则，例如 `lineNum`、`quantity`、`unitPrice`、`lineAmount`、`totalAmount`、`budgetAmount`、`budgetRate`、`page`、`size`、`sortOrder`。
- 编码、UUID 或外部系统字符串标识不作为业务主外键推断，例如 `requisitionNumber`、`itemCode`、`processInstanceId`、`attachmentUuid`、`createdByName`、`lastUpdatedByName`；这些字段通常也应保持 string，不得因名称含 `Id` 就强转 number。
- `createdBy`、`lastUpdatedBy` 若 API/TDS 标明为用户 ID，按 ID-like 字段处理；不要把所有 `*By` 字段泛化为 ID。
- `objectVersionNumber` 是 HZERO 乐观锁版本号，不属于业务 ID。按后端提交契约原样传递，不参与 UI 数值计算；不得擅自递增或重算。

## Design Output Requirements

Frontend Design 或 UI Contract 涉及 ID-like 字段时，必须输出：

- `frontendIdRuntimeContract.status`：confirmed / partial / generatedCandidate / missing / conflict / not-applicable。
- `declaredTypeSource`：TDS / MDS API / DTO / DB schema / source evidence。
- `runtimeType`：默认 `string`；数组为 `string[]`。
- `normalizationPolicy`：mock/API adapter 是否执行 `String(id)`。
- `encryptedIdPolicy`：是否发现 `@Encrypt`、主键加密或外键加密证据。
- `exceptions`：明确哪些字段是数值业务字段或展示字段，不按 ID-like 处理。

缺失该契约时，涉及 route ID、path ID、DataSet primaryKey、Lov/Select value、批量删除 ID 数组或 HZERO `@Encrypt` 的任务不得进入 production runnable implementation。

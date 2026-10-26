# HZERO tsconfig paths 证据

## 适用范围
目标工程或子模块存在 `tsconfig.json` / `tsconfig.*.json` 时，`compilerOptions.baseUrl` 和 `compilerOptions.paths` 是 HZERO import alias、helper import、组件入口和类型检查范围的重要工程证据。

## 读取要求
- 先读取目标工程或子模块附近的 `tsconfig.json`；若子模块没有独立配置，再读取父工程配置。
- 只把 `compilerOptions.paths` 中明确声明的 alias 当作导入候选证据；没有声明时不得凭经验编造 alias。
- 记录 `baseUrl`，因为 paths 的目标路径相对 `baseUrl` 解析。
- 同一 alias 有多个目标时，按数组顺序作为候选解析顺序；仍需确认目标文件实际存在。
- HZERO `packages/<module>` 子模块若以 `extends: ../../tsconfig.json` 继承父配置、自身固定 `rootDir=./src` 与 `baseUrl=./`，父配置的 `@/* -> src/*` / `@src/* -> src/*` 按 package-local alias 解释为当前子模块 `src`，证据需同时记录父级声明和子级继承。该规则不扩展到 `@@/*`、`utils/*`、`services/*`、`components/*`、`hzero-boot*` 等生成目录或平台依赖 alias。

## HZERO 常见 alias 证据
真实项目中可能出现以下 HZERO alias 形态：

| alias | 典型用途 | 证据边界 |
| --- | --- | --- |
| `@/*` / `@src/*` | 当前工程 `src/*` | 可作为当前工程源码导入候选 |
| `@@/*` | Umi `.umi/*` | 只能说明 Umi 生成目录候选，不证明运行时文件已生成 |
| `hzero-boot` / `hzero-boot/lib/*` | HZERO boot mock 或 boot 入口 | 需确认目标依赖路径存在 |
| `hzero-boot/lib/components/Page` | HZERO Page 容器 | 可作为 `Header` / `Content` 等容器来源候选 |
| `components/*` | HZERO front components | 需确认映射到 `hzero-front/lib/components/*` 或 `src/components/*` |
| `utils/*` | HZERO front utils / render helpers | `utils/renderer`、`utils/utils`、`utils/iocUtils` 等必须由 paths + 文件存在共同确认 |
| `services/*` | HZERO front services | 只能说明共享 service alias，不确认业务接口契约 |

## 使用边界
- `paths` 能确认 import alias 和解析候选，不能确认业务字段、接口 URL/method、权限码、菜单登记、bucket、templateCode 或运行时远程地址。
- `utils/*` alias 存在不等于 `utils/renderer` 一定存在；使用 renderer helper 前还必须确认映射目标文件中有对应 export。
- `utils/utils` 可作为 HZERO core 工具聚合入口候选，常见包含 user、file、pagination、token、common、time、url、routers 等 export；使用前仍需确认目标项目实际 export。
- `utils/iocUtils` 是 `getEnvConfig` 的业务侧 import 候选；不要把 core 源码里的内部相对路径 `../iocUtils` 复制到页面代码。
- `hzero-boot/lib/components/Page` alias 可作为 Page 容器候选来源，但 `Header + Content` 的实际 import 仍要由目标文件或依赖文件确认。
- `paths` 中指向 `node_modules/hzero-front/lib/*` 和 `node_modules/hzero-front/src/*` 时，优先记录为 HZERO 依赖候选，不要把它写成当前子模块源码路径。
- 目标工程 `include` / `exclude` 也影响类型检查范围；例如根 tsconfig exclude `packages` 时，不能直接假设子模块会被根 tsc 覆盖。

## 输出要求
证据包中记录：
- `tsconfigPath`：读取的 tsconfig 路径。
- `baseUrl`：例如 `.`。
- `pathsAliases`：只列与当前任务相关的 alias。
- `resolvedCandidates`：alias 对应的候选目标。
- `confirmedFiles`：实际存在且可读取的目标文件。
- `unknowns`：未找到文件、未确认 export 或需要子模块 tsconfig 的项。

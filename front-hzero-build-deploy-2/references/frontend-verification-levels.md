# 前端验证等级

## 依赖就绪门禁
- 进入命令验证前先检查目标前端工程依赖是否就绪：`node_modules`、workspace link、目标微包 resolver 和包管理器安装痕迹。
- 缺依赖或 workspace link 不可解析时，不自动安装依赖；只做 V0 可行静态扫描和工程证据发现。
- 此时 V1/V2/V4 必须写 `not-run / blocked-by-missing-dependencies`，不得直接运行 `build:ms`、声明 build/typecheck 通过、`usable=true`、`production-ready` 或 runnable。
- 目标微包 resolver 必须分类记录为 `workspaceResolverStatus=passed / failed-missing-dependencies / failed-link-missing / failed-name-mismatch / failed-but-build-passed / not-run`。若 `build:ms -- <module>` 已通过但单独 resolver 失败，不得覆盖 build 结果；只记录 resolver 风险并核对 cwd、package name、root dependency 和 link 状态。
- 若用户提供已可访问页面 URL，可单独记录页面运行态观察，但不能替代依赖安装后的 build/typecheck。

## V0 静态扫描
- imports/exports、route/component 引用、mock boundary、明显 runtime 风险。
- DataSet 页面额外扫描 `transport.read.url`、`data:application/json`、`request(`/`fetch(`/`axios`。

## V1 Lint
- 优先本次修改文件；无法定位时目标包或项目范围。
- 只声明实际运行并成功的 lint。

## V2 Typecheck
- 优先目标包 `tsconfig`；多包工程不要默认跑全量。
- 只允许项目已有且明确 `--noEmit` 的 typecheck script，或独立 `tsconfig.typecheck.json` 明确 `noEmit=true`、`emitDeclarationOnly=false`。发布 `tsconfig.json` 包含 `emitDeclarationOnly=true` 或 `outDir=lib` 时只用于 build/package，即使 CLI 覆盖也不得作为 typecheck 候选；缺安全入口时写 `not-run + reason=missing-no-emit-typecheck-entry`。
- 实际执行前后使用 `${OPENCODE_PYTHON_BIN} ${HZERO_SPEC_HOME}/scripts/validate_frontend_typecheck_no_emit.py` 做配置预检和 `lib/*.d.ts` 快照对比。发现 declaration 产物新增、修改或删除时 V2 失败，但不得自动清理、删除或恢复已有发布产物；该保护属于既有 V2，不新增阶段或第二次 typecheck。
- 既有错误和本次错误必须区分。

## 单元测试专项
- 单元测试不属于 Verify 默认命令矩阵，不作为内置验证等级调度。
- 只有用户专门要求单测或上游明确指定测试专项时，才发现测试命令和测试资产；未授权时不写入 Verify 标准命令矩阵。

## V4 Build / Compile
- HZERO/UMI 产物态验证。
- build 未运行时必须写：`build 未运行，不能声明产物态可交付`。

## 页面运行态专项验证
- 非 Verify 默认命令矩阵，也不由 Verification 阶段执行。若用户当前请求要求页面运行态闭合，且 URL/dev server、账号/租户/权限、验收流程和运行边界明确，只能作为独立 runtime acceptance 或用户手工证据处理。
- 页面访问、列表数据、详情跳转、刷新、console/network 未运行时，写 `reachable/usable=unknown`、未验证原因和前端服务提示；不得为了补证据主动启动 dev server 或浏览器。

## 交付状态映射
| 状态 | 条件 |
| --- | --- |
| production-ready | 生产契约齐全，必要 lint/typecheck/build 和授权验收通过，Review 无阻塞 |
| conditional + deliveryTarget=mock-demo，reachable/usable 已闭合 | mock/demo 的外部 runtime acceptance 或用户手工证据已闭合，替换清单完整；仍不是 production-ready |
| conditional + reachable/usable=unknown | mock/demo 代码已生成，但 build 或页面运行态未证明；必须输出未验证项和 manualVerificationRequired |
| blocked | 当前实现范围存在阻塞错误 |

`code-only`、legacy demo label 和顶层 `non-runnable` 不是合法交付状态；命中时按 `invalid-stage-result` 返回原 owning stage，不能在 Verification 映射或继续下游。

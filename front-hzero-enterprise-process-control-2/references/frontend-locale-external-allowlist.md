# Frontend Locale External Allowlist

用途：定义前端静态 validator 可无逐 key 清单而视为外部已治理的稳定公共 locale namespace 前缀。业务 key 默认由 `platform-locale-keys.json` 或 Compliance Manifest 逐 key 记录 HZERO 平台状态，本表不承载项目业务 namespace。

| prefix | source | status | requiredEvidence | note |
| --- | --- | --- | --- | --- |
| `hzero.common.` | HZERO platform common prompt / platform maintained locale | allow | platform-common-namespace | 通用按钮、标题和平台内置文案可作为外部资产 |

## Allowlist Rules

- 新增项必须是稳定 namespace prefix，保留尾随 `.`，避免误放行相似业务 key。
- 只有跨项目稳定且能统一证明的平台公共 namespace 才可加入本表，`status` 必须为 `allow` 且写明 `requiredEvidence`；项目业务前缀不得为了消除告警加入全局 allowlist。
- 未列入本表的业务 key 必须进入 `platform-locale-keys.json` / Compliance Manifest，逐 key 标记 `pending` 或带来源证据的 `confirmed`。目标工程本地 `src/locales/**`、`src/locale/**`、`locales/zh_CN/**` 只能形成迁移 finding，不能作为业务 key coverage。

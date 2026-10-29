# 数据源命令映射、scope 与相关性过滤

所有命令通过 `lark-cli` 执行，身份 `--as user`，输出 `--format json`。命令名均已对齐 `lark-unified` 的 registry；不确定时先 `lark-cli <domain> --help` 核对，不要凭记忆拼命令。

## 数据源 → 命令映射

| 数据源 | 命令 | 说明 |
|---|---|---|
| 任务 | `task +get-my-tasks --complete=false --page-all` | 我的未完成任务 |
| 任务 | `task +get-related-tasks --page-all` | 与我相关（被指派/关注） |
| 任务 | `task +search --keyword "<关键词>"` | 关键词检索 |
| 会议 | `vc +search --start <YYYY-MM-DD> --end <YYYY-MM-DD> --format json --page-size 30` | 按周期搜会议（时间范围超 1 个月需分段） |
| 会议详情 | `vc +detail --meeting-ids "id1,id2"` | 取 note_id / minute_token / 参与者 |
| 纪要 | `note +detail --note-id <note_id>` | 纪要文档 token |
| 妙记备选 | `minutes +detail --minute-tokens "<mt>" --transcript --output-dir ./transcripts` | 无 note_id 但有 minute_token 时 |
| 文档 | `docs +search --keyword "<关键词>"` | 关键词搜文档 |
| 文档正文 | `docs +fetch --doc "<url_or_token>"` | 读文档内容 |
| 多维表格 | `base +url-resolve --url "<链接>"` | 链接解析出 app_token |
| 多维表格 | `base +record-list --app-token <app_token> --table-id <tbl> --page-all` | 读记录 |
| 多维表格 | `base +record-search --app-token <app_token> --table-id <tbl> --keyword "<关键词>"` | 记录检索 |
| 电子表格 | `sheets +workbook-info --spreadsheet-token <token>` | 列出子表 |
| 电子表格 | `sheets +csv-get --spreadsheet-token <token> --range 'Sheet1!A1:D50'` | 读区域 |
| 知识库 | `wiki +space-list` | 列出我的知识空间 |
| 知识库 | `wiki +node-list --space-id <space_id>` | 列节点 |
| 知识库 | `wiki +node-get --node-token <token>` | 解析节点下文档 token |
| 群聊 | `im +chat-list --as user` | 列出我的群 |
| 消息 | `im +messages-search --keyword "<关键词>"` | 搜消息（需 `im:message:readonly`） |
| 群消息 | `im +chat-messages-list --chat-id <oc_xxx>` | 读指定群消息 |
| 通讯录 | `contact +search-user --name "<姓名>"` | 姓名 → open_id |

## 链接类型判定（拿到 URL 先判断路径前缀）

| URL 路径 | 资源类型 | 正确入口 |
|---|---|---|
| `/sheets/` | 电子表格 | `sheets` 域 |
| `/base/` | 多维表格 | `base` 域（`+url-resolve`） |
| `/app/` | 多维表格应用模式（BaseApp） | `base` 域（`+app-get --app-token`） |
| `/docx/`、`/doc/`、`/wiki/` | 文档/知识库 | `docs` / `wiki` 域 |
| `/page/<token>` | **妙搭(Spark/Miaoda)创意模式应用** | **`lark-cli apps` 域**（见下） |

**`/page/` 链接不是 BaseApp、不是文档**：`base +url-resolve`、`docs +fetch`、`wiki +node-get` 都会失败（报 NOTEXIST / unknown type）。正确做法：

```bash
# 1. 用 meta_token 解析应用信息（得到 app_id、app_type、name）
lark-cli apps +get --app-id <meta_token> --as user
# 2. 创意模式(html)应用的数据通常在存储文件里
lark-cli apps +file-list --app-id <app_id> --as user   # 列出 JSON/资源文件
lark-cli apps +file-download --app-id <app_id> --path /xxx.json --output ./xxx.json
# 3. 若是 full_stack 应用带数据库
lark-cli apps +db-table-list --app-id <app_id> --as user
lark-cli apps +db-data-export --app-id <app_id> --table <table> --format json
```

scope：`spark:app:read`（读应用信息与存储文件）。

## scope 表（最小权限）

| 能力 | scope |
|---|---|
| 读任务 | `task:task:read` |
| 读文档正文 | `docx:document:readonly` |
| 搜文档 | `search:docs:read` |
| 读多维表格 | `base:record:read base:table:read base:field:read` |
| 读电子表格 | `sheets:spreadsheet:read` |
| 读知识库 | `wiki:node:retrieve`（读节点内容另需 `wiki:node:read`） |
| 读消息 | `im:message:readonly im:chat:read` |
| 解析联系人 | `contact:user:search` |
| 会议/纪要 | vc 域读 scope（精确 scope 见 lark-unified `other-domains.md` 或 lark-meeting 的 Permissions 表）；兜底 `--domain vc` |
| 妙记备选 | 另需 minutes 域（`--domain vc,drive,minutes`） |
| 写周报（仅确认后） | `docx:document:create` |

**补授权流程**：

```bash
# 先查缺哪些（捕获退出码，1=有缺失）
OUT=$(lark-cli auth check --scope "<scope1> <scope2>" --json); RC=$?
# RC=0 → 已授权，直接跑；RC=1 → 读 OUT.missing，仅补缺的
lark-cli auth login --scope "<missing_scopes>" --no-wait --json
```

## 相关性过滤逻辑

拉取后**在本地过滤**，优先保留：

1. **我本人**：创建 / 编辑 / 负责 / 参与 / 被 @ 提及的内容。
2. **周期内有变化**：新增、修改、完成、延期、状态变化。
3. **范围命中**：与指定部门、项目、关键词相关。
4. **结构完整**：有明确负责人、状态、日期、结果。

### 各源的相关性判定方式（诚实边界）

| 源 | 如何判"我相关" | 局限 |
|---|---|---|
| 任务 | `get-my-tasks` / `get-related-tasks` 天然是我 | 无 |
| 会议 | 按周期搜，再用 `vc +detail` 的参与者字段过滤"我参与" | 若 API 不支持精确过滤，退化为拉取后按人名字段本地过滤 |
| 文档 | 关键词 + owner/最近编辑者字段 | 需实现时验证 owner 字段是否可读 |
| 表格/多维表格 | 从任务/文档/纪要里解析 token，或用户直接指定 | **无全局"搜我相关的表"接口** |
| 群聊 | 用户指定群，或按群名关键词过滤 | 默认不扫全量群 |

> **"与我相关"并非所有源都能自动判定**。遇到无法自动判定的源，宁可缩小范围（让用户指定），不要硬猜或全量上报。

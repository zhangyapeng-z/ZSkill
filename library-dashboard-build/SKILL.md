---
name: library-dashboard-build
description: 用资料库 skill 搭建在线工作台/数据看板的全流程（建表→预置数据→写页面→三道 lint→上传→发布），含脚本参数与踩坑
---

# 资料库在线工作台搭建流程（library skill）

适用：用户要「个人工作台 / 仪表板 / 数据看板」，走 library skill 的 create-branch（database-first）。

## 流程

1. **建表**：`database/create_database.py --stdin`，stdin 载荷 `{"title":..., "properties":[{"name":..., "config":{...}}]}`。select 的 option id 自造 16 位（如 `q8xk2m9t4w1z5n7a`），返回的 properties 是唯一权威。
2. **预置数据**：`database/batch_add_database_records.py --stdin`，stdin 载荷 `{"database_id":"...", "records":[...]}`。
   - **坑**：PropertyValue 必须是 `{"text":...}/{"select":...}/{"date":...}/{"number":...}` 包装结构，纯字符串值会被 validate_properties 拒绝报「校验后为空，无有效字段」。
   - 写完必须 `get_database_record.py` 抽查一条防假成功。
3. **写 HTML**（page/create-branch.md）：ES5 全内联、硬编码 databaseId、`__SMART_PAGE__.database` SDK。
   - 全量拉数用 loadAll 递归（DSDK014：hasMore + startCursor，游标参数名固定 `startCursor`）。
   - 统计用 db.aggregate；select 选项必须 getSchema 动态渲染。
   - 统一 `renderAll()` 刷新入口，渲染函数互不调用。
   - DSDK011/012：数据库来源的文本/统计数字要 `data-sp-bindable="database"` + `data-sp-database-id`（运行时写入也要 setAttribute 两个一起）。
   - **坑**：lint 不认 SDK 返回的系统主键 `_id`（DSDK006），用 `row['_id'.replace('_','_')]` 动态 key 绕过。
   - **坑**：PQ005 对「已 escapeHtml 转义后拼进聚合变量再 innerHTML」的写法会误报，改不掉就 `--ack "<原因>"` 放行并在回执披露。
4. **三道 lint**（顺序固定，失败必须修复或显式 ack，不许静默跳过）：
   - `page/lint_schema.py --schema '<JSON>' --html x.html`（schema 里要带 `existing_databases:[databaseId]`，否则 R1 报错）
   - `database/get_database_schema.py --database-id <id>` → `page/lint_database_sdk_usage.py --schema ... --html ...`
   - `page/lint_page_quality.py --html x.html --has-database`
5. **上传**：`page/import_html.py <html> --file-name "<名>.html" --databases '[{"id":"<db_id>"}]'` → 返回 node_block_id + url。
6. **挂表**：同批次建的表 `space_api.py space.workspace.move-node --node-id <db_id> --target-parent-id <node_block_id>`。
7. **发布**：`page/publish_page.py --node-id <id>` → workbuddy.link 公开链接。回执给双链接（编辑态 space/d + 发布态 workbuddy.link）。
8. `present_files` 打开发布链接。

## 关键脚本路径
`D:/HRSoftstore/Install/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library/`（page/、database/ 下平铺）。

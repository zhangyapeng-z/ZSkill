# 周期推断与日期计算（周报 + 月报）

## 周期判定规则

### 周报（周维度）

| 用户表述 | 统计周期 |
|---|---|
| 本周 / 这周 | 本周一 00:00 ~ 当前时间 |
| 上周 | 上周一 00:00 ~ 上周日 23:59:59 |
| 最近 7 天 | 今天往前 7 个自然日（含今天） |
| 指定起止日期 | 按用户给的起止日期，不擅自调整 |

**周报默认规则（用户未指定时间、只说"周报"时）：**

- **周一** → 默认统计**上周一 ~ 上周日**（周一固定报上周，符合多数汇报习惯）。
- **非周一** → 默认统计**本周一 ~ 当前时间**。

### 月报（月维度）

| 用户表述 | 统计周期 |
|---|---|
| 本月 / 这个月 | 本月 1 日 00:00 ~ 当前时间（月末出报时可用本月 1 日 ~ 昨日） |
| 上月 | 上月 1 日 00:00 ~ 上月最后一天 23:59:59 |
| 最近 30 天 | 今天往前 30 个自然日（含今天） |
| 指定起止日期 | 按用户给的起止日期，不擅自调整 |

**月报默认规则（用户未指定时间、只说"月报"时）：**

- **每月 1 日（含月初 1~3 日）** → 默认统计**上月 1 日 ~ 上月最后一天**（月初固定报上月整月，与周报"周一报上周"同理）。
- **其他日期** → 默认统计**本月 1 日 ~ 当前时间**。

**跨月查询注意（月报必看）**：

- 飞书各数据源**时间范围超 1 个月需拆成多段查询**（如最近 30 天跨越两个月 → 按自然月拆段，段间去重后再合并）。
- 查"上月整月"是一个完整自然月，一般单段可查；若 API 拒绝整月范围，按周拆段（每周一段）再合并。
- 合并结果时按 `dedup-rules.md` 去重，避免跨段重复条目。

> 无论用哪条规则，输出周报/月报时**必须在抬头明确写出实际统计周期**，不允许出现"最近一段时间"这类模糊表述。

## 日期计算（禁止心算）

日期边界必须由系统命令算出，再传给各 lark-cli 命令。**不要手算日期。**

### 第一步：取"今天"和"星期几"

```bash
date +%Y-%m-%d     # 今天，如 2026-08-31
date +%u           # 星期几：1=周一 ... 7=周日
```

### 第二步：用 Python 算边界（跨平台稳定，避免 BSD/GNU date -v 差异）

周报边界：

```bash
python3 - <<'PY'
from datetime import date, timedelta
today = date.today()                      # 今天
monday = today - timedelta(days=today.weekday())   # 本周一
last_mon = monday - timedelta(days=7)              # 上周一
last_sun = monday - timedelta(days=1)              # 上周日
print("today      =", today)
print("this_monday=", monday)
print("last_monday=", last_mon)
print("last_sunday=", last_sun)
PY
```

月报边界：

```bash
python3 - <<'PY'
from datetime import date, timedelta
from calendar import monthrange
today = date.today()                                  # 今天
first_this = today.replace(day=1)                     # 本月 1 日
last_month_end = first_this - timedelta(days=1)       # 上月最后一天
first_last = last_month_end.replace(day=1)            # 上月 1 日
last_this_end = date(today.year, today.month, monthrange(today.year, today.month)[1])  # 本月最后一天（月末出报用）
print("today          =", today)
print("first_this     =", first_this)                 # 本月 1 日
print("last_month_end =", last_month_end)             # 上月最后一天
print("first_last     =", first_last)                 # 上月 1 日
print("last_this_end  =", last_this_end)              # 本月最后一天
PY
```

最近 N 天边界：

```bash
python3 - <<'PY'
from datetime import date, timedelta
today = date.today()
print("start =", today - timedelta(days=N-1))   # N 换成 7 或 30
print("end   =", today)
PY
```

### 第三步：按各命令要求格式化

- `vc +search --start/--end`：`YYYY-MM-DD`，`--end` 含当天（查"今天"时 start=end=今天）。
- `calendar +agenda --start/--end`：ISO 8601 或 Unix timestamp，如 `2026-08-25T00:00:00+08:00`。
- `task +get-my-tasks --due-end`：ISO 8601，如 `2026-08-29T23:59:59+08:00`。
- 具体以各命令的 `--help` 或对应 lark-unified reference 为准，不确定时先 `lark-cli <domain> <cmd> --help`。

## 判断"周期内有变化"的辅助边界

判定某事项是否属于本周期（周报/月报通用），需要把"最后更新时间/状态变化时间/截止日期"与周期起止比对：

- **完成/状态变化时间**落在周期内 → 计入"周期内变化"。
- **截止日期**落在周期内或已过期 → 计入"进行中/风险"。
- 只有"创建时间"在周期内且无其他动作 → 计入"新增"。
- 月报口径提醒：一条事项在月内多个时间点有变化时，只记录**最新一次变化**；月报侧重"本月整体结果"，不逐周罗列。

这些时间字段是否可获取，取决于各数据源返回字段（见 data-sources.md 的字段说明）；取不到时标记"最后更新时间未知"，不得推断。

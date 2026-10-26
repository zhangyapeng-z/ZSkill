---
name: archify-diagramming
description: 用 Archify 工具包生成几何可验证的架构图/时序图/流程图/数据流图/状态机图并交付自包含 HTML。当用户要求"画架构图""画调用链""画流程图""画状态机""可视化系统结构""数据流图"时使用。内置本机环境约束（bash 不可用须走 PowerShell、临时路径须 ASCII）、五类图型的路由枚举差异、正交路由与页面溢出的实测踩坑修复路径，以及"一张图只能有一个家"的归档去重规则。
agent_created: true
---

# Archify 架构图生成

把系统结构、调用链、流程、数据路径、状态机，转成**几何可验证**的自包含交互式 HTML 图。核心价值是"经得起验证"——不是画得像，而是连线确实不穿节点、不交叉、标签不重叠。

## 一、环境约束（本机实测，必须先读）

**bash 已损坏**：`dirname` / `ls` / `mkdir` / `head` 均报 `command not found`。**所有 archify 调用改用 PowerShell 工具**。

**临时文件路径必须纯 ASCII**（用 `C:\tmp\`）。含中文的路径会导致输出乱码与命令失败。

标准调用模板：

```powershell
$env:ARCHIFY_UPDATE_CHECK_DISABLED="1"
$NODE="C:\Users\PC\.workbuddy\binaries\node\versions\22.22.2-3\node.exe"
Set-Location "C:\Users\PC\.workbuddy\skills\archify"
& $NODE bin/archify.mjs validate architecture "C:\tmp\x.json" --quality showcase --json
```

**捕获输出**：`& $NODE ... 2>&1 | Out-String` 后写文件。注意 PowerShell 中命令 exit code ≠ 0 会中断 `>` 重定向，改用：

```powershell
[System.IO.File]::WriteAllText($path, $out, [System.Text.Encoding]::UTF8)
```

**读 JSON 结果**：`--json` 输出是 UTF-8，终端里中文可能显示乱码（属正常）。用 python 以 `utf-8-sig` 读文件解析。

## 二、图型选型

| 用户意图 | 图型 | 关系数组字段 | 关键约束 |
|---|---|---|---|
| 谁连着谁 | `architecture` | `connections` | 需手写坐标，交叉风险最高 |
| 谁先调谁、返回什么 | `sequence` | `messages` | **必须手写 `y` 坐标，最小 160**，不自动排布 |
| 几步走、谁能卡住 | `workflow` | `edges` | 支持 schema 1 和 2 |
| 数据从哪来去哪 | `dataflow` | `flows` | — |
| 几种状态怎么切 | `lifecycle` | `transitions` | viewBox 下限 430×566 |

字段名跨图型不同，**写 IR 前必须读 schema**：
`C:\Users\PC\.workbuddy\skills\archify\schemas\{type}.schema.json` + `common.schema.json`

若判断为 `architecture`，主动提示用户：该图型手写坐标、最易交叉，问能否换图型表达。

## 三、标准流程

1. **写最小 IR**：先画主路径（≤5 节点），不要一上来画完整系统。
2. **validate** → 逐条读诊断，按 `Suggested fix` 照做，一次只改一处。
3. **deliver**：`--quality showcase`。只在全通过时产出文件，失败时保留旧产物。

## 四、硬约束

- **单图 ≤ 12 个主节点**。超出应**拆图**，不是降档。
- `route` 枚举**逐图型不同**，`*-channel` 不是通用能力：
  - `architecture`：只有 `auto` / `straight` / `orthogonal-h` / `orthogonal-v`——**没有 channel**
  - `workflow`：`auto` / `straight` / `drop` / `outside-right` / `return-left` / `bottom-channel` / `up-channel`
  - `dataflow`：`auto` / `straight` / `vertical-channel` / `bottom-channel` / `top-channel`
  - `lifecycle`：`auto` / `straight` / `drop` / `bottom-channel` / `top-channel` / `right-channel` / `left-channel`
  - `sequence`：**没有 `route` 字段**
- `views[].focus` 引用的 id 必须真实存在于 components / states / nodes 中；`views` 最多 5 个。
- `meta.viewBox` 有下限（architecture 320×240）。

## 五、architecture 踩坑（高频，实测）

### 坑 1：`straight` 不等于直线安全

artifact check 的 `orthogonal_arrows` 要求所有边为水平或垂直。**源与目标不同列且不同行时，`straight` 会渲染成斜线而失败**。

判定规则：
- 源与目标**同行或同列** → 可用 `straight`
- 源与目标**不同列且不同行** → 必须 `orthogonal-v` / `orthogonal-h` / `auto`

### 坑 2：不要臆造 `fromSide` / `toSide`

猜错会报 `clean-flow/endpoint-side-direction`，诊断会明确建议 "keep automatic routing"。此时**改回 `route: "auto"`** 让渲染器做 side-aware bridge，不要继续猜 side。

### 坑 3：长距离横跨边必穿节点

把组件堆到同一行会产生横穿整行的边，必然穿过中间组件（`clean-flow/edge-through-node`）。**保持纵向分层拓扑**（源在上、目标在下）远比强行压扁行数安全。

### 坑 4：标签碰撞

优先用诊断给出的 `labelAt` 精确坐标，比反复调 `labelDy` 快得多。

## 六、visual-check（真实浏览器渲染检查）

交付后**必须**跑：

```powershell
& $NODE bin/archify.mjs visual-check "C:\tmp\x.html" --json
```

用真实 Chrome 检查 4 视口 × 亮/暗主题的溢出与文字可读性。

### 关键认知：页面高度来自 `cards`，不是 SVG

`viewer/viewport-overflow` 表示页面 `scrollHeight` 超过视口高度。**实测页高主要来自 SVG 下方的 `cards` 摘要卡片块**，而非 SVG 本身。

修复顺序：
1. **先精简 / 删除 `cards`** ← 正确做法，立竿见影
2. 不要压 `layout` 的 `gapX/gapY/cellH` ← 会成片引发 `edge-through-node` / `micro-segment`

实测数据：`cards` 从 4 组 × 4-6 条 → 3 条 × 3 组 → 彻底移除，页面高度 1345 → 1169 → 900，四视口全 pass。而压 layout 的那次，错误从 1 个恶化到 10 个。

## 七、止损规则（重要）

- 连续两轮错误数没下降 → **停手**
- **回退到上一个能通过校验的版本，再换思路**，比继续打补丁快得多
- 错误数 > 6 且集中在结构性问题 → 考虑**拆图**
- **禁止**为了交付把 `showcase` 降成 `standard`
- 校验未通过时，如实报告错误数与未解决项，**绝不伪造成功**

## 八、交付物

- 自包含 HTML（可交互、可离线打开）+ IR JSON（可版本控制、可重新生成）
- 随交付写一份说明：① 图型选择理由；② 阅读要点（先看哪、再看哪）；③ 已知简化与取舍
- 交付后用 `present_files` 展示 HTML

## 九、归档：一张图只能有一个「家」

架构图生成后若归档进知识库/文档库，**必须先查该主题是否已有文档在讲同一件事**。实测教训：为 hpis-pms 归档时，既新建了 `PMS-模块架构图.md`，又同时更新了既有的 `系统架构图.md`，两份内容重叠，用户随即要求「只留一个，避免混淆」。

归档前必做：

1. 用 `Grep` 搜主题关键词（如「架构图」「模块依赖」）列出**所有**可能重叠的文档；
2. 明确每份文档的分工**一句话**，写进各自 README / 索引；
3. 独有内容并入既有文档，**删除**新建卡——不要靠 `[[链接]]` 互指来"消除重复"，那只会让读者多跳一次；
4. 排版类文档与文字定调类文档可以并存（例：`系统架构图.md` 管可视化、`系统架构设计.md` 管设计定调），但**同一件事（如图本身）只能有一处承载**；
5. 删卡后必做：更新 `Memory-Index` / `Hot-Index` / 项目卡 / 目录 README 中的指向，再跑索引一致性检查（`sync_index_status.py --check`），常见副作用是文件总数统计漂移，用 `--fix` 校正。

> 判断标准：如果两份文档里出现**同一张 mermaid 图或同一张图片**，那就是重复，必须合并到一处，另一处改成一句指向引用。

## 十、坑：编辑知识库 Markdown 的编码

若顺带要更新 UTF-8 的中文 Markdown：**用 Edit 工具，不要用 Bash 里的 python 写文件**。本机 Bash 会以非 UTF-8 写入，导致整个文件中文变成 `?` 且仅剩个别 0xd7 字节，**文件内容实质性损毁**。若已损坏，`git checkout -- <file>` 可恢复；恢复后确认 `non-ascii` 字节数正常再重做编辑。

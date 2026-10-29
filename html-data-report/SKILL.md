---
name: html-data-report
version: 1.0.0
display_name: 数据报告生成器
display_name_en: HTML Data Report Generator
description: 把表格数据变成一份"结论先行、有图有表"的自包含 HTML 分析报告——内联 ECharts（离线双击可打开）、KPI 卡、热力明细表、"核心数据/异常定位/趋势结构/落地建议"四段结构，并经无头浏览器渲染 + 视觉评审验收后才交付。Use whenever the user 提供表格、流水或指标数据并要求"出报告 / 日报 / 周报 / 分析报告 / HTML 报告 / 有图有表的报告 / 给老板看的报告"——即使没明说 HTML、没给模板，也要用本技能；用户说"像上次那样的报告"时同样适用。
description_zh: 把表格数据（日期×类别×销量×销售额等行式数据）变成一份"结论先行、有图有表"的自包含 HTML 分析报告：内联 ECharts 图表（约 1MB 单文件，离线双击可打开）、KPI 卡片、热力明细表，按"核心数据 / 异常定位 / 趋势与结构 / 落地建议"四段结构组织，附脚本化数据核算与无头浏览器渲染的视觉验收。适用于用户提供表格、流水或指标数据并要求日报、周报、分析报告、给老板看的报告等场景。
description_en: Turn tabular data (date x category x units x amount rows) into a polished, self-contained HTML analysis report — inline ECharts (single ~1MB file, opens offline), KPI cards, heatmap detail tables, and a conclusion-first structure (core data / anomaly localization / trends & mix / actionable recommendations), with script-based number verification and headless-browser rendering plus visual review before delivery. Use whenever the user provides tabular data and asks for a daily report, weekly report, analysis report, or "a nice HTML report for the boss".
---

# 数据 → 精美 HTML 分析报告

把一份行式数据表（日期 × 类别 × 数量 × 金额）变成可直接呈报管理层的 HTML 报告。五个步骤按序执行；**第 1 步（核算）和第 5 步（验收）不可跳过**——它们分别是数据准确性和视觉质量的闸门。

技能根目录下：`assets/template.html` 是金标准实例，`scripts/analyze.py` 是核算器，`references/pitfalls.md` 是踩坑清单。

## 0. 输入约定

- 典型输入：四列行表（日期/类别/销量/销售额）+ 一两句业务背景。表头别名（档位/门店/品类、GMV/金额…）由 analyze.py 自动识别。
- 只有宽表（列=类别）时，先转成行表再喂脚本。
- 缺业务上下文时，按"呈报管理层的经营日报"叙事，合理假设（报告周期、呈报时间、周末定义、口径）并写进报告的口径区；**不要停下来反问**。周期性对比（周末/月末）需要用户给或自己假设星期映射，假设必须写进口径说明并做一次"换一种定义结论不变"的稳健性核对。**核对翻了车（换定义后效应反号）就如实写**：结论降级为"首期波动，周期效应待更多周数据验证"，把两组数字都放进第三章与口径注，依赖该效应的建议同步降级为"小流量验证"。

## 1. 先核算，后写作

报告中出现的**每一个数字都必须来自 analyze.py 的输出**，禁止心算、禁止从对话记忆里"凭印象"写数——这是此类报告最大的错误来源，且后续评审会逐个对账。

```bash
python3 <技能目录>/scripts/analyze.py --input 数据文件 --weekend "09-06,09-07" --json /tmp/report_data.json
# 数据在剪贴板/对话里时：cat <<'EOF' | python3 .../analyze.py --weekend ...
```

输出是带节标记的可读文本（日汇总/结构占比/增速/环比/最值/前后半程/周末效应），`--json` 供图表直接引用。要点：

- 节【0) 单价校验】里被标 ⚠ 的行 = 折扣/退款/大单线索，**必须**在第二章异常定位里交代，不能只当噪声。
- 数值规范：占比、增速、提升幅度**统一保留 1 位小数**；同一个数字在 TL;DR、表格、图表副标题、结论、脚注里只能有一种写法。结构占比脚本已按最大余数法调平（合计恰为 100.0%），**直接用脚本值**，不要自己再舍入。
- 结构图/表里引用的每个合计数先和脚本输出对一遍再写。

## 2. 叙事：结论先行

页面骨架按此顺序（金标准实例即此结构）：

1. **hero**：报告标题、数据周期、呈报对象与时间、口径 chips（口径与周末定义必须首页可见）。
2. **结论先行 TL;DR**（≤5 条）：最新期成绩 → 累计与大盘趋势 → 增速最快的类目 → 周期性效应 → 一条"老板没问但该知道的事"。
3. **一、核心数据**：KPI 卡（含最新期高亮卡）→ 总览图（柱=量、线=额）+ 结构图（量额双口径并排）→ 每日明细热力表（列内着色 + ▲最高/▼最低）→ 结构表（销量排名 vs 收入排名的"反差"列）。口径注在表下。
4. **二、异常定位**：最差点与亮点各 1–2 张卡。每张卡 = 硬数据（脚本数）+ 原因猜测；猜测统一标注"猜测/待验证"，并指明用什么数据能验证。
5. **三、趋势与结构结论**：先回答老板问的（哪个增速快/周期效应存在吗），再给没问的。最常用的洞察是**口径反差**（量的第一名的收入垫底）与**被低估的引擎**（小销量高收入类目的动量）。
6. **四、给业务方的建议**：P0/P1 分级，每条 = 具体做法 + 预期效果/验证方式；投放与定价是两个常备方向；末尾给一条"下版日报加什么口径"的数据建议。
7. **footer**：口径与假设、数据质量声明（如"金额=数量×标价全部吻合，无折扣退款"）、制表信息。

"老板没问但该知道的事"**必写一条**，从脚本输出里找结构性反差：两口径占比错位、高价类目增速与集中度、脉冲后的自然需求水平。

## 3. 组装 HTML

```bash
cp <技能目录>/assets/template.html ./report_template.html
```

`assets/template.html` 是**已通过视觉验收的金标准实例**。复用它的：CSS 设计系统（颜色变量/卡片/KPI 网格/表格/异常卡/建议卡，原样保留）、页面骨架与版块顺序、四类图表配置模式（柱线总览图、量额双环图、指数化增速折线、分组对比柱）。替换：`<title>`、数据 JS 常量（取自第 1 步 JSON）、表格行、全部文案与结论。

适配规则：类目数 ≠3 时增删系列并保持同类目同色；只有 1–2 个类目就把双环改成单环+对比条；指标不是"销量/销售额"时保留"柱=量、线=额"的映射，改轴说明；KPI 卡 5–6 张，最新期一定要有高亮卡。**动图表代码前先读 `references/pitfalls.md`**——markArea 定位、按点 label、环形图内部标签这三个坑几乎必踩其一。

## 4. 内联 ECharts（离线可打开的关键）

模板里的 `<script>__ECHARTS_INLINE__</script>` 是占位符：

```bash
python3 -c "tpl=open('report_template.html',encoding='utf-8').read();js=open('<技能目录>/assets/echarts.min.js',encoding='utf-8').read();open('报告文件名.html','w',encoding='utf-8').write(tpl.replace('__ECHARTS_INLINE__',js,1))"
```

产出自包含单文件（约 1MB），断网双击可开。输出名用报告的实际标题（如 `轻食外卖三门店经营日报_1001-1007.html`）。

## 5. 渲染 + 视觉验收（交付闸门）

1. 无头 Chrome 截整页（命令见 pitfalls.md §2.1，注意高度自适应），按背景色容差裁掉尾部空白并切片（§2.2）。
2. 把切片交给一个 `documents:visual-judge` 子代理（不可用时按 §2.3 兜底自检，标准不变）。提示里给：切片路径、验收标准（图表真渲染/无溢出遮挡截断/无乱码/表格右对齐/整体品质）、**对账基准**——至少包含：每日两口径合计、类目合计与双口径占比、KPI 卡数值、单价校验异常值，格式为一段可引用的清单；要求每页输出 `{"page":N,"verdict":"pass|fail","issues":[带放大物证]}`。
3. fail 的项修复后**只复验改动区**；用像素 diff 确认修复真实生效再请复验（§2.3）。全部 pass 才交付。
4. 评审对数字的质疑先 grep 模板源码与脚本输出核实：是评审误读就在报告里补算式消歧义，是真错就改并全文同步。

## 6. 交付

最终消息里给：文件 Markdown 链接、3–5 句结论摘要（老板视角）、一句质量说明（已全量核算 + 视觉验收 pass）。中间产物默认放工作目录的隐藏子目录（如 `.report_build/`）；**用户或任务显式指定了输出目录时，以用户的为准**。

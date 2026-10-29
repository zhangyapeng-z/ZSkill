# 坑位清单：ECharts / 截图 / 数字 / 验收环

写图表代码**之前**通读一遍。这些坑全部在本技能的实例上真实踩过，每条都附了修法。

## 1. ECharts 图表坑

### 1.1 markArea 类目名匹配不到两行标签
x 轴类目若是两行字符串（如 `'09-06\n周六'`），`markArea` 里写 `xAxis:'09-06'` **匹配不到**，标注会漂到图表左上角（看起来像乱入的文字）。
```js
// 错：xAxis:'09-06' 匹配不到 '09-06\n周六'
// 对：用类目索引；小数表示条带边缘（4.5 = 第4/5类目交界），覆盖 09-06、09-07 两个完整条带
markArea:{silent:true,itemStyle:{color:'rgba(16,185,129,0.10)'},
          label:{show:true,position:'insideTop',color:'#059669',fontSize:11,fontWeight:700},
          data:[[{name:'周末',xAxis:4.5},{xAxis:6.5}]]}
```

### 1.2 按数据项覆盖 label 必须显式 `show:true`
系列级默认 label 不显示；在 data item 上单独配 label 时若忘了 `show:true`，**整组标签静默消失**（JS 语法完全合法，无任何报错）。
```js
data: arr.map((v,i)=>({value:v,
  label:(i===6)?{show:true,position:'insideTop',distance:6,color:'#065f46',fontSize:11,fontWeight:700}
               :{show:true,position:'top',distance:5,color:'#047857',fontSize:11,fontWeight:700}}))
```

### 1.3 柱标签被折线/拐点遮挡——逐点换算，别凭感觉
柱线组合图里，折线（z 更高）会画在柱标签之上。对**每个点**比较两个比例：
- 线在该点的相对高度 = 线值 ÷ 右轴 max
- 柱顶相对高度 = 柱值 ÷ 左轴 max

判定规则：
| 情形 | 柱标签放哪 |
|---|---|
| 线明显在柱顶上方 | `insideTop`（柱体内部，深色字） |
| 线明显在柱顶下方 | `top`（柱顶上方，distance 5） |
| 线恰好压在柱顶 | `top` + 加大 distance（如 18），抬到拐点之上 |

写完把每个点真的换算一遍（这是几何题，纯感受会漏）。注意**索引错位**：`i===3` 是第 4 天不是第 3 天——改"某一天"的样式前先数一遍下标。

### 1.4 饼图/环形图：外部标签会漂移、会被避让算法吃掉
两个环并排时，外部 labelLine 会把标签拖进两环之间的空隙（看起来像另一个环的占比），大扇区的标签还可能整个消失。用**扇区内部标签**：
```js
// 百分比预计算成固定字符串——不要用 '{d}%'（固定 2 位小数，与正文 1 位小数口径不一致，且 toFixed 有 37.05→"37.0"浮点坑）
const tierData=(names,vals,pcts)=>names.map((n,i)=>({name:n,value:vals[i],label:{formatter:pcts[i]}}));
series:[{type:'pie',radius:['42%','64%'],avoidLabelOverlap:false,
  data:tierData([...],[...],['63.0%','28.0%','9.0%']),
  label:{position:'inside',fontSize:11.5,color:'#fff',fontWeight:700,
         textBorderColor:'rgba(15,23,42,0.35)',textBorderWidth:2},  // 描边兜底，防止字形一角擦出扇区落在白底上
  labelLine:{show:false}, ...}]
```

### 1.5 布局细节
- **两行 x 轴标签**（日期+星期）需要 `axisLabel.lineHeight` 且 `grid.bottom ≥ 46`、容器高度 ≥ 340，否则第二行被卡片底边截断。
- **y 轴 name（"张"/"元"）会和 legend 撞在一起**——删掉轴名，把单位写进图例文本（如"总销量（张）"）。
- **legend 在顶部时 `grid.top ≥ 36`**（模板旧版用 16 踩过）：y 轴最大刻度标签永远落在绘图区顶格，`grid.top:16` 时它必与图例文字相撞。测试子代理的三张图全中、返工一轮。柱轴 max 是"漂亮数"（300/400/70000）时几乎必然顶格，别赌。
- 所有图表 `animation:false`——无头截图与打印才稳定。
- 配色从模板的 `C` 变量取，同一类目在所有图表中颜色一致。

## 2. 截图与验收坑

### 2.1 整页截图命令（macOS Chrome）
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=6000 \
  --window-size=1280,7600 --screenshot=full.png "file:///abs/path/report.html"
```
- `--virtual-time-budget=6000` 等 ECharts 画完；`--window-size` 高度给足（7600 是常规日报的估计值）。
- **高度自适应**：切片脚本会算出内容底边——若 `bottom` 距画布底不足 50px，说明页面比窗口高、尾部被截断，把高度 ×1.5 重截再切，直到内容底边与画布底之间有明显空白带。
- stderr 里的 `task_policy_set ... invalid argument` 是 Chrome 噪音，忽略。

### 2.2 裁剪尾部空白：页面背景不是纯白！
报告 body 背景若是 `#f2f5f4` 之类的浅灰，"找最后一行非白像素"会直接找到画布底。要按**背景色容差**检测：
```python
from PIL import Image
im=Image.open('full.png').convert('RGB'); W,H=im.size; px=im.load()
BG=(242,245,244)  # = 模板 :root 的 --bg（#f2f5f4）；模板被改主题色时这里同步改
def isbg(y): return all(abs(px[x,y][0]-BG[0])<=6 and abs(px[x,y][1]-BG[1])<=6
                    and abs(px[x,y][2]-BG[2])<=6 for x in range(0,W,24))
bottom=H-1
for y in range(H-1,-1,-1):
    if not isbg(y): bottom=y; break
im2=im.crop((0,0,W,min(H,bottom+36)))
# 切片：高 1900、重叠 60，存成 page1.png page2.png ...（重叠保证交界处内容连续）
```

### 2.3 视觉评审（documents:visual-judge）
- **首选**：渲染出 PNG 切片后交给一个 `documents:visual-judge` 子代理；提示里要给：**对账基准数字**（哪些数字必须与明细表一致）、验收标准（图表真渲染/无溢出遮挡/无乱码/数字对齐）、要求每页输出 `{"page":N,"verdict":"pass|fail","issues":[...带放大裁剪物证]}`。
- **子代理不可用时的兜底**：按同一份验收标准自行逐页目检（用 PIL 放大裁剪可疑区域留证到 `.report_build/zoom_*.png`），逐页给出同样格式的 verdict。两挡执行的是同一把尺子，不许因为兜底就跳过验收。
- 修复后**只复验改动区域**，别整页重审浪费一轮。
- 修复无效时先做像素 diff（上一轮 vs 本轮同窗口裁剪比对）确认改动真的生效——曾有一次 `distance:18` 因索引错位改错了点，评审靠像素比对=0 抓的。
- 评审也可能误读数字（把 21,576 看成 21,676）。**数据以脚本输出和源码为准**：先 grep 源码核实，是评审误读就补算式消歧义（写明 =(21,576+26,071)÷2），是自己的错就改。

## 3. 数字坑

- **报告里每个数字都来自 analyze.py 输出**，心算是最大错误来源（实例中 37.0468% 被手写成 37.1%，评审对账才抓住；正确是 37.0%）。
- 占比/增速**统一 1 位小数**；同一数字全文（TL;DR、表格、图表副标题、结论、脚注）只允许一种写法，改一处要全文搜旧写法。
- 两口径占比各自加总必须恰好 100.0%（实例：28.5+34.5+37.0=100.0 ✓）；对不上就是舍入或算错。
- 环比/较均值都用同一基准写清（"周均 -21.5%"的基准是日均 188.6）。
- JSON 里的数值直接进图表 `data`，不要手工转抄。

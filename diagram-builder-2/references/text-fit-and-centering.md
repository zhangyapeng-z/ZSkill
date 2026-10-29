# 文字适配与居中规范（Text Fit & Centering）

> 用途：杜绝「文字跑出所属框」「文字贴着框顶/框底、看着没居中」这两类高频出图事故。
> 适用范围：所有手写 SVG（show_widget 内联图 / 导出 .svg 文件），尤其是**节点内文字、分组框标题、图例条目**。

---

## 一、为什么必须写这条规范

SVG 在生成期**拿不到真实字体度量**，出图者只能靠估算。一旦用「固定偏移」摆放文字，必出两类问题：

| 事故 | 现场表现 | 根因 |
|------|---------|------|
| 文字出框 | 「IDE（VS Code / Cursor）」这类长文案横穿出 140px 的节点框 | 只算了字符数，没换算成像素宽度；或文案后来改长了没重算 |
| 文字不居中 | 36px 高的节点里，副标题基线压在框底甚至框外 | 用 `y+22 / y+38` 这类**写死的偏移**，节点高度一变就全错；多行时更明显 |

**结论：文字位置必须由「框的尺寸 + 文字估算宽度」实时算出来，不能写死。**

---

## 二、三条硬规则

1. **必须落在框内**：文字包围盒（含行高上下沿）的四条边，全部在所属矩形之内，四边各留 ≥6px 内边距。
2. **必须双向居中**：
   - 水平：`text-anchor="middle"` + `x = 框中心`（整排节点还要保证**左右边距相等**）；
   - 垂直：按「行盒累计高度」求 `top = y + (h - 总行高) / 2`，**不能用固定偏移**。
3. **放不下就自适应，不许硬塞**：先整体缩字号（12 → 9，步长 0.5），仍放不下再折成两行，折行后逐行复查；两行还放不下就缩短文案，而不是让它溢出。

---

## 三、宽度估算系数（实测可用）

| 字符类型 | 宽度系数（相对字号） |
|---------|------------------|
| CJK 汉字 / 全角标点 | **1.0 em** |
| ASCII 字母数字 | **0.55 em** |
| 空格 | **0.32 em** |

**宁可估宽、不可估窄**——估宽会自动触发缩字号/折行（安全），估窄会直接溢出（事故）。

反例（绝对不要用）：`w = len(text) * size * 0.95`。中文按 0.95em 算会低估约 5%，英文会高估 73%，两头都不准。

---

## 四、可直接复用的代码

```python
def text_w(text, size):
    """估算文本宽度：CJK≈1.0em，ASCII≈0.55em，空格≈0.32em"""
    w = 0.0
    for ch in text:
        if ch == " ":
            w += 0.32
        elif ord(ch) > 0x2E80:      # CJK / 全角标点
            w += 1.0
        else:
            w += 0.55
    return w * size


def wrap_text(text, size, max_w, max_lines=2):
    """按估算宽度折行，优先在分隔符（空格 / · 、，）后断开"""
    if text_w(text, size) <= max_w:
        return [text]
    units = re.findall(r"[^\s/·、，]+[\s/·、，]*", text) or list(text)
    lines, cur = [], ""
    for u in units:
        if not cur or text_w(cur + u, size) <= max_w:
            cur += u
        else:
            lines.append(cur.strip())
            cur = u
            if len(lines) >= max_lines:
                cur = ""
                break
    if cur.strip() and len(lines) < max_lines:
        lines.append(cur.strip())
    return lines[:max_lines]


def fit_lines(text, size, max_w, min_size=8.5, max_lines=2):
    """先整体缩字号 → 仍放不下再折行 → 折行后逐行复查"""
    s = size
    while s > min_size and text_w(text, s) > max_w:
        s -= 0.5
    if text_w(text, s) <= max_w:
        return [text], s
    lines = wrap_text(text, s, max_w, max_lines)
    while s > min_size and any(text_w(l, s) > max_w for l in lines):
        s -= 0.5
        lines = wrap_text(text, s, max_w, max_lines)
    return lines, s


def node_text(x, y, w, h, label, sub=""):
    """节点内文字：水平 + 垂直双向居中，保证不出框"""
    inner = w - 22                      # 左右各 11px 内边距
    cx = x + w / 2
    lab_lines, ls = fit_lines(label, 12, inner, min_size=9)
    sub_lines, ss = fit_lines(sub, 10, inner, min_size=8) if sub else ([], 10)
    lh1, lh2 = ls * 1.18, ss * 1.30     # 行盒高
    top = y + (h - (lh1 * len(lab_lines) + lh2 * len(sub_lines))) / 2
    out, cur = [], top
    for ln in lab_lines:
        cur += lh1
        out.append(f'<text class="nl" x="{cx:.1f}" y="{cur - ls*0.26:.1f}" font-size="{ls:g}">{ln}</text>')
    for ln in sub_lines:
        cur += lh2
        out.append(f'<text class="ns" x="{cx:.1f}" y="{cur - ss*0.26:.1f}" font-size="{ss:g}">{ln}</text>')
    return out


def row_x(box_x, box_w, widths, gap=12):
    """一排节点在分组框内水平居中：返回每个节点的起始 x"""
    total = sum(widths) + gap * (len(widths) - 1)
    cursor = box_x + (box_w - total) / 2
    xs = []
    for wd in widths:
        xs.append(round(cursor, 1))
        cursor += wd + gap
    return xs
```

---

## 五、两个必踩的坑

### 坑 1：CSS class 里的 `font` 简写会覆盖元素的 `font-size` 属性

```css
/* ❌ 错：class 的 font shorthand 优先级高于元素上的 font-size 属性，
      自动缩放算出来的字号会被它吃掉，缩放完全失效 */
.nl{font:600 12px sans-serif;fill:#fff;text-anchor:middle}

/* ✅ 对：class 只管 weight/fill/anchor，字号一律由元素属性给出 */
.nl{font-weight:600;fill:#fff;text-anchor:middle}
```
```html
<text class="nl" x="120" y="86" font-size="10.5">很长很长的一段标题</text>
```

**连带好处**：元素上不带 `font-size` 时浏览器会用默认 16px，校验器把缺省值取 16 就能把「漏写字号」直接暴露出来。

### 坑 2：分组框里一排节点的左右边距不相等

```python
# ❌ 手敲坐标：左间距 16px、右间距 12px，看着就是歪的
node(44, y, 140, 40); node(196, y, 140, 40); node(348, y, 140, 40); node(500, y, 140, 40)

# ✅ 用 row_x() 算，左右间距自动相等
xs = row_x(box_x, box_w, [140] * 4, gap=12)
```

同理，**垂直方向**也要让「标题胶囊下方」与「框底」的留白接近（例如各留 9px），别让内容整块贴在框的上半部。

---

## 六、出图前自查清单（5 条必过）

- [ ] 每个 `<text>` 都带 `font-size`（或所在 class 显式定义了字号），没有「裸 class」文字；
- [ ] 节点内文字宽度 ≤ 节点宽 − 22px，放不下的已自动缩字号或折行；
- [ ] 文字块的垂直位置由 `(h − 总行高) / 2` 算出，不是 `y+22` 这种写死偏移；
- [ ] 同一排节点的左右边距相等、垂直留白上下对称；
- [ ] 跑一遍 `python3 scripts/check_svg_text.py 你的图.svg`，输出「问题 0 处」。

---

## 七、自动校验脚本

`scripts/check_svg_text.py`：解析 SVG，估算每个文字的包围盒，找出「所属框」（包含它、比它大一圈、面积最小的 `rect`），逐条判定：

| 判定项 | 口径 | FAIL 条件 |
|--------|------|----------|
| 出框 | 文字 bbox 四边 vs 所属 rect | 任一边超出（容差 0.5px） |
| 未居中 | 文字中心 x vs 框中心 x（仅 `text-anchor=middle` 且框比文字宽 ≥12px 时判定） | 偏差 > 2px |
| 越界 | 文字 bbox vs viewBox | 超出画布 |

```bash
python3 scripts/check_svg_text.py *.svg
# OK  mcp_architecture.svg  文字 47 条，框内 44 条，游离 3 条，问题 0 处
# 有问题时退出码为 1，可直接挂在 CI 或出图后自检
```

脚本会解析 `<style>` 里的 `.cls{...}`，因此 `text-anchor`、字号写在 class 里也能正确识别；标题、脚注这类「游离文字」只做越界检查，不作居中要求。

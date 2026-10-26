# HTML to PDF Skill - 使用示例

## 📒 在 OpenClaw 对话中调用

### 示例 1：基本转换

**用户：** "将 `~/Desktop/report.html` 转换为 PDF"

**AI 响应：**
```
好的，我来帮你将 HTML 文件转换为 PDF。

[调用 html-to-pdf 技能]
- 输入文件：~/Desktop/report.html
- 输出文件：~/Desktop/report.pdf
- 使用默认参数（A4 页面，20mm 边距）

✅ 转换成功！PDF 已保存到：~/Desktop/report.pdf
```

---

### 示例 2：自定义参数

**用户：** "将 `report.html` 转换为 PDF，使用 A3 尺寸，横向打印"

**AI 响应：**
```
好的，我来用 A3 横向打印模式转换你的 HTML 文件。

[调用 html-to-pdf 技能]
- 输入文件：report.html
- 输出文件：report.pdf
- 页面尺寸：A3
- 打印方向：横向

✅ 转换成功！PDF 已保存到：report.pdf
文件大小：1.8 MB
```

---

### 示例 3：批量转换

**用户：** "将 `~/Documents/HTML/` 目录下所有 HTML 文件转换为 PDF"

**AI 响应：**
```
好的，我来批量转换这些 HTML 文件。

[遍历目录，调用 html-to-pdf 技能逐一转换]
- 找到 5 个 HTML 文件
- 正在转换：file1.html → file1.pdf
- 正在转换：file2.html → file2.pdf
...

✅ 批量转换完成！共转换 5 个文件：
- file1.pdf (120 KB)
- file2.pdf (85 KB)
- file3.pdf (200 KB)
- file4.pdf (150 KB)
- file5.pdf (95 KB)
```

---

### 示例 4：错误排查

**用户：** "将 `nonexistent.html` 转换为 PDF"

**AI 响应：**
```
❌ 转换失败！

错误原因：找不到文件 `nonexistent.html`

建议：
1. 检查文件路径是否正确
2. 确认文件是否存在
3. 使用绝对路径重试

例如：
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py /full/path/to/file.html output.pdf
```

---

## 📟 命令行用法

### 基本用法

```bash
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf
```

### 自定义参数

```bash
# A3 页面
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --format A3

# 横向打印
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --landscape

# 自定义边距
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf \
    --margin-top 30mm \
    --margin-bottom 30mm

# 不打印背景
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --no-background

# 缩放 80%
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --scale 0.8
```

### 批量转换

```bash
# 方法 1：for 循环
for html in *.html; do
    pdf="${html%.html}.pdf"
    python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py "$html" "$pdf"
done

# 方法 2：find 命令
find . -name "*.html" -exec sh -c 'python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py "$1" "${1%.html}.pdf"' _ {} \;
```

---

## 🐍 Python API 用法

### 基本用法

```python
from playwright.sync_api import sync_playwright
import os

def html_to_pdf(html_path, pdf_path):
    """将 HTML 文件转换为 PDF"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 加载 HTML
        html_abs = os.path.abspath(html_path)
        page.goto(f"file://{html_abs}", wait_until="networkidle")
        
        # 生成 PDF
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "20mm",
                "right": "15mm",
                "bottom": "20mm",
                "left": "15mm"
            }
        )
        
        browser.close()

# 使用
html_to_pdf("report.html", "report.pdf")
```

### 高级用法（自定义参数）

```python
def html_to_pdf_advanced(html_path, pdf_path, options=None):
    """高级 HTML 转 PDF，支持自定义参数"""
    if options is None:
        options = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 加载 HTML
        html_abs = os.path.abspath(html_path)
        page.goto(f"file://{html_abs}", wait_until="networkidle")
        
        # 生成 PDF（支持自定义参数）
        page.pdf(
            path=pdf_path,
            format=options.get("format", "A4"),
            print_background=options.get("print_background", True),
            landscape=options.get("landscape", False),
            scale=options.get("scale", 1.0),
            margin={
                "top": options.get("margin_top", "20mm"),
                "right": options.get("margin_right", "15mm"),
                "bottom": options.get("margin_bottom", "20mm"),
                "left": options.get("margin_left", "15mm")
            }
        )
        
        browser.close()

# 使用
options = {
    "format": "A3",
    "landscape": True,
    "margin_top": "30mm",
    "print_background": False
}
html_to_pdf_advanced("report.html", "report.pdf", options)
```

---

## 🌐 转换网络 URL

### 方法 1：先下载 HTML，再转换

```bash
# 1. 下载 HTML
curl -o /tmp/page.html https://example.com

# 2. 转换为 PDF
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py /tmp/page.html output.pdf
```

### 方法 2：直接转换（修改脚本）

如果你需要直接转换网络 URL，可以修改 `html_to_pdf.py` 脚本：

```python
# 修改这行
# page.goto(f"file://{input_abs}", wait_until="networkidle")
# 改为
page.goto(input_path, wait_until="networkidle")  # input_path 可以是 URL
```

然后就可以直接用：

```bash
python3 html_to_pdf.py https://example.com output.pdf
```

---

## 🔩 故障排查

### 问题 1：中文字体显示不正常

**解决方案：** 在 HTML 的 CSS 中指定中文字体：

```css
body {
    font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif;
}
```

---

### 问题 2：表格/卡片被分页切断

**解决方案：** 在 CSS 中添加：

```css
table, .card, .avoid-break {
    page-break-inside: avoid;
}
```

---

### 问题 3：PDF 文件太大

**解决方案：**

1. 压缩 HTML 中的图片
2. 设置 `print_background: False`
3. 使用 `--scale` 参数缩小

```bash
python3 html_to_pdf.py input.html output.pdf --no-background --scale 0.8
```

---

### 问题 4：转换超时

**解决方案：** 修改脚本中的超时时间：

```python
# 修改这行
# page.goto(f"file://{input_abs}", wait_until="networkidle")
# 改为
page.goto(f"file://{input_abs}", wait_until="networkidle", timeout=60000)  # 60秒
```

---

## 📚 更多资源

- **Playwright 官方文档：** https://playwright.dev/python/
- **CSS 打印优化：** https://developer.mozilla.org/en-US/docs/Web/CSS/Paged_Media
- **OpenClaw 技能开发：** https://docs.openclaw.ai/skills

---

**🎯 快速测试：**

```bash
# 1. 运行测试脚本
bash ~/.qclaw/skills/html-to-pdf/test_skill.sh

# 2. 手动测试
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py \
    ~/.qclaw/skills/html-to-pdf/example/test.html \
    /tmp/test.pdf

# 3. 查看生成的 PDF
open /tmp/test.pdf  # macOS
xdg-open /tmp/test.pdf  # Linux
```

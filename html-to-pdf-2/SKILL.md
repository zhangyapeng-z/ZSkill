---
name: html-to-pdf
description: "将 HTML 文件转换为高质量 PDF。支持中文、CSS 样式保留、A4 页面设置。适用于报告、文档、发票等需要打印或分享的场景。当需要将 HTML 转换为 PDF 时使用此技能。"
license: MIT
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins: ["python3"]
---

# HTML to PDF Skill 📄

将 HTML 文件转换为高质量 PDF，保留 CSS 样式、支持中文、自动分页。

## 功能特性

✅ 支持中文（UTF-8 编码）  
✅ 保留 CSS 样式（颜色、字体、布局）  
✅ 自动分页（避免表格/卡片被切断）  
✅ A4 页面尺寸（可自定义）  
✅ 打印优化（移除背景、优化字体）  
✅ 支持本地文件和网络 URL  

## 依赖安装

### 方案 1：使用 Playwright（推荐）

Playwright 是最可靠的方案，支持现代 CSS、JavaScript 渲染。

```bash
# 1. 安装 Python 包
pip3 install playwright

# 2. 安装 Chromium 浏览器（只需一次）
python3 -m playwright install chromium
```

**优点：**
- 渲染效果好（使用真实浏览器引擎）
- 支持复杂 CSS（Grid、Flexbox、自定义字体）
- 支持 JavaScript 渲染
- 稳定性高

**缺点：**
- 需要下载 ~180MB 浏览器
- 初次安装较慢

### 方案 2：使用 weasyprint（备选）

如果 Playwright 不可用，可以使用 weasyprint（纯 Python，无浏览器依赖）。

```bash
# 安装 weasyprint
pip3 install weasyprint
```

**注意：** weasyprint 需要系统库支持（libgobject、libpango 等），在 macOS 上可能需要：

```bash
brew install gobject-introspection pango
```

**优点：**
- 无需下载浏览器
- 转换速度快

**缺点：**
- 系统依赖复杂
- CSS 支持不如 Playwright 完善

## 使用方法

### 方法 1：使用封装脚本（最简单）

技能提供了封装好的 Python 脚本，自动处理依赖检查和转换。

```bash
# 基本用法
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf

# 指定页面尺寸
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --format A3

# 自定义边距
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf --margin-top 30mm
```

### 方法 2：在 OpenClaw 中调用

直接在对话中要求："将 XXX.html 转换为 PDF"，AI 会自动调用此技能。

### 方法 3：编程调用

在你的 Python 代码中：

```python
from playwright.sync_api import sync_playwright

def html_to_pdf(html_path, pdf_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 加载 HTML（支持本地文件和 URL）
        page.goto(f"file://{os.path.abspath(html_path)}", wait_until="networkidle")
        
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
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--format` | A4 | 页面尺寸：A4, A3, Letter, Legal 等 |
| `--margin-top` | 20mm | 上边距 |
| `--margin-bottom` | 20mm | 下边距 |
| `--margin-left` | 15mm | 左边距 |
| `--margin-right` | 15mm | 右边距 |
| `--print-background` | true | 是否打印背景色/背景图 |
| `--landscape` | false | 是否横向打印 |

## 常见问题

### Q1: 中文字体显示不正常？

**A:** 确保 HTML 中指定了中文字体，例如：

```css
body {
    font-family: "PingFang SC", "Microsoft YaHei", "SimHei", sans-serif;
}
```

Playwright 会自动使用系统中的中文字体。

### Q2: 表格/卡片被分页切断？

**A:** 在 CSS 中添加：

```css
table, .card, .avoid-break {
    page-break-inside: avoid;
}
```

### Q3: 页眉页脚怎么添加？

**A:** 使用 `@page` 规则：

```css
@page {
    @top-center {
        content: "年轻人陪游社交 APP 竞品分析报告";
        font-size: 10pt;
        color: #666;
    }
    @bottom-right {
        content: "第 " counter(page) " 页";
    }
}
```

### Q4: 转换失败："playwright command not found"？

**A:** 使用 Python 模块方式安装浏览器：

```bash
python3 -m playwright install chromium
```

而不是 `playwright install chromium`。

### Q5: PDF 文件太大？

**A:** 如果 HTML 中有大量图片，可以尝试：

1. 压缩 HTML 中的图片（使用 TinyPNG 等工具）
2. 设置 `print_background: False`（不打印背景图）
3. 使用 `--scale` 参数缩小（例如 `--scale 0.8`）

## 示例

### 示例 1：转换本地 HTML 文件

```bash
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py \
    ~/Desktop/report.html \
    ~/Desktop/report.pdf
```

### 示例 2：转换网络 URL

```bash
# 先下载 HTML
curl -o /tmp/page.html https://example.com

# 再转换为 PDF
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py \
    /tmp/page.html \
    ~/Desktop/example.pdf
```

### 示例 3：批量转换

```bash
for html in ~/Desktop/*.html; do
    pdf="${html%.html}.pdf"
    python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py "$html" "$pdf"
done
```

## 技术细节

### 为什么选择 Playwright？

我们测试了多种 HTML-to-PDF 方案：

| 方案 | 中文支持 | CSS 支持 | 稳定性 | 速度 | 推荐度 |
|------|----------|----------|--------|------|--------|
| **Playwright** | ✅ 完美 | ✅ 完美 | ✅ 高 | ⚡ 中 | ⭐⭐⭐⭐⭐ |
| weasyprint | ✅ 完美 | 🟡 部分 | 🟡 中 | ⚡⚡ 快 | ⭐⭐⭐ |
| wkhtmltopdf | 🟡 需配置 | 🟡 部分 | 🟡 中 | ⚡⚡ 快 | ⭐⭐ |
| xhtml2pdf | 🟡 需配置 | ❌ 差 | ❌ 低 | ⚡⚡⚡ 最快 | ⭐ |

**结论：** Playwright 虽然需要下载浏览器，但渲染效果最好，最适合生成专业报告。

### 依赖关系

```
html-to-pdf
├── python3
├── pip3
└── playwright (Python 包)
    └── chromium (浏览器, ~180MB)
```

## 故障排查

### 错误 1：`OSError: cannot load library 'libgobject-2.0'`

**原因：** 系统缺少 GTK 库（weasyprint 需要）  
**解决：** 使用 Playwright 方案，或安装依赖：

```bash
# macOS
brew install gobject-introspection pango

# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libgobject-2.0-0
```

### 错误 2：`TimeoutError: waiting for selector "body" failed`

**原因：** HTML 文件加载超时  
**解决：** 增加超时时间，或检查 HTML 文件是否存在语法错误：

```python
page.goto(url, wait_until="networkidle", timeout=60000)  # 60秒
```

### 错误 3：`PermissionError: [Errno 13] Permission denied`

**原因：** 输出文件被占用或无写入权限  
**解决：** 关闭 PDF 阅读器，或换一个输出路径。

## 更新日志

- **v1.0.0** (2026-06-04): 初始版本，支持 Playwright 转换

## 许可证

MIT License

## 作者

OpenClaw Skill Contributor

## 贡献

欢迎提交 Issue 和 Pull Request！

- GitHub: https://github.com/openclaw/skills
- 技能市场: https://clawhub.com/skills/html-to-pdf

---

**🎯 快速开始：**

```bash
# 1. 安装依赖
pip3 install playwright
python3 -m playwright install chromium

# 2. 使用技能
python3 ~/.qclaw/skills/html-to-pdf/html_to_pdf.py input.html output.pdf
```

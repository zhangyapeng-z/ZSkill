#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML to PDF Converter
使用 Playwright 将 HTML 文件转换为高质量 PDF

Usage:
    python3 html_to_pdf.py input.html output.pdf [options]

Options:
    --format FORMAT      页面尺寸 (A4, A3, Letter, etc.) [default: A4]
    --margin-top SIZE    上边距 (e.g., 20mm) [default: 20mm]
    --margin-bottom SIZE 下边距 [default: 20mm]
    --margin-left SIZE   左边距 [default: 15mm]
    --margin-right SIZE  右边距 [default: 15mm]
    --no-background     不打印背景色/背景图
    --landscape         横向打印
    --scale FLOAT       缩放比例 (0.1-2.0) [default: 1.0]
    --help              显示帮助信息
"""

import sys
import os
import argparse

def check_dependencies():
    """检查依赖是否已安装"""
    missing = []
    
    try:
        import playwright
    except ImportError:
        missing.append("playwright")
    
    if missing:
        print("❌ 缺少依赖:", ", ".join(missing))
        print("\n请运行以下命令安装:")
        print("  pip3 install playwright")
        print("  python3 -m playwright install chromium")
        return False
    
    return True

def html_to_pdf(input_path, output_path, options=None):
    """
    将 HTML 文件转换为 PDF
    
    Args:
        input_path: HTML 文件路径（绝对或相对）
        output_path: 输出 PDF 文件路径
        options: 可选参数字典
            - format: 页面尺寸 (A4, A3, etc.)
            - margin_top/margin_bottom/margin_left/margin_right: 边距
            - print_background: 是否打印背景 (True/False)
            - landscape: 是否横向 (True/False)
            - scale: 缩放比例 (0.1-2.0)
    
    Returns:
        bool: 成功返回 True，失败返回 False
    """
    if options is None:
        options = {}
    
    try:
        from playwright.sync_api import sync_playwright
        import time
        
        # 默认参数
        page_format = options.get("format", "A4")
        margin_top = options.get("margin_top", "20mm")
        margin_bottom = options.get("margin_bottom", "20mm")
        margin_left = options.get("margin_left", "15mm")
        margin_right = options.get("margin_right", "15mm")
        print_background = options.get("print_background", True)
        landscape = options.get("landscape", False)
        scale = options.get("scale", 1.0)
        
        print(f"📄 正在转换: {input_path}")
        print(f"💾 输出到: {output_path}")
        print(f"⚙️  参数: format={page_format}, margins={margin_top}/{margin_right}/{margin_bottom}/{margin_left}")
        
        # 确保输入文件存在
        if not os.path.exists(input_path):
            print(f"❌ 错误: 找不到文件 {input_path}")
            return False
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 转换为绝对路径
        input_abs = os.path.abspath(input_path)
        
        with sync_playwright() as p:
            # 启动浏览器
            print("🚀 启动浏览器...")
            browser = p.chromium.launch(headless=True)
            
            # 创建新页面
            page = browser.new_page()
            
            # 加载 HTML 文件
            print("⏳ 加载 HTML 文件...")
            file_url = f"file://{input_abs}"
            page.goto(file_url, wait_until="networkidle", timeout=30000)
            
            # 等待页面渲染完成
            time.sleep(2)
            
            # 生成 PDF
            print("📸 生成 PDF...")
            page.pdf(
                path=output_path,
                format=page_format,
                print_background=print_background,
                landscape=landscape,
                scale=scale,
                margin={
                    "top": margin_top,
                    "right": margin_right,
                    "bottom": margin_bottom,
                    "left": margin_left
                }
            )
            
            # 关闭浏览器
            browser.close()
        
        # 检查输出文件
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ 转换成功！PDF 已保存到: {output_path}")
            print(f"📊 文件大小: {file_size / 1024:.1f} KB")
            return True
        else:
            print(f"❌ 错误: PDF 文件未生成")
            return False
            
    except ImportError as e:
        print(f"❌ 依赖错误: {e}")
        print("请运行: pip3 install playwright")
        return False
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="HTML to PDF Converter - 将 HTML 文件转换为高质量 PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 html_to_pdf.py input.html output.pdf
  python3 html_to_pdf.py input.html output.pdf --format A3
  python3 html_to_pdf.py input.html output.pdf --margin-top 30mm --no-background
        """
    )
    
    parser.add_argument("input", help="输入 HTML 文件路径")
    parser.add_argument("output", help="输出 PDF 文件路径")
    parser.add_argument("--format", default="A4", help="页面尺寸 (A4, A3, Letter, etc.) [default: A4]")
    parser.add_argument("--margin-top", default="20mm", help="上边距 [default: 20mm]")
    parser.add_argument("--margin-bottom", default="20mm", help="下边距 [default: 20mm]")
    parser.add_argument("--margin-left", default="15mm", help="左边距 [default: 15mm]")
    parser.add_argument("--margin-right", default="15mm", help="右边距 [default: 15mm]")
    parser.add_argument("--no-background", action="store_true", help="不打印背景色/背景图")
    parser.add_argument("--landscape", action="store_true", help="横向打印")
    parser.add_argument("--scale", type=float, default=1.0, help="缩放比例 (0.1-2.0) [default: 1.0]")
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 组装选项
    options = {
        "format": args.format,
        "margin_top": args.margin_top,
        "margin_bottom": args.margin_bottom,
        "margin_left": args.margin_left,
        "margin_right": args.margin_right,
        "print_background": not args.no_background,
        "landscape": args.landscape,
        "scale": args.scale
    }
    
    # 执行转换
    success = html_to_pdf(args.input, args.output, options)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

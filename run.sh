#!/bin/bash
# Anki学习卡片生成器 - 快速启动脚本

set -e

echo "============================================================"
echo "📚 Anki学习卡片生成器 v1.0"
echo "============================================================"

# 激活虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "✅ 激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "📋 检查依赖..."
pip install -q PyPDF2 pdfplumber jieba genanki flask 2>/dev/null || true

# 创建输出目录
mkdir -p output uploads

# 显示选项
echo ""
echo "请选择启动方式:"
echo "  1) Web界面 (推荐)"
echo "  2) 命令行模式"
echo "  3) 运行测试"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🌐 启动Web服务..."
        echo "   访问: http://localhost:5000"
        echo "   按 Ctrl+C 停止服务"
        echo ""
        cd web && python app.py
        ;;
    2)
        echo ""
        read -p "请输入PDF文件路径: " pdf_file
        if [ -f "$pdf_file" ]; then
            echo "📄 处理PDF: $pdf_file"
            python anki_gen.py "$pdf_file" --format all
            echo ""
            echo "✅ 完成！查看 output/ 目录"
        else
            echo "❌ 文件不存在: $pdf_file"
        fi
        ;;
    3)
        echo ""
        echo "🧪 运行测试..."
        python test_generator.py
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

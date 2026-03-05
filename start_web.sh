#!/bin/bash
# Anki学习卡片生成器 - Web服务一键启动脚本

echo "========================================"
echo "📚 Anki学习卡片生成器 - Web服务"
echo "========================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 检查依赖
echo ""
echo "🔍 检查依赖..."

python3 -c "import pdfplumber" 2>/dev/null || {
    echo "❌ 缺少依赖: pdfplumber"
    echo "正在安装依赖..."
    pip install -r requirements.txt
}

python3 -c "import genanki" 2>/dev/null || {
    echo "❌ 缺少依赖: genanki"
    echo "正在安装依赖..."
    pip install -r requirements.txt
}

python3 -c "import flask" 2>/dev/null || {
    echo "❌ 缺少依赖: flask"
    echo "正在安装依赖..."
    pip install -r requirements.txt
}

echo "✅ 依赖检查完成"

# 进入Web目录
cd "$(dirname "$0")/web"

# 创建必要目录
mkdir -p uploads output

# 获取本机IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="localhost"
fi

echo ""
echo "========================================"
echo "🚀 启动Web服务"
echo "========================================"
echo ""
echo "服务地址:"
echo "  本地访问: http://localhost:5000"
echo "  网络访问: http://$LOCAL_IP:5000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""
echo "========================================"
echo ""

# 启动Flask服务
python3 app.py

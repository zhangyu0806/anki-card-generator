# 📚 Anki学习卡片生成器

**把PDF教材自动变成Anki卡片，1小时搞定500页！**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)

---

## ✨ 特性

- **🚀 快速生成**：500页PDF只需几分钟
- **🎯 智能提取**：自动识别重点内容
- **📝 多种卡片**：问答卡、填空卡、概念卡
- **📱 多平台支持**：Anki、Quizlet、Flashcards
- **💻 简单易用**：Web界面，拖拽上传

---

## 🎯 适用场景

- 📖 **考研党**：英语/政治/专业课教材
- 📝 **考证党**：CPA/法考/教资/建造师
- 💻 **技能学习**：编程教程/技术文档
- 🌍 **语言学习**：外语教材/词汇书

---

## 🚀 快速开始

### 方法1: Web界面（推荐）

```bash
# 克隆仓库
git clone https://github.com/zhangyu0806/anki-card-generator.git
cd anki-card-generator

# 激活虚拟环境并启动
./run.sh
# 选择选项1启动Web服务

# 浏览器访问
http://localhost:5000
```

### 方法2: 命令行

```bash
# 激活虚拟环境
source venv/bin/activate

# 生成Anki卡片
python anki_gen.py your_textbook.pdf \
    --deck-name "我的教材" \
    --types qa,cloze,concept \
    --format apkg

# 输出文件在 output/ 目录
```

---

## 📸 界面预览

### Web界面
精美的渐变紫色UI，支持拖拽上传

![Web界面](docs/web_ui.png)

### 生成效果
```
卡片 1 [问答卡]
问: 什么是机器学习？
答: 机器学习是人工智能的一个分支...

卡片 2 [填空卡]
问: {{c1::机器学习}}是人工智能的一个分支...
答: 机器学习是人工智能的一个分支...

卡片 3 [概念卡]
问: 机器学习
答: 人工智能的一个分支，它使计算机能够从数据中学习...
```

---

## 🎴 卡片类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **问答卡 (QA)** | 问答形式 | "什么是机器学习？" → 答案 |
| **填空卡 (Cloze)** | 挖空填空 | "{{c1::机器学习}}是..." |
| **概念卡 (Concept)** | 概念解释 | "机器学习" → 定义 |

---

## 📦 输出格式

| 格式 | 文件 | 用途 |
|------|------|------|
| **Anki** | .apkg | 导入Anki桌面版/移动版 |
| **Quizlet** | .csv | 导入Quizlet网站 |
| **Flashcards** | .json | 通用JSON格式 |

---

## 🛠️ 技术栈

### 后端
- **Python 3.12**
- **Flask 3.1.0** - Web框架
- **pdfplumber 0.11.9** - PDF解析
- **genanki 0.13.0** - Anki格式
- **jieba 0.42.1** - 中文分词

### 前端
- 原生HTML/CSS/JavaScript
- 响应式设计
- 渐变紫色主题

---

## 📖 使用文档

详细使用说明请查看 [USAGE.md](USAGE.md)

---

## 🧪 测试

```bash
# 运行测试
python test_generator.py

# 测试结果示例
✅ 卡片生成器: 通过 (生成10张卡片)
✅ Anki导出: 通过 (52.2 KB .apkg文件)
✅ Quizlet导出: 通过 (1.4 KB CSV文件)
✅ Flashcards导出: 通过 (2.2 KB JSON文件)
```

---

## 📂 项目结构

```
anki-card-generator/
├── core/                  # 核心模块
│   ├── pdf_parser.py          # PDF解析器
│   ├── card_generator.py      # 卡片生成器
│   └── anki_exporter.py       # Anki导出器
├── web/                   # Web界面
│   ├── app.py                # Flask应用
│   └── templates/
│       └── index.html        # HTML模板
├── examples/              # 示例文件
├── marketing/             # 推广素材
├── README.md              # 项目说明
├── USAGE.md              # 使用指南
├── anki_gen.py           # CLI入口
├── test_generator.py     # 测试脚本
└── run.sh               # 快速启动
```

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF解析
- [genanki](https://github.com/kerrickstaley/genanki) - Anki格式生成

---

## 📞 联系方式

- 项目地址：[GitHub](https://github.com/zhangyu0806/anki-card-generator)
- 在线演示：[待上线]

---

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**

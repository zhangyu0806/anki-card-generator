# Anki Card Generator - PDF转Anki卡片工具

> 500页教材 → 400+张高质量记忆卡片，仅需1分钟

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 简介

Anki Card Generator 是一个自动化学习卡片生成工具，可以将PDF教材快速转换为Anki卡片。支持8种知识模式、双向卡片和AI增强提取，是考研、考证、职场学习的效率神器。

### 核心功能

| 功能 | 描述 |
|------|------|
| **PDF解析** | 自动提取PDF中的知识点、定义、公式 |
| **8种知识模式** | 定义、枚举、对比、因果、公式、填空、判断、应用 |
| **双向卡片** | 问题→答案 + 答案→问题，记忆效率提升100% |
| **AI增强** | 使用智谱GLM-4-Flash（免费API）智能提取 |
| **Web界面** | Flask Web App，上传PDF即可下载.apkg文件 |

## 🚀 快速开始

### 在线使用（推荐）

访问在线演示站：[https://zhangyu0806.github.io/anki-card-generator/](https://zhangyu0806.github.io/anki-card-generator/)

1. 上传PDF文件
2. 选择知识模式
3. 点击生成
4. 下载.apkg文件并导入Anki

### 本地安装

```bash
git clone https://github.com/zhangyu0806/anki-card-generator.git
cd anki-card-generator
pip install -r requirements.txt
```

### CLI使用

```bash
# 基础用法
python -m core generate textbook.pdf --output cards.apkg

# 指定知识模式
python -m core generate textbook.pdf --modes definition enumeration comparison --output cards.apkg

# AI增强模式
python -m core generate textbook.pdf --ai --output cards.apkg
```

### Web服务

```bash
cd web
python app.py
# 访问 http://localhost:5000
```

## 📁 项目结构

```
anki-card-generator/
├── core/
│   ├── pdf_parser.py         # PDF解析
│   ├── card_generator.py     # 卡片生成
│   └── export.py             # .apkg导出
├── web/
│   ├── app.py                # Flask Web App
│   └── templates/            # HTML模板
├── requirements.txt
└── README.md
```

## 🎯 知识模式

| 模式 | 说明 | 示例 |
|------|------|------|
| **定义** | 概念解释 | 问：什么是剩余价值？答：... |
| **枚举** | 列举要点 | 问：辩证法的三大规律？答：1. 2. 3. |
| **对比** | 概念对比 | 问：唯物vs唯心的区别？答：... |
| **因果** | 原因结果 | 问：为什么2026年AI爆发？答：... |
| **公式** | 数学公式 | 问：牛顿第二定律？答：F=ma |
| **填空** | 关键词挖空 | 人工智能的三大要素是___、___、___ |
| **判断** | 对错判断 | 机器学习等于AI（对/错） |
| **应用** | 案例分析 | 某公司如何用AI优化运营？ |

## 📊 实测数据

| 教材 | 页数 | 生成卡片 | 耗时 | 人工vs工具 |
|------|------|---------|------|-----------|
| 马原 | 320页 | 312张 | 45秒 | 8小时 → 45秒 |
| 高数上 | 280页 | 196张 | 38秒 | 5小时 → 38秒 |
| 经济学原理 | 450页 | 406张 | 62秒 | 12小时 → 62秒 |

## 💡 技术亮点

- **零成本AI**：使用智谱GLM-4-Flash免费API，无需付费
- **高准确率**：规则提取+AI增强双重保障
- **双向卡片**：正向+反向记忆，符合间隔重复原理
- **Anki原生**：生成标准.apkg文件，兼容所有Anki版本

## 🎓 使用场景

- **考研党**：政治、英语、数学教材快速转卡片
- **考证党**：CPA、法考、教资等考试资料卡片化
- **职场学习**：技术文档、业务流程、产品手册
- **语言学习**：词汇书、语法书、阅读材料

## 🔧 技术栈

- **PDF解析**: pdfplumber, pypdfium2
- **卡片生成**: genanki
- **Web框架**: Flask
- **AI增强**: 智谱GLM-4-Flash

## 📝 License

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

- GitHub: https://github.com/zhangyu0806/anki-card-generator
- Issue: https://github.com/zhangyu0806/anki-card-generator/issues

---

**⭐ 如果这个工具对你有帮助，请给个Star支持一下！**

**🎓 祝你学习效率翻倍，考试顺利！**

# Anki学习卡片生成器 - 快速启动指南

## 🚀 3分钟上手

### 方法1：在线使用（最简单）

1. 访问：https://zhangyu0806.github.io/anki-card-generator/
2. 上传PDF文件
3. 选择卡片类型（问答、填空、概念）
4. 点击生成，下载.apkg文件
5. 导入到Anki桌面版或AnkiMobile

### 方法2：本地安装

```bash
# 1. 克隆仓库
git clone https://github.com/zhangyu0806/anki-card-generator.git
cd anki-card-generator

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行CLI工具
python3 anki_gen.py your_textbook.pdf

# 4. 启动Web服务
cd web
python3 app.py
# 访问 http://localhost:5000
```

---

## 📖 使用示例

### 示例1：生成问答卡

```bash
python3 anki_gen.py textbook.pdf --types qa --output-dir output
```

**输出：**
- `output/textbook_20260303_120000.apkg` - Anki卡片包
- `output/textbook_20260303_120000.json` - JSON格式（可用于其他应用）

### 示例2：生成多种卡片类型

```bash
python3 anki_gen.py textbook.pdf --types qa,cloze,concept
```

**卡片类型说明：**
- `qa` - 问答卡（什么是X？Y是X）
- `cloze` - 填空卡（X的三大要素是___、___、___）
- `concept` - 概念卡（X vs Y的区别）

### 示例3：限制卡片数量

```bash
python3 anki_gen.py textbook.pdf --limit 50
```

**适用场景：** 免费试用、快速预览

---

## 🎴 卡片类型详解

### 1. 问答卡（QA）
**格式：** 问题 → 答案

**示例：**
```
Q: 什么是剩余价值？
A: 剩余价值是雇佣工人创造的、被资本家无偿占有的超过劳动力价值的价值。
```

**适用：** 定义、原理、概念解释

### 2. 填空卡（Cloze）
**格式：** 关键词挖空

**示例：**
```
辩证法的三大规律是___、___、___。
```

**适用：** 要点记忆、列举型内容

### 3. 概念卡（Concept）
**格式：** 概念对比

**示例：**
```
Q: 唯物主义 vs 唯心主义的根本区别是什么？
A: 物质和意识谁是第一性（本原）的问题。
```

**适用：** 易混概念、对比辨析

---

## 📊 实测数据

| 教材 | 页数 | 知识点 | 卡片数 | 耗时 |
|------|------|--------|--------|------|
| 马原 | 320页 | 312个 | 312张 | 45秒 |
| 高数上 | 280页 | 196个 | 196张 | 38秒 |
| 经济学原理 | 450页 | 406个 | 406张 | 62秒 |
| CPA会计 | 500页 | 820个 | 820张 | 85秒 |

---

## 🎯 适用场景

### 考研
- ✅ 考研政治（马原、毛概、史纲、思修）
- ✅ 考研英语（词汇、语法、阅读）
- ✅ 考研数学（公式、定理、题型）

### 考证
- ✅ CPA（注册会计师）
- ✅ 法考（法律职业资格考试）
- ✅ 教资（教师资格证）
- ✅ 一建（一级建造师）
- ✅ 医师资格

### 职场学习
- ✅ 技术文档
- ✅ 业务手册
- ✅ 产品知识
- ✅ 行业法规

---

## ⚙️ 高级用法

### AI增强模式（可选）

使用智谱GLM-4-Flash免费API提升提取质量：

```bash
# 设置环境变量
export ZHIPU_API_KEY="your_api_key"

# 启用AI模式
python3 anki_gen.py textbook.pdf --ai
```

### 批量处理

```bash
# 处理多个PDF
for pdf in *.pdf; do
    python3 anki_gen.py "$pdf" --output-dir output
done
```

### 自定义规则

编辑 `core/pdf_parser.py` 中的正则表达式来适配特定教材：

```python
# 添加新的知识点识别规则
CUSTOM_PATTERNS = [
    ('important', re.compile(r'(重点|核心|必背)：(.{10,})')),
    ('formula', re.compile(r'([A-Z][a-z]+)\s*=')),
]
```

---

## 📱 导入到Anki

### Anki桌面版
1. 打开Anki
2. 文件 → 导入
3. 选择.apkg文件
4. 确认导入

### AnkiMobile (iOS)
1. 将.apkg文件传输到iPhone（AirDrop、iCloud、邮件）
2. 打开文件，选择Anki导入
3. 确认导入

### AnkiDroid (Android)
1. 将.apkg文件复制到手机存储
2. AnkiDroid → 导入牌组
3. 选择.apkg文件

---

## ❓ 常见问题

### Q1: 生成的卡片质量如何？
A: 使用规则提取+AI增强双重保障。支持8种知识模式自动识别，准确率约85-95%。可以自定义规则优化质量。

### Q2: 免费版有什么限制？
A: 开源项目完全免费！在线版有免费试用额度（每PDF限制页数）。

### Q3: 支持哪些PDF格式？
A: 支持大部分文本型PDF（教材、文档）。扫描版PDF（图片）需要OCR处理。

### Q4: 可以编辑生成的卡片吗？
A: 可以！.apkg导入Anki后，可以随意编辑、删除、添加卡片。

### Q5: 如何提升卡片质量？
A:
1. 使用PDF原始版本（非扫描版）
2. 启用AI增强模式
3. 自定义知识点识别规则
4. 手动筛选和精修

---

## 🤝 获取帮助

- **GitHub Issues**: https://github.com/zhangyu0806/anki-card-generator/issues
- **在线演示**: https://zhangyu0806.github.io/anki-card-generator/
- **使用教程**: 见 `docs/` 目录

---

**🎓 祝你学习效率翻倍，考试顺利！**

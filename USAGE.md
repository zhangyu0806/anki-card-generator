# 使用指南

## 快速开始

### 方法1: 命令行

```bash
# 激活虚拟环境
cd /root/.openclaw/workspace/anki-card-generator
source venv/bin/activate

# 生成Anki卡片
python anki_gen.py your_textbook.pdf \
    --deck-name "我的教材" \
    --types qa,cloze \
    --format apkg

# 输出文件在 output/ 目录
```

### 方法2: Web界面

```bash
# 启动Web服务
cd /root/.openclaw/workspace/anki-card-generator/web
../venv/bin/python app.py

# 浏览器访问
http://localhost:5000
```

## 选项说明

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--deck-name` | 牌组名称 | PDF文件名 |
| `--types` | 卡片类型 (qa,cloze,concept,all) | all |
| `--format` | 输出格式 (apkg,quizlet,flashcards,all) | apkg |
| `--limit` | 最多生成卡片数 | 不限制 |

## 卡片类型

### 问答卡 (QA)
- 正面: 问题
- 背面: 答案
- 示例: "什么是机器学习？" → "机器学习是..."

### 填空卡 (Cloze)
- 正面: 带空格的句子
- 背面: 完整句子
- 示例: "{{c1::机器学习}}是..." → "机器学习是..."

### 概念卡 (Concept)
- 正面: 概念名称
- 背面: 概念解释
- 示例: "机器学习" → "人工智能的一个分支..."

## 输出格式

| 格式 | 文件扩展名 | 用途 |
|------|-----------|------|
| Anki | .apkg | 导入到Anki桌面版/移动版 |
| Quizlet | .csv | 导入到Quizlet网站 |
| Flashcards | .json | 通用JSON格式 |

## 导入到Anki

1. 下载生成的.apkg文件
2. 打开Anki桌面版
3. 文件 → 导入
4. 选择.apkg文件
5. 开始学习！

## 使用建议

1. **首次使用**：先用小PDF测试（10-20页）
2. **卡片数量**：500页PDF可能生成数百张卡片，建议用--limit限制
3. **卡片质量**：生成后检查卡片质量，删除不合适的
4. **批量处理**：多本教材可以分开处理，创建多个牌组

## 故障排除

### PDF无法解析
- 确认PDF是文本格式（非扫描图片）
- 尝试用其他工具转换PDF

### 生成的卡片质量差
- 调整card_types参数
- 手动编辑生成的.csv文件再导入

### .apkg文件无法导入
- 确认Anki版本（2.1+）
- 尝试用JSON格式导入

## 进阶使用

### 自定义规则
编辑 `core/card_generator.py` 中的模式匹配规则

### Web部署
使用Gunicorn部署：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
```

### Docker部署
```bash
docker build -t anki-gen .
docker run -p 5000:5000 anki-gen
```

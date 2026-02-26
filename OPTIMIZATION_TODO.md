# 卡片生成器优化清单

## 测试结果总结

### ✅ 工作良好的场景
- 定义型内容：能正确识别"X是Y"结构
- 分类型内容：能识别"X包括Y"结构
- 特点型内容：能识别"X的特点是Y"结构
- 作用型内容：能识别"X的作用是Y"结构

### ⚠️ 需要改进的问题

#### 1. 问题表述不自然（优先级：高）
**问题示例：**
- "深度学习是机是什么？" → 应该是 "什么是深度学习？"
- "梯度下降是一是什么？" → 应该是 "什么是梯度下降？"

**原因：** 概念提取位置错误，提取了"深度学习是"而不是"深度学习"

**解决方案：**
- 改进 `_extract_concept()` 方法
- 对于"X是Y"结构，应该提取"X"而不是"X是"

#### 2. 概念提取位置错误（优先级：高）
**问题示例：**
- "通过引入残差是什么？" → 应该提取 "ResNet"
- "注意力机制允是什么？" → 应该提取 "注意力机制"

**原因：** 句子主语位置判断错误

**解决方案：**
- 优先匹配"名词+是"模式
- 改进中文分词，识别主语

#### 3. 填空卡挖空位置问题（优先级：中）
**问题示例：**
- "{{c1::深度学习分}}为..." → 应该是 "{{c1::深度学习}}分为..."

**原因：** 正则匹配时没有考虑"分为"应该作为一个整体

**解决方案：**
- 改进 `_create_cloze()` 方法的正则表达式
- 对于"分为"等词，应该在其之前挖空

#### 4. 复杂句未拆分（优先级：中）
**问题示例：**
- "ResNet通过引入残差连接，解决了深层网络中的梯度消失问题，使得训练非常深的网络成为可能。"
- 这个长句子应该拆分成2-3张卡片

**解决方案：**
- 添加句子复杂度判断
- 对于超过一定长度的句子，进行拆分

---

## 优化计划

### P0 - 立即修复（影响用户体验）
1. 修复问题表述：确保"什么是X？"格式正确
2. 改进概念提取：准确识别主语/核心概念
3. 修复填空挖空位置

### P1 - 本周优化
4. 添加复杂句拆分功能
5. 添加更多生成规则模板
6. 改进去重逻辑

### P2 - 后续版本
7. 添加NLP模型进行语义分析
8. 支持用户自定义卡片模板
9. 添加卡片质量评分

---

## 代码修改建议

### card_generator.py - QACardGenerator._extract_concept()

```python
# 当前代码（有问题）
def _extract_concept(self, text: str) -> str:
    match = re.search(r'^(.{2,8?})是', text)
    if match:
        return match.group(1)
    match = re.search(r'定义：(.{2,8?})', text)
    if match:
        return match.group(1)
    return ""

# 改进建议
def _extract_concept(self, text: str) -> str:
    # 模式1: "XXX是..." → 提取XXX
    match = re.search(r'^([\u4e00-\u9fa5\w]{2,10})是', text)
    if match:
        return match.group(1)
    # 模式2: "定义：XXX..." → 提取XXX
    match = re.search(r'定义：([\u4e00-\u9fa5\w]{2,10})', text)
    if match:
        return match.group(1)
    # 模式3: 句首名词短语
    match = re.search(r'^([\u4e00-\u9fa5]{2,8})(?:分为|包括|是指)', text)
    if match:
        return match.group(1)
    return ""
```

### card_generator.py - ClozeCardGenerator._create_cloze()

```python
# 改进建议
def _create_cloze(self, text: str) -> str:
    # 模式1: "XXX分为YYY" → "{{c1::XXX}}分为YYY"
    match = re.match(r'^([\u4e00-\u9fa5\w]{2,10})分为(.+)', text)
    if match:
        term = match.group(1)
        rest = text[len(term):]
        return f"{{{{c1::{term}}}}}{rest}"
    # 模式2: "XXX包括YYY" → "{{c1::XXX}}包括YYY"
    match = re.match(r'^([\u4e00-\u9fa5\w]{2,10})包括(.+)', text)
    if match:
        term = match.group(1)
        rest = text[len(term):]
        return f"{{{{c1::{term}}}}}{rest}"
    # ... 其他模式
    return text
```

---

*创建时间：2026-02-26 11:20*
*状态：待实施*

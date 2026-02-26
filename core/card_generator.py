#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki卡片生成器
从知识点生成多种类型的Anki卡片
"""

import re
import json
from typing import List, Dict, Literal
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AnkiCard:
    """Anki卡片"""
    front: str  # 问题/正面
    back: str   # 答案/背面
    card_type: str  # 类型: qa(问答), cloze(填空), concept(概念)
    tags: List[str]  # 标签
    source: str  # 来源页/章节


class CardGenerator(ABC):
    """卡片生成器基类"""
    
    @abstractmethod
    def generate(self, text: str, context: str, metadata: Dict) -> List[AnkiCard]:
        """生成卡片"""
        pass


class QACardGenerator(CardGenerator):
    """问答卡片生成器"""
    
    def generate(self, text: str, context: str, metadata: Dict) -> List[AnkiCard]:
        """从知识点生成问答卡"""
        cards = []
        
        # 模式1: "定义：..." → "什么是X？"
        if "定义：" in text or"是指" in text:
            question = self._extract_concept(text)
            if question:
                cards.append(AnkiCard(
                    front=f"什么是{question}？",
                    back=text,
                    card_type="qa",
                    tags=metadata.get("tags", []),
                    source=metadata.get("source", "")
                ))
        
        # 模式2: "X包括..." → "X包括哪些？"
        include_match = re.search(r'(.{2,10}?)包括(.+)', text)
        if include_match:
            concept = include_match.group(1)
            cards.append(AnkiCard(
                front=f"{concept}包括哪些？",
                back=text,
                card_type="qa",
                tags=metadata.get("tags", []),
                source=metadata.get("source", "")
            ))
        
        # 模式2.5: "X分为..." → "X分为哪些？"
        divide_match = re.search(r'(.{2,10}?)分为(.+)', text)
        if divide_match:
            concept = divide_match.group(1)
            cards.append(AnkiCard(
                front=f"{concept}分为哪些？",
                back=text,
                card_type="qa",
                tags=metadata.get("tags", []),
                source=metadata.get("source", "")
            ))
        
        # 模式3: "X的特点是..." → "X有什么特点？"
        feature_match = re.search(r'(.{2,10}?)的特点?(?:是|为)(.+)', text)
        if feature_match:
            concept = feature_match.group(1)
            cards.append(AnkiCard(
                front=f"{concept}有什么特点？",
                back=text,
                card_type="qa",
                tags=metadata.get("tags", []),
                source=metadata.get("source", "")
            ))
        
        # 默认: 将关键信息挖空
        if not cards and len(text) > 10 and len(text) < 100:
            # 提取关键术语
            key_term = self._extract_key_term(text)
            if key_term:
                cards.append(AnkiCard(
                    front=f"{key_term}是什么？",
                    back=text,
                    card_type="qa",
                    tags=metadata.get("tags", []),
                    source=metadata.get("source", "")
                ))
        
        return cards
    
    def _extract_concept(self, text: str) -> str:
        """提取概念名称"""
        # "XXX是指..." → XXX (只匹配中文字符/字母数字，不包括"是")
        match = re.search(r'^([\u4e00-\u9fa5\w]{2,10})(是指|是指为)', text)
        if match:
            return match.group(1)
        
        # "XXX是..." → XXX
        match = re.search(r'^([\u4e00-\u9fa5\w]{2,10})是([\u4e00-\u9fa5\w]|.{2,})', text)
        if match:
            # 确保后面不是"分为"等动词
            following = match.group(2)
            if following not in ['分为', '包括', '是指']:
                return match.group(1)
        
        # "定义：XXX..." → XXX
        match = re.search(r'定义：([\u4e00-\u9fa5\w]{2,10})', text)
        if match:
            return match.group(1)
        
        # "XXX分为..." → XXX
        match = re.search(r'^([\u4e00-\u9fa5\w]{2,10})分为', text)
        if match:
            return match.group(1)
        
        # "XXX包括..." → XXX
        match = re.search(r'^([\u4e00-\u9fa5\w]{2,10})包括', text)
        if match:
            return match.group(1)
        
        return ""
    
    def _extract_key_term(self, text: str) -> str:
        """提取关键术语"""
        # 优先提取：主语 + 是
        match = re.search(r'^([\u4e00-\u9fa5\w]{2,10})是', text)
        if match:
            return match.group(1)
        
        # 次选：提取中文短语（在常见动词/介词前停止）
        # 在 是、为、分、包、的、了、于、等 前停止
        match = re.search(r'^([\u4e00-\u9fa5]{2,8})(?=[是分为包的了于等以及]|[，。；：！？、的是的了]|[a-zA-Z0-9]|$)', text)
        if match:
            return match.group(1)
        
        # 兜底：提取中文词组（避免跨词）
        # 使用jieba分词或更简单的方法：在非中文字符前停止
        words = re.findall(r'[\u4e00-\u9fa5]{2,6}(?![\u4e00-\u9fa5])', text[:30])
        if words:
            return words[0]
        return ""


class ClozeCardGenerator(CardGenerator):
    """填空卡片生成器"""
    
    def generate(self, text: str, context: str, metadata: Dict) -> List[AnkiCard]:
        """从知识点生成填空卡"""
        cards = []
        
        # Anki填空格式: {{c1::答案}}
        cloze_text = self._create_cloze(text)
        if cloze_text != text:
            cards.append(AnkiCard(
                front=cloze_text,
                back=text,
                card_type="cloze",
                tags=metadata.get("tags", []),
                source=metadata.get("source", "")
            ))
        
        return cards
    
    def _create_cloze(self, text: str) -> str:
        """创建填空题"""
        # 模式1: "XXX是YYY" → "{{c1::XXX}}是YYY"
        match = re.match(r'^([\u4e00-\u9fa5\w]{2,10})(是|为|指)(.+)', text)
        if match:
            term = match.group(1)
            rest = text[len(term):]
            return f"{{{{c1::{term}}}}}{rest}"
        
        # 模式2: "XXX分为YYY" → "{{c1::XXX}}分为YYY"
        match = re.match(r'^([\u4e00-\u9fa5\w]{2,10})分为(.+)', text)
        if match:
            term = match.group(1)
            rest = text[len(term):]
            return f"{{{{c1::{term}}}}}{rest}"
        
        # 模式3: "XXX包括YYY" → "{{c1::XXX}}包括YYY"
        match = re.match(r'^([\u4e00-\u9fa5\w]{2,10})包括(.+)', text)
        if match:
            term = match.group(1)
            rest = text[len(term):]
            return f"{{{{c1::{term}}}}}{rest}"
        
        # 模式4: "包括A, B, C" → "包括{{c1::A, B, C}}"
        include_match = re.search(r'包括(.+)', text)
        if include_match:
            items = include_match.group(1)
            if len(items) > 3 and len(items) < 50:
                prefix = text[:include_match.start()]
                return f"{prefix}包括{{{{c1::{items}}}}}"
        
        # 默认: 挖第一个词
        words = re.findall(r'([\u4e00-\u9fa5]{2,6})', text)
        if len(words) >= 2:
            first_word = words[0]
            rest = text[len(first_word):]
            return f"{{{{c1::{first_word}}}}}{rest}"
        
        return text


class ConceptCardGenerator(CardGenerator):
    """概念卡片生成器"""
    
    def generate(self, text: str, context: str, metadata: Dict) -> List[AnkiCard]:
        """从知识点生成概念卡"""
        cards = []
        
        # 提取概念和解释
        concept = self._extract_concept(text)
        explanation = self._extract_explanation(text)
        
        if concept and explanation:
            cards.append(AnkiCard(
                front=concept,
                back=explanation,
                card_type="concept",
                tags=metadata.get("tags", []),
                source=metadata.get("source", "")
            ))
        
        return cards
    
    def _extract_concept(self, text: str) -> str:
        """提取概念"""
        match = re.search(r'^(.{2,10}?)(?:是|为|指|：)', text)
        if match:
            return match.group(1)
        return ""
    
    def _extract_explanation(self, text: str) -> str:
        """提取解释"""
        # 去掉概念部分，保留解释
        match = re.match(r'^.{2,10?}(?:是|为|指|：)(.+)', text)
        if match:
            return match.group(1).strip()
        return text


class AnkiCardGenerator:
    """主卡片生成器"""
    
    def __init__(self):
        self.generators = {
            "qa": QACardGenerator(),
            "cloze": ClozeCardGenerator(),
            "concept": ConceptCardGenerator()
        }
    
    def generate_from_keypoints(
        self,
        key_points: List[Dict],
        card_types: List[str] = None
    ) -> List[AnkiCard]:
        """从知识点列表生成卡片"""
        if card_types is None:
            card_types = ["qa", "cloze", "concept"]
        
        all_cards = []
        
        for kp in key_points:
            text = kp.get("text", "")
            context = kp.get("context", "")
            metadata = {
                "tags": [kp.get("section", "")],
                "source": f"第{kp.get('page', '')}页"
            }
            
            for card_type in card_types:
                if card_type in self.generators:
                    cards = self.generators[card_type].generate(text, context, metadata)
                    all_cards.extend(cards)
        
        # 去重
        seen = set()
        unique_cards = []
        for card in all_cards:
            key = (card.front, card.back)
            if key not in seen:
                seen.add(key)
                unique_cards.append(card)
        
        return unique_cards
    
    def generate_from_text(
        self,
        text: str,
        card_types: List[str] = None
    ) -> List[AnkiCard]:
        """从文本生成卡片"""
        if card_types is None:
            card_types = ["qa"]
        
        metadata = {
            "tags": [],
            "source": "手动输入"
        }
        
        all_cards = []
        for card_type in card_types:
            if card_type in self.generators:
                cards = self.generators[card_type].generate(text, "", metadata)
                all_cards.extend(cards)
        
        return all_cards
    
    def export_to_dict(self, cards: List[AnkiCard]) -> List[Dict]:
        """导出为字典格式"""
        return [
            {
                "front": card.front,
                "back": card.back,
                "type": card.card_type,
                "tags": card.tags,
                "source": card.source
            }
            for card in cards
        ]


def main():
    """测试代码"""
    generator = AnkiCardGenerator()
    
    # 测试知识点
    test_keypoints = [
        {"text": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习。", "page": 10, "section": "第一章"},
        {"text": "深度学习包括神经网络、卷积神经网络、循环神经网络等。", "page": 15, "section": "第二章"},
        {"text": "过拟合是指模型在训练数据上表现很好，但在新数据上表现差。", "page": 20, "section": "第三章"},
    ]
    
    cards = generator.generate_from_keypoints(test_keypoints)
    
    print(f"📝 生成卡片数: {len(cards)}")
    print("\n卡片预览:")
    for i, card in enumerate(cards[:10], 1):
        print(f"\n卡片 {i} [{card.card_type}]:")
        print(f"  问: {card.front}")
        print(f"  答: {card.back}")
        print(f"  标签: {card.tags}")


if __name__ == "__main__":
    main()

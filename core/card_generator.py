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
        tags = metadata.get("tags", [])
        source = metadata.get("source", "")
        
        # 模式1: "定义：X是Y" → "X的定义是什么？"
        def_match = re.match(r'定义[：:]\s*(.+?)(?:是指|是)(.+)', text)
        if def_match:
            concept = def_match.group(1).strip()
            if 2 <= len(concept) <= 20:
                cards.append(AnkiCard(
                    front=f"{concept}的定义是什么？",
                    back=text,
                    card_type="qa", tags=tags, source=source
                ))
                return cards
        
        # 模式2: "X是指Y" → "什么是X？"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})是指(.+)', text)
        if m:
            concept = m.group(1).strip()
            cards.append(AnkiCard(
                front=f"什么是{concept}？",
                back=text,
                card_type="qa", tags=tags, source=source
            ))
            return cards
        
        # 模式3: "X包括Y" → "X包括哪些？"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})包括(.+)', text)
        if m:
            concept = m.group(1).strip()
            cards.append(AnkiCard(
                front=f"{concept}包括哪些？",
                back=text,
                card_type="qa", tags=tags, source=source
            ))
            return cards
        
        # 模式4: "X分为Y" → "X分为哪些？"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})分为(.+)', text)
        if m:
            concept = m.group(1).strip()
            cards.append(AnkiCard(
                front=f"{concept}分为哪几类？",
                back=text,
                card_type="qa", tags=tags, source=source
            ))
            return cards
        
        # 模式5: "X的特点是Y" → "X有什么特点？"
        m = re.search(r'^([\u4e00-\u9fa5\w]{2,20})的特点是(.+)', text)
        if m:
            concept = m.group(1).strip()
            cards.append(AnkiCard(
                front=f"{concept}有什么特点？",
                back=text,
                card_type="qa", tags=tags, source=source
            ))
            return cards
        
        # 模式6: "X的作用是Y" → "X的作用是什么？"
        m = re.search(r'^([\u4e00-\u9fa5\w]{2,20})的作用是(.+)', text)
        if m:
            concept = m.group(1).strip()
            cards.append(AnkiCard(
                front=f"{concept}的作用是什么？",
                back=text,
                card_type="qa", tags=tags, source=source
            ))
            return cards
        
        # 模式7: "X的优点是Y" / "X的缺点是Y"
        m = re.search(r'^([\u4e00-\u9fa5\w]{2,20})的(优点|缺点)是(.+)', text)
        if m:
            concept = m.group(1).strip()
            cards.append(AnkiCard(
                front=f"{concept}的{m.group(2)}是什么？",
                back=text,
                card_type="qa", tags=tags, source=source
            ))
            return cards
        
        # 模式8: "X是Y" (通用定义) → "什么是X？"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})是(.{5,})', text)
        if m:
            subject = m.group(1).strip()
            # 排除太泛的主语
            if not re.match(r'^(这|那|它|其|本)', subject):
                cards.append(AnkiCard(
                    front=f"什么是{subject}？",
                    back=text,
                    card_type="qa", tags=tags, source=source
                ))
                return cards
        
        return cards
    
    def _extract_subject(self, text: str) -> str:
        """从句子中提取主语概念"""
        m = re.match(r'^(.+?)(?:是|为|指|，)', text)
        if m and 2 <= len(m.group(1)) <= 20:
            return m.group(1)
        return ""


class ClozeCardGenerator(CardGenerator):
    """填空卡片生成器"""
    
    def generate(self, text: str, context: str, metadata: Dict) -> List[AnkiCard]:
        """从知识点生成填空卡"""
        cards = []
        tags = metadata.get("tags", [])
        source = metadata.get("source", "")
        
        # Anki填空格式: {{c1::答案}}
        cloze_text = self._create_cloze(text)
        if cloze_text and cloze_text != text:
            cards.append(AnkiCard(
                front=cloze_text,
                back=text,
                card_type="cloze",
                tags=tags,
                source=source
            ))
        
        return cards
    
    def _create_cloze(self, text: str) -> str:
        """创建填空题 - 挖掉关键概念"""
        
        # 模式0: "定义：X是Y" → "定义：X是{{c1::Y}}"
        m = re.match(r'^(定义[：:]\s*.+?(?:是指|是))(.{5,})', text)
        if m:
            return f"{m.group(1)}{{{{c1::{m.group(2)}}}}}"
        
        # 模式1: "X是指Y" → "X是指{{c1::Y}}"
        m = re.match(r'^(.+?是指)(.+)', text)
        if m and len(m.group(2)) > 3:
            return f"{m.group(1)}{{{{c1::{m.group(2)}}}}}"
        
        # 模式2: "X包括Y" → "X包括{{c1::Y}}"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})(包括)(.+)', text)
        if m and len(m.group(3)) > 3:
            return f"{m.group(1)}{m.group(2)}{{{{c1::{m.group(3)}}}}}"
        
        # 模式3: "X分为Y" → "X分为{{c1::Y}}"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})(分为)(.+)', text)
        if m and len(m.group(3)) > 3:
            return f"{m.group(1)}{m.group(2)}{{{{c1::{m.group(3)}}}}}"
        
        # 模式4: "X的特点是Y" → "X的特点是{{c1::Y}}"
        m = re.match(r'^(.+?的特点是)(.+)', text)
        if m and len(m.group(2)) > 3:
            return f"{m.group(1)}{{{{c1::{m.group(2)}}}}}"
        
        # 模式5: "X的作用是Y" → "X的作用是{{c1::Y}}"
        m = re.match(r'^(.+?的作用是)(.+)', text)
        if m and len(m.group(2)) > 3:
            return f"{m.group(1)}{{{{c1::{m.group(2)}}}}}"
        
        # 模式6: "定义：X是Y" → "定义：{{c1::X是Y}}"
        m = re.match(r'^(定义[：:]\s*)(.+)', text)
        if m:
            return f"{m.group(1)}{{{{c1::{m.group(2)}}}}}"
        
        # 模式7: "X是Y"（通用） → "{{c1::X}}是Y"
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})是(.{5,})', text)
        if m:
            return f"{{{{c1::{m.group(1)}}}}}是{m.group(2)}"
        
        return ""


class ConceptCardGenerator(CardGenerator):
    """概念卡片生成器"""
    
    def generate(self, text: str, context: str, metadata: Dict) -> List[AnkiCard]:
        """从知识点生成概念卡"""
        cards = []
        tags = metadata.get("tags", [])
        source = metadata.get("source", "")
        
        # 提取概念和解释
        concept, explanation = self._split_concept(text)
        
        if concept and explanation and len(explanation) > 5:
            cards.append(AnkiCard(
                front=f"📖 {concept}",
                back=explanation,
                card_type="concept",
                tags=tags,
                source=source
            ))
        
        return cards
    
    def _split_concept(self, text: str):
        """将文本拆分为概念+解释"""
        # "定义：X是Y" → (X, 完整文本)
        m = re.match(r'定义[：:]\s*([\u4e00-\u9fa5\w]{2,20})(?:是指|是)(.+)', text)
        if m:
            return m.group(1).strip(), text
        
        # "X是指Y" → (X, Y)
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})是指(.+)', text)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        
        # "X是Y" → (X, Y)
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})是(.{5,})', text)
        if m:
            return m.group(1).strip(), text
        
        # "X包括Y" → (X, Y)
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})包括(.+)', text)
        if m:
            return m.group(1).strip(), text
        
        # "X分为Y" → (X, Y)
        m = re.match(r'^([\u4e00-\u9fa5\w]{2,20})分为(.+)', text)
        if m:
            return m.group(1).strip(), text
        
        return "", ""


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

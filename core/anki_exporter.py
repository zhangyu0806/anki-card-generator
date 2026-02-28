#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki导出器
生成Anki .apkg文件
"""

import genanki
import random
import hashlib
from datetime import datetime
from typing import List, Dict
from .card_generator import AnkiCard


# Anki模型ID (固定值，保证每次导入不会创建重复模型)
MODEL_ID = 1607392319
DECK_ID = 2059400110


class AnkiModel:
    """Anki卡片模型"""
    
    @staticmethod
    def get_basic_model():
        """基础问答模型"""
        return genanki.Model(
            MODEL_ID,
            "AnkiCardGenerator Model",
            fields=[
                {"name": "Front"},
                {"name": "Back"},
                {"name": "Tags"},
                {"name": "Source"},
            ],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": "<div class='card-front'>{{Front}}</div>",
                    "afmt": """
{{FrontSide}}

<hr class='answer-separator'>

<div class='card-back'>{{Back}}</div>

<div class='card-meta'>
<small>{{Tags}}<br>{{Source}}</small>
</div>

<style>
.card-front { font-size: 24px; text-align: center; padding: 20px; }
.card-back { font-size: 18px; padding: 20px; }
.card-meta { color: #666; margin-top: 20px; text-align: center; }
.answer-separator { margin: 20px 0; }
</style>
                    """,
                },
            ],
            css="""
.card {
    font-family: Arial;
    font-size: 20px;
    color: black;
    background-color: white;
}
            """
        )
    
    @staticmethod
    def get_cloze_model():
        """填空题模型"""
        return genanki.Model(
            MODEL_ID + 1,
            "Cloze Model",
            fields=[
                {"name": "Text"},
                {"name": "Back Extra"},
                {"name": "Tags"},
                {"name": "Source"},
            ],
            templates=[
                {
                    "name": "Cloze Card",
                    "qfmt": "{{cloze:Text}}",
                    "afmt": """
{{cloze:Text}}<br>
{{Back Extra}}

<div class='card-meta'>
<small>{{Tags}}<br>{{Source}}</small>
</div>
                    """,
                },
            ],
            model_type=genanki.Model.CLOZE
        )


class AnkiExporter:
    """Anki导出器"""
    
    def __init__(self, deck_name: str = "Anki学习卡片"):
        self.deck_name = deck_name
        self.model = AnkiModel.get_basic_model()
        self.deck = genanki.Deck(DECK_ID, deck_name)
        
    def add_cards(self, cards: List[AnkiCard]) -> None:
        """添加卡片到牌组"""
        for card in cards:
            # Anki tags不能包含空格，替换为下划线
            safe_tags = [t.replace(" ", "_").replace("\t", "_") for t in card.tags if t]
            
            # 处理填空题
            if card.card_type == "cloze":
                note = genanki.Note(
                    model=self.model,
                    fields=[
                        card.front,  # 填空文本
                        card.back,   # 完整文本
                        ", ".join(card.tags),
                        card.source
                    ],
                    tags=safe_tags
                )
            else:
                # 问答卡和概念卡
                note = genanki.Note(
                    model=self.model,
                    fields=[
                        card.front,
                        card.back,
                        ", ".join(card.tags),
                        card.source
                    ],
                    tags=safe_tags
                )
            
            self.deck.add_note(note)
    
    def export(self, output_path: str) -> str:
        """导出为.apkg文件"""
        genanki.Package(self.deck).write_to_file(output_path)
        return output_path
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "deck_name": self.deck_name,
            "card_count": len(self.deck.notes),
            "export_time": datetime.now().isoformat()
        }


class QuizletExporter:
    """Quizlet格式导出器"""
    
    @staticmethod
    def export(cards: List[AnkiCard], output_path: str) -> str:
        """导出为Quizlet兼容的CSV格式"""
        import csv
        
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Term", "Definition"])  # Quizlet格式
            
            for card in cards:
                writer.writerow([card.front, card.back])
        
        return output_path


class FlashcardsExporter:
    """Flashcards格式导出器"""
    
    @staticmethod
    def export(cards: List[AnkiCard], output_path: str) -> str:
        """导出为通用JSON格式"""
        import json
        
        data = [
            {
                "front": card.front,
                "back": card.back,
                "tags": card.tags
            }
            for card in cards
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return output_path


def export_cards(
    cards: List[AnkiCard],
    deck_name: str = "Anki学习卡片",
    output_format: str = "apkg",
    output_dir: str = "output"
) -> Dict[str, str]:
    """
    导出卡片
    
    Args:
        cards: 卡片列表
        deck_name: 牌组名称
        output_format: 输出格式 (apkg, quizlet, flashcards, all)
        output_dir: 输出目录
    
    Returns:
        导出文件路径字典
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}
    
    if output_format in ["apkg", "all"]:
        apkg_path = f"{output_dir}/{deck_name}_{timestamp}.apkg"
        exporter = AnkiExporter(deck_name)
        exporter.add_cards(cards)
        exporter.export(apkg_path)
        results["apkg"] = apkg_path
    
    if output_format in ["quizlet", "all"]:
        csv_path = f"{output_dir}/{deck_name}_{timestamp}_quizlet.csv"
        QuizletExporter.export(cards, csv_path)
        results["quizlet"] = csv_path
    
    if output_format in ["flashcards", "all"]:
        json_path = f"{output_dir}/{deck_name}_{timestamp}_flashcards.json"
        FlashcardsExporter.export(cards, json_path)
        results["flashcards"] = json_path
    
    return results


def main():
    """测试代码"""
    from .card_generator import AnkiCard
    
    # 测试卡片
    test_cards = [
        AnkiCard(
            front="什么是机器学习？",
            back="机器学习是人工智能的一个分支，它使计算机能够从数据中学习。",
            card_type="qa",
            tags=["AI", "第一章"],
            source="第10页"
        ),
        AnkiCard(
            front="深度学习",
            back="深度学习是机器学习的一个子集，使用神经网络模拟人脑。",
            card_type="concept",
            tags=["AI", "第二章"],
            source="第15页"
        ),
    ]
    
    # 导出测试
    results = export_cards(test_cards, deck_name="测试牌组", output_format="all")
    
    print("✅ 导出完成:")
    for format_type, path in results.items():
        print(f"  {format_type}: {path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不同类型的内容对卡片生成的影响
"""

from core.card_generator import AnkiCardGenerator

# 测试场景：不同类型的内容
test_cases = {
    "定义型": [
        "人工智能是指由人制造出来的机器所表现出来的智能。",
        "深度学习是机器学习的一个子领域，它使用多层神经网络。",
    ],
    "分类型": [
        "机器学习分为监督学习、无监督学习和强化学习三大类。",
        "激活函数包括ReLU、Sigmoid、Tanh、Softmax等。",
    ],
    "特点型": [
        "深度学习的特点是自动特征提取、端到端学习、大数据驱动。",
        "卷积神经网络的优势是局部连接和权重共享。",
    ],
    "作用型": [
        "池化层的作用是降低特征图的维度，减少计算量。",
        "损失函数用于衡量模型预测值与真实值之间的差距。",
    ],
    "原理型": [
        "反向传播算法通过链式法则计算梯度，更新网络参数。",
        "梯度下降是一种优化算法，通过迭代更新参数来最小化损失函数。",
    ],
    "复杂句": [
        "ResNet通过引入残差连接，解决了深层网络中的梯度消失问题，使得训练非常深的网络成为可能。",
        "注意力机制允许模型在处理序列数据时，动态地关注不同位置的信息。",
    ],
    "包含多个概念": [
        "卷积神经网络由卷积层、池化层和全连接层组成。",
        "自然语言处理包括文本分类、命名实体识别、机器翻译等任务。",
    ],
}

def run_tests():
    generator = AnkiCardGenerator()

    print("=" * 70)
    print("卡片生成器 - 场景测试")
    print("=" * 70)

    for category, texts in test_cases.items():
        print(f"\n📋 测试场景：{category}")
        print("-" * 70)

        for text in texts:
            cards = generator.generate_from_text(text, ["qa", "cloze", "concept"])

            # 统计
            qa_cards = [c for c in cards if c.card_type == "qa"]
            cloze_cards = [c for c in cards if c.card_type == "cloze"]
            concept_cards = [c for c in cards if c.card_type == "concept"]

            print(f"\n输入: {text}")
            print(f"  → QA: {len(qa_cards)}张, Cloze: {len(cloze_cards)}张, Concept: {len(concept_cards)}张")

            if cards:
                print(f"  → 最佳卡片: [{cards[0].card_type}] {cards[0].front[:40]}...")
            else:
                print(f"  → ⚠️ 未生成卡片")

    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

    # 生成统计报告
    print("\n📊 生成质量分析：")
    print("建议优化点：")
    print("1. 复杂句拆分：长句子应该拆分成多个知识点")
    print("2. 概念提取：更准确地识别核心概念")
    print("3. 填空位置：改进挖空位置的准确性")
    print("4. 问答生成：问题表述更自然")

if __name__ == "__main__":
    run_tests()

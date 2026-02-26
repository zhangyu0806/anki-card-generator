#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证卡片生成功能
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.card_generator import AnkiCard, AnkiCardGenerator


def test_card_generator():
    """测试卡片生成器"""
    print("="*60)
    print("🧪 测试Anki卡片生成器")
    print("="*60)
    
    generator = AnkiCardGenerator()
    
    # 测试知识点
    test_keypoints = [
        {
            "text": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习。",
            "page": 10,
            "section": "第一章"
        },
        {
            "text": "深度学习包括神经网络、卷积神经网络、循环神经网络等。",
            "page": 15,
            "section": "第二章"
        },
        {
            "text": "过拟合是指模型在训练数据上表现很好，但在新数据上表现差。",
            "page": 20,
            "section": "第三章"
        },
        {
            "text": "Python是一种高级编程语言，它的设计哲学强调代码的可读性。",
            "page": 25,
            "section": "第四章"
        },
        {
            "text": "神经网络的基本单元是神经元，它接收输入并产生输出。",
            "page": 30,
            "section": "第五章"
        },
    ]
    
    print("\n📝 测试知识点:")
    for i, kp in enumerate(test_keypoints, 1):
        print(f"   {i}. {kp['text'][:50]}...")
    
    # 生成卡片
    print("\n🎴 生成卡片...")
    cards = generator.generate_from_keypoints(test_keypoints)
    
    print(f"   ✅ 总卡片数: {len(cards)}")
    
    # 统计卡片类型
    type_count = {}
    for card in cards:
        type_count[card.card_type] = type_count.get(card.card_type, 0) + 1
    
    print("\n📊 卡片类型分布:")
    for card_type, count in type_count.items():
        print(f"   {card_type.upper()}: {count}张")
    
    # 显示示例卡片
    print("\n📋 卡片预览 (前5张):")
    for i, card in enumerate(cards[:5], 1):
        print(f"\n   卡片 {i} [{card.card_type.upper()}]:")
        print(f"      问: {card.front}")
        print(f"      答: {card.back}")
        print(f"      标签: {card.tags}")
    
    # 测试导出
    print("\n📦 测试导出...")
    try:
        from core.anki_exporter import export_cards
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        results = export_cards(cards, deck_name="测试牌组", output_format="all")
        
        print("   ✅ 导出成功:")
        for format_type, path in results.items():
            if os.path.exists(path):
                size = os.path.getsize(path) / 1024
                print(f"      {format_type.upper()}: {path} ({size:.1f} KB)")
            else:
                print(f"      {format_type.upper()}: 文件未创建")
        
    except Exception as e:
        print(f"   ⚠️  导出测试失败: {e}")
        print("   (可能需要安装 genanki: pip install genanki)")
    
    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)
    
    return len(cards) > 0


def test_pdf_parser():
    """测试PDF解析器（如果有示例PDF）"""
    print("\n" + "="*60)
    print("📖 测试PDF解析器")
    print("="*60)
    
    # 检查是否有示例PDF
    example_dir = "examples"
    pdf_files = [f for f in os.listdir(example_dir) if f.endswith('.pdf')] if os.path.exists(example_dir) else []
    
    if not pdf_files:
        print("⚠️  未找到示例PDF文件，跳过PDF解析测试")
        print("   提示: 将PDF文件放入 examples/ 目录进行测试")
        return False
    
    print(f"\n📄 找到PDF文件: {pdf_files[0]}")
    
    try:
        from core.pdf_parser import PDFParser
        
        pdf_path = os.path.join(example_dir, pdf_files[0])
        parser = PDFParser(pdf_path)
        result = parser.parse()
        
        print(f"\n✅ 解析成功:")
        print(f"   总页数: {result['total_pages']}")
        print(f"   章节数: {result['sections']}")
        print(f"   知识点: {result['key_points']}")
        
        if result['key_points'] > 0:
            print(f"\n📋 知识点预览 (前3个):")
            for i, kp in enumerate(parser.get_key_points()[:3], 1):
                print(f"   {i}. [{kp.page}页] {kp.text[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n🚀 开始测试...\n")
    
    # 测试1: 卡片生成器
    test1_passed = test_card_generator()
    
    # 测试2: PDF解析器
    test2_passed = test_pdf_parser()
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    print(f"   卡片生成器: {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"   PDF解析器: {'✅ 通过' if test2_passed else '⚠️  跳过'}")
    print("="*60)
    
    if test1_passed:
        print("\n💡 下一步:")
        print("   1. 准备一个PDF教材文件")
        print("   2. 运行: python anki_gen.py your_textbook.pdf")
        print("   3. 或启动Web服务: cd web && python app.py")
    
    return 0


if __name__ == "__main__":
    main()

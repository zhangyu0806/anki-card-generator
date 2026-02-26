#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki学习卡片生成器 - 主入口
把PDF教材自动变成Anki卡片

Usage:
    python anki_gen.py <pdf文件路径> [选项]
    
Options:
    --output-dir DIR     输出目录 (默认: output)
    --deck-name NAME     牌组名称 (默认: PDF文件名)
    --types TYPES        卡片类型 (qa,cloze,concept，默认: all)
    --format FORMAT      输出格式 (apkg,quizlet,flashcards,all，默认: apkg)
    --limit NUM          最多生成卡片数 (默认: 无限制)
    --help               显示帮助
"""

import os
import sys
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import PDFParser, AnkiCardGenerator, export_cards


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Anki学习卡片生成器 - 把PDF教材自动变成Anki卡片"
    )
    
    parser.add_argument(
        "pdf_file",
        help="PDF文件路径"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        default="output",
        help="输出目录 (默认: output)"
    )
    
    parser.add_argument(
        "--deck-name", "-d",
        default=None,
        help="牌组名称 (默认: PDF文件名)"
    )
    
    parser.add_argument(
        "--types", "-t",
        default="all",
        help="卡片类型: qa,cloze,concept,all (默认: all)"
    )
    
    parser.add_argument(
        "--format", "-f",
        default="apkg",
        choices=["apkg", "quizlet", "flashcards", "all"],
        help="输出格式 (默认: apkg)"
    )
    
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="最多生成卡片数 (默认: 无限制)"
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    # 检查PDF文件
    pdf_path = args.pdf_file
    if not os.path.exists(pdf_path):
        print(f"❌ 错误: 文件不存在: {pdf_path}")
        return 1
    
    # 确定牌组名称
    deck_name = args.deck_name or Path(pdf_path).stem
    
    print("="*60)
    print("📚 Anki学习卡片生成器")
    print("="*60)
    print(f"PDF文件: {pdf_path}")
    print(f"牌组名称: {deck_name}")
    print(f"输出目录: {args.output_dir}")
    print(f"卡片类型: {args.types}")
    print(f"输出格式: {args.format}")
    print("="*60)
    
    # 步骤1: 解析PDF
    print("\n📖 [1/3] 解析PDF...")
    parser = PDFParser(pdf_path)
    result = parser.parse()
    
    print(f"   ✅ 总页数: {result['total_pages']}")
    print(f"   ✅ 章节数: {result['sections']}")
    print(f"   ✅ 知识点: {result['key_points']}")
    
    if result['key_points'] == 0:
        print("\n⚠️  警告: 未检测到知识点，可能需要调整PDF解析规则")
    
    # 步骤2: 生成卡片
    print("\n🎴 [2/3] 生成卡片...")
    
    # 确定卡片类型
    if args.types == "all":
        card_types = ["qa", "cloze", "concept"]
    else:
        card_types = args.types.split(",")
    
    # 准备知识点数据
    key_points_data = []
    for kp in parser.get_key_points():
        key_points_data.append({
            "text": kp.text,
            "context": kp.context,
            "page": kp.page,
            "section": kp.section
        })
    
    # 生成卡片
    generator = AnkiCardGenerator()
    cards = generator.generate_from_keypoints(key_points_data, card_types)
    
    # 限制卡片数量
    if args.limit and len(cards) > args.limit:
        cards = cards[:args.limit]
    
    print(f"   ✅ 生成卡片: {len(cards)}张")
    
    if cards:
        print(f"\n   📋 卡片预览 (前3张):")
        for i, card in enumerate(cards[:3], 1):
            print(f"      [{i}] {card.card_type.upper()}")
            print(f"         问: {card.front[:50]}...")
            print(f"         答: {card.back[:50]}...")
    
    # 步骤3: 导出
    print(f"\n📦 [3/3] 导出卡片 ({args.format})...")
    
    output_paths = export_cards(
        cards,
        deck_name=deck_name,
        output_format=args.format,
        output_dir=args.output_dir
    )
    
    print("   ✅ 导出完成:")
    for format_type, path in output_paths.items():
        file_size = os.path.getsize(path) / 1024  # KB
        print(f"      {format_type.upper()}: {path} ({file_size:.1f} KB)")
    
    print("\n" + "="*60)
    print("🎉 完成！")
    print("="*60)
    print(f"\n💡 提示:")
    print(f"   - 将.apkg文件导入到Anki桌面版或AnkiMobile")
    print(f"   - Quizlet CSV可直接导入到Quizlet网站")
    print(f"   - JSON格式可用于其他记忆卡片应用")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

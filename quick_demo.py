#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki学习卡片生成器 - 快速演示脚本
展示完整功能：PDF解析 → 卡片生成 → 导出
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import PDFParser, AnkiCardGenerator, export_cards


def print_section(title):
    """打印分隔符"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_complete_workflow():
    """完整工作流演示"""
    print_section("Anki学习卡片生成器 - 完整演示")

    # 检查示例PDF
    demo_pdf = "examples/demo_ai_textbook.pdf"
    if not os.path.exists(demo_pdf):
        print(f"❌ 示例PDF不存在: {demo_pdf}")
        print("请先运行: python create_demo_pdf.py")
        return False

    print(f"\n📚 演示PDF: {demo_pdf}")
    print(f"   文件大小: {os.path.getsize(demo_pdf) / 1024:.1f} KB")

    # 步骤1: 解析PDF
    print_section("步骤 1/3: 解析PDF")

    parser = PDFParser(demo_pdf)
    result = parser.parse()

    print(f"\n✅ 解析完成:")
    print(f"   - 总页数: {result['total_pages']}")
    print(f"   - 章节数: {result['sections']}")
    print(f"   - 知识点: {result['key_points']}")

    # 显示章节结构
    if parser.sections:
        print(f"\n📑 章节结构:")
        for section in parser.sections[:5]:
            indent = "  " * (section.level - 1)
            print(f"   {indent}{'▶' if section.level == 1 else '•'} {section.title}")

    # 步骤2: 生成卡片
    print_section("步骤 2/3: 生成卡片")

    # 准备知识点数据
    key_points_data = []
    for kp in parser.get_key_points():
        key_points_data.append({
            "text": kp.text,
            "context": kp.context,
            "page": kp.page,
            "section": kp.section
        })

    # 生成多种类型的卡片
    card_types = ["qa", "cloze", "concept"]
    generator = AnkiCardGenerator()
    cards = generator.generate_from_keypoints(key_points_data, card_types)

    print(f"\n✅ 生成卡片: {len(cards)}张")

    # 按类型统计
    type_count = {}
    for card in cards:
        type_count[card.card_type] = type_count.get(card.card_type, 0) + 1

    print(f"\n📊 卡片类型分布:")
    for card_type, count in type_count.items():
        print(f"   - {card_type.upper()}: {count}张")

    # 显示卡片预览
    print(f"\n🎴 卡片预览 (前5张):")
    for i, card in enumerate(cards[:5], 1):
        print(f"\n   [{i}] {card.card_type.upper()} - {card.tags[0] if card.tags else '未分类'}")
        print(f"       问: {card.front[:60]}...")
        print(f"       答: {card.back[:60]}...")

    # 步骤3: 导出
    print_section("步骤 3/3: 导出卡片")

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 导出所有格式
    print("\n📦 正在导出...")

    output_paths = export_cards(
        cards,
        deck_name="AI导论演示",
        output_format="all",  # 导出所有格式
        output_dir=output_dir
    )

    print(f"\n✅ 导出完成:")
    for format_type, path in output_paths.items():
        file_size = os.path.getsize(path) / 1024  # KB
        print(f"   - {format_type.upper()}: {path} ({file_size:.1f} KB)")

    # 总结
    print_section("演示完成！")

    print(f"\n📈 处理统计:")
    print(f"   输入: {demo_pdf}")
    print(f"   输出: {len(output_paths)} 个文件")
    print(f"   卡片: {len(cards)}张")

    print(f"\n💡 下一步:")
    print(f"   1. 将 .apkg 文件导入到 Anki")
    print(f"   2. 将 .csv 文件导入到 Quizlet")
    print(f"   3. 查看源码了解实现细节")

    return True


def demo_cli_usage():
    """CLI使用演示"""
    print_section("CLI 使用方法")

    print("\n基本用法:")
    print("  python anki_gen.py <PDF文件>")
    print("\n高级选项:")
    print("  --output-dir DIR     输出目录 (默认: output)")
    print("  --deck-name NAME     牌组名称 (默认: PDF文件名)")
    print("  --types TYPES        卡片类型 (qa,cloze,concept,all)")
    print("  --format FORMAT      输出格式 (apkg,quizlet,flashcards,all)")
    print("  --limit NUM          最多生成卡片数")

    print("\n示例:")
    print("  python anki_gen.py examples/demo_ai_textbook.pdf")
    print("  python anki_gen.py book.pdf --types qa,cloze --format all")
    print("  python anki_gen.py book.pdf --deck-name \"我的牌组\" --limit 50")


def demo_web_usage():
    """Web界面使用演示"""
    print_section("Web 界面使用方法")

    print("\n启动Web服务:")
    print("  bash start_web.sh")
    print("  或")
    print("  streamlit run web/app.py")

    print("\n然后访问:")
    print("  http://localhost:5001")

    print("\n功能:")
    print("  1. 上传PDF文件")
    print("  2. 选择卡片类型")
    print("  3. 选择输出格式")
    print("  4. 点击生成")
    print("  5. 下载生成的文件")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Anki学习卡片生成器 - 快速演示")
    parser.add_argument(
        "--web",
        action="store_true",
        help="显示Web界面使用说明"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="显示CLI使用说明"
    )

    args = parser.parse_args()

    if args.web:
        demo_web_usage()
    elif args.cli:
        demo_cli_usage()
    else:
        # 运行完整演示
        success = demo_complete_workflow()

        if success:
            print("\n" + "="*60)
            print("✅ 演示成功！现在可以使用自己的PDF了")
            print("="*60)
            return 0
        else:
            print("\n❌ 演示失败，请检查错误信息")
            return 1


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

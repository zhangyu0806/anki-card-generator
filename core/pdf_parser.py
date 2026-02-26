#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF解析器 - 从PDF中提取文本内容
支持多种PDF格式，保留文本结构
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
import pdfplumber


@dataclass
class Section:
    """章节结构"""
    title: str
    level: int  # 1=章, 2=节, 3=小节
    content: str
    page_start: int
    page_end: int


@dataclass
class KeyPoint:
    """知识点"""
    text: str
    context: str
    page: int
    section: str


class PDFParser:
    """PDF解析器"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.sections: List[Section] = []
        self.key_points: List[KeyPoint] = []
        
    def parse(self) -> Dict:
        """解析PDF，提取结构化内容"""
        print(f"📖 开始解析PDF: {self.pdf_path}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"   总页数: {total_pages}")
            
            # 提取所有文本
            all_text = ""
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                all_text += f"\n--- 第{i}页 ---\n{text}"
            
            # 识别章节结构
            self._extract_sections(pdf)
            
            # 提取知识点
            self._extract_key_points(pdf)
            
            return {
                "total_pages": total_pages,
                "sections": len(self.sections),
                "key_points": len(self.key_points),
                "full_text": all_text[:2000] + "..." if len(all_text) > 2000 else all_text
            }
    
    def _extract_sections(self, pdf) -> None:
        """提取章节结构"""
        self.sections = []
        
        chapter_pattern = re.compile(r'^第[一二三四五六七八九十\d]+[章讲课]|^Chapter\s+\d+|^[\d]+\s+', re.MULTILINE)
        section_pattern = re.compile(r'^[\d]+\.[\d]+\s+|^[\u4e00-\u9fa5]+、', re.MULTILINE)
        
        current_chapter = None
        current_section = None
        
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 检测章标题
                if chapter_pattern.match(line):
                    if current_chapter:
                        current_chapter.page_end = i - 1
                    current_chapter = Section(
                        title=line,
                        level=1,
                        content="",
                        page_start=i,
                        page_end=i
                    )
                    self.sections.append(current_chapter)
                    current_section = None
                
                # 检测节标题
                elif section_pattern.match(line) and current_chapter:
                    if current_section:
                        current_section.page_end = i - 1
                    current_section = Section(
                        title=line,
                        level=2,
                        content="",
                        page_start=i,
                        page_end=i
                    )
                    self.sections.append(current_section)
    
    def _extract_key_points(self, pdf) -> None:
        """提取知识点（基于规则）"""
        self.key_points = []
        
        # 关键词模式
        patterns = [
            r'定义：(.+?)(?:\n|$)',
            r'所谓(.{5,30}?)是指',
            r'(.{5,30}?)的特点是',
            r'(.{5,30}?)包括',
            r'重要：(.+?)(?:\n|$)',
            r'注意：(.+?)(?:\n|$)',
            r'(.{5,30}?)分为',
            r'(.{5,30}?)是指',
        ]
        
        combined_pattern = re.compile('|'.join(patterns))
        
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            
            # 查找匹配的知识点
            matches = combined_pattern.finditer(text)
            for match in matches:
                point_text = match.group(0).strip()
                if len(point_text) > 5 and len(point_text) < 100:
                    # 找到所属章节
                    section_name = self._find_section_for_page(i)
                    
                    self.key_points.append(KeyPoint(
                        text=point_text,
                        context=text[max(0, match.start()-50):match.end()+50],
                        page=i,
                        section=section_name
                    ))
        
        # 如果基于规则提取的知识点太少，使用句子级提取作为补充
        if len(self.key_points) < 5:
            self._extract_key_sentences(pdf)
        
        # 去重
        seen = set()
        unique_points = []
        for point in self.key_points:
            if point.text not in seen:
                seen.add(point.text)
                unique_points.append(point)
        
        self.key_points = unique_points
    
    def _extract_key_sentences(self, pdf) -> None:
        """基于句子的知识点提取（当规则匹配不足时的补充方案）"""
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            # 按句号、分号、换行分割
            sentences = re.split(r'[。；\n]', text)
            section_name = self._find_section_for_page(i)
            
            for sent in sentences:
                sent = sent.strip()
                # 过滤太短或太长的句子
                if len(sent) < 15 or len(sent) > 200:
                    continue
                # 过滤纯数字、页码等噪音
                if re.match(r'^[\d\s\-—]+$', sent):
                    continue
                # 保留包含关键信息的句子
                if any(kw in sent for kw in [
                    '是', '为', '指', '即', '称为', '叫做',
                    '包括', '分为', '特点', '原则', '方法',
                    '步骤', '条件', '因素', '作用', '功能',
                    '优点', '缺点', '区别', '联系', '意义',
                    '概念', '定义', '理论', '规律', '公式',
                ]):
                    self.key_points.append(KeyPoint(
                        text=sent,
                        context=sent,
                        page=i,
                        section=section_name
                    ))
    
    def _find_section_for_page(self, page_num: int) -> str:
        """找到页面对应的章节"""
        for section in self.sections:
            if section.page_start <= page_num <= section.page_end:
                return section.title
        return "未知章节"
    
    def get_sections(self) -> List[Section]:
        """获取所有章节"""
        return self.sections
    
    def get_key_points(self) -> List[KeyPoint]:
        """获取所有知识点"""
        return self.key_points
    
    def get_text_by_pages(self, start: int, end: int) -> str:
        """获取指定页范围的文本"""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for i in range(start-1, min(end, len(pdf.pages))):
                page_text = pdf.pages[i].extract_text() or ""
                text += page_text + "\n"
        return text


def main():
    """测试代码"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python pdf_parser.py <pdf文件路径>")
        return
    
    pdf_path = sys.argv[1]
    parser = PDFParser(pdf_path)
    
    result = parser.parse()
    
    print("\n" + "="*50)
    print("📊 解析结果:")
    print("="*50)
    print(f"总页数: {result['total_pages']}")
    print(f"章节数: {result['sections']}")
    print(f"知识点: {result['key_points']}")
    
    print("\n📚 章节列表:")
    for section in parser.sections[:10]:
        print(f"  {section.title} (第{section.page_start}-{section.page_end}页)")
    
    print(f"\n🎯 知识点预览 (前10个):")
    for point in parser.key_points[:10]:
        print(f"  [{point.page}页] {point.text[:60]}...")


if __name__ == "__main__":
    main()

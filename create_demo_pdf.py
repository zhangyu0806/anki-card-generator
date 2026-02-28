#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成演示用PDF教材 - 人工智能导论（模拟50页教材）"""

from fpdf import FPDF
import os


class DemoPDF(FPDF):
    def header(self):
        self.set_font('', 'B', 10)
        self.cell(0, 8, '人工智能导论（演示版）', 0, 1, 'C')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('', '', 8)
        self.cell(0, 10, f'第 {self.page_no()} 页', 0, 0, 'C')


def create_demo_pdf(output_path="examples/demo_ai_textbook.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = DemoPDF()
    # 使用内置字体支持中文 - fpdf2 支持 unifont
    font_path = None
    # 尝试找系统中文字体
    for fp in [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]:
        if os.path.exists(fp):
            font_path = fp
            break

    if font_path:
        pdf.add_font("zh", "", font_path, uni=True)
        pdf.add_font("zh", "B", font_path, uni=True)
        pdf.set_font("zh", size=12)
    else:
        # 没有中文字体，用英文内容
        print("⚠️ 未找到中文字体，将生成英文版演示PDF")
        pdf.set_font("Helvetica", size=12)

    has_chinese = font_path is not None

    if has_chinese:
        _create_chinese_content(pdf)
    else:
        _create_english_content(pdf)

    pdf.output(output_path)
    file_size = os.path.getsize(output_path) / 1024
    print(f"✅ 演示PDF已生成: {output_path} ({file_size:.1f} KB, {pdf.page_no()}页)")
    return output_path


def _create_chinese_content(pdf):
    """生成中文教材内容"""
    chapters = [
        {
            "title": "第一章 人工智能概述",
            "sections": [
                ("1.1 人工智能的定义", [
                    "人工智能是指由人工制造出来的系统所表现出来的智能。",
                    "人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。",
                    "人工智能的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。",
                    "人工智能的定义：人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
                    "强人工智能是指具有与人类同等智慧或超越人类的人工智能。",
                    "弱人工智能是指不能制造出真正地推理和解决问题的智能机器。",
                ]),
                ("1.2 人工智能的发展历史", [
                    "人工智能的发展分为三个阶段：萌芽期、发展期和爆发期。",
                    "1956年达特茅斯会议标志着人工智能学科的正式诞生。",
                    "人工智能的发展经历了两次低谷，分别称为AI寒冬。",
                    "深度学习的突破是指2012年AlexNet在ImageNet竞赛中取得突破性成绩。",
                    "人工智能的三大要素包括数据、算法和算力。",
                    "图灵测试是指如果一台机器能够与人类展开对话而不能被辨别出其机器身份，那么称这台机器具有智能。",
                ]),
                ("1.3 人工智能的应用领域", [
                    "人工智能的应用领域包括自然语言处理、计算机视觉、语音识别、推荐系统和自动驾驶等。",
                    "自然语言处理是指让计算机理解和生成人类语言的技术。",
                    "计算机视觉是指让计算机从图像或视频中获取信息的技术。",
                    "推荐系统的特点是能够根据用户的历史行为和偏好，自动推荐相关内容。",
                    "自动驾驶分为L0到L5六个等级，其中L5为完全自动驾驶。",
                ]),
            ]
        },
        {
            "title": "第二章 机器学习基础",
            "sections": [
                ("2.1 机器学习的概念", [
                    "机器学习是指计算机程序能够从经验中学习，并改善其在某些任务上的性能。",
                    "机器学习是人工智能的核心方法，它使计算机能够从数据中自动学习规律。",
                    "监督学习是指从标注数据中学习一个映射函数的机器学习方法。",
                    "无监督学习是指从无标注数据中发现隐藏结构的机器学习方法。",
                    "强化学习是指智能体通过与环境交互来学习最优策略的方法。",
                    "机器学习的基本流程包括数据收集、数据预处理、特征工程、模型训练、模型评估和模型部署。",
                ]),
                ("2.2 监督学习算法", [
                    "线性回归是指用一条直线来拟合数据点的监督学习算法。",
                    "逻辑回归是指用于二分类问题的监督学习算法，输出概率值。",
                    "决策树是指通过树形结构进行决策的分类和回归算法。",
                    "决策树的优点是易于理解和解释，缺点是容易过拟合。",
                    "随机森林包括多棵决策树，通过集成学习提高预测准确率。",
                    "支持向量机是指在特征空间中寻找最优超平面的分类算法。",
                    "K近邻算法的特点是简单直观，不需要训练过程，但计算量大。",
                ]),
                ("2.3 模型评估", [
                    "过拟合是指模型在训练数据上表现很好，但在新数据上表现差的现象。",
                    "欠拟合是指模型在训练数据和新数据上都表现不好的现象。",
                    "交叉验证是指将数据集分成K份，轮流用其中一份做验证集的评估方法。",
                    "准确率是指分类正确的样本数占总样本数的比例。",
                    "精确率是指预测为正类的样本中实际为正类的比例。",
                    "召回率是指实际为正类的样本中被正确预测为正类的比例。",
                    "F1分数是精确率和召回率的调和平均值。",
                    "正则化的作用是防止模型过拟合，提高模型的泛化能力。",
                ]),
            ]
        },
        {
            "title": "第三章 深度学习",
            "sections": [
                ("3.1 神经网络基础", [
                    "神经网络是指模拟人脑神经元连接方式的计算模型。",
                    "感知机是最简单的神经网络，由输入层和输出层组成。",
                    "激活函数的作用是引入非线性，使神经网络能够学习复杂的模式。",
                    "常用的激活函数包括Sigmoid、ReLU、Tanh和Softmax。",
                    "反向传播算法是指通过计算损失函数的梯度来更新网络权重的算法。",
                    "梯度下降是指沿着损失函数梯度的反方向更新参数的优化方法。",
                    "学习率是指每次参数更新的步长大小，过大会导致震荡，过小会导致收敛慢。",
                ]),
                ("3.2 卷积神经网络", [
                    "卷积神经网络是指专门用于处理网格状数据（如图像）的深度学习模型。",
                    "卷积层的作用是提取输入数据的局部特征。",
                    "池化层的作用是降低特征图的空间维度，减少计算量。",
                    "卷积神经网络的典型结构包括卷积层、池化层和全连接层。",
                    "AlexNet是2012年ImageNet竞赛冠军，标志着深度学习时代的开始。",
                    "ResNet的特点是引入了残差连接，解决了深层网络的梯度消失问题。",
                    "VGG网络的特点是使用小卷积核（3x3）堆叠来增加网络深度。",
                ]),
                ("3.3 循环神经网络", [
                    "循环神经网络是指能够处理序列数据的神经网络。",
                    "LSTM是指长短期记忆网络，它通过门控机制解决了长期依赖问题。",
                    "GRU是指门控循环单元，是LSTM的简化版本。",
                    "注意力机制的作用是让模型能够关注输入序列中最重要的部分。",
                    "Transformer是指完全基于注意力机制的序列到序列模型。",
                    "BERT是指基于Transformer的双向编码器表示模型，用于自然语言理解。",
                    "GPT是指基于Transformer的生成式预训练模型，用于文本生成。",
                ]),
            ]
        },
        {
            "title": "第四章 自然语言处理",
            "sections": [
                ("4.1 文本预处理", [
                    "分词是指将连续的文本切分成有意义的词语序列。",
                    "中文分词的方法包括基于词典的方法、基于统计的方法和基于深度学习的方法。",
                    "停用词是指在文本处理中需要过滤掉的高频但无实际意义的词语。",
                    "词向量是指将词语映射到低维连续向量空间的表示方法。",
                    "Word2Vec包括CBOW和Skip-gram两种模型架构。",
                    "TF-IDF是指词频-逆文档频率，用于衡量词语在文档中的重要程度。",
                ]),
                ("4.2 文本分类与情感分析", [
                    "文本分类是指将文本自动归入预定义类别的任务。",
                    "情感分析是指识别和提取文本中主观信息的技术。",
                    "朴素贝叶斯分类器的特点是基于贝叶斯定理和特征独立性假设。",
                    "文本分类的应用包括垃圾邮件过滤、新闻分类和情感分析等。",
                    "预训练语言模型的优点是能够利用大量无标注文本学习通用的语言表示。",
                ]),
                ("4.3 机器翻译", [
                    "机器翻译是指利用计算机将一种自然语言翻译成另一种自然语言的技术。",
                    "统计机器翻译是指基于统计模型的机器翻译方法。",
                    "神经机器翻译是指基于神经网络的端到端机器翻译方法。",
                    "注意力机制在机器翻译中的作用是让解码器能够关注源语言中最相关的部分。",
                    "BLEU分数是指用于评估机器翻译质量的自动评价指标。",
                ]),
            ]
        },
        {
            "title": "第五章 计算机视觉",
            "sections": [
                ("5.1 图像处理基础", [
                    "图像是指由像素组成的二维数据矩阵。",
                    "图像处理的基本操作包括滤波、边缘检测、形态学操作和图像增强。",
                    "卷积操作是指用卷积核在图像上滑动并计算加权和的操作。",
                    "边缘检测的作用是找到图像中亮度变化剧烈的区域。",
                    "图像增强的方法包括直方图均衡化、对比度拉伸和锐化等。",
                ]),
                ("5.2 目标检测", [
                    "目标检测是指在图像中定位和识别特定目标的任务。",
                    "YOLO是指You Only Look Once，一种实时目标检测算法。",
                    "YOLO的特点是将目标检测转化为回归问题，实现端到端的检测。",
                    "目标检测的评价指标包括mAP、IoU和FPS等。",
                    "Faster R-CNN包括区域提议网络和Fast R-CNN两个部分。",
                    "目标检测的应用包括自动驾驶、安防监控和医学影像分析等。",
                ]),
                ("5.3 图像生成", [
                    "生成对抗网络是指由生成器和判别器组成的对抗训练框架。",
                    "GAN的训练过程是生成器和判别器相互博弈的过程。",
                    "扩散模型是指通过逐步去噪来生成图像的生成模型。",
                    "图像风格迁移是指将一张图像的风格应用到另一张图像上的技术。",
                    "图像超分辨率是指将低分辨率图像恢复为高分辨率图像的技术。",
                ]),
            ]
        },
    ]

    # 封面
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("zh", "B", 28)
    pdf.cell(0, 20, "人工智能导论", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("zh", "", 16)
    pdf.cell(0, 12, "（演示版教材）", 0, 1, "C")
    pdf.ln(20)
    pdf.set_font("zh", "", 12)
    pdf.cell(0, 10, "适用于：考研 / 考证 / 自学", 0, 1, "C")
    pdf.cell(0, 10, "Anki Card Generator 演示用", 0, 1, "C")
    pdf.ln(30)
    pdf.cell(0, 10, "2026年版", 0, 1, "C")

    # 目录
    pdf.add_page()
    pdf.set_font("zh", "B", 20)
    pdf.cell(0, 15, "目录", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("zh", "", 12)
    for ch in chapters:
        pdf.cell(0, 8, ch["title"], 0, 1)
        for sec_title, _ in ch["sections"]:
            pdf.cell(10)
            pdf.cell(0, 7, sec_title, 0, 1)
        pdf.ln(3)

    # 正文
    for ch in chapters:
        pdf.add_page()
        pdf.set_font("zh", "B", 22)
        pdf.cell(0, 15, ch["title"], 0, 1)
        pdf.ln(5)

        for sec_title, paragraphs in ch["sections"]:
            pdf.set_font("zh", "B", 14)
            pdf.cell(0, 10, sec_title, 0, 1)
            pdf.ln(3)
            pdf.set_font("zh", "", 11)
            for para in paragraphs:
                pdf.multi_cell(0, 7, para)
                pdf.ln(2)
            pdf.ln(5)

            # 如果页面快满了，换页
            if pdf.get_y() > 250:
                pdf.add_page()

    # 总结页
    pdf.add_page()
    pdf.set_font("zh", "B", 20)
    pdf.cell(0, 15, "总结", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("zh", "", 12)
    summary_points = [
        "人工智能是当今最重要的技术领域之一。",
        "机器学习是人工智能的核心方法。",
        "深度学习推动了人工智能的快速发展。",
        "自然语言处理和计算机视觉是AI的两大应用方向。",
        "掌握这些基础知识对于理解和应用AI至关重要。",
    ]
    for p in summary_points:
        pdf.cell(0, 8, f"• {p}", 0, 1)
        pdf.ln(2)


def _create_english_content(pdf):
    """Fallback: English content if no Chinese font available"""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, "Introduction to Artificial Intelligence", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)

    content = [
        ("Chapter 1: AI Overview", [
            "Artificial Intelligence is a branch of computer science that aims to create intelligent machines.",
            "AI includes machine learning, natural language processing, computer vision, and robotics.",
            "The Turing Test is a measure of machine intelligence proposed by Alan Turing in 1950.",
            "Strong AI refers to machines with consciousness and general intelligence.",
            "Weak AI refers to systems designed for specific tasks without general intelligence.",
        ]),
        ("Chapter 2: Machine Learning", [
            "Machine learning is a subset of AI that enables computers to learn from data.",
            "Supervised learning uses labeled data to train models for prediction.",
            "Unsupervised learning discovers hidden patterns in unlabeled data.",
            "Reinforcement learning trains agents through interaction with an environment.",
            "Overfitting occurs when a model performs well on training data but poorly on new data.",
            "Cross-validation divides data into K folds for robust model evaluation.",
        ]),
        ("Chapter 3: Deep Learning", [
            "Neural networks are computing systems inspired by biological neural networks.",
            "Convolutional Neural Networks (CNNs) are specialized for processing grid-like data such as images.",
            "Recurrent Neural Networks (RNNs) are designed for sequential data processing.",
            "The Transformer architecture relies entirely on attention mechanisms.",
            "BERT is a bidirectional encoder model for natural language understanding.",
            "GPT is a generative pre-trained model for text generation.",
        ]),
    ]

    for title, paragraphs in content:
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, title, 0, 1)
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 11)
        for para in paragraphs:
            pdf.multi_cell(0, 7, para)
            pdf.ln(2)
        pdf.ln(5)
        if pdf.get_y() > 250:
            pdf.add_page()


if __name__ == "__main__":
    create_demo_pdf()

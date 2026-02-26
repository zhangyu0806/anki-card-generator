#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki学习卡片生成器 - Web界面
上传PDF → 下载.apkg文件
"""

import os
import sys
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import PDFParser, AnkiCardGenerator, export_cards

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB最大上传
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['SECRET_KEY'] = 'anki-card-generator-2026'

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """检查文件类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """上传并处理PDF"""
    try:
        # 检查文件
        if 'file' not in request.files:
            return jsonify({'error': '请选择PDF文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '请选择PDF文件'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '只支持PDF格式'}), 400
        
        # 获取参数
        deck_name = request.form.get('deck_name', '学习卡片')
        card_types = request.form.get('card_types', 'qa,cloze,concept')
        output_format = request.form.get('format', 'apkg')
        card_limit = int(request.form.get('card_limit', 0)) or None
        
        # 保存上传的文件
        file_id = str(uuid.uuid4())[:8]
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        file.save(upload_path)
        
        # 解析PDF
        parser = PDFParser(upload_path)
        parse_result = parser.parse()
        
        # 生成卡片
        card_types_list = card_types.split(',') if card_types else ['qa']
        key_points_data = [
            {
                "text": kp.text,
                "context": kp.context,
                "page": kp.page,
                "section": kp.section
            }
            for kp in parser.get_key_points()
        ]
        
        generator = AnkiCardGenerator()
        cards = generator.generate_from_keypoints(key_points_data, card_types_list)
        
        if card_limit and len(cards) > card_limit:
            cards = cards[:card_limit]
        
        # 导出（使用file_id防止文件名冲突）
        output_paths = export_cards(
            cards,
            deck_name=f"{deck_name}_{file_id}",
            output_format=output_format,
            output_dir=app.config['OUTPUT_FOLDER']
        )
        
        # 删除上传的文件
        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(upload_path):
                    os.remove(upload_path)
            except:
                pass
            return response
        
        # 返回结果
        return jsonify({
            'success': True,
            'stats': {
                'total_pages': parse_result['total_pages'],
                'sections': parse_result['sections'],
                'key_points': parse_result['key_points'],
                'cards_generated': len(cards)
            },
            'files': {
                k: os.path.basename(v) for k, v in output_paths.items()
            },
            'download_urls': {
                k: f"/download/{os.path.basename(v)}"
                for k, v in output_paths.items()
            },
            'preview': [
                {
                    'front': c.front[:100],
                    'back': c.back[:100],
                    'type': c.card_type
                }
                for c in cards[:5]
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download(filename):
    """下载生成的文件"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename
            )
        return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    print("="*60)
    print("🌐 Anki学习卡片生成器 - Web服务")
    print("="*60)
    print(f"启动服务: http://0.0.0.0:5000")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

# 公网部署方案

## 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| HF Space | 免费、GPU可选、简单 | 冷启动慢、国内访问可能慢 | ⭐⭐⭐⭐ |
| UShudi VPS | 快速、稳定、国内快 | 需要维护 | ⭐⭐⭐⭐⭐ |
| 阿里云VPS | 国内访问快 | 需要额外费用 | ⭐⭐⭐ |

## 部署方案A：UShudi VPS（推荐）

### 优点
- 已有服务器，无额外成本
- 国内访问快
- 可以后台持续运行

### 步骤

1. **上传代码到VPS**
```bash
# 在VPS上
cd /root
git clone https://github.com/zhangyu0806/anki-card-generator.git
cd anki-card-generator
```

2. **安装Python依赖**
```bash
apt update
apt install -y python3-pip python3-venv

cd /root/anki-card-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **配置systemd服务**
```bash
cat > /etc/systemd/system/anki-web.service << 'EOF'
[Unit]
Description=Anki Card Generator Web Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/anki-card-generator
Environment="PATH=/root/anki-card-generator/venv/bin"
ExecStart=/root/anki-card-generator/venv/bin/python web/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable anki-web
systemctl start anki-web
```

4. **配置Nginx反向代理**
```bash
apt install -y nginx

cat > /etc/nginx/sites-available/anki-card-generator << 'EOF'
server {
    listen 80;
    server_name 38.55.133.19;  # 你的VPS IP

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
EOF

ln -s /etc/nginx/sites-available/anki-card-generator /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

5. **访问**
```
http://38.55.133.19
```

---

## 部署方案B：Hugging Face Space

### 优点
- 免费
- 自动部署
- 可选GPU

### 步骤

1. **创建Space**
- 访问 https://huggingface.co/spaces
- 点击 "Create new Space"
- Name: anki-card-generator
- License: MIT
- SDK: Gradio (或Streamlit)

2. **修改代码适配Gradio**

需要创建 `app.py` 适配Gradio接口：

```python
import gradio as gr
from core import PDFParser, AnkiCardGenerator, export_cards
import os

def generate_cards(pdf_file, deck_name="学习卡片", card_types="qa,cloze,concept"):
    """生成Anki卡片"""
    if pdf_file is None:
        return "请上传PDF文件", None
    
    try:
        # 保存上传的文件
        temp_path = f"/tmp/{os.path.basename(pdf_file.name)}"
        import shutil
        shutil.copy(pdf_file.name, temp_path)
        
        # 解析PDF
        parser = PDFParser(temp_path)
        parse_result = parser.parse()
        
        # 生成卡片
        card_types_list = card_types.split(',')
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
        
        # 导出
        output_paths = export_cards(
            cards,
            deck_name=deck_name,
            output_format="apkg",
            output_dir="/tmp"
        )
        
        apkg_path = output_paths.get("apkg")
        
        stats = f"""
✅ 生成成功！
📄 页数: {parse_result['total_pages']}
🔑 知识点: {parse_result['key_points']}
🃏 卡片数: {len(cards)}
"""
        return stats, apkg_path
        
    except Exception as e:
        return f"❌ 错误: {str(e)}", None

# Gradio界面
with gr.Blocks(title="Anki学习卡片生成器") as app:
    gr.Markdown("# 📚 Anki学习卡片生成器")
    gr.Markdown("上传PDF，一键生成Anki记忆卡片")
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="上传PDF", file_types=[".pdf"])
            deck_name = gr.Textbox(label="卡组名称", value="学习卡片")
            card_types = gr.CheckboxGroup(
                choices=["qa", "cloze", "concept"],
                value=["qa", "cloze", "concept"],
                label="卡片类型"
            )
            submit_btn = gr.Button("🚀 生成卡片", variant="primary")
        
        with gr.Column():
            output_text = gr.Textbox(label="生成结果")
            download_file = gr.File(label="下载.apkg")
    
    submit_btn.click(
        generate_cards,
        inputs=[pdf_input, deck_name, gr.Textbox(value="qa,cloze,concept", visible=False)],
        outputs=[output_text, download_file]
    )

if __name__ == "__main__":
    app.launch()
```

3. **创建README.md**

```markdown
---
title: Anki Card Generator
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# Anki学习卡片生成器

上传PDF，一键生成Anki记忆卡片
```

4. **requirements.txt**

```txt
gradio>=4.0.0
pypdfium2
genanki
```

5. **部署**
- 将代码推送到GitHub仓库
- 在Space中关联GitHub仓库
- 自动部署

---

## 部署方案C：本地测试

### 启动Web服务

```bash
cd /root/.openclaw/workspace/anki-card-generator
source venv/bin/activate
python web/app.py
```

### 访问
```
http://localhost:5000
```

---

## 推荐执行顺序

1. **先本地测试**（5分钟）
   - 确认Web功能正常

2. **部署到UShudi VPS**（15分钟）
   - 这是主方案，快速稳定

3. **可选：部署HF Space**（30分钟）
   - 作为备用和展示

---

## 定价策略

### 测试期（现在 - 3月15日）
- **完全免费**
- 收集用户反馈
- 目标：10个测试用户

### 正式上线（3月16日起）
- **按课付费：** 19.9-49.9元/课
  - 基础版：19.9元（单次使用，限500页）
  - 专业版：29.9元（单次使用，限1000页）
  - 终身版：49.9元（无限次使用）

- **订阅制：** 19.9元/月
  - 每月无限使用
  - 优先更新功能
  - 专属客服

- **早鸟优惠：** 前100名用户，终身半价
  - 基础版：9.9元
  - 专业版：14.9元
  - 终身版：24.9元

---

## 推广计划

### Week 1: 种子用户（目标10人）
- 小红书发帖
- B站发视频
- 考研群/考证群分享

### Week 2-3: 用户增长（目标50人）
- 技术社区发布（掘金/知乎/V2EX）
- 朋友圈传播
- 用户推荐奖励

### Week 4: 付费转化
- 推出付费版
- 限时优惠
- 案例展示

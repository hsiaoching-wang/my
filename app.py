from flask import Flask, request, jsonify, send_file
import os
import requests
import uuid
from werkzeug.utils import secure_filename
import threading

from prompt import apply_modifications

app = Flask(__name__)

# 这里假设你有OpenAI API的密钥
OPENAI_API_KEY = 'your_openai_api_key'

# 设置上传文件保存的目录
UPLOAD_FOLDER = 'uploads'
MODIFIED_FOLDER = 'modified'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODIFIED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODIFIED_FOLDER'] = MODIFIED_FOLDER
# 設定文件上傳的保存路徑和允許的文件類型
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB 上傳文件大小限制

def get_openai_response(prompt):
    url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 1500,  # 根据需要调整
        'n': 1,
        'stop': None,
        'temperature': 0.2
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api', methods=['POST'])
def api():
    return 'api running'

@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Correct sentence postback based on selected work.
    Expected JSON format: { "work": ["structure", "child"], "content": "article" }
    Returns JSON: { "openai_response": "modified_article" }
    """
    data = request.get_json()
    modified_article = apply_modifications(data)

    # 从OpenAI获取响应
    openai_response = get_openai_response(modified_article)
    openai_text = openai_response['choices'][0]['text']

    return jsonify({'openai_response': openai_text})

@app.route('/api/get', methods=['POST'])
def api_get():
    """
    獲取格式文件並用字符串命名
    預期：上傳文件，格式名稱
    返回 JSON: { "openai_response": "modified_article" }
    """
    if 'file' not in request.files or 'format_name' not in request.form:
        return jsonify({"error": "Missing file or format name"}), 400

    file = request.files['file']
    format_name = request.form['format_name']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        with open(file_path, 'r') as f:
            file_content = f.read()

        # 調用 OpenAI API 進行處理
        prompt = f"Format the following text using the '{format_name}' format:\n{file_content}"
        openai_response = get_openai_response(prompt)
        
        # 假設 OpenAI API 返回的修改後內容在 choices[0].text 中
        modified_article = openai_response.get('choices', [{}])[0].get('text', '')

        # 刪除臨時文件
        os.remove(file_path)

        return jsonify({"openai_response": modified_article})

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/api/enter', methods=['POST'])
def enter():
    """
    根據選擇的格式修改格式。
    預期 JSON 格式： { format:format_name, sentence: 不超過1500字（包含以上句子為佳） }
    返回 JSON: { "openai_response": "modified_article" }
    """
    data = request.get_json()

    if not data or 'format' not in data or 'sentence' not in data:
        return jsonify({"error": "Missing format or sentence"}), 400

    format_name = data['format']
    sentence = data['sentence']

    if len(sentence.split()) > 1500:
        return jsonify({"error": "Sentence exceeds 1500 words"}), 400

    # 調用 OpenAI API 進行處理
    prompt = f"Revise the following sentence using the '{format_name}' format:\n{sentence}"
    openai_response = get_openai_response(prompt)
    
    # 假設 OpenAI API 返回的修改後內容在 choices[0].text 中
    modified_article = openai_response.get('choices', [{}])[0].get('text', '')

    return jsonify({"openai_response": modified_article})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    app.run(debug=True, threaded=True)

# -*- coding: utf-8 -*-
import json
import os
import webbrowser
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Directory where this script lives
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / '答题记录.json'

def ensure_data():
    """Create empty data file if it doesn't exist."""
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({"choice": {}, "fill": {}}, ensure_ascii=False, indent=2), encoding='utf-8')
        print('  [初始化] 已创建答题记录.json')

def read_data():
    ensure_data()
    try:
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    except:
        return {"choice": {}, "fill": {}}

def write_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# ---- Routes ----

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, '2026中考物理预测题.html')

@app.route('/api/load')
def load_data():
    return jsonify(read_data())

@app.route('/api/save', methods=['POST'])
def save_data():
    data = request.get_json()
    if not isinstance(data, dict) or 'choice' not in data or 'fill' not in data:
        return jsonify({'ok': False, 'error': 'Invalid data'}), 400
    write_data({'choice': data['choice'], 'fill': data['fill']})
    print('  [保存] 答题记录已更新')
    return jsonify({'ok': True})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    write_data({"choice": {}, "fill": {}})
    print('  [清空] 答题记录已重置')
    return jsonify({'ok': True})

# ---- Static files (JS, CSS, etc.) ----
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    ensure_data()
    port = 19520
    url = f'http://localhost:{port}'
    print('')
    print('  ╔══════════════════════════════════════╗')
    print('  ║   天津中考物理 · 2026预测题         ║')
    print('  ║   答题记录自动保存到同级 JSON       ║')
    print('  ╚══════════════════════════════════════╝')
    print('')
    print(f'  打开浏览器访问: {url}')
    print(f'  答题记录文件: {DATA_FILE}')
    print('')
    print('  关闭此窗口即可停止服务')
    print('')
    webbrowser.open(url)
    app.run(host='127.0.0.1', port=port, debug=False)

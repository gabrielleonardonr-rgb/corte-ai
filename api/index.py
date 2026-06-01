from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re, os, json, datetime, requests

app = Flask(__name__)
CORS(app)

def extrair_id(url):
    m = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    return m.group(1) if m else None

@app.route('/')
def home():
    return jsonify({'status': 'ok'})

@app.route('/transcript')
def transcript():
    url = request.args.get('url', '')
    vid = extrair_id(url)
    if not vid:
        return jsonify({'sucesso': False, 'erro': 'Link inválido'})
    try:
        ytt = YouTubeTranscriptApi()
        data = ytt.fetch(vid, languages=['en'])
        texto = ' '.join([s.text for s in data])
        return jsonify({'sucesso': True, 'transcricao': texto, 'idioma': 'en'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

@app.route('/save', methods=['POST', 'OPTIONS'])
def save():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    body = request.get_json()
    titulo = body.get('titulo', 'Roteiro')
    nicho = body.get('nicho', 'Geral')
    conteudo = body.get('conteudo', '')
    data = datetime.datetime.now().strftime('%d-%m-%Y')
    nome = f"{data} — {titulo}.txt"
    return jsonify({'sucesso': True, 'nome': nome, 'link': '#', 'mensagem': 'Roteiro recebido com sucesso!'})

@app.route('/claude', methods=['POST', 'OPTIONS'])
def claude_proxy():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        body = request.get_json()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return jsonify({'error': 'ANTHROPIC_API_KEY não configurada'}), 500
        response = requests.post(
            'https://api.anthrop

from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

app = Flask(__name__)
CORS(app)

def extrair_video_id(url):
    padrao = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(padrao, url)
    return match.group(1) if match else None

@app.route('/')
def home():
    return jsonify({'status': 'CORTE.AI API rodando!'})

@app.route('/transcript')
def transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({'sucesso': False, 'erro': 'URL obrigatória'})

    video_id = extrair_video_id(url)
    if not video_id:
        return jsonify({'sucesso': False, 'erro': 'Link inválido'})

    try:
        ytt = YouTubeTranscriptApi()
        fetched = ytt.fetch(video_id, languages=['en'])
        texto = ' '.join([s.text for s in fetched])
        return jsonify({'sucesso': True, 'transcricao': texto, 'idioma': 'en'})
    except Exception as e:
        try:
            ytt = YouTubeTranscriptApi()
            transcript_list = ytt.list(video_id)

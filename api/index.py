from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re, os

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

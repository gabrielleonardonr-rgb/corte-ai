from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
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
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        texto = ' '.join([t['text'] for t in transcript])
        return jsonify({'sucesso': True, 'transcricao': texto, 'idioma': 'en'})
    except NoTranscriptFound:
        try:
            lista = YouTubeTranscriptApi.list_transcripts(video_id)
            for t in lista:
                transcript = t.fetch()
                texto = ' '.join([seg['text'] for seg in transcript])
                return jsonify({'sucesso': True, 'transcricao': texto, 'idioma': t.language_code})
        except Exception as e:
            return jsonify({'sucesso': False, 'erro': str(e)})
    except TranscriptsDisabled:
        return jsonify({'sucesso': False, 'erro': 'Transcrições desativadas'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

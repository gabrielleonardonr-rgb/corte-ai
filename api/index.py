from flask import Flask, request, jsonify
from flask_cors import CORS
import re, os, json, datetime, requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'ok'})

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

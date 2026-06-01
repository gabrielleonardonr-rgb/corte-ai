from http.server import HTTPServer, BaseHTTPRequestHandler
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import json, datetime

with open("C:/Users/qa-nb03/token_drive.json") as f:
    t = json.load(f)

creds = Credentials(token=t["token"], refresh_token=t["refresh_token"], token_uri=t["token_uri"], client_id=t["client_id"], client_secret=t["client_secret"], scopes=t["scopes"])
service = build("drive", "v3", credentials=creds)

def encontrar_pasta(nome, pai=None):
    q = f"name='{nome}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if pai: q += f" and '{pai}' in parents"
    res = service.files().list(q=q, fields="files(id)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))
        titulo = body.get("titulo", "Roteiro")
        nicho = body.get("nicho", "🔬 Ciência & Saúde")
        conteudo = body.get("conteudo", "")
        try:
            raiz = encontrar_pasta("🎬 AGENTE ROTEIROS")
            roteiros = encontrar_pasta("📁 Roteiros", raiz)
            nicho_id = encontrar_pasta(nicho, roteiros)
            data = datetime.datetime.now().strftime("%d-%m-%Y")
            nome = f"{data} — {titulo}.txt"
            media = MediaInMemoryUpload(conteudo.encode("utf-8"), mimetype="text/plain")
            arquivo = service.files().create(body={"name": nome, "parents": [nicho_id]}, media_body=media, fields="id,name,webViewLink").execute()
            resposta = {"sucesso": True, "link": arquivo["webViewLink"], "nome": arquivo["name"]}
        except Exception as e:
            resposta = {"sucesso": False, "erro": str(e)}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(resposta).encode())

    def log_message(self, format, *args): pass

print("🟢 Servidor Drive rodando em http://localhost:8766")
HTTPServer(('localhost', 8766), Handler).serve_forever()

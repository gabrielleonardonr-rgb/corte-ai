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

raiz = encontrar_pasta("🎬 AGENTE ROTEIROS")
roteiros = encontrar_pasta("📁 Roteiros", raiz)
nicho = encontrar_pasta("🔬 Ciência & Saúde", roteiros)
data = datetime.datetime.now().strftime("%d-%m-%Y")
nome = f"{data} — Teste de conexão.txt"
media = MediaInMemoryUpload("Roteiro de teste salvo com sucesso!".encode("utf-8"), mimetype="text/plain")
arquivo = service.files().create(body={"name": nome, "parents": [nicho]}, media_body=media, fields="id,name,webViewLink").execute()
print("Salvo:", arquivo["name"])
print("Link:", arquivo["webViewLink"])

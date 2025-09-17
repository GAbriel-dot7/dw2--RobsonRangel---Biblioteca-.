# app.py
# Escolha entre FastAPI ou Flask. Exemplo com FastAPI:
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à API da Biblioteca!"}

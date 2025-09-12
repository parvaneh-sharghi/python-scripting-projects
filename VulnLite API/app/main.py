# app/main.py
from fastapi import FastAPI
from .db import init_db 

app = FastAPI(title="VulnLite API (hello)", version="0.0.1")

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
def health():
    return {"ok": True}



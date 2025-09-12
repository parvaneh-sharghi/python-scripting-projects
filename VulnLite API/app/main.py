# app/main.py
from fastapi import FastAPI

app = FastAPI(title="VulnLite API (hello)", version="0.0.1")

@app.get("/health")
def health():
    return {"ok": True}



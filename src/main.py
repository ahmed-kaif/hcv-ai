from fastapi import FastAPI
from src.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"msg": "Welcome to hcv-ai"}

@app.get("/healthz")
async def check_api_health():
    return {"status": "ok"}

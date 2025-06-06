from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"msg": "Welcome to hcv-ai"}

@app.get("/healthz")
async def check_api_health():
    return {"status": "ok"}

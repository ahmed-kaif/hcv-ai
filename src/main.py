from fastapi import FastAPI
from src.database import Base, engine
from src.api.users import router as user_router
from src.api.auth import router as auth_router
from src.api.predictions import router as prediction_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(prediction_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"msg": "Welcome to hcv-ai"}

@app.get("/healthz")
async def check_api_health():
    return {"status": "ok"}

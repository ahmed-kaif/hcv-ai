from fastapi import FastAPI
from src.database import Base, engine, SessionLocal
from contextlib import asynccontextmanager
from src.api.users import router as user_router
from src.api.auth import router as auth_router
from src.api.predictions import router as prediction_router
from src import seeds


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed the database
    db = SessionLocal()
    try:
        seeds.run()
        print("✅ Seeding complete")
    finally:
        db.close()

    # Yield control to the app
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(prediction_router)

@app.get("/")
async def read_root():
    return {"msg": "Welcome to hcv-ai"}

@app.get("/healthz")
async def check_api_health():
    return {"status": "ok"}

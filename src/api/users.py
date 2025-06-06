from fastapi import APIRouter
from services import user_service

router = APIRouter(prefix="/users")

@router.get("/")
async def get_all_users():
    return user_service.get_all_users()

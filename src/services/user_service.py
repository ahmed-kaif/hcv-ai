from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db

async def get_all_user(db: Session = Depends(get_db)):
    pass


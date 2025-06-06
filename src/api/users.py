from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import models, schemas, database, oauth

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(oauth.get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(
        user_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(oauth.get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db.query(models.User).get(user_id)

@router.get("/", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth.get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db.query(models.User).all()

@router.put("/me", response_model=schemas.UserOut)
def update_me(
    update: schemas.UserCreate,
    db: Session = Depends(database.get_db),
        current_user: models.User = Depends(oauth.get_current_user)
):
    for attr, value in update.model_dump().items():
        setattr(current_user, attr, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me")
def delete_me(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(oauth.get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted"}


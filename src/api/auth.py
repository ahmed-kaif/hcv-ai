from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src import models, schemas, utils, oauth, database

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump(exclude={"password"}), password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not utils.verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/google-login")
async def google_login():
    return {"url": oauth.get_google_oauth_url()}

@router.get("/callback")
async def google_callback(code: str, db: Session = Depends(database.get_db)):
    profile = oauth.get_google_profile(code)
    user = db.query(models.User).filter(models.User.email == profile.email).first()
    if not user:
        user = models.User(name=profile.name, email=profile.email, auth_provider="google")
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

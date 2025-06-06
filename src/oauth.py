from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional
from src import models, database
from src.core.config import Config
import requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc) + 
        (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Google OAuth2 (Basic Flow)
def get_google_oauth_url():
    return (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={Config.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={Config.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
    )


def get_google_profile(code: str):
    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "redirect_uri": Config.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    ).json()
    access_token = token_resp.get("access_token")

    profile_resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    class Profile:
        email: str = profile_resp.get("email")
        name: str = profile_resp.get("name")
    return Profile()

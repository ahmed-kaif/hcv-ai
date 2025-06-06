from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)  # Empty if auth_provider is Google
    is_admin = Column(Boolean, default=False)
    auth_provider = Column(String, default="email")  # "email" or "google"
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")


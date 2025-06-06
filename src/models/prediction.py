from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Required fields
    ALB = Column(Float, nullable=False)
    ALP = Column(Float, nullable=False)
    AST = Column(Float, nullable=False)
    CHE = Column(Float, nullable=False)
    CGT = Column(Float, nullable=False)

    # Optional fields
    CREA = Column(Float, nullable=True)
    CHOL = Column(Float, nullable=True)
    PROT = Column(Float, nullable=True)
    BIL = Column(Float, nullable=True)
    ALT = Column(Float, nullable=True)
    Age = Column(Integer, nullable=True)
    Sex = Column(String, nullable=True)

    # Result from classification table (foreign key to results table)
    result_id = Column(Integer, ForeignKey("results.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship
    user = relationship("User", back_populates="predictions")
    result = relationship("Result", back_populates="predictions")

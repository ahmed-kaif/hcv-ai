from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 0 to 3
    label = Column(String, nullable=False, unique=True)  # e.g., "Negative"

    # Reverse relationship to predictions
    predictions = relationship("Prediction", back_populates="result")

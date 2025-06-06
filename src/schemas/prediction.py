from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class PredictionBase(BaseModel):
    ALB: float = Field(title="Albumin")
    ALP: float
    AST: float = Field(title="aspartate amino-transferase")
    CHE: float = Field(title="choline esterase")
    CGT: float = Field(title="γ-glutamyl-transferase")

    CREA: Optional[float] = Field(default=None, title="")
    CHOL: Optional[float] = Field(default=None, title="")
    PROT: Optional[float] = None
    BIL: Optional[float] = Field(default=None, title="Bilirubin")
    ALT: Optional[float] = Field(default=None, title="Alanine Amino-Transferase")
    Age: Optional[float] = None
    Sex: Optional[str] = None

# For creation
class PredictionCreate(PredictionBase):
    pass


# For reading
class PredictionOut(PredictionBase):
    id: int
    user_id: Optional[int]
    result_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

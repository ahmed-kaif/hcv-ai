from pydantic import BaseModel, ConfigDict


class ResultBase(BaseModel):
    id: int
    label: str
    
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel


class ResultBase(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True

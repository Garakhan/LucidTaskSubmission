from typing import List, Annotated
from pydantic import BaseModel, StringConstraints

class PostCreate(BaseModel):
    text: Annotated[str, StringConstraints(max_length=1_048_576)]

class PostOut(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True

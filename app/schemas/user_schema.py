from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints

class UserCreate(BaseModel):
    email: EmailStr
    # password: constr(min_length=8)
    password: Annotated[
        str,
        StringConstraints(min_length=8),
    ]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

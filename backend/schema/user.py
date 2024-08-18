from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True


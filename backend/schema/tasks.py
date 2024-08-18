from pydantic import BaseModel
from typing import Optional, List

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    id: int

class TaskResponse(TaskBase):
    id: int
    owner_id: str

    class Config:
        orm_mode = True

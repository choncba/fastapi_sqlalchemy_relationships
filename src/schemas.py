from pydantic import BaseModel
from typing import List

class TaskBase(BaseModel):
    id: int
    title : str
    description : str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: int
    username : str
    password : str

    class Config:
        orm_mode = True

class TaskSchema(TaskBase):
    owners: List[UserBase]

class UserSchema(UserBase):
    tasks: List[TaskBase]

class NoteSchema(BaseModel):
    note : str
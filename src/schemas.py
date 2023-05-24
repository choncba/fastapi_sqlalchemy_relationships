from pydantic import BaseModel, Field, EmailStr, validator, validate_email, AnyUrl, Json
from typing import Optional, Any

class TaskSchema(BaseModel):
    title : str
    description : str
    created_by : int
    started_by : Optional[int]
    finished_by : Optional[int]
    notes_id: Optional[int]

class UserSchema(BaseModel):
    username : str
    password : str

class NoteSchema(BaseModel):
    note : str
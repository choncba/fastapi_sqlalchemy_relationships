from pydantic import BaseModel, Field, EmailStr, validator, validate_email, AnyUrl, Json
from typing import Optional, Any

class TaskSchema(BaseModel):
    title : str
    description : str

class UserSchema(BaseModel):
    username : str
    password : str

class NoteSchema(BaseModel):
    note : str
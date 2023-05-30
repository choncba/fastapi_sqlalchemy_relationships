from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Users
class UsersBase(SQLModel):
    username : str
    password : str

class Users(UsersBase, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    started_tasks: List['Tasks'] = Relationship(back_populates="started_by")

class UsersRead(SQLModel):
    id: int
    username: str

class UsersCreate(UsersBase):
    pass

class UsersUpdate(SQLModel):
    id: int
    username : Optional[str] = None
    password : Optional[str] = None

# Tasks

# Clase Base referida a SQLModel, acá van los campos principales, pero no define la tabla de la BD
class TasksBase(SQLModel):
    title : str
    description : str
    started_by_id: Optional[int] = Field(default=None, foreign_key="users.id")

# table=True indica que se CREARA este modelo de tabla en la BD
# el id debe estar en la tabla y se crea de forma automática
# Los otros campos se heredan de TaskBase
class Tasks(TasksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    started_by: Optional[Users] = Relationship(back_populates="started_tasks")

# Para lectura, incluyo el id
class TasksRead(TasksBase):
    id: int

class TaskRead(SQLModel):
    id: int
    title : str
    description : str

# Para escritura, utilizo la clase base, la dejo como referencia
class TasksCreate(TasksBase):
    pass

class TasksUpdate(SQLModel):
    title : Optional[str] = None
    description : Optional[str] = None
    started_by_id: Optional[int] = None

# Relationships
class TasksWithUsers(TaskRead):
    started_by : Optional[UsersRead] = None

class UsersWithTasks(UsersRead):
    started_tasks: List[TaskRead] = []







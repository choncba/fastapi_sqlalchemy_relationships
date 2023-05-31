from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint


# Link Tables

class TasksOwners(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

# class TaskNotes(SQLModel, table=True):
#     task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", primary_key=True)
#     note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
#     user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

# Users
class UsersBase(SQLModel):
    username : str
    password : str

class Users(UsersBase, table=True):
    # Se pueden definir parámetros adicionales de la tabla igualmente acá
    __table_args__ = (
        UniqueConstraint("username"),             # Defino campos unicos
        # {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )
    id : Optional[int] = Field(default=None, primary_key=True)
    started_tasks: List['Tasks'] = Relationship(back_populates="started_by")
    owned_tasks: List["Tasks"] = Relationship(back_populates="owners", link_model=TasksOwners)
    notes: List["Notes"] = Relationship(back_populates="owner")

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
    owners: List["Users"] = Relationship(back_populates="owned_tasks", link_model=TasksOwners)
    notes: List["Notes"] = Relationship(back_populates="task")

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
    owners: Optional[List[int]] = None

class NotesBase(SQLModel):
    date: str
    note: str
    task_id: int = Field(default=None, foreign_key="tasks.id")
    owner_id: int = Field(default=None, foreign_key="users.id")

class Notes(NotesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner: Users = Relationship(back_populates="notes")
    task: Tasks = Relationship(back_populates="notes")

class NotesCreate(NotesBase):
    pass

class NotesRead(SQLModel):
    date: str
    note: str
    owner_id: int

# Vistas ampliadas incluyendo las relciones
class TasksWithUsers(TaskRead):
    started_by : Optional[UsersRead] = None
    owners : List[UsersRead] = []
    notes : List[NotesRead] = []

class UsersWithTasks(UsersRead):
    started_tasks: List[TaskRead] = []








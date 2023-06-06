from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime

# Link Tables

class TasksOwners(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

class TaskChanges(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", primary_key=True)
    started_by_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    canceled_by_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    finished_by_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

class TaskNotes(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", primary_key=True)
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)

# Users
class UsersBase(SQLModel):
    username : str = Field(min_length=4, max_length=50)
    password : str = Field(min_length=4, max_length=50)

class Users(UsersBase, table=True):
    # Se pueden definir parámetros adicionales de la tabla igualmente acá
    __table_args__ = (
        UniqueConstraint("username"),             # Defino campos unicos
        # {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )
    id : Optional[int] = Field(default=None, primary_key=True)
    started_tasks: List["Tasks"] = Relationship(back_populates="started_by", link_model=TaskChanges, 
                                                sa_relationship_kwargs=dict(
                                                    primaryjoin="Tasks.id==TaskChanges.task_id",
                                                    secondaryjoin="Tasks.id==TaskChanges.started_by_id",
                                                ))
    canceled_tasks: List["Tasks"] = Relationship(back_populates="canceled_by", link_model=TaskChanges, 
                                                sa_relationship_kwargs=dict(
                                                    primaryjoin="Tasks.id==TaskChanges.task_id",
                                                    secondaryjoin="Tasks.id==TaskChanges.canceled_by_id",
                                                ))
    finished_tasks: List["Tasks"] = Relationship(back_populates="finished_by", link_model=TaskChanges,
                                                sa_relationship_kwargs=dict(
                                                    primaryjoin="Tasks.id==TaskChanges.task_id",
                                                    secondaryjoin="Tasks.id==TaskChanges.finished_by_id",
                                                ))
    owned_tasks: List["Tasks"] = Relationship(back_populates="owners", link_model=TasksOwners)
    notes: List["Notes"] = Relationship(back_populates="user", link_model=TaskNotes)

class UsersRead(SQLModel):
    id: int
    username: str

class UsersCreate(UsersBase):
    pass

class UsersUpdate(SQLModel):
    username : Optional[str] = Field(min_length=4, max_length=50, default=None)
    password : Optional[str] = Field(min_length=4, max_length=50, default=None)

class UserName(SQLModel):
    username: str

# Tasks
# Clase Base referida a SQLModel, acá van los campos principales, pero no define la tabla de la BD
class TasksBase(SQLModel):
    title : str = Field(max_length=100)
    description : str = Field(max_length=2000)   

# table=True indica que se CREARA este modelo de tabla en la BD
# el id debe estar en la tabla y se crea de forma automática
# Los otros campos se heredan de TaskBase
class Tasks(TasksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    started_by: Optional[Users] = Relationship(back_populates="started_tasks", link_model=TaskChanges)
    canceled_by: Optional[Users] = Relationship(back_populates="canceled_tasks", link_model=TaskChanges)
    finished_by: Optional[Users] = Relationship(back_populates="finished_tasks", link_model=TaskChanges)
    owners: List["Users"] = Relationship(back_populates="owned_tasks", link_model=TasksOwners)
    notes: List["Notes"] = Relationship(back_populates="task", link_model=TaskNotes)

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
    title : Optional[str] = Field(max_length=100, default=None)
    description : Optional[str] = Field(max_length=2000, default=None)
    started_by_id: Optional[int] = None

# Notas
class NotesBase(SQLModel):
    note: str = Field(max_length=2000, default=None)

class Notes(NotesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[datetime] = Field(default=None) 
    task: Tasks = Relationship(back_populates="notes", link_model=TaskNotes)
    user: Users = Relationship(back_populates="notes", link_model=TaskNotes)

class NotesCreate(NotesBase):
    pass

class NotesRead(SQLModel):
    date: str
    note: str

# Vistas ampliadas incluyendo las relciones
class NotesWithUser(NotesRead):
    user : UserName

class TasksWithUsers(TaskRead):
    started_by : Optional[UsersRead] = None
    finished_by : Optional[UsersRead] = None
    canceled_by : Optional[UsersRead] = None
    owners : List[UsersRead] = []
    notes : List[NotesWithUser] = []

class UsersWithTasks(UsersRead):
    started_tasks: List[TaskRead] = []










from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from datetime import datetime

# Link Tables

class TasksOwners(SQLModel, table=True):
    """
    Tabla Many-To-Many entre Tasks y Users
    """
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)

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

    # Debe estar la relación porque es many-to-many
    owned_tasks: List["Tasks"] = Relationship(back_populates="owners", link_model=TasksOwners)

    # Ver si es necesario con sqlmodel
    # class Config:
    #     orm_mode = True

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

class UsersIds(SQLModel):
    id: int

    def get_ids(self):
        return self.id

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
    
    # Relación Many(Tasks)-To-One(Users) para definir qué usuario inicia la tarea
    started_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    # Al tener multiples foreign_keys apuntando a la misma columna de la tabla Users, debo indicar cuál es la relación con esta tabla así:
    started_by: Optional[Users] = Relationship(sa_relationship_kwargs={"primaryjoin": "(Tasks.started_by_id==Users.id)", "lazy": "joined"})
    
    canceled_by_id: Optional[int] = Field(default=None, foreign_key="users.id")
    canceled_by: Optional[Users] = Relationship(sa_relationship_kwargs={"primaryjoin": "Tasks.canceled_by_id==Users.id", "lazy": "joined"})
    
    finished_by_id: Optional[int] = Field(default=None, foreign_key="users.id")    
    finished_by: Optional[Users] = Relationship(sa_relationship_kwargs={"primaryjoin": "Tasks.finished_by_id==Users.id", "lazy": "joined"})
    
    #users_actions: Users = Relationship(sa_relationship_kwargs={"primaryjoin": "or_(Tasks.started_by_id==Users.id, Tasks.canceled_by_id==Users.id, Tasks.finished_by_id==Users.id)", "lazy": "joined"})

    # Relacion Many-To-Many con los usuarios owners de la tarea
    owners: List["Users"] = Relationship(link_model=TasksOwners, back_populates="owned_tasks") # Al eliminar una tarea también se elimina la relación de la tabla TaskOwners
    # Relación One(Tasks)-To-Many(Notes), multiples notas para cada tarea
    # notes: List["Notes"] = Relationship(back_populates="task") # Esto al eliminar una tarea pone el id de la tarea en la tabla Notes en null
    notes: List["Notes"] = Relationship(sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"}, back_populates="task") # Esto al eliminar la tarea también elimina las notas asociadas

    # class Config:
    #     orm_mode = True

# Para lectura, incluyo el id
class TasksRead(TasksBase):
    id: int

class TaskRead(SQLModel):
    id: int
    title : str
    description : str
    started_by_id: Optional[int]
    canceled_by_id: Optional[int]
    finished_by_id: Optional[int]
    owners: List[UsersRead]

# Para escritura, utilizo la clase base, la dejo como referencia
class TasksCreate(TasksBase):
    pass

class TasksUpdate(SQLModel):
    title : Optional[str] = Field(max_length=100, default=None)
    description : Optional[str] = Field(max_length=2000, default=None)
    started_by_id: Optional[int] = None
    canceled_by_id: Optional[int] = None
    finished_by_id: Optional[int] = None

# Notas
class NotesBase(SQLModel):
    note: str = Field(max_length=2000, default=None)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")

class Notes(NotesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[datetime] = Field(default=None)

    user: Users = Relationship()
    task: Tasks = Relationship()

    # class Config:
    #     orm_mode = True
    
class NotesCreate(NotesBase):
    pass

class NotesRead(SQLModel):
    date: datetime
    note: str

# Vistas ampliadas incluyendo las relciones
class NotesWithUser(NotesRead):
    user : UsersRead

class TasksWithNotes(TaskRead):
    notes : List[NotesWithUser] = []

class UsersWithTasks(UsersRead):
    started_tasks: List[TaskRead] = []










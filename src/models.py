from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from schemas import UserSchema, TaskSchema, NoteSchema

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)

    # created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # started_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # finished_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # created_by = relationship("Users", foreign_keys=[created_by_id])
    # started_by = relationship("Users", foreign_keys=[started_by_id])
    # finished_by = relationship("Users", foreign_keys=[finished_by_id])

    # notes_id = Column(Integer, ForeignKey("notes.id"), nullable=True)
    # notes = relationship("Notes")

    def __init__(self, task: TaskSchema | None = None):
        if task: 
            self.title = task.title
            self.description = task.description

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)    
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)
    # tasks = relationship(   "Tasks",
    #                         cascade="all,delete-orphan",
    #                         back_populates="created_by",
    #                         uselist=True
    #                     )

    def __init__(self, user: UserSchema | None = None):
        if user: 
            self.username = user.username
            self.password = user.password

    
class Notes(Base):
    __tablename__ = "notes"
    
    id = Column("tasks_id", Integer, ForeignKey("tasks.id", name="notes_tasks"), nullable=False, autoincrement=False, primary_key=True)
    note = Column(String(500))

    task = relationship("Tasks", foreign_keys=[id], backref="notes")

    def __init__(self, note: NoteSchema | None = None):
        if note: 
            self.note = note.note

class Tasks_Users(Base):
    __tablename__ = "tasks_users"
    id = Column("task_id", Integer, ForeignKey("tasks.id", name="task_id"), nullable=False, autoincrement=False, primary_key=True)
    created_by = Column(Integer, ForeignKey("users.id", name="created_by"), nullable=False, index=True)
    started_by = Column(Integer, ForeignKey("users.id", name="started_by"), nullable=False, index=True)
    finished_by = Column(Integer, ForeignKey("users.id", name="finished_by"), nullable=False, index=True)

    task = relationship("Tasks", foreign_keys=[id], backref="tasksUsers")
    user = relationship("Users", foreign_keys=[created_by], backref="tasksUsers")
    user = relationship("Users", foreign_keys=[started_by], backref="tasksUsers")
    user = relationship("Users", foreign_keys=[finished_by], backref="tasksUsers")






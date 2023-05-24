from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)         
    started_by = Column(Integer, ForeignKey("users.id"), nullable=True)        
    finished_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("Users", back_populates="tasks")

    notes_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = relationship("Notes", back_populates="tasks")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)    
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)
    tasks = relationship(   "Tasks",
                            cascade="all,delete-orphan",
                            back_populates="user",
                            uselist=True
                        )
    
class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    note = Column(String(500), nullable=True)
    tasks = relationship(   "Tasks",
                            cascade="all,delete-orphan",
                            back_populates="notes",
                            uselist=True
                        )


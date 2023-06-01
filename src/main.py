from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from starlette.responses import RedirectResponse
from database import create_db_and_tables, get_session, Session, select
import models

from typing import List

# database.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Redirecciono todo a los docs de Swagger
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

# Users
@app.get("/users", response_model=List[models.UsersRead]) # Notar como el modelo devuelto es distinto al leido en la BD
async def get_users(db: Session = Depends(get_session)):
    users = db.exec(select(models.Users)).all()
    return users

@app.get("/users/{id}", response_model=models.Users)
async def get_user(id: int, db: Session = Depends(get_session)):
    user = db.get(models.Users, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=models.UsersRead)
async def add_user(new_user: models.UsersCreate, db: Session = Depends(get_session)):
    db_user = models.Users.from_orm(new_user) # Esto lo hago porque uso modelos de subclases, si no no haria falta y solo hago db.add(new_ser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.patch("/users/{id}", response_model=models.UsersRead)
async def edit_user(id: int, user: models.UsersUpdate, db: Session = Depends(get_session)):
    db_user = await get_user(id, db)
    user_data = user.dict(exclude_unset=True) # exclude_unset=True indica a pydantic que excluya los valores del modelo no enviados por el cliente, de esta forma, no los borra
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{id}")
async def delete_user(id: int, db: Session = Depends(get_session)):
    db_user = await get_user(id, db)
    db.delete(db_user)
    db.commit()
    return { "user deleted" : db_user.username }

# Tasks
@app.get("/tasks", response_model=List[models.TasksRead])
async def get_tasks(db: Session = Depends(get_session)):
    tasks = db.exec(select(models.Tasks)).all()
    return tasks

@app.get("/task/{id}", response_model=models.TasksWithUsers)
async def get_task(id: int, db: Session = Depends(get_session)):
    task = db.get(models.Tasks, id)
    if not task:
        raise HTTPException(status_code=404, detail="Hero not found")
    return task

@app.post("/task/", response_model=models.TasksRead)
async def add_task(new_task: models.TasksCreate, db: Session = Depends(get_session)):
    db_task = models.Tasks.from_orm(new_task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.patch("/task/{id}", response_model=models.TasksRead)
async def edit_task(id: int, task: models.TasksUpdate, db: Session = Depends(get_session)):
    db_task = await get_task(id, db)
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/task/{id}")
async def delete_task(id: int, db: Session = Depends(get_session)):
    db_task = await get_task(id, db)
    db.delete(db_task)
    db.commit()
    return { "task deleted" : db_task.title }

# Notes
@app.post("/notes/", response_model=models.NotesWithUser)
async def add_note(new_note: models.NotesCreate, db: Session = Depends(get_session)):
    db_note = models.Notes.from_orm(new_note)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note



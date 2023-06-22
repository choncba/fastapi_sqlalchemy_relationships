from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from starlette.responses import RedirectResponse
from database import create_db_and_tables, get_session, Session, select
import models
from typing import List, Optional
from datetime import datetime
from pydantic import ValidationError

app = FastAPI()

# Si uso Alembic comento este método
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Redirecciono todo a los docs de Swagger
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

# Users
@app.get("/users", response_model=List[models.UsersRead], tags=["Users"]) # Notar como el modelo devuelto es distinto al leido en la BD
async def get_users(db: Session = Depends(get_session)):
    users = db.exec(select(models.Users)).all()
    return users

@app.get("/users/{id}", response_model=models.UsersRead, tags=["Users"])
async def get_user(id: int, db: Session = Depends(get_session)):
    user = db.get(models.Users, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.post("/users/", response_model=models.UsersRead, tags=["Users"])
async def add_user(new_user: models.UsersCreate, db: Session = Depends(get_session)):
    if db.exec(select(models.Users).filter(models.Users.username == new_user.username)).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {new_user.username} already exists")
    else: 
        db_user = models.Users.from_orm(new_user) # Esto lo hago porque uso modelos de subclases, si no no haria falta y solo hago db.add(new_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

@app.patch("/users/{id}", response_model=models.UsersRead, tags=["Users"])
async def edit_user(id: int, user: models.UsersUpdate, db: Session = Depends(get_session)):
    db_user = await get_user(id, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        user_data = user.dict(exclude_unset=True) # exclude_unset=True indica a pydantic que excluya los valores del modelo no enviados por el cliente, de esta forma, no los borra
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

@app.delete("/users/{id}", tags=["Users"])
async def delete_user(id: int, db: Session = Depends(get_session)):
    db_user = await get_user(id, db)
    db.delete(db_user)
    db.commit()
    return { "user deleted" : db_user.username }

# Tasks
#@app.get("/tasks", response_model=List[models.TaskRead], response_model_include={"id"}, tags=["Tasks"])
@app.get("/tasks", response_model=List[models.TaskRead], tags=["Tasks"])
async def get_tasks(db: Session = Depends(get_session)):
    tasks = db.exec(select(models.Tasks)).all()
    return tasks

@app.get("/task/{id}", response_model=models.TasksWithNotes, tags=["Tasks"])
async def get_task(id: int, db: Session = Depends(get_session)):
    task = db.get(models.Tasks, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task ID {id} not found")
    return task

@app.post("/task/", response_model=models.TasksRead, tags=["Tasks"])
async def add_task(new_task: models.TasksCreate, owner_ids: List[int], db: Session = Depends(get_session)):
    
    # Verifico que los usuarios existan
    owners = [db.get(models.Users, id) for id in owner_ids if db.get(models.Users, id) is not None]
    if len(owners) == 0:
        raise HTTPException(status_code=404, detail=f"User/s id {owner_ids} not found")
    else:
        # Primero cargo la info de la tarea, esto genera el id de la tarea automaticamente
        db_task = models.Tasks.from_orm(new_task)
        db.add(db_task)
        db.commit()
        # Ahora Guardo las referencias a los id's de los usuarios owners en la tabla TaskOwners
        db_task_owners = [models.TasksOwners(task_id=db_task.id, user_id=id) for id in owner_ids]
        db.add_all(db_task_owners)
        db.commit()
        db.refresh(db_task)
        return db_task

@app.patch("/task/{id}", response_model=models.TasksRead, tags=["Tasks"])
async def edit_task(id: int, task: models.TasksUpdate, owner_ids: Optional[List[int]] | None = None, db: Session = Depends(get_session)):
    db_task = await get_task(id, db)
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    if owner_ids:
        owners = [db.get(models.Users, id) for id in owner_ids if db.get(models.Users, id) is not None]
        if len(owners) == 0:
            raise HTTPException(status_code=404, detail=f"User/s id {owner_ids} not found")
        else:
            db_task_owners = [models.TasksOwners(task_id=db_task.id, user_id=id) for id in owner_ids]
            db.add_all(db_task_owners)
            db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/task/{id}", tags=["Tasks"])
async def delete_task(id: int, db: Session = Depends(get_session)):
    # Elimino la tarea
    db_task = await get_task(id, db)
    db.delete(db_task)
    db.commit()
    # Elimino las notas asociadas, el id de la tarea queda en none al borarla
    # notes = db.exec(select(models.Notes).where(models.Notes.task_id == None)).all()
    # for note in notes:
    #     db.delete(note)
    # db.commit()
    return { f"Task {id} deleted" : db_task.title }

# Notes
@app.post("/notes/", response_model=models.NotesWithUser, tags=["Notes"])
async def add_note(new_note: models.NotesCreate, db: Session = Depends(get_session)):
        user = db.get(models.Users, new_note.user_id)
        task = db.get(models.Tasks, new_note.task_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User id {new_note.user_id} not found")
        elif task is None:
            raise HTTPException(status_code=404, detail=f"Task id {new_note.task_id} not found")
        else:            
            db_note = models.Notes.from_orm(new_note)
            #db_note.date = datetime.now().strftime("%d/%m/%Y %H:%M")    # Pongo la fecha automáticamente
            db_note.date = datetime.now()    # Pongo la fecha automáticamente
            db.add(db_note)
            db.commit()
            db.refresh(db_note)
            return db_note


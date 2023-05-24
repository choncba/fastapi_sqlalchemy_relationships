from fastapi import FastAPI, Depends
from starlette import status
from starlette.responses import RedirectResponse

import database
from models import Users, Tasks, Notes
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from schemas import UserSchema, TaskSchema, NoteSchema

database.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Redirecciono todo a los docs de Swagger
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

@app.get("/users/", status_code=200)
async def get_user(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users

@app.post("/users/", status_code=200)
async def add_user(new_user: UserSchema, db: Session = Depends(get_db)):
    db.add(Users(new_user))
    db.commit()
    return new_user

@app.get("/tasks/", status_code=200)
async def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Tasks).all()
    return tasks

@app.post("/task/", status_code=200)
async def add_task(new_task: TaskSchema, db: Session = Depends(get_db)):
    db.add(Tasks(new_task))
    db.commit()
    return new_task


@app.get("/notes/", status_code=200)
async def get_notes(db: Session = Depends(get_db)):
    users = db.query(Notes).all()
    return users



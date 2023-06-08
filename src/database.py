import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models import Tasks, Users, Notes
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data"
DB_NAME = "test"
DATABASE_URL = 'sqlite:///' + os.path.join(basedir, DB_NAME + '.db')

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:chon2185@localhost:32768/test"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    #Cargo datos iniciales de prueba
    with Session(engine) as session:
        users = session.exec(select(Users)).all()
        tasks = session.exec(select(Tasks)).all()
        notes = session.exec(select(Notes)).all()
        if len(users) == 0 and len(tasks) == 0 and len(notes) == 0:
            user1 = Users(username="Pepe Argento", password="123456")
            user2 = Users(username="chon", password="chon2185")
            user3 = Users(username="Juan Perez", password="lalalala")

            task1 = Tasks(title="Tarea 1", description="Tarea de prueba 1", owners=[user1, user2])
            task2 = Tasks(title="Tarea 2", description="Tarea de prueba 2", owners=[user3])
            task3 = Tasks(title="Tarea 3", description="Tarea de prueba 3", owners=[user1, user3])
            task4 = Tasks(title="Tarea 4", description="Tarea de prueba 4", owners=[user1])

            note1 = Notes(note="Nota de prueba 1", date=datetime.now(), user=user1, task=task1)
            note2 = Notes(note="Nota de prueba 2", date=datetime.now(), user=user2, task=task3)

            session.add_all([user1, user2, user3, task1, task2, task3, task4, note1, note2])
            session.commit()
            
            # El id es generado luego del commit, ahora puedo asignar los usuarios
            task1.started_by_id = user1.id   # Asigno un usuario que inicia task1
            task2.finished_by_id = user2.id
            task3.canceled_by_id = user3.id
            
            # O crear una entera, por ejemplo
            task5 = Tasks(  title="Tarea 5", 
                            description="Tarea de prueba 5", 
                            owners=[user2, Users(username="Homero Simpson", password="alalalala")], # Creo un usuario en la declaracion!
                            started_by_id=user1.id,
                            canceled_by_id=user2.id,
                            finished_by_id=user1.id,
                            notes=[Notes(note="Nota de prueba 1", date=datetime.now(), user=user1, task=task1)] # También una nota!
                        )
            
            session.add_all([task1, task2, task3, task5])
            session.commit()

        # Ver como se muestra en el mensaje cómo todos los campos están relacionados, en started, canceled, finished y en notes
        for task in tasks:
            task_msg =f"""
            {task.title}: {task.description}
            owners: {[owner.username for owner in task.owners]}, 
            started: {task.started_by.username if task.started_by is not None else ""},     
            canceled: {task.canceled_by.username if task.canceled_by is not None else ""},
            finished: {task.finished_by.username if task.finished_by is not None else ""},
            notes: {[f'{note.user.username} - {note.note}' for note in task.notes]}"
            """
            print(task_msg)
            
            




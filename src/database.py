import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from models import Tasks, Users

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data"
DB_NAME = "test"
DATABASE_URL = 'sqlite:///' + os.path.join(basedir, DB_NAME + '.db')

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:chon2185@localhost:32768/test"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Cargo datos iniciales de prueba
    # with Session(engine) as session:
    #     users = session.exec(select(Users)).all()
    #     tasks = session.exec(select(Tasks)).all()
    #     if len(users) == 0 and len(tasks) == 0:
    #         user1 = Users(username="Pepe Argento", password="123456")
    #         user2 = Users(username="chon", password="chon2185")
    #         user3 = Users(username="Juan Perez", password="lalalala")

    #         task1 = Tasks(title="Tarea 1", description="Tarea de prueba 1", owners=[user1, user2], started_by=user3)
    #         task2 = Tasks(title="Tarea 2", description="Tarea de prueba 2", owners=[user3])
    #         task3 = Tasks(title="Tarea 3", description="Tarea de prueba 3", owners=[user1, user3])
    #         task4 = Tasks(title="Tarea 4", description="Tarea de prueba 4")

    #         # task1.started_by = user1        # Asigno un usuario que inicia task1
    #         # task1.owners = [user1, user2]   # Asigno owners a task1

    #         # task2.owners = [user2, user3]
    #         # task3.owners = [user1, user2]
    #         # task4.owners = [user1, user2, user3]

    #         session.add_all([user1, user2, user3, task1, task2, task3, task4])
    #         session.commit()
            
            




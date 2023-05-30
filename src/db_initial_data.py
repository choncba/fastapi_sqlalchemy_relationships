import database
from database import engine, SessionLocal
from models import Tasks, Users

def set_initial_data():
    database.Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        
        user1 = Users(username="Pepe Argento", password="123456")
        user2 = Users(username="chon", password="chon2185")
        user3 = Users(username="Juan Perez", password="lalalala")

        task1 = Tasks(title="Tarea 1", description="Tarea de prueba 1")
        task2 = Tasks(title="Tarea 2", description="Tarea de prueba 2")
        task3 = Tasks(title="Tarea 3", description="Tarea de prueba 3")
        task4 = Tasks(title="Tarea 4", description="Tarea de prueba 4")

        task1.owners = [user1]
        task2.owners = [user2, user3]
        task3.owners = [user1, user2]
        task4.owners = [user1, user2, user3]

        session.add_all([user1, user2, user3, task1, task2, task3, task4])

        session.commit()



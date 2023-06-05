# FastAPI SQLAlchemy

Test de relaciones en la BD

## VER 
https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/
https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
https://launchschool.com/books/sql/read/table_relationships
https://lightrun.com/solutions/tiangolo-fastapi-how-to-use-pydantic-and-sqlalchemy-models-with-relationship/
https://misovirtual.virtual.uniandes.edu.co/codelabs/tutorial-SQLAlchemy-Python-ejemplo/index.html?index=..%2F..index#5
https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/
https://sqlmodel.tiangolo.com/

## MySQL workbench
Traslator to sqlalchemy https://github.com/PiTiLeZarD/workbench_alchemy


## Alembic
Utilizo Alembic para las migraciones de la BD y creación de Tablas.
Ver: https://testdriven.io/blog/fastapi-sqlmodel/#alembic

- Comento la parte de creación de Tablas en main.py:
```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```
- Inicio Alembic, dentro de la carpeta src:
```
pipenv run alembic init alembic
```
- Edito alembic.ini y env.py para agregar sqlmodel y apuntar a mi BD
- Genero la primer versión, --autogenerate genera automáticamente el código de las tablas en la versión de alembic
```
alembic revision --autogenerate -m "init"
```
- Ejecuto la migración
```
pipenv run alembic upgrade head
```
(O utilizar el id de la versión en lugar de head)



import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_NAME = "test"

basedir = os.path.abspath(os.path.dirname(__file__)) + "/data"
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, DB_NAME + '.db')

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:chon2185@localhost:32768/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
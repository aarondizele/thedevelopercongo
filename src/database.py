from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from os import getenv

from src import models


SQLALCHEMY_DATABASE_URL = 'sqlite:///./thedevelopercongo.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@postgresserver/db'
# SQLALCHEMY_DATABASE_URL = f'{getenv("DB_CONNECTION")}://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Database:
    def create_db_and_tables():
        models.Base.metadata.create_all(bind=engine)

    def session():
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()

        db: Session = Depends(get_db)
        return db
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from src import models

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:username@localhost/youtube'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Database:
    def init():
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
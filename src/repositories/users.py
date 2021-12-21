from fastapi import status, HTTPException
from src import models, schemas
from src.hashing import Hash
from src.database import Database


class UserRepository:
    
    def create_user(request: schemas.Signup, db = Database.session()):
        new_user = models.User(firstname=request.firstname, lastname=request.lastname, email=request.email, hashed_password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


    def get_user(id: str, db = Database.session()):
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

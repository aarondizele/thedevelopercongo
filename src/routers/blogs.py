from fastapi import APIRouter, status, Depends
from typing import List, Optional
from src import models, schemas, oauth2
from src.hashing import Hash
from src.database import Database
from src.repositories.blogs import BlogRepository


router = APIRouter(
    prefix="/v1/blogs",
    tags=["Blogs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.InsertBlog, db=Database.session()):
    return BlogRepository.create(request, db)

@router.get("/", response_model=List[schemas.Blog])
def all(
    db=Database.session(),
    current_user: schemas.User = Depends(oauth2.get_current_active_user),
):
    return BlogRepository.all(current_user, db)

@router.get("/{id}", response_model=schemas.Blog)
def show(id: str, db=Database.session()):
    return BlogRepository.show(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str, db=Database.session()):
    return BlogRepository.delete(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: str, request: schemas.InsertBlog, db=Database.session()):
    return BlogRepository.update(id, request, db)

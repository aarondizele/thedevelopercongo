import shutil
from typing import List
from fastapi import APIRouter, status, UploadFile, File
from src import models, schemas
from src.hashing import Hash
from src.database import Database
from src.repositories.users import UserRepository
import os
from uuid import uuid4

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

sep = os.path.sep
cur_dir = os.getcwd() + sep

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(request: schemas.Signup, db = Database.session()):
    print(request.dict())
    return UserRepository.create_user(request, db)


@router.get('/{id}', response_model=schemas.User)
def get_user(id: str, db = Database.session()):
    return UserRepository.get_user(id, db)

@router.post("/upload")
async def upload_profile(file: UploadFile = File(...)):
    with open(cur_dir + "files" + sep + uuid4().hex, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        # content = await file.read()
        # buffer.write(content)cls
        # buffer.close()
    return {"filename": file.filename}
    # return {"filename": file.filename, "content_type": file.content_type}

@router.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    # return {"filenames": [file.filename for file in files]}
    for file in files:
        with open(cur_dir + "files" + sep + uuid4().hex, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"msg": "success"}

from typing import List
from fastapi import APIRouter, status, UploadFile, File
from .. import models, schemas
from ..hashing import Hash
from ..database import Database
from ..repositories.users import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(request: schemas.Signup, db = Database.session()):
    return UserRepository.create_user(request, db)


@router.get('/{id}', response_model=schemas.User)
def get_user(id: str, db = Database.session()):
    return UserRepository.get_user(id, db)

@router.post("/upload")
async def upload_profile(file: UploadFile = File(...)):
    return {"filename": file.filename, "content_type": file.content_type}

@router.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
from .. import schemas, models, oauth2, keys
from ..database import Database
from ..hashing import Hash
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authenticate"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, keys.SECRET_KEY, algorithm=keys.ALGORITHM)
    return encoded_jwt


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db=Database.session()):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Invalid Credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not Hash.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=404, 
            detail="Incorrect password", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=keys.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/user/me', response_model=schemas.User, response_model_exclude={"blogs"})
async def get_current_user(current_user: schemas.User = Depends(oauth2.get_current_active_user)):
    return current_user
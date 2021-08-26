from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import sys
import token
sys.path.append("..")
import database, models
from sqlalchemy.orm import Session
from hashing import Hash
from . import token

router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User, models.Role.name).join(models.Role).filter(models.User.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    if not Hash.verify(request.password, user.User.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    
    access_token = token.create_access_token(data={"sub": user.User.email, "scopes": [user.name]})
    return {"access_token": access_token, "token_type": "bearer"}
    
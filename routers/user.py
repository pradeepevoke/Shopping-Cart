from typing import List
from fastapi import APIRouter, Depends, Security, status
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session
from repository import user, role
from routers.oauth2 import get_current_user

router = APIRouter(
    tags=['Users']
)

@router.get('/users', response_model=List[schemas.ShowUser])
def getUsers(db: Session = Depends(database.get_db), current_user: models.User = Security(get_current_user, scopes=['admin'])):
    try:
        return user.get_all(db)
    except Exception as e:
        return e

@router.post('/user/register', status_code=status.HTTP_201_CREATED)
def register(request: schemas.Register, db: Session = Depends(database.get_db)):
    if role.show(request.role_id, db):
        return user.create(request, db)

@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return user.delete(id, db)

@router.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return user.update(id, request, db)   

@router.get('/user/{id}', status_code=200, response_model=schemas.ShowUser)
def getUsers(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):   
    return user.show(id, db)
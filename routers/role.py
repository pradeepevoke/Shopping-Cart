from typing import List
from fastapi import APIRouter, Depends, Security, status
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session
from repository import role
from routers.oauth2 import get_current_user

router = APIRouter(
    tags=['Roles']
)

@router.get('/roles', response_model=List[schemas.Roles])
def getRoles(db: Session = Depends(database.get_db), current_user: models.User = Security(get_current_user)):
    try:
        return role.get_all(db)
    except Exception as e:
        return e

@router.post('/role/add', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Roles, db: Session = Depends(database.get_db)):
    return role.create(request, db)

@router.delete('/role/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return role.delete(id, db)

@router.get('/role/{id}', status_code=200, response_model=schemas.Roles)
def getRole(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):   
    return role.show(id, db)
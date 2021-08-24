from routers.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status, HTTPException
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session
from repository import category

router = APIRouter(
    tags=['Category']
)

@router.get('/categories')
def getCategories(db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):   
    return category.get_all(db)

@router.post('/category/add', status_code=status.HTTP_201_CREATED)
def create_category(request: schemas.Category, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return category.create(request, db)

@router.delete('/category/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return category.delete(id, db)

@router.put('/category/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Category, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return category.update(id, request, db)    

@router.get('/category/{id}', status_code=200)
def getCategory(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):   
    return category.show(id, db)
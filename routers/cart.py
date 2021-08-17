from typing import List
from fastapi import APIRouter, Depends, status
import sys
sys.path.append("..")
import database, schemas
from sqlalchemy.orm import Session
from repository import cart

router = APIRouter(
    tags=['Cart']
)

@router.get('/cart', response_model=List[schemas.ShowCart])
def getCart(user_id:int, db: Session = Depends(database.get_db)):   
    return cart.get_all(user_id, db)

@router.post('/cart/add', status_code=status.HTTP_201_CREATED)
def addCart(request: schemas.Cart, db: Session = Depends(database.get_db)):
    return cart.create(request, db)    

@router.delete('/cart/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
    return cart.delete(id, db)

@router.put('/cart/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Cart, db: Session = Depends(database.get_db)):
    return cart.update(id, request, db)   

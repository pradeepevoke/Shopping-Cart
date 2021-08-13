from typing import List
from fastapi import APIRouter, Depends, status
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/cart/add', status_code=status.HTTP_201_CREATED, tags=['Cart'])
def addCart(request: schemas.Cart, db: Session = Depends(database.get_db)):
    data = models.Cart(user_id=request.user_id, product_id=request.product_id, quantity=request.quantity)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.delete('/cart/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Cart'])
def destroy(id, db: Session = Depends(database.get_db)):
    db.query(models.Cart).filter(models.Cart.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@router.put('/cart/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Cart'])
def update(id, request: schemas.Cart, db: Session = Depends(database.get_db)):
    db.query(models.Cart).filter(models.Cart.id == id).update({"user_id":request.user_id, "product_id":request.product_id, "quantity":request.quantity})
    db.commit()
    return "Updated Successfully"    

@router.get('/cart', response_model=List[schemas.ShowCart], tags=['Cart'])
def getCart(db: Session = Depends(database.get_db)):   
    return db.query(models.Cart).all()
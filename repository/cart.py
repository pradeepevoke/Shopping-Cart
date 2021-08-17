from fastapi import status, HTTPException
from sqlalchemy.orm.session import Session
import sys
sys.path.append("..")
import schemas, models

def get_all(id, db: Session):
    return db.query(models.Cart).filter(models.Cart.user_id == id).all()

def create(request: schemas.Cart, db: Session):
    data = models.Cart(user_id=request.user_id, product_id=request.product_id, quantity=request.quantity)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def delete(id, db: Session):
    cart = db.query(models.Cart).filter(models.Cart.id == id)
    if not cart.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Cart with id {id} not found')
    cart.delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

def update(id, request: schemas.Cart, db: Session):
    db.query(models.Cart).filter(models.Cart.id == id).update({"user_id":request.user_id, "product_id":request.product_id, "quantity":request.quantity})
    db.commit()
    return "Updated Successfully" 
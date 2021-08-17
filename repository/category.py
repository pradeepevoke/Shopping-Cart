from fastapi import status, HTTPException
from sqlalchemy.orm.session import Session
import sys
sys.path.append("..")
import schemas, models

def get_all(db: Session):
    return db.query(models.Category).all()

def create(request: schemas.Category, db: Session):
    data = models.Category(name=request.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def delete(id, db: Session):
    category = db.query(models.Category).filter(models.Category.id == id)
    if not category.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Category with id {id} not found')
    
    category.delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

def update(id, request: schemas.Category, db: Session):
    db.query(models.Category).filter(models.Category.id == id).update({"name":request.name})
    db.commit()
    return "Updated Successfully"

def show(id, db: Session):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Category with id {id} not found')
    return category

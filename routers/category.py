from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/category/add', status_code=status.HTTP_201_CREATED, tags=['Category'])
def create_category(request: schemas.Category, db: Session = Depends(database.get_db)):
    data = models.Category(name=request.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.delete('/category/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Category'])
def destroy(id, db: Session = Depends(database.get_db)):
    db.query(models.Category).filter(models.Category.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@router.put('/category/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Category'])
def update(id, request: schemas.Category, db: Session = Depends(database.get_db)):
    db.query(models.Category).filter(models.Category.id == id).update({"name":request.name})
    db.commit()
    return "Updated Successfully"    

@router.get('/categories', tags=['Category'])
def getCategories(db: Session = Depends(database.get_db)):   
    return db.query(models.Category).all()

@router.get('/category/{id}', status_code=200, tags=['Category'])
def getCategory(id, db: Session = Depends(database.get_db)):   
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Category with id {id} not found')
    return category
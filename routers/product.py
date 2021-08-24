from fastapi import APIRouter, Depends, status, File, UploadFile
import sys
from typing import List
sys.path.append("..")
import database, schemas
from sqlalchemy.orm import Session
from repository import product
from routers.oauth2 import get_current_user

router = APIRouter(
    tags=['Product']
)

@router.get('/products', response_model=List[schemas.Product])
def getProducts(db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):   
    return product.get_all(db)

@router.post('/product/add', status_code=status.HTTP_201_CREATED)
def create_product(name: str = File(...), category_id: int = File(...), description: str = File(...), price: int = File(...), image: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return product.create(name, category_id, description, price, image, db)
    
@router.delete('/product/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return product.delete(id, db)

@router.put('/product/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, name: str = File(...), category_id: int = File(...), description: str = File(...), price: int = File(...), image: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return product.update(id, name, category_id, description, price, image, db)

@router.get('/product/{id}', status_code=200, response_model=schemas.Product)
def getProduct(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):   
    return product.show(id, db)

@router.get("/product/export/excel")
async def exportExcel(db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return product.excel(db)

@router.get("/product/export/pdf/{id}")
async def exportPDF(id, db: Session = Depends(database.get_db), current_user: schemas.ShowUser = Depends(get_current_user)):
    return product.pdf(id, db)
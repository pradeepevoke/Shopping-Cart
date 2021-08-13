from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session
from io import BytesIO
import xlsxwriter
from starlette.responses import StreamingResponse

router = APIRouter()

@router.post('/product/add', status_code=status.HTTP_201_CREATED, tags=['Product'])
def create_product(name: str = File(...), category_id: int = File(...), description: str = File(...), price: int = File(...), image: UploadFile = File(...), db: Session = Depends(database.get_db)):
    file_path = ""
    if image:
        import os
        from datetime import datetime
        file_base, extension = os.path.splitext(image.filename)
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        file_path = os.getcwd()+"/images/"+file_base.replace(" ", "-")+"-"+dt_string+extension
        with open(file_path,'wb+') as f:
            f.write(image.file.read())
            f.close()

    data = models.Product(name=name, category_id=category_id, image=file_path, description=description, price=price)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.delete('/product/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Product'])
def destroy(id, db: Session = Depends(database.get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@router.put('/product/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Product'])
def update(id, name: str = File(...), category_id: int = File(...), description: str = File(...), price: int = File(...), image: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if image:
        import os
        from datetime import datetime
        file_base, extension = os.path.splitext(image.filename)
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        file_path = os.getcwd()+"/images/"+file_base.replace(" ", "-")+"-"+dt_string+extension
        with open(file_path,'wb+') as f:
            f.write(image.file.read())
            f.close()
            
    db.query(models.Product).filter(models.Product.id == id).update({"name":name, "category_id":category_id, "image":file_path, "description":description, "price":price})
    db.commit()
    return "Updated Successfully"    

@router.get('/products', tags=['Product'])
def getProducts(db: Session = Depends(database.get_db)):   
    return db.query(models.Product).all()

@router.get('/product/{id}', status_code=200, tags=['Product'])
def getProduct(id, db: Session = Depends(database.get_db)):   
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
    return product


@router.get("/product/export/excel", response_model=List[schemas.Product], tags=['Product'])
async def exportExcel(db: Session = Depends(database.get_db)):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Name')
    worksheet.write(0, 1, 'Description')
    worksheet.write(0, 2, 'Price')
    worksheet.write(0, 3, 'Image')
    worksheet.write(0, 3, 'Category')

    data = db.query(models.Product).all()
    
    workbook.close()
    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="filename.xlsx"'
    }
    return StreamingResponse(output, headers=headers)
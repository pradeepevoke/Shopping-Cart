from fastapi import status, HTTPException, Response
from sqlalchemy.orm.session import Session
import sys
sys.path.append("..")
import models

from io import BytesIO
import xlsxwriter
import fpdf
from starlette.responses import StreamingResponse


def get_all(db: Session):
    return db.query(models.Product).all()

def create(name, category_id, description, price, image, db: Session):
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

def delete(id, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
    product.delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

def update(id, name, category_id, description, price, image, db: Session):
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

def show(id, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
    return product

def excel(db: Session):
    from datetime import datetime
    
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Name')
    worksheet.write(0, 1, 'Description')
    worksheet.write(0, 2, 'Price')
    worksheet.write(0, 3, 'Image')
    worksheet.write(0, 4, 'Category')

    data = db.query(models.Product, models.Category.name).join(models.Category).all()
    
    index = 1
    for product in data:
        worksheet.write(index, 0, product.Product.name)
        worksheet.write(index, 1, product.Product.description)
        worksheet.write(index, 2, product.Product.price)
        # worksheet.write(index, 3, product.Product.image)
        worksheet.insert_image(index, 3, product.Product.image, {'x_scale': 0.1, 'y_scale': 0.1})
        worksheet.write(index, 4, product.name)
        index = index+1

    workbook.close()
    output.seek(0)
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    filename = "product" + dt_string +".xlsx"
    headers = {
        'Content-Disposition': 'attachment; filename="%s"' %(filename)
    }
    return StreamingResponse(output, headers=headers)

def pdf(id, db: Session):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    data = db.query(models.Product, models.Category.name).join(models.Category).filter(models.Product.id == id)
    if data:
        pdf.cell(0, 10, "Shopping Cart", 0,1,'C')
        pdf.line(10, 20, 200, 20)
        for product in data:
            pdf.cell(0, 10, 'Name : ' + product.Product.name, 0, 1)
            pdf.cell(0, 10, 'Description : ' + product.Product.description, 0, 1)
            pdf.cell(0, 10, 'Price : ' + str(product.Product.price), 0, 1)
            pdf.image(product.Product.image, 115, 25, 60,40)
            pdf.cell(0, 10, 'Category : ' + product.name, 0, 1)
        
        filename = "testing.pdf"
        headers = {
            'Content-Disposition': 'attachment; content-type: application/octet-stream; filename='+filename
        }
        return Response(pdf.output(dest='S').encode('latin-1'), media_type="application/pdf", headers=headers)
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
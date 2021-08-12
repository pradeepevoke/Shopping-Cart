from typing import List
from sqlalchemy.sql.expression import false
from fastapi import FastAPI, Depends, status, HTTPException, File, UploadFile
import schemas
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        pass
    finally:
        db.close()

@app.post('/user/register', status_code=status.HTTP_201_CREATED, tags=['Users'])
def register(request: schemas.Register, db: Session = Depends(get_db)):
    data = models.User(firstname=request.firstname, lastname=request.lastname, email=request.email, password=Hash.bcrypt(request.password), mobile=request.mobile, address=request.address)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Users'])
def update(id, request: schemas.Register, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).update({"firstname":request.firstname, "lastname":request.lastname, "email":request.email, "mobile":request.mobile, "address":request.address})
    db.commit()
    return "Updated Successfully"    

@app.get('/users', response_model=List[schemas.ShowUser], tags=['Users'])
def getUsers(db: Session = Depends(get_db)):   
    users = db.query(models.User).all()
    return users

@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=['Users'])
def getUsers(id, db: Session = Depends(get_db)):   
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user


@app.post('/category/add', status_code=status.HTTP_201_CREATED, tags=['Category'])
def create_category(request: schemas.Category, db: Session = Depends(get_db)):
    data = models.Category(name=request.name)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.delete('/category/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Category'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Category).filter(models.Category.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@app.put('/category/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Category'])
def update(id, request: schemas.Category, db: Session = Depends(get_db)):
    db.query(models.Category).filter(models.Category.id == id).update({"name":request.name})
    db.commit()
    return "Updated Successfully"    

@app.get('/categories', tags=['Category'])
def getCategories(db: Session = Depends(get_db)):   
    return db.query(models.Category).all()

@app.get('/category/{id}', status_code=200, tags=['Category'])
def getCategory(id, db: Session = Depends(get_db)):   
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Category with id {id} not found')
    return category


@app.post('/product/add', status_code=status.HTTP_201_CREATED, tags=['Product'])
def create_product(name: str = File(...), category_id: int = File(...), description: str = File(...), price: int = File(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
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

@app.delete('/product/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Product'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@app.put('/product/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Product'])
def update(id, name: str = File(...), category_id: int = File(...), description: str = File(...), price: int = File(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
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

@app.get('/products', tags=['Product'])
def getProducts(db: Session = Depends(get_db)):   
    return db.query(models.Product).all()

@app.get('/product/{id}', status_code=200, tags=['Product'])
def getProduct(id, db: Session = Depends(get_db)):   
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')
    return product

@app.post('/cart/add', status_code=status.HTTP_201_CREATED, tags=['Cart'])
def addCart(request: schemas.Cart, db: Session = Depends(get_db)):
    data = models.Cart(user_id=request.user_id, product_id=request.product_id, quantity=request.quantity)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.delete('/cart/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Cart'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Cart).filter(models.Cart.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@app.put('/cart/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Cart'])
def update(id, request: schemas.Cart, db: Session = Depends(get_db)):
    db.query(models.Cart).filter(models.Cart.id == id).update({"user_id":request.user_id, "product_id":request.product_id, "quantity":request.quantity})
    db.commit()
    return "Updated Successfully"    

@app.get('/cart', tags=['Cart'])
def getCategories(db: Session = Depends(get_db)):   
    return db.query(models.Cart).all()

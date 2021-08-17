from fastapi import status, HTTPException
from sqlalchemy.orm.session import Session
import sys
sys.path.append("..")
import schemas, models
from hashing import Hash

def get_all(db: Session):
    return db.query(models.User).all()

def create(request: schemas.Register, db: Session):
    data = models.User(firstname=request.firstname, lastname=request.lastname, email=request.email, password=Hash.bcrypt(request.password), mobile=request.mobile, address=request.address)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def delete(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    user.delete(synchronize_session=False)
    db.commit()
    return {"user deleted"}

def update(id, request: schemas.Register, db: Session):
    db.query(models.User).filter(models.User.id == id).update({"firstname":request.firstname, "lastname":request.lastname, "email":request.email, "mobile":request.mobile, "address":request.address})
    db.commit()
    return "Updated Successfully" 

def show(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user
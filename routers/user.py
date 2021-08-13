from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import sys
sys.path.append("..")
import database, schemas, models
from sqlalchemy.orm import Session
from hashing import Hash

router = APIRouter()

@router.get('/users', response_model=List[schemas.ShowUser], tags=['Users'])
def getUsers(db: Session = Depends(database.get_db)):   
    users = db.query(models.User).all()
    return users

@router.post('/user/register', status_code=status.HTTP_201_CREATED, tags=['Users'])
def register(request: schemas.Register, db: Session = Depends(database.get_db)):
    data = models.User(firstname=request.firstname, lastname=request.lastname, email=request.email, password=Hash.bcrypt(request.password), mobile=request.mobile, address=request.address)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
def destroy(id, db: Session = Depends(database.get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@router.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Users'])
def update(id, request: schemas.Register, db: Session = Depends(database.get_db)):
    db.query(models.User).filter(models.User.id == id).update({"firstname":request.firstname, "lastname":request.lastname, "email":request.email, "mobile":request.mobile, "address":request.address})
    db.commit()
    return "Updated Successfully"    

@router.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=['Users'])
def getUsers(id, db: Session = Depends(database.get_db)):   
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user
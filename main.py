from sqlalchemy.sql.expression import false
from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

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

@app.post('/user/register', status_code=status.HTTP_201_CREATED)
def register(request: schemas.Register, db: Session = Depends(get_db)):
    data = models.User(firstname=request.firstname, lastname=request.lastname, email=request.email, password=request.password, mobile=request.mobile, address=request.address)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return {"data":"deleted"}

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Register, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    return user
    db.commit()
    return "Updated Successfully"    

@app.get('/users')
def getUsers(db: Session = Depends(get_db)):   
    users = db.query(models.User).all()
    return users

@app.get('/user/{id}', status_code=200)
def getUsers(id, response:Response, db: Session = Depends(get_db)):   
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user
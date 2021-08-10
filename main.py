from fastapi import FastAPI, Depends
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

@app.post('/user/register')
def register(request: schemas.Register, db: Session = Depends(get_db)):
    data = models.User(firstname=request.firstname, lastname=request.lastname, email=request.email, password=request.password, mobile=request.mobile, address=request.address)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.get('/user/{id}')
def show(id:int):
    #fetch user with id
    return {'user_id': id}
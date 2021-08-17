from fastapi import APIRouter, Depends, HTTPException, status
import sys
import token
sys.path.append("..")
import schemas, database, models
from sqlalchemy.orm import Session
from hashing import Hash
from . import token
router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    
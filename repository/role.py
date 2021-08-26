from fastapi import status, HTTPException
from sqlalchemy.orm.session import Session
import sys
sys.path.append("..")
import schemas, models

def get_all(db: Session):
    return db.query(models.Role).all()

def create(request: schemas.Roles, db: Session):
    data = models.Role(name=request.name, description=request.description)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def delete(id, db: Session):
    role = db.query(models.Role).filter(models.Role.id == id)
    if not role.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Role with id {id} not found')
    role.delete(synchronize_session=False)
    db.commit()
    return {"role deleted"}

def show(id, db: Session):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Role with id {id} not found')
    return role
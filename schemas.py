from models import Product
from pydantic import BaseModel

class Register(BaseModel):
    firstname: str
    lastname: str
    password: str
    email: str
    mobile: str
    address: str

class ShowUser(BaseModel):
    id : int
    firstname: str
    lastname: str
    email: str
    mobile: str
    address: str

    class Config:
        orm_mode = True

class Category(BaseModel):
    name: str

class Cart(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

from models import Role
from typing import List
from pydantic import BaseModel
from typing import Optional

class Roles(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True
        
class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    mobile: str
    address: str

class ShowUser(User):
    id : int
    user_role: Roles

    class Config:
        orm_mode = True

class Register(User):
    role_id: int
    password: str

class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Cart(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class Product(BaseModel):
    name: str
    image: str
    description: str
    price: int
    category: Category

    class Config:
        orm_mode = True

class ShowCart(BaseModel):
    id: int
    quantity: int
    products: Product

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: List[str] = []



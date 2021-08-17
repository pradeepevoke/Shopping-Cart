from pydantic import BaseModel
from typing import Optional

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
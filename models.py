from typing import Text
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    email = Column(String)
    mobile = Column(String)
    address = Column(String)

    # cart = relationship("Cart", back_populates="user")

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    # product = relationship("Product", back_populates='category')

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("category.id", ondelete='CASCADE'))
    image = Column(String)
    description = Column(Text)
    price = Column(Integer)

    category = relationship("Category", backref="products")

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    quantity = Column(Integer)

    user = relationship("User", backref="carts")
    products = relationship("Product", backref="carts")
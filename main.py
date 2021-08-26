from fastapi import FastAPI
import models
from database import engine
from routers import authentication, cart, product, user, category, role

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)







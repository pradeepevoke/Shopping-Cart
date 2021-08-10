from pydantic import BaseModel

class Register(BaseModel):
    password: str
    firstname: str
    lastname: str
    mobile: str
    email: str
    address: str

from pydantic import BaseModel

class Register(BaseModel):
    firstname: str
    lastname: str
    password: str
    email: str
    mobile: str
    address: str

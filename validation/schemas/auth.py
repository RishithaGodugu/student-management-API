from pydantic import BaseModel,Field

class UserRegister(BaseModel):
    email:str
    password:str=Field(min_length=8)

class UserLogin(BaseModel):
    email:str
    password:str
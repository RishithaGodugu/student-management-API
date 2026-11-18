from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    name:str=Field(min_length=3,max_length=50)
    age:int=Field(ge=16,le=60)
    course:str


class StudentPatch(BaseModel):
    name:str|None=Field(default=None,min_length=3,max_length=50)
    age:int|None=Field(default=None,ge=16,le=60)
    course:str|None=None
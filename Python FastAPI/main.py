# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Welcome to my API"}

# @app.get("/students")
# def get_students():
#     return [
#         {"id": 1, "name": "Ravi"},
#         {"id": 2, "name": "Priya"},
#         {"id": 3, "name": "ristha"}
#     ]

# @app.get("/courses")
# def get_courses():
#     return [
#         {"id":1,"course":"python"},
#         {"id":2,"course":"sql"}
#     ]



from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

students=[ {"id":1,"name":"Ravi","course":"python"},
          {"id":2,"name":"priya","course":"java"}]

class student(BaseModel):
    name:str
    course:str

@app.get("/students")
def get_students():
    return students

@app.post("/students",status_code=201)
def add_student(student:student):

    new_student={
        "id":len(student)+1,
        "name":student.name,
        "course":student.course
    }

    students.append(new_student)
    return{
        "message":"Student added successfully",
        "student":new_student
    }
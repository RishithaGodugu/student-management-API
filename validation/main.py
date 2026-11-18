# from fastapi import FastAPI
# from .routers.students import router as students_router

# app=FastAPI()

# app.include_router(
#     students_router,
#     prefix="/students",
#     tags=["students"]
# )

# @app.get("/")
# def home():
#     return {"message":"Welcome to my API"}




# ##########################################################

# #  from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel, Field
# # from .database import get_connection

# # app=FastAPI()

# # class studentPatch(BaseModel):
# #     name: str | None = None
# #     age: int | None = None
# #     course: str | None = None


# # class student(BaseModel):
# #     name:str=Field(min_length=3,max_length=50)
# #     age:int=Field(ge=16,le=60)
# #     course:str

# # @app.post("/students",status_code=201)
# # def add_student(student:student):

# #     connection=get_connection()
# #     cursor=connection.cursor()

# #     try:
# #         query=""" 
# #         INSERT INTO students(name,age,course)
# #         VALUES (%s,%s,%s)
# #         """

# #         values=(student.name,student.age,student.course)

# #         cursor.execute(query, values)
# #         connection.commit()

# #         return {
# #             "message":"Student added successfully",
# #             "student_id":cursor.lastrowid,
# #             "name":student.name
# #         }

# #     except Exception as e:
# #         connection.rollback()
# #         print("DATABASE ERROR:",repr(e))

# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not add student.check terminal"
# #         )

# #     finally:
# #         cursor.close()
# #         connection.close()

# # @app.get("/students")
# # def get_students():

# #     connection=get_connection()
# #     cursor=connection.cursor(dictionary=True)

# #     try:
# #         query="SELECT * FROM students"

# #         cursor.execute(query)

# #         students=cursor.fetchall()

# #         return {
# #             "total_students":len(students),
# #             "students": students
# #         }

# #     except Exception as e:
# #         print("DATABASE ERROR:",repr(e))
# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not retrieve students"
# #         )

# #     finally:
# #         cursor.close()
# #         connection.close()

# # @app.get("/students/{student_id}")
# # def get_student(student_id:int):

# #     connection=get_connection()
# #     cursor=connection.cursor(dictionary=True)

# #     try:
# #         query="SELECT * FROM students WHERE id=%s"

# #         values=(student_id,)
# #         cursor.execute(query,values)
# #         student=cursor.fetchone()

# #         if student is None:
# #             raise HTTPException(
# #                 status_code=404,
# #                 detail="Student not found"
# #             )
# #         return student

# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         print("DATABASE ERROR:",repr(e))
# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not retrieve student"
# #         )

# #     finally:
# #         cursor.close()
# #         connection.close()

# # @app.put("/students/{student_id}")
# # def update_student(student_id:int,student:student):

# #     connection=get_connection()
# #     cursor=connection.cursor()

# #     try:
# #         cursor.execute(
# #             "SELECT id FROM students WHERE id=%s",
# #             (student_id,)
# #         )

# #         existing=cursor.fetchone()

# #         if existing is None:
# #             raise HTTPException(
# #                 status_code=404,
# #                 detail="Student not found"
# #             )

# #         query=""" UPDATE students SET name=%s,age=%s,course=%s WHERE id=%s"""
# #         values=(
# #             student.name,student.age,student.course,student_id
# #         )

# #         cursor.execute(query,values)
# #         connection.commit()

# #         return {
# #             "message":"Student updated successfully",
# #             "student_id":student_id
# #         }

# #     except HTTPException:
# #         raise

# #     except Exception as e:
# #         connection.rollback()
# #         print("DATABASE ERROR:",repr(e))
# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not update student"
# #         )

# #     finally:
# #         cursor.close()
# #         connection.close()



# # @app.patch("/students/{student_id}")
# # def patch_student(student_id: int, student: studentPatch):

# #     connection = get_connection()
# #     cursor = connection.cursor()

# #     try:
# #         cursor.execute(
# #             "SELECT id FROM students WHERE id = %s",
# #             (student_id,)
# #         )

# #         existing = cursor.fetchone()

# #         if existing is None:
# #             raise HTTPException(
# #                 status_code=404,
# #                 detail="Student not found"
# #             )

# #         # Get only fields supplied by the user
# #         updates = student.model_dump(exclude_unset=True)

# #         if not updates:
# #             raise HTTPException(
# #                 status_code=400,
# #                 detail="No fields provided for update"
# #             )

# #         # Build the UPDATE query using allowed model fields
# #         set_clause = ", ".join(
# #             f"{field} = %s" for field in updates
# #         )

# #         query = f"""
# #         UPDATE students
# #         SET {set_clause}
# #         WHERE id = %s
# #         """

# #         values = tuple(updates.values()) + (student_id,)

# #         cursor.execute(query, values)
# #         connection.commit()

# #         return {
# #             "message": "Student partially updated",
# #             "student_id": student_id,
# #             "updated_fields": updates
# #         }

# #     except HTTPException:
# #         raise

# #     except Exception as e:
# #         connection.rollback()
# #         print("DATABASE ERROR:", repr(e))
# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not update student"
# #         )

# #     finally:
# #         cursor.close()
# #         connection.close()

# # @app.delete("/students/{student_id}")
# # def delete_student(student_id:int):

# #     connection=get_connection()
# #     cursor=connection.cursor()

# #     try:
# #         cursor.execute(
# #             "SELECT id FROM students WHERE id=%s",(student_id,)
# #         )

# #         existing=cursor.fetchone()

# #         if existing is None:
# #             raise HTTPException(
# #                 status_code=404,
# #                 detail="Student not found"
# #             )

# #         query="DELETE FROM students WHERE id=%s"
# #         cursor.execute(query,(student_id,))
# #         connection.commit()

# #         return {
# #             "message":"Student deleted succesfully",
# #             "Student_id":student_id
# #         }
# #     except HTTPException:
# #         raise

# #     except Exception as e:
# #         connection.rollback()
# #         print("DATABASE ERROR:",repr(e))
# #         raise HTTPException(
# #             status_code=500,
# #             detail="Could not delete student"
# #         )

# #     finally:
# #         cursor.close()
# #         connection.close()

# ##################################################################


# #     new_student={
# #         "id":len(students)+1,
# #         "name":student.name,
# #         "age":student.age,
# #         "course":student.course
# #     }

# #     students.append(new_student)

# #     return {
# #         "message":"student registered successfully",
# #         "student":new_student
# #     }

# # @app.get("/students")
# # def get_students():
# #     return students

# # @app.get("/students/{student_id}")
# # def get_students(student_id:int):

# #     for student in students:
# #         if student["id"]==student_id:
# #             return student

# #     raise HTTPException(
# #         status_code=404,
# #         detail="Student not found"
# #     )


# # from fastapi import FastAPI
# # from database import get_connection

# # app=FastAPI()

# # @app.get("/students")
# # def get_students():

# #     connection=get_connection()
# #     cursor=connection.cursor(dictionary=True)

# #     cursor.execute("SELECT FROM students")

# #     students=cursor.fetchall()

# #     cursor.close()
# #     connection.close()

# #     return students

###################################################

import logging
import time
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware 
from .routers.students import router as students_router
from .routers.auth import router as auth_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)

logger=logging.getLogger(__name__)

app=FastAPI(
    title="student Management API",
    description="A FastAPI apllication connected to MySQL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_requests(request:Request,call_next):

    start_time=time.time()

    response=await call_next(request)

    process_time=time.time()-start_time

    logger.info("Method:%s",request.method)
    logger.info("URL:%s",request.url)
    logger.info("Status_code:%s",response.status_code)
    logger.info("Processing Time:%.4f",process_time)

    logger.error("Database connection failed")
    logger.warning("Invalid login attempt")
    logger.info("User logged in successfully")

    return response

app.include_router(
    students_router,
    prefix="/students",
    tags=["Students"]
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def home():
    return {
        "message":"Welcome to Student Management API"
    }
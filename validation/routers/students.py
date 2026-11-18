# from fastapi import APIRouter

# router=APIRouter()

# @router.get("/")
# def get_student():
#     return {
#         "message":"Student router is working"
#     }

# @router.get("/{studen_id}")
# def get_student(student_id:int):
#     return {
#         "message":"Stduent details",
#         "Stduent_id": student_id
#     }


from fastapi import APIRouter, HTTPException
from ..database import get_connection
from ..schemas.students import StudentCreate, StudentPatch

router = APIRouter()


# CREATE - Add student
@router.post("/", status_code=201)
def add_student(student: StudentCreate):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO students (name, age, course)
        VALUES (%s, %s, %s)
        """

        values = (student.name, student.age, student.course)

        cursor.execute(query, values)
        connection.commit()

        return {
            "message": "Student added successfully",
            "student_id": cursor.lastrowid
        }

    except Exception as e:
        connection.rollback()
        print("DATABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Could not add student")

    finally:
        cursor.close()
        connection.close()


# READ - Get all students
@router.get("/")
def get_students():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        return {
            "total_students": len(students),
            "students": students
        }

    except Exception as e:
        print("DATABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Could not retrieve students")

    finally:
        cursor.close()
        connection.close()


# READ - Get one student
@router.get("/{student_id}")
def get_student(student_id: int):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        return student

    except HTTPException:
        raise

    except Exception as e:
        print("DATABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Could not retrieve student")

    finally:
        cursor.close()
        connection.close()


# UPDATE - Replace all student fields
@router.put("/{student_id}")
def update_student(student_id: int, student: StudentCreate):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM students WHERE id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Student not found")

        query = """
        UPDATE students
        SET name = %s, age = %s, course = %s
        WHERE id = %s
        """

        values = (
            student.name,
            student.age,
            student.course,
            student_id
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "message": "Student updated successfully",
            "student_id": student_id
        }

    except HTTPException:
        raise

    except Exception as e:
        connection.rollback()
        print("DATABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Could not update student")

    finally:
        cursor.close()
        connection.close()


# UPDATE - Modify selected student fields
@router.patch("/{student_id}")
def patch_student(student_id: int, student: StudentPatch):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM students WHERE id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Student not found")

        updates = student.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )

        set_clause = ", ".join(
            f"{field} = %s" for field in updates.keys()
        )

        query = f"""
        UPDATE students
        SET {set_clause}
        WHERE id = %s
        """

        values = tuple(updates.values()) + (student_id,)

        cursor.execute(query, values)
        connection.commit()

        return {
            "message": "Student partially updated",
            "student_id": student_id,
            "updated_fields": updates
        }

    except HTTPException:
        raise

    except Exception as e:
        connection.rollback()
        print("DATABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Could not update student")

    finally:
        cursor.close()
        connection.close()


# DELETE - Remove student
@router.delete("/{student_id}")
def delete_student(student_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM students WHERE id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Student not found")

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        connection.commit()

        return {
            "message": "Student deleted successfully",
            "student_id": student_id
        }

    except HTTPException:
        raise

    except Exception as e:
        connection.rollback()
        print("DATABASE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Could not delete student")

    finally:
        cursor.close()
        connection.close()

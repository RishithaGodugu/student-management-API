from fastapi import APIRouter,HTTPException,Depends

from ..database import get_connection
from ..security import hash_password,verify_password
from ..schemas.auth import UserRegister,UserLogin
from ..tokens import create_access_token,get_current_user,require_role

router=APIRouter()

@router.post("/register",status_code=201)
def register_user(user:UserRegister):

    connection=get_connection()
    cursor=connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (user.email,)
        )

        if cursor.fetchone() is not None:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        hashed_password=hash_password(user.password)

        cursor.execute(
            """ INSERT INTO users (email,password_hash)
             VALUES (%s,%s) """,
             (user.email,hashed_password)
        )

        connection.commit()

        return {
            "message":"User registered successfully",
            "user_id":cursor.lastrowid
        }

    except HTTPException:
        raise

    except Exception as e:
        connection.rollback()
        print("DATABASE ERROR:",repr(e))
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

    finally:
        cursor.close()
        connection.close()

@router.post("/login")
def login_user(user:UserLogin):

    connection=get_connection()
    cursor=connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """ SELECT id,email,password_hash,role FROM users WHERE email=%s""",
            (user.email,)
        )

        db_user=cursor.fetchone()

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            user.password,
            db_user["password_hash"]
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token=create_access_token(db_user["id"],db_user["role"])

        return {
            "access_token":access_token,
            "token_type":"bearer"
        }

        # return {
        #     "message":"Login Successful",
        #     "user_id":db_user["id"],
        #     "email":db_user["email"]
        # }

    except HTTPException:
        raise

    except Exception as e:
        print("DATABASE ERROR:",repr(e))
        raise HTTPException(
            status_code=500,
            detail="Login failed"
        )

    finally:
        cursor.close()
        connection.close()

@router.get("/me")
def get_my_profile(
    current_user:dict=Depends(get_current_user)
):
    return {
        "message":"You are authenticated!",
        "user_id":current_user["user_id"]
    }

@router.get("/admin-dashboard")
def admin_dashboard(
    current_user:dict=Depends(require_role("admin"))
):
    return {
        "message":"Welcome to Admin Dashboard",
        "user_id":current_user["user_id"],
        "role":current_user["role"]
    }
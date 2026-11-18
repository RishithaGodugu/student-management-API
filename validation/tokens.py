import os
from datetime import datetime,timedelta,timezone

from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from dotenv import load_dotenv
from jose import jwt,JWTError

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30")
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing from .env")

def create_access_token(user_id: int,role:str):
    expire=datetime.now(timezone.utc)+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload={
        "sub":str(user_id),
        "role": role,
        "exp":expire
    }

    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

bearer_scheme=HTTPBearer()

def get_current_user(
        credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme)
):
    token=credentials.credentials

    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id=payload.get("sub")
        role=payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {"user_id":int(user_id),"role":role}

    except (JWTError,ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate":"Bearer"}
        )

def require_role(required_role:str):
    def role_checker(
        current_user:dict=Depends(get_current_user)
    ):
        user_role=current_user.get("role")

        if user_role!=required_role:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission"
            )

        return current_user

    return role_checker
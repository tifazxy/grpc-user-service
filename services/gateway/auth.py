from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from services.gateway import client, utils
from config import (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPERE_MINUTES)


pwd_context = CryptContext(schemes=['bcrypt'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str) -> Optional[utils.User]:
    user = client.getUserbyEmail(email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    # TODO add checking
    # if user.disabled: 
    #     return None
    
    return utils.user_to_dict(user)

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("get_current_user:",token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print("decoded email:", email)
        if email is None:
            raise credentials_exception
        user = client.getUserbyEmail(email)
        print(user)
        if not user:
            raise credentials_exception # user is not exist
        return utils.user_to_dict(user)
    except JWTError as e:
        print("JWT error", e)
        raise credentials_exception

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Generator

from barbershop.models import (
    User, UserCreate, Token, LoginRequest, 
    PasswordResetRequest, PasswordResetConfirm
)
from barbershop.repositories import UserRepository, get_db
from barbershop.repositories.users import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_current_user(token: str = Depends(oauth2_scheme), conn=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = UserRepository(conn).get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=User, tags=["Auth"])
def register(user_data: UserCreate, conn=Depends(get_db)):
    repo = UserRepository(conn)
    
    if repo.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    if repo.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return repo.create_user(user_data)


@router.post("/login", response_model=Token, tags=["Auth"])
def login(login_data: LoginRequest, conn=Depends(get_db)):
    repo = UserRepository(conn)
    user = repo.authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = repo.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, user=user)


@router.post("/token", response_model=Token, tags=["Auth"])
def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(), conn=Depends(get_db)):
    repo = UserRepository(conn)
    user = repo.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = repo.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, user=user)


@router.post("/password-reset", tags=["Auth"])
def request_password_reset(request: PasswordResetRequest, conn=Depends(get_db)):
    repo = UserRepository(conn)
    token = repo.create_password_reset_token(request.email)
    
    if token is None:
        return {"message": "If the email exists, a reset link will be sent"}
    
    return {
        "message": "If the email exists, a reset link will be sent",
        "reset_token": token
    }


@router.post("/password-reset/confirm", tags=["Auth"])
def confirm_password_reset(confirm: PasswordResetConfirm, conn=Depends(get_db)):
    repo = UserRepository(conn)
    success = repo.reset_password(confirm.token, confirm.new_password)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )
    
    return {"message": "Password reset successfully"}


@router.get("/me", response_model=User, tags=["Auth"])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

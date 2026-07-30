from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from schemas.user import UserRegisterSchema, UserLoginSchema
from core.db import get_session
from core.auth import get_password_hash, verify_password, create_access_token, get_current_user

from models.user import User

user_router = APIRouter(prefix='/auth')


@user_router.post('/register')
def register_user(user_data: UserRegisterSchema, session: Session = Depends(get_session)):
    user = session.query(User).where(User.login == user_data.login).all()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Login is already taken."
        )
    password = get_password_hash(user_data.password)
    new_user = User()
    new_user.name = user_data.name
    new_user.is_admin = False
    new_user.login = user_data.login
    new_user.password_hash = password
    session.add(new_user)
    session.commit()
    return {"result": "success"}


@user_router.post('/login')
def auth_user(response: Response, user_data: UserLoginSchema, session: Session = Depends(get_session)):
    user = session.query(User).where(User.login == user_data.login).one()
    if not user or verify_password(plain_password=user_data.password, hashed_password=str(user.password_hash)) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password"
        )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@user_router.post('/logout')
def logout(response: Response, user_data: User = Depends(get_current_user)):
    response.delete_cookie("users_access_token")
    return {"result": "success"}
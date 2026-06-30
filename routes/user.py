from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user import UserRegisterSchema
from core.db import get_session
from core.auth import get_password_hash

from models.user import User

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/register')
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



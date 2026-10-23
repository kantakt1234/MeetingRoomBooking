from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.schemas.user import UserRegisterSchema, UserLoginSchema
from app.core.db import get_session
from app.core.auth import get_password_hash, verify_password, create_access_token

from app.models.user import User
from app.services.user import UserService

user_router = APIRouter(prefix='/auth', tags=["Authorization"])


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    user_service = UserService(user_repository)
    return user_service


@user_router.post('/register')
async def register_user(user_data: UserRegisterSchema, user_service: UserService = Depends(get_user_service)):
    user = await user_service.register(user_data)
    return user


@user_router.post('/login')
async def auth_user(response: Response, user_data: UserLoginSchema, user_service: UserService = Depends(get_user_service)):
    access_token = await user_service.auth(user_data)
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@user_router.post('/logout')
async def logout(response: Response):
    response.delete_cookie("users_access_token")
    return {"result": "success"}
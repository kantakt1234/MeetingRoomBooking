from fastapi import APIRouter, Depends, Response

from app.core.config import settings
from app.dependencies import get_user_service
from app.schemas.user import (UserRegisterSchema, UserResponseSchema,
                              UserCredentialsSchema, AccessTokenResponseSchema,
                              LogoutResponseSchema)

from app.services.user import UserService

user_router = APIRouter(prefix='/auth', tags=["Authorization"])


@user_router.post('/register')
async def register_user(
        user_data: UserRegisterSchema,
        user_service: UserService = Depends(get_user_service)
) -> UserResponseSchema:

    return await user_service.register(user_data)


@user_router.post('/login')
async def auth_user(
        response: Response,
        user_data: UserCredentialsSchema,
        user_service: UserService = Depends(get_user_service)
) -> AccessTokenResponseSchema:

    access_token = await user_service.auth(user_data)
    response.set_cookie(key="users_access_token", value=access_token, httponly=True,
                        samesite="lax", max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return AccessTokenResponseSchema(access_token=access_token)


@user_router.post('/logout')
async def logout(response: Response) -> LogoutResponseSchema:
    response.delete_cookie("users_access_token")
    return LogoutResponseSchema(detail="success")
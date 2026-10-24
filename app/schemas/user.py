from pydantic import BaseModel, ConfigDict


class UserCredentialsSchema(BaseModel):
    login: str
    password: str


class UserRegisterSchema(UserCredentialsSchema):
    name: str


class UserResponseSchema(BaseModel):
    id: int
    name: str
    login: str
    model_config = ConfigDict(from_attributes=True)


class CurrentUserSchema(UserResponseSchema):
    is_admin: bool


class AccessTokenResponseSchema(BaseModel):
    access_token: str


class LogoutResponseSchema(BaseModel):
    detail: str


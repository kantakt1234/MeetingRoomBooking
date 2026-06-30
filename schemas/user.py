from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    name: str
    login: str
    password: str

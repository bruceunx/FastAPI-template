from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserLoginSchema(UserBaseSchema):
    password: str

class UserTokenSchema(BaseModel):
    refresh_token: str

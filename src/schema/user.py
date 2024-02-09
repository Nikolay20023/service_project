from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str | None = None


class UserInDB(BaseModel):
    hashed_password: str


class UserCreate(User):
    hashed_password: str


class UserUpdate(User):
    email: str

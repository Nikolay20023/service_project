from pydantic import BaseModel
import uuid


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


class UserService(BaseModel):
    user_id: uuid.UUID
    service_id: uuid.UUID
    amount: int
    price: int = 0


class UserServiceUpdate(BaseModel):
    price: int
    amount: int

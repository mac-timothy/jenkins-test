from pydantic import BaseModel


class UserResponse(BaseModel):

    username: str
    email: str



class UserCreatedResponse(BaseModel):

    message: str
    user: UserResponse



class LoginResponse(BaseModel):

    message: str
    user: UserResponse
from pydantic import BaseModel


class SignupRequest(BaseModel):
    username: str
    password: str

class SignupResponse(BaseModel):
    id: int
    username: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
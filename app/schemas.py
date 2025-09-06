from pydantic import BaseModel

# Request model
class MessageRequest(BaseModel):
    user: str
    message: str

# Response model
class MessageResponse(BaseModel):
    session_id: str
    user: str
    ai_reply: str

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

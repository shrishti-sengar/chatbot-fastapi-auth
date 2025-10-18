from pydantic import BaseModel
from typing import Optional


class MessageRequest(BaseModel):
    user: str
    message: str
    session_id: Optional[str] = None


class MessageResponse(BaseModel):
    session_id: str
    user: str
    ai_reply: str
from fastapi import APIRouter
from app.schemas import MessageRequest, MessageResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=MessageResponse)
def chat(request: MessageRequest):
    reply = f"Hello {request.user}, you said: {request.message}"
    return MessageResponse(
        session_id="session_123",
        user=request.user,
        ai_reply=reply
    )

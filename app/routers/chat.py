# app/routers/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import MessageRequest, MessageResponse
from app.core.auth import get_current_user, get_db
from app import models

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=MessageResponse)
def chat(request: MessageRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Use current_user to associate messages
    reply = f"Hello {current_user.username}, you said: {request.message}"

    # persist message (example)
    new_msg = models.Message(session_id="session_123", user_id=current_user.id,
                             user_message=request.message, ai_reply=reply)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    return MessageResponse(session_id=new_msg.session_id, user=current_user.username, ai_reply=reply)

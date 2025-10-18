from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import uuid4
from app.schemas.message import MessageRequest, MessageResponse
from app.core.auth import get_current_user
from app.core.s3_client import upload_session_to_s3
from app import database
from app.models.user import User
from app import models
from app.models.message import Message
from app.core.openai_client import get_ai_reply

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=MessageResponse)
async def chat(request: MessageRequest,
               background_tasks: BackgroundTasks,
               current_user: User = Depends(get_current_user),
               db: Session = Depends(database.get_db)):

    session_id = request.session_id or uuid4().hex
    existing = db.query(models.chatsession.ChatSession).filter(models.chatsession.ChatSession.id == session_id).first()
    if not existing:
        new_session = models.chatsession.ChatSession(id=session_id, user_id=current_user.id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    try:
        ai_reply = await get_ai_reply(request.message)
    except Exception as e:
        ai_reply = "Sorry — AI service temporarily unavailable (quota). I'll respond with a placeholder: Hello!"

    new_msg = Message(session_id=session_id,
                             user_id=current_user.id,
                             user_message=request.message,
                             ai_reply=ai_reply)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    msgs = db.query(Message).filter(Message.session_id == session_id).order_by(Message.id).all()
    messages_payload = [{"user_message": m.user_message, "ai_reply": m.ai_reply} for m in msgs]
    background_tasks.add_task(upload_session_to_s3, session_id, messages_payload)

    # 4) optional: schedule background S3 upload (we'll implement tomorrow)
    # background_tasks.add_task(upload_session_to_s3, session_id)

    return MessageResponse(session_id=session_id, user=current_user.username, ai_reply=ai_reply)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app import models, database

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/{session_id}")
def get_history(session_id: str,
                current_user: models.user.User = Depends(get_current_user),
                db: Session = Depends(database.get_db)):
    # get all messages for this session
    msgs = db.query(models.message.Message).filter(models.message.Message.session_id == session_id).all()
    if not msgs:
        raise HTTPException(status_code=404, detail="Session not found")

    # if not admin, enforce ownership
    if current_user.role != "admin":
        if not any(m.user_id == current_user.id for m in msgs):
            raise HTTPException(status_code=403, detail="Not allowed to view this session")

    return [
        {"user_message": m.user_message, "ai_reply": m.ai_reply}
        for m in msgs
    ]
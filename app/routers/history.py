# app/routers/history.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db
from app import models

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/{session_id}")
def get_history(session_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    msgs = db.query(models.Message).filter(models.Message.session_id == session_id).all()
    if not msgs:
        raise HTTPException(status_code=404, detail="Session not found")

    # ensure ownership unless admin
    if current_user.role != "admin":
        # check that at least one message exists for this user in the session
        owner_ok = any(m.user_id == current_user.id for m in msgs)
        if not owner_ok:
            raise HTTPException(status_code=403, detail="Not allowed to view this session")

    return [{"user_message": m.user_message, "ai_reply": m.ai_reply} for m in msgs]

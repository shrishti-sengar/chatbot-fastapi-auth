from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app import models,database

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/sessions")
def list_sessions(current_user: models.user.User = Depends(get_current_user),
                  db: Session = Depends(database.get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    # query distinct session_ids with owner user_id (first user in session)
    rows = db.query(models.message.Message.session_id, models.message.Message.user_id).distinct(models.message.Message.session_id).all()
    result = []
    for session_id, user_id in rows:
        user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
        result.append({"session_id": session_id, "owner": user.username if user else None})
    return result

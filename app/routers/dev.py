from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_db
from app import models

router = APIRouter(prefix="/dev", tags=["dev"])

@router.post("/promote/{username}")
def promote(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = "admin"
    db.commit()
    db.refresh(user)
    return {"username": user.username, "role": user.role}

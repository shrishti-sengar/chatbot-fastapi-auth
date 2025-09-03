from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, database, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.SignupResponse)
def signup(request: schemas.SignupRequest, db: Session = Depends(get_db)):
    # check if user exists
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = pwd_context.hash(request.password)
    new_user = models.User(username=request.username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

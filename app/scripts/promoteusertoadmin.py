from app.database import SessionLocal
from app import models

db = SessionLocal()
u = db.query(models.User).filter(models.User.username == "sss").first()
u.role = "admin"
db.commit()
db.close()

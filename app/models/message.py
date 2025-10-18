from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_message = Column(Text)
    ai_reply = Column(Text)

    user = relationship("User", back_populates="messages")
    session = relationship("Session", back_populates="messages")
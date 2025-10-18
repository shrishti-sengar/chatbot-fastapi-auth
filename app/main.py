from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers import chat, auth, history, admin, dev
from app.database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Chatbot API with Auth")

# include routers
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(history.router)
app.include_router(admin.router)
app.include_router(dev.router)


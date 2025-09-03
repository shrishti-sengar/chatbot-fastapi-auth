from fastapi import FastAPI
from app.routers import chat, auth
from app import models, database


app = FastAPI(title="Chatbot API with Auth")

# include routers
app.include_router(chat.router)
app.include_router(auth.router)

# create DB tables
models.Base.metadata.create_all(bind=database.engine)


@app.get("/hello")
def hello():
    return {"message": "Hello Shrishti 👋, FastAPI is running!"}

@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}


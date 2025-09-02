from fastapi import FastAPI

app = FastAPI(title="Chatbot API with Auth")

@app.get("/hello")
def hello():
    return {"message": "Hello Shrishti 👋, FastAPI is running!"}

@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

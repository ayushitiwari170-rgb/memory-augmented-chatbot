from fastapi import FastAPI
from workflow import route_query

app = FastAPI()

@app.get("/chat")
def chat(query: str):
    return {"response": route_query(query)}
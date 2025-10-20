from fastapi import FastAPI
from pydantic import BaseModel
from web_agent.rag.pipeline import RAGpipeline

app = FastAPI(title="Web Agent API")
pipeline = RAGpipeline()

class AskIn(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Welcome to the Web Agent API!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(body:AskIn):
    return {"answer": pipeline.answer(body.question)}




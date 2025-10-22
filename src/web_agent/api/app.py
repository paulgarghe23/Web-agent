from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web_agent.rag.pipeline import RAGpipeline

app = FastAPI(title="Web Agent API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Puerto de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
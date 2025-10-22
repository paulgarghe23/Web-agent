from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web_agent.rag.pipeline import RAGpipeline

app = FastAPI(title="Web Agent API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://paulgarghe.com",
        "https://www.paulgarghe.com",
        "https://agent.paulgarghe.com",
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,  # pon True solo si usas cookies/autenticación
    max_age=86400,
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
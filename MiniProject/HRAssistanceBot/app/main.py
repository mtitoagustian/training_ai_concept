"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag_engine import RAGHRBot
from app.api_utils import log_interaction

app = FastAPI(title="HR Assistance Bot")
bot = RAGHRBot()

class QueryRequest(BaseModel):
    question: str
    language: str = "id"

@app.post("/ask")
def ask_question(req: QueryRequest):
    try:
        answer = bot.get_answer(req.question)
        log_interaction(req.question, answer, req.language)
        return {"question": req.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# filepath: app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag_engine import RAGHRBot
from app.api_utils import log_interaction
from app.config import settings

app = FastAPI(title="HR Assistance Bot")
bot = RAGHRBot()

class QueryRequest(BaseModel):
    question: str
    language: str = "id"

@app.post("/ask")
def ask_question(req: QueryRequest):
    try:
        # Jawab pertanyaan
        answer = bot.get_answer(req.question)

        # Log interaksi ke API atau file tergantung config
        if settings.api_logging_endpoint:
            log_interaction(req.question, answer, req.language)

        return {
            "question": req.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

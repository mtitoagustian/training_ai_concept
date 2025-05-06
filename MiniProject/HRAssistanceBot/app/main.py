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

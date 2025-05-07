from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag_engine import RAGHRBot

app = FastAPI(title="HR Chatbot", version="1.0")
bot = RAGHRBot()

class Query(BaseModel):
    question: str

class Feedback(BaseModel):
    question: str
    answer: str
    feedback: str

@app.get("/")
def read_root():
    return {"message": "HR Assistant Bot is running."}

@app.post("/ask")
def ask_bot(query: Query):
    try:
        answer = bot.get_answer(query.question)
        return {"question": query.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def give_feedback(feedback: Feedback):
    try:
        result = bot.provide_feedback(feedback.question, feedback.answer, feedback.feedback)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

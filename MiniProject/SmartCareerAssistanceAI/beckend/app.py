from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from resume_cleaner_id import clean_text
from career_matcher import CareerMatcher
from cv_feedback_gpt import generate_cv_feedback
from interview_bot import simulate_interview
from career_qa_rag import ask_question

# Inisialisasi FastAPI
app = FastAPI()

# Inisialisasi Career Matcher
matcher = CareerMatcher()

# Pydantic models untuk validasi input
class CVInput(BaseModel):
    cv_text: str
    job_title: str

class InterviewInput(BaseModel):
    answer: str
    question_context: str

class QuestionInput(BaseModel):
    question: str

@app.post("/predict-position")
async def predict_position(cv_input: CVInput):
    try:
        cv_cleaned = clean_text(cv_input.cv_text)
        predicted_position = matcher.predict_position(cv_cleaned)
        feedback = generate_cv_feedback(cv_input.cv_text, job_title=cv_input.job_title)
        return {
            "predicted_position": predicted_position,
            "feedback": feedback
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate-interview")
async def simulate_interview_endpoint(interview_input: InterviewInput):
    try:
        evaluation = simulate_interview(interview_input.answer, question_context=interview_input.question_context)
        return {"evaluation": evaluation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/career-qa")
async def career_qa_endpoint(question_input: QuestionInput):
    try:
        answer = ask_question(question_input.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

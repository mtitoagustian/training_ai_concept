import json
from datetime import datetime
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_interaction(question: str, answer: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    with open(os.path.join(LOG_DIR, "interactions.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def log_feedback(question: str, answer: str, feedback: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "feedback": feedback
    }
    with open(os.path.join(LOG_DIR, "feedbacks.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

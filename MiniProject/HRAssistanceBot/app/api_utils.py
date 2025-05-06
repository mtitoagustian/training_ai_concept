import requests
from app.config import API_FAQ_URL, API_LOG_URL

def fetch_faq_data():
    response = requests.get(API_FAQ_URL)
    response.raise_for_status()
    return response.json()

def log_interaction(question, answer, lang="id"):
    payload = {"question": question, "answer": answer, "language": lang}
    try:
        requests.post(API_LOG_URL, json=payload)
    except Exception as e:
        print(f"[Warning] Failed to log: {e}")

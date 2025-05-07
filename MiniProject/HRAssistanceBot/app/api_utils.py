"""
import requests
# filepath: /Users/muhamad.agustian/Documents/training_ai_concept/MiniProject/HRAssistanceBot/app/api_utils.py
from app.config import settings
# Use settings.api_faq_source and settings.api_logging_endpoint
API_FAQ_URL = settings.api_faq_source
API_LOG_URL = settings.api_logging_endpoint

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

"""

import requests
import pandas as pd
from pathlib import Path
from app.config import settings

# Constants from config
API_FAQ_URL = settings.api_faq_source
API_LOG_URL = settings.api_logging_endpoint

# Local CSV fallback (for dev mode)
LOCAL_FAQ_CSV = Path("data/faq.csv")
LOCAL_LOG_CSV = Path("data/logs.csv")

def fetch_faq_data():
    if settings.mode == "dev":
        if not LOCAL_FAQ_CSV.exists():
            raise FileNotFoundError(f"CSV file not found at {LOCAL_FAQ_CSV}")
        return pd.read_csv(LOCAL_FAQ_CSV).to_dict(orient="records")
    else:
        response = requests.get(API_FAQ_URL)
        response.raise_for_status()
        return response.json()

def log_interaction(question, answer, lang="id"):
    if settings.mode == "dev":
        new_row = pd.DataFrame([{
            "question": question,
            "answer": answer,
            "language": lang
        }])
        if LOCAL_LOG_CSV.exists():
            new_row.to_csv(LOCAL_LOG_CSV, mode='a', index=False, header=False)
        else:
            new_row.to_csv(LOCAL_LOG_CSV, index=False)
    else:
        payload = {"question": question, "answer": answer, "language": lang}
        try:
            requests.post(API_LOG_URL, json=payload)
        except Exception as e:
            print(f"[Warning] Failed to log: {e}")

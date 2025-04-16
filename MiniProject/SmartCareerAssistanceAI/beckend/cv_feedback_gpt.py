# cv_feedback_gpt.py

import openai

openai.api_key = "YOUR_OPENAI_API_KEY"  # Ganti dengan API key-mu

def generate_cv_feedback(cv_text, job_title="Data Analyst"):
    """
    Memberikan saran perbaikan CV menggunakan GPT-4 (Bahasa Indonesia).
    """
    prompt = f"""
Saya ingin kamu menjadi HRD profesional yang ahli dalam mengevaluasi CV pelamar kerja.
Berikan saran perbaikan secara singkat dan jelas (dalam Bahasa Indonesia) untuk CV berikut, agar cocok dengan posisi: {job_title}.

CV:
\"\"\"
{cv_text}
\"\"\"

Balasan:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )
    return response['choices'][0]['message']['content'].strip()

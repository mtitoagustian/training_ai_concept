# interview_bot.py

import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def simulate_interview(user_answer, question_context="Ceritakan tentang diri Anda"):
    """
    Memberikan pertanyaan dan mengevaluasi jawaban pelamar.
    """
    prompt = f"""
Kamu adalah pewawancara profesional. Pertanyaannya adalah:
\"{question_context}\"

Jawaban kandidat:
\"{user_answer}\"

Beri evaluasi dalam Bahasa Indonesia, dan berikan saran agar jawaban lebih kuat.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}], 
        temperature=0.7, # # Mengatur suhu untuk variasi jawaban 
        # Suhu rendah menghasilkan jawaban yang lebih terstruktur dan formal
        # Suhu tinggi menghasilkan jawaban yang lebih kreatif dan beragam
        # Dalam konteks wawancara, suhu rendah mungkin lebih sesuai untuk evaluasi yang objektif
        # dan formal.
        # Namun, suhu tinggi bisa digunakan untuk mendapatkan perspektif yang lebih kreatif.

        max_tokens=300 # # Mengatur batasan jumlah token untuk jawaban
        ## Mengatur batasan token membantu mengontrol panjang jawaban yang dihasilkan
        # dan memastikan bahwa jawaban tetap relevan dan fokus pada pertanyaan yang diajukan.
        # Dalam konteks wawancara, batasan token yang lebih rendah dapat membantu menjaga fokus pada 

     )
    return response['choices'][0]['message']['content'].strip()

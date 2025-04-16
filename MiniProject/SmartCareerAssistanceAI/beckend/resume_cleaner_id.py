# resume_cleaner_id.py

import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi stemmer dan stopword remover
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

def clean_text(text):
    """
    Membersihkan teks resume berbahasa Indonesia.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Hapus simbol dan angka
    text = stopword_remover.remove(text)
    text = stemmer.stem(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text, skill_keywords):
    """
    Ekstrak skill dari teks berdasarkan daftar skill (dalam bahasa Indonesia).
    """
    extracted = []
    for skill in skill_keywords:
        if skill.lower() in text:
            extracted.append(skill)
    return extracted

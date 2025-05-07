import torch
import pandas as pd
import re
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
from app.api_utils import log_interaction, log_feedback
from app.config import settings


def clean_answer(answer: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s.,?!\u00C0-\u017F\u0600-\u06FF]', '', answer).strip()


class RAGHRBot:
    def __init__(self):
        # Load model & tokenizer
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(settings.GENERATOR_MODEL)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(settings.GENERATOR_MODEL)

        self.device = torch.device("cpu")
        self.model.to(self.device)

        self.data = self._load_knowledge()
        self.chat_memory = []

    def _load_knowledge(self):
        if settings.USE_API and settings.API_ENDPOINT:
            try:
                response = requests.get(settings.API_ENDPOINT)
                response.raise_for_status()
                records = response.json()
                df = pd.DataFrame(records)
            except Exception as e:
                raise RuntimeError(f"Gagal mengambil data dari API: {e}")
        else:
            try:
                df = pd.read_csv(settings.CSV_PATH)
            except Exception as e:
                raise RuntimeError(f"Gagal membaca file CSV: {e}")

        if "Pertanyaan" not in df.columns or "Jawaban" not in df.columns:
            raise KeyError("CSV atau API harus punya kolom 'Pertanyaan' dan 'Jawaban'")

        embeddings = self.embedder.encode(df["Pertanyaan"].tolist(), convert_to_tensor=True)
        df["embedding"] = [emb.cpu() for emb in embeddings]
        return df

    def get_answer(self, question: str) -> str:
        if self.data.empty:
            return "Data FAQ tidak tersedia."

        q_embed = self.embedder.encode([question], convert_to_tensor=True).to(self.device)
        embeddings = torch.stack([torch.tensor(e).to(self.device) for e in self.data["embedding"]])
        scores = torch.nn.functional.cosine_similarity(q_embed, embeddings)

        top_idx = torch.argmax(scores).item()
        top_score = scores[top_idx].item()

        if top_score < 0.7:
            return "Maaf, saya belum menemukan jawaban yang sesuai. Silakan hubungi HRD."

        matched_q = self.data.iloc[top_idx]["Pertanyaan"]
        context = self.data.iloc[top_idx]["Jawaban"]

        self.chat_memory.append({"question": question, "answer": context})
        prompt = self._get_full_prompt()

        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)
        outputs = self.model.generate(**inputs, max_length=128)

        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        cleaned = clean_answer(answer)

        log_interaction(question, cleaned)
        return cleaned

    def _get_full_prompt(self):
        # Ambil percakapan terakhir saja (terakhir 1024 karakter)
        return "\n".join([f"User: {x['question']}\nBot: {x['answer']}" for x in self.chat_memory])[-1024:]

    def provide_feedback(self, question: str, answer: str, feedback: str):
        log_feedback(question, answer, feedback)
        return "Terima kasih atas feedback Anda!"

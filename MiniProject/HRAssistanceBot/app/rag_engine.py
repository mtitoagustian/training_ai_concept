import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from app.api_utils import fetch_faq_data

class RAGHRBot:
    def __init__(self):
        self.embedder = SentenceTransformer("models/distiluse-base-multilingual-cased-v1")
        self.tokenizer = AutoTokenizer.from_pretrained("models/mt5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("models/mt5-small")
        self.device = torch.device("cpu")

        self.data = self._load_knowledge()

    def _load_knowledge(self):
        raw = fetch_faq_data()
        df = pd.DataFrame(raw)
        df["combined"] = df["Kategori"] + ": " + df["Subkategori"] + " - " + df["Pertanyaan"]
        df["embedding"] = self.embedder.encode(df["combined"].tolist(), convert_to_tensor=True)
        return df

    def get_answer(self, question: str) -> str:
        question_embedding = self.embedder.encode([question], convert_to_tensor=True)
        cosine_scores = torch.nn.functional.cosine_similarity(question_embedding, torch.stack(self.data["embedding"].tolist()))
        top_idx = torch.argmax(cosine_scores).item()
        top_context = self.data.iloc[top_idx]["combined"]
        answer_context = self.data.iloc[top_idx]["Jawaban"]

        prompt = f"Pertanyaan: {question}\nTopik: {top_context}\nJawaban: {answer_context}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
        outputs = self.model.generate(**inputs, max_length=128)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

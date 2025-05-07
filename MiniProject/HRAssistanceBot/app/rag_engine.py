import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from app.api_utils import fetch_faq_data

class RAGHRBot:
    def __init__(self):
        # Menggunakan SentenceTransformer dan model untuk pertanyaan dan jawaban
        self.embedder = SentenceTransformer("models/distiluse-base-multilingual-cased-v1")
        self.tokenizer = AutoTokenizer.from_pretrained("models/mt5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("models/mt5-small")
        self.device = torch.device("cpu")  # Ganti ke "cuda" jika menggunakan GPU

        # Memuat data FAQ
        self.data = self._load_knowledge()

    def _load_knowledge(self):
        try:
            # Membaca CSV ke dalam DataFrame
            df = pd.read_csv("data/faq.csv")
            
            # Periksa apakah kolom 'text' ada di DataFrame
            if "Pertanyaan" not in df.columns:
                raise KeyError("'Pertanyaan' column not found in the CSV file")

            # Encode teks menjadi embedding dan simpan di kolom 'embedding_raw'
            print("Encoding FAQ data to embeddings...")
            embeddings = self.embedder.encode(df["Pertanyaan"].tolist(), convert_to_tensor=True)
            df["embedding_raw"] = [e.tolist() for e in embeddings]
            
            print("FAQ data loaded and embeddings generated.")
            return df
        except Exception as e:
            print(f"Error loading knowledge: {e}")
            return pd.DataFrame()  # Return an empty DataFrame if error occurs

    def get_answer(self, question: str) -> str:
        if self.data.empty:
            return "Data FAQ tidak tersedia. Mohon coba lagi nanti."

        # Encode pertanyaan ke dalam embedding
        question_embedding = self.embedder.encode([question], convert_to_tensor=True)

        # Membuat tensor embeddings dari 'embedding_raw' di DataFrame
        embeddings = torch.stack(self.data["embedding_raw"].apply(torch.tensor).tolist())
        
        # Hitung cosine similarity antara pertanyaan dan setiap embedding FAQ
        cosine_scores = torch.nn.functional.cosine_similarity(question_embedding, embeddings)

        # Debugging: Periksa skor cosine untuk pertanyaan dan embedding
        print(f"Cosine Scores: {cosine_scores}")

        # Menemukan indeks dengan skor cosine tertinggi
        top_idx = torch.argmax(cosine_scores).item()
        best_score = cosine_scores[top_idx].item()

        # Ambil pertanyaan dan jawaban yang sesuai
        matched_question = self.data.iloc[top_idx]["Pertanyaan"]
        answer_context = self.data.iloc[top_idx]["Jawaban"]

        # Pengecekan threshold skor cosine
        if best_score < 0.5:
            return "Maaf, saya belum menemukan jawaban yang sesuai. Silakan hubungi tim HRD."

        # Buat prompt untuk model t5
        prompt = f"Pertanyaan: {question}\nTopik: {matched_question}\nJawaban: {answer_context}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(self.device)
        
        # Hasilkan jawaban menggunakan model
        outputs = self.model.generate(**inputs, max_length=128)

        # Decode dan kembalikan hasilnya
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

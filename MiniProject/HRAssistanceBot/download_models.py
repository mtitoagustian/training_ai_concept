from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer

"""

# ===== Embedder (multilingual & ringan) =====
print("Downloading SentenceTransformer embedder...")
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embedder.save("models/paraphrase-multilingual-MiniLM-L12-v2")

"""

# ===== Generator (Bahasa Indonesia) =====
print("Downloading T5-small Indonesian model...")
generator_model = AutoModelForSeq2SeqLM.from_pretrained("indobenchmark/indobart")
generator_tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobart")

generator_model.save_pretrained("models/indobart")
generator_tokenizer.save_pretrained("models/indobart")

print("✅ All models downloaded and saved to local 'models/' directory.")
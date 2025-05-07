#from transformers import AutoModel, AutoTokenizer
from transformers import T5Tokenizer, T5Model
from sentence_transformers import SentenceTransformer
import os

def download_embedding_model(save_dir="models/distiluse-base-multilingual-cased-v1"):
    print("📥 Downloading embedding model...")
    model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased-v1")
    model.save(save_dir)
    print(f"✅ Embedding model saved to: {save_dir}")

## def download_generator_model(save_dir="models/mt5-small"):
##    print("📥 Downloading generator model...")
 #   tokenizer = AutoTokenizer.from_pretrained("google/mt5-small")
 #   model = AutoModel.from_pretrained("google/mt5-small")
 #   tokenizer.save_pretrained(save_dir)
 #   model.save_pretrained(save_dir)
#    print(f"✅ Generator model saved to: {save_dir}")

def download_generator_model(save_dir="models/mt5-small"):
    print("📥 Downloading generator model...")
    tokenizer = T5Tokenizer.from_pretrained("google/mt5-small")
    model = T5Model.from_pretrained("google/mt5-small")
    tokenizer.save_pretrained(save_dir)
    model.save_pretrained(save_dir)
    print(f"✅ Generator model saved to: {save_dir}")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
   ## download_embedding_model()
    download_generator_model()
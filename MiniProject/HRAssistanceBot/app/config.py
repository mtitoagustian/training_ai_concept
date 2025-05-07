from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CSV_PATH: str = "data/faq.csv"
    API_ENDPOINT: str = ""
    USE_API: bool = False
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    GENERATOR_MODEL: str = "cahya/bert2bert-indonesian-summarization"

    class Config:
        env_file = ".env"

settings = Settings()

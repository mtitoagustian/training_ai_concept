import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_faq_source: str = "https://your-data-api.com/faqs"
    api_logging_endpoint: str = "https://your-log-api.com/logs"
    debug: bool = False
    class Config:
        env_file = ".env"

settings = Settings()
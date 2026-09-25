import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    READONLY_DATABASE_URL: str = os.getenv("READONLY_DATABASE_URL")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27019")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "sql_copilot_logs")
    LOG_COLLECTION_NAME: str = os.getenv("LOG_COLLECTION_NAME", "query_logs")

settings = Settings()
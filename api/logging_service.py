from datetime import datetime, timezone
from pymongo import MongoClient
from fastapi.concurrency import run_in_threadpool
from config import settings

mongo_client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
db = mongo_client[settings.MONGO_DB_NAME]
log_collection = db[settings.LOG_COLLECTION_NAME]


def _log_sync(entry: dict) -> None:
    log_collection.insert_one(entry)


async def log_query_safely(
    question: str, generated_sql: str, row_count: int, usage: dict, latency_ms: float
) -> None:
    """Loglama başarısız olsa bile asıl /ask isteğini asla düşürmez."""
    entry = {
        "question": question,
        "generated_sql": generated_sql,
        "row_count": row_count,
        "usage": usage,
        "latency_ms": round(latency_ms, 2),
        "logged_at": datetime.now(timezone.utc),
    }
    try:
        await run_in_threadpool(_log_sync, entry)
    except Exception as e:
        print(f"[WARN] Loglama başarısız: {e}")
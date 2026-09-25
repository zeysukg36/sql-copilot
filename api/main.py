from fastapi import FastAPI, HTTPException
from models import AskRequest, AskResponse
from llm_service import generate_sql
from sql_safety import validate_sql_is_safe, enforce_row_limit
from database import run_readonly_query
import time
from logging_service import log_query_safely 
from sqlalchemy import text
from database import engine

app = FastAPI(title="SQL Copilot API", version="1.0.0")


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    start = time.perf_counter()

    sql, usage = generate_sql(request.question)

    try:
        validate_sql_is_safe(sql)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Üretilen SQL güvenlik kontrolünden geçemedi: {e} | SQL: {sql}",
        )

    sql = enforce_row_limit(sql)

    try:
        results = run_readonly_query(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sorgu çalıştırılamadı: {e}")

    latency_ms = (time.perf_counter() - start) * 1000
    await log_query_safely(request.question, sql, len(results), usage, latency_ms)

    return AskResponse(
        question=request.question,
        generated_sql=sql,
        results=results,
        row_count=len(results),
         )

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = True
    except Exception:
        db_status = False
    return {"status": "ok", "database_connected": db_status} 
   
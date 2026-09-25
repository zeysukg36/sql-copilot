from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(settings.READONLY_DATABASE_URL, pool_pre_ping=True)


def get_schema_description() -> str:
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'customers'
        ORDER BY ordinal_position;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()
    lines = [f"- {col}: {dtype}" for col, dtype in rows]
    return "customers tablosu sütunları:\n" + "\n".join(lines)


def run_readonly_query(sql: str) -> list[dict]:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
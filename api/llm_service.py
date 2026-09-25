# api/llm_service.py
import re
from google import genai
from config import settings
from database import get_schema_description
import os

MOCK_MODE = os.getenv("MOCK_LLM", "false").lower() == "true"
MOCK_SQL_RESPONSE = 'SELECT COUNT(*) FROM customers WHERE "Contract" = \'Two year\' LIMIT 10'

client = genai.Client()  # GEMINI_API_KEY ortam değişkeninden otomatik okunur

SYSTEM_PROMPT_TEMPLATE = """Sen bir PostgreSQL sorgu asistanısın. Kullanıcının doğal dildeki
sorusunu, aşağıdaki şemaya uygun, SADECE bir SELECT sorgusuna çevir.

{schema}

Kurallar:
- Yalnızca SELECT sorgusu üret, asla INSERT/UPDATE/DELETE/DROP/ALTER üretme.
- Sorgunun sonuna LIMIT 100 ekle.
- Yanıtında SADECE SQL sorgusunu döndür, açıklama veya markdown blok işareti ekleme.
- Var olmayan bir sütun/tablo kullanma."""


# api/llm_service.py — generate_sql fonksiyonu güncellendi
def generate_sql(question: str) -> tuple[str, dict]:
    if MOCK_MODE:
        return MOCK_SQL_RESPONSE, {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    schema = get_schema_description()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=schema)
    full_input = f"{system_prompt}\n\nKullanıcı sorusu: {question}"

    interaction = client.interactions.create(
        model=settings.GEMINI_MODEL,
        input=full_input,
    )

    raw_sql = interaction.output_text.strip()
    raw_sql = re.sub(r"^```sql\s*|```$", "", raw_sql, flags=re.MULTILINE).strip()

    usage = {
        "input_tokens": interaction.usage.total_input_tokens,
        "output_tokens": interaction.usage.total_output_tokens,
        "total_tokens": interaction.usage.total_tokens,
    }
    return raw_sql, usage
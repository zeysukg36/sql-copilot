FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
    "TRUNCATE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "COPY",
]


def validate_sql_is_safe(sql: str) -> None:
    cleaned = sql.strip().rstrip(";")
    upper = cleaned.upper()

    if not upper.startswith("SELECT"):
        raise ValueError("Sadece SELECT sorgularına izin veriliyor.")

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in upper:
            raise ValueError(f"Yasaklı anahtar kelime tespit edildi: {keyword}")

    if ";" in cleaned:
        raise ValueError("Birden fazla komut (statement chaining) tespit edildi.")


def enforce_row_limit(sql: str, max_rows: int = 100) -> str:
    cleaned = sql.strip().rstrip(";")
    if "LIMIT" not in cleaned.upper():
        cleaned += f" LIMIT {max_rows}"
    return cleaned
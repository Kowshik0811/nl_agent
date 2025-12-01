# db_access.py
from sqlalchemy import create_engine, text
from config import DB_URL, ALLOWED_TABLES

engine = create_engine(DB_URL)


def safe_query(table: str, columns: list, condition: str = "1=1"):
    """
    Only allow queries on predefined tables and columns.
    """
    if table not in ALLOWED_TABLES:
        return "Access Denied: Table not allowed"
    if not set(columns).issubset(set(ALLOWED_TABLES[table])):
        return "Access Denied: Column not allowed"

    columns_str = ", ".join(columns)
    query = f"SELECT {columns_str} FROM {table} WHERE {condition} LIMIT 100;"

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row) for row in result]

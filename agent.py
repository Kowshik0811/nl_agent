import re
import psycopg2
from psycopg2.extras import RealDictCursor
from table_rules import ALLOWED_TABLES, BLOCKED_TABLES

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "sensordb",
    "user": "postgres",
    "password": "root"
}

# Map columns to their tables
COLUMN_KEYWORD_MAP = {}
for table, meta in ALLOWED_TABLES.items():
    for col in meta["columns"]:
        COLUMN_KEYWORD_MAP[col.lower()] = table

# Synonyms for natural language
SYNONYMS = {
    "battery": "battery_level",
    "power": "battery_level",
    "charge": "battery_level",
    "volt": "voltage",
    "voltage": "voltage",
    "location": "location",
    "place": "location",
    "temp": "temperature",
    "temperature": "temperature",
    "humidity": "humidity",
    "status": "status",
    "alert": "alert_type",
    "severity": "severity",
    "reading": "temperature",
    "device_type": "device_type",
    "type": "device_type"
}

# Aggregation keywords
AGG_KEYWORDS = {
    "average": "AVG",
    "avg": "AVG",
    "maximum": "MAX",
    "max": "MAX",
    "minimum": "MIN",
    "min": "MIN",
    "sum": "SUM",
    "count": "COUNT"
}

# Comparison keywords
COMP_KEYWORDS = {
    "below": "<",
    "under": "<",
    "less than": "<",
    "above": ">",
    "over": ">",
    "greater than": ">"
}


def parse_nl_to_query(nl_query: str):
    q = nl_query.lower().replace(":", " ")

    # --- Detect multiple sensors ---
    sensor_matches = re.findall(r"(?<!\d)(\d{3,6})(?!\d)", q)
    sensor_id_list = sensor_matches if sensor_matches else None

    # --- Aggregation detection ---
    agg_func = None
    for key, val in AGG_KEYWORDS.items():
        if key in q:
            agg_func = val
            break

    # --- Detect columns ---
    detected_tables = set()
    selected_columns = []

    words = re.findall(r"\w+", q)
    for word in words:
        col = SYNONYMS.get(word, word)
        if col in COLUMN_KEYWORD_MAP:
            table = COLUMN_KEYWORD_MAP[col]
            detected_tables.add(table)
            if col not in selected_columns:
                selected_columns.append(col)

    if not detected_tables:
        return {"error": "Cannot detect columns/tables from your query."}

    detected_tables = [t for t in detected_tables if t not in BLOCKED_TABLES]
    if not detected_tables:
        return {"error": "Access denied to the requested tables."}

    # --- Primary table selection ---
    table_column_count = {t: 0 for t in detected_tables}
    for col in selected_columns:
        table_column_count[COLUMN_KEYWORD_MAP[col]] += 1
    primary_table = max(table_column_count, key=table_column_count.get)

    join_tables = [t for t in detected_tables if t != primary_table]

    # Validate joins
    for t in join_tables:
        if t not in ALLOWED_TABLES[primary_table]["joinable_with"]:
            if "sensor_metadata" in detected_tables:
                continue
            return {"error": f"Join between {primary_table} and {t} is not allowed."}

    # --- Comparison detection ---
    comparison_condition = None
    comp_pattern = rf"(\w+)\s*({'|'.join(COMP_KEYWORDS.keys())})\s*(\d+)"
    comp_match = re.search(comp_pattern, q)
    if comp_match:
        col_word = comp_match.group(1)
        op_word = comp_match.group(2)
        num = comp_match.group(3)
        col = SYNONYMS.get(col_word, col_word)
        if col in COLUMN_KEYWORD_MAP:
            tbl = COLUMN_KEYWORD_MAP[col]
            comparison_condition = f"{tbl}.{col} {COMP_KEYWORDS[op_word]} {num}"

    # --- Range detection ---
    range_condition = None
    range_pattern = r"(\w+)\s*(?:between|-)\s*(\d+)\s*(?:and)?\s*(\d+)"
    range_match = re.search(range_pattern, q)
    if range_match:
        col_word = range_match.group(1)
        start = range_match.group(2)
        end = range_match.group(3)
        col = SYNONYMS.get(col_word, col_word)
        if col in COLUMN_KEYWORD_MAP:
            tbl = COLUMN_KEYWORD_MAP[col]
            range_condition = f"{tbl}.{col} BETWEEN {start} AND {end}"

    # --- Build sensor_id condition ---
    if sensor_id_list:
        sensor_condition = f"{primary_table}.sensor_id IN ({','.join(sensor_id_list)})"
    else:
        sensor_condition = "1=1"

    # --- Merge all conditions ---
    conditions = [sensor_condition]
    if comparison_condition:
        conditions.append(comparison_condition)
    if range_condition:
        conditions.append(range_condition)
    condition_str = " AND ".join(conditions)

    return {
        "primary_table": primary_table,
        "join_tables": join_tables,
        "columns": selected_columns,
        "condition": condition_str,
        "aggregation": agg_func
    }


def ask_agent(query: str):
    parsed = parse_nl_to_query(query)
    return ask_agent_parsed(parsed)


def ask_agent_parsed(parsed: dict):
    if "error" in parsed:
        return parsed["error"]

    primary = parsed["primary_table"]
    join_tables = parsed["join_tables"]
    columns = parsed["columns"]
    condition = parsed["condition"]
    agg_func = parsed.get("aggregation")

    # --- Build SQL ---
    col_str_list = []
    for c in columns:
        tbl = COLUMN_KEYWORD_MAP[c]
        if agg_func:
            col_str_list.append(f"{agg_func}({tbl}.{c}) AS {c}")
        else:
            col_str_list.append(f"{tbl}.{c}")
    cols_str = ", ".join(col_str_list)

    sql = f"SELECT {cols_str} FROM {primary}"

    for t in join_tables:
        sql += f" LEFT JOIN {t} ON {t}.sensor_id = {primary}.sensor_id"

    sql += f" WHERE {condition}"

    # Limit for optional sensor_id
    if "1=1" in condition:
        sql += " LIMIT 20"

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        return f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return results

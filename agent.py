import re
import psycopg2
from psycopg2.extras import RealDictCursor

# Update these with your database credentials
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "sensordb",
    "user": "postgres",
    "password": "root"
}


def parse_nl_to_query(nl_query: str):
    """
    Convert natural language query to a dictionary for the database agent.
    Handles:
      - Sensor status queries (active/inactive)
      - Sensor readings queries (temperature, humidity, timestamp)
      - Optional sensor_id filtering
      - Specific column requests (e.g., "only temperature")
    """
    nl_query = nl_query.lower()

    # Determine table and columns
    table = None
    columns = []
    condition = None

    # SENSOR STATUS QUERIES
    if "status" in nl_query or "active" in nl_query or "inactive" in nl_query:
        table = "sensor_status"
        columns = ["sensor_id", "status", "last_update"]

        # Filter for active/inactive if mentioned
        if "active" in nl_query:
            condition = "status='active'"
        elif "inactive" in nl_query:
            condition = "status='inactive'"

    # SENSOR READINGS QUERIES
    elif "reading" in nl_query or "temperature" in nl_query or "humidity" in nl_query or "timestamp" in nl_query or "time" in nl_query:
        table = "sensor_readings"
        columns = ["sensor_id"]  # Always include sensor_id

        # Add requested columns
        if "temperature" in nl_query:
            columns.append("temperature")
        if "humidity" in nl_query:
            columns.append("humidity")
        if "timestamp" in nl_query or "time" in nl_query:
            columns.append("timestamp")

        # If no column explicitly requested, include all
        if len(columns) == 1:
            columns += ["temperature", "humidity", "timestamp"]

    else:
        return {"error": "Cannot understand query"}

    # SENSOR ID FILTER
    sensor_id_match = re.findall(r'\b\d{3,}\b', nl_query)  # Support multiple sensor IDs
    if sensor_id_match:
        ids = ",".join(sensor_id_match)
        condition = (f"{condition} AND " if condition else "") + f"sensor_id IN ({ids})"

    return {"table": table, "columns": columns, "condition": condition}


def ask_agent(query: str):
    """
    Process a natural language query and return results from the PostgreSQL database.
    """
    parsed = parse_nl_to_query(query)
    return ask_agent_parsed(parsed)


def ask_agent_parsed(parsed: dict):
    """
    Execute a parsed query dictionary on the database.
    parsed: dict returned by parse_nl_to_query
    """
    # Check for error
    if "error" in parsed:
        return parsed["error"]

    table = parsed["table"]
    columns = parsed["columns"]
    condition = parsed["condition"]

    # Build SQL query
    cols_str = ", ".join(columns)
    sql = f"SELECT {cols_str} FROM {table}"
    if condition:
        sql += f" WHERE {condition}"

    # Connect and execute
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

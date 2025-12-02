ALLOWED_TABLES = {
    "sensor_status": {
        "columns": ["sensor_id", "status", "last_update"],
        "allow_full_access": False,
        "requires_sensor_id": True,
        "joinable_with": ["sensor_metadata", "sensor_battery"]
    },
    "sensor_readings": {
        "columns": ["sensor_id", "temperature", "humidity", "timestamp"],
        "allow_full_access": False,
        "requires_sensor_id": True,
        "joinable_with": ["sensor_metadata", "sensor_battery"]
    },
    "sensor_metadata": {
        "columns": ["sensor_id", "location", "device_type"],
        "allow_full_access": True,
        "requires_sensor_id": False,
        "joinable_with" : ["sensor_status", "sensor_data", "sensor_battery"]
    },
    "sensor_alerts": {
        "columns": ["sensor_id", "alert_type", "severity", "alert_time"],
        "allow_full_access": False,
        "requires_sensor_id": True,
        "joinable_with": ["sensor_metadata", "sensor_status"]
    },
    "sensor_battery": {
        "columns": ["sensor_id", "battery_level", "voltage", "timestamp"],
        "allow_full_access": False,
        "requires_sensor_id": True,
        "joinable_with": ["sensor_metadata", "sensor_readings"]
    }
}

# These tables must NEVER be accessible
BLOCKED_TABLES = [ "users", "auth", "roles", "system_logs"]

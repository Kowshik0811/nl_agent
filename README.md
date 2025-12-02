SnowFlare Sensor Data Agent
Project Objective

The SnowFlare Sensor Data Agent is designed to provide a natural language interface for querying sensor data stored in a PostgreSQL database. The goal is to allow users to extract meaningful insights from sensors without writing SQL, supporting both technical and non-technical stakeholders.

Core Functionalities

Natural Language Queries

Users can query sensor data using plain English.

Supports single sensor queries, multi-sensor queries, and conditions.

Multi-Table Support and Joins

Works with multiple tables including:

sensor_status

sensor_readings

sensor_metadata

sensor_battery

sensor_alerts

Automatically performs multi-table joins where allowed.

Comparison and Range Queries

Handles conditions like:

"battery below 20"

"temperature between 20 and 30"

Aggregations

Supports aggregate functions such as:

AVG, MIN, MAX, SUM, COUNT

Example: "Average temperature of all sensors"

Multi-Sensor Queries

Supports querying multiple sensors at once:

"sensors 1012,1015,1020"

Synonym Handling

Understands variations in natural language, e.g.:

battery → battery_level

temp → temperature

volt → voltage

place → location

Security and Access Control

Only allowed tables can be queried.

Blocked tables like users, auth, roles are never accessible.

Join permissions are enforced to maintain data integrity.

Key Benefits

Simplifies data retrieval from complex sensor systems.

Reduces dependency on SQL knowledge.

Supports real-time queries for dashboards or analytics pipelines.

Extensible for future features such as multi-condition queries, alerts, and RAG-based retrieval.

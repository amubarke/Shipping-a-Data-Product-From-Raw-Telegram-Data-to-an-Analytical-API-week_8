import os
import json
import psycopg2
from pathlib import Path

# PostgreSQL connection settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "medical_warehouse"
DB_USER = "postgres"
DB_PASS = "12345678"

RAW_DATA_DIR = "data/raw/telegram_messages"

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# Create raw schema and table if not exists
cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    date TIMESTAMP,
    message_text TEXT,
    message_length INT,
    view_count INT,
    forward_count INT,
    has_image BOOLEAN,
    image_path TEXT
);
""")
conn.commit()

# Load JSON files
for json_file in Path(RAW_DATA_DIR).rglob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cur.execute("""
            INSERT INTO raw.telegram_messages (
                message_id, channel_name, date, message_text, message_length, 
                view_count, forward_count, has_image, image_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (message_id) DO NOTHING;
            """, (
                msg["message_id"], msg["channel_name"], msg["date"], msg["message_text"],
                msg.get("message_length"), msg.get("view_count"), msg.get("forward_count"),
                msg.get("has_image"), msg.get("image_path")
            ))
conn.commit()
cur.close()
conn.close()
print("Raw data loaded successfully!")

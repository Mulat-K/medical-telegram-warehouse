import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "telegram_messages"

def load_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;
        DROP TABLE IF EXISTS raw.telegram_messages;
        CREATE TABLE raw.telegram_messages (
            message_id BIGINT,
            channel_name TEXT,
            message_date TIMESTAMP,
            message_text TEXT,
            views INTEGER,
            forwards INTEGER,
            has_media BOOLEAN,
            image_path TEXT
        );
    """)

    for date_dir in RAW_DATA_DIR.iterdir():
        for file in date_dir.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                records = json.load(f)

            for r in records:
                cur.execute("""
                    INSERT INTO raw.telegram_messages VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    r["message_id"],
                    r["channel_name"],
                    r["message_date"],
                    r["message_text"],
                    r["views"],
                    r["forwards"],
                    r["has_media"],
                    r["image_path"]
                ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()

import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "processed" / "image_detections.csv"

df = pd.read_csv(CSV_PATH)

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    DROP TABLE IF EXISTS raw.image_detections;
    CREATE TABLE raw.image_detections (
        message_id BIGINT,
        channel_name TEXT,
        detected_objects TEXT,
        confidence_score FLOAT,
        image_category TEXT
    );
""")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO raw.image_detections VALUES (%s,%s,%s,%s,%s)
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

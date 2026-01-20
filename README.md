# Medical Telegram Data Warehouse

An end-to-end ELT data platform that extracts data from Ethiopian medical Telegram channels,
transforms it using dbt, enriches it with computer vision, and exposes insights via an API.

## Tech Stack
- Telethon
- PostgreSQL
- dbt
- YOLOv8
- FastAPI
- Dagster
- Docker

## Architecture
Raw Data Lake → PostgreSQL → dbt (Staging & Marts) → API

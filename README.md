# Medical Telegram Data Warehouse

This project implements an end-to-end data pipeline to extract, transform, and analyze data from public Telegram channels focusing on Ethiopian medical businesses. Leveraging modern data tools like Telethon for scraping, dbt for transformation, YOLOv8 for data enrichment, Dagster for orchestration, and FastAPI for API exposure, this platform aims to generate actionable insights into medical products, pricing, and channel activity.

## Table of Contents

1.  [Overview](#overview)
    *   [Business Need](#business-need)
    *   [Key Business Questions](#key-business-questions)
    *   [Data Product Goals](#data-product-goals)
2.  [Data and Features](#data-and-features)
    *   [Telegram Channels to Scrape](#telegram-channels-to-scrape)
    *   [Data Fields Collected](#data-fields-collected)
3.  [Learning Outcomes](#learning-outcomes)
    *   [Skills Acquired](#skills-acquired)
    *   [Knowledge Gained](#knowledge-gained)
    *   [Communication](#communication)
4.  [Team](#team)
5.  [Key Dates](#key-dates)
6.  [Project Structure](#project-structure)
7.  [Setup and Local Development](#setup-and-local-development)
    *   [Prerequisites](#prerequisites)
    *   [Folder Structure Creation (Initial Setup)](#folder-structure-creation-initial-setup)
    *   [Git Initialization](#git-initialization)
    *   [GitHub Repository Setup](#github-repository-setup)
    *   [Docker Environment Setup](#docker-environment-setup)
8.  [Tasks](#tasks)
    *   [Task 1: Data Scraping and Collection (Extract & Load)](#task-1-data-scraping-and-collection-extract--load)
    *   [Task 2: Data Modeling and Transformation (Transform)](#task-2-data-modeling-and-transformation-transform)
    *   [Task 3: Data Enrichment with Object Detection (YOLO)](#task-3-data-enrichment-with-object-detection-yolo)
    *   [Task 4: Build an Analytical API](#task-4-build-an-analytical-api)
    *   [Task 5: Pipeline Orchestration](#task-5-pipeline-orchestration)
9.  [Running the Pipeline](#running-the-pipeline)
10. [API Endpoints](#api-endpoints)
11. [Reporting and Documentation](#reporting-and-documentation)
12. [Challenges and Solutions](#challenges-and-solutions)
13. [Future Enhancements](#future-enhancements)
14. [License](#license)

---

## 1. Overview

As a Data Engineer at Kara Solutions, a leading data science consultancy in Ethiopia, our mission is to build a robust data platform that generates actionable insights about Ethiopian medical businesses using data scraped from public Telegram channels. This project focuses on establishing a reliable, scalable, and analytical data foundation.

### Business Need

A well-designed data platform is crucial for advanced data analysis. This project implements a modern ELT (Extract, Load, Transform) framework. Raw data from Telegram will be loaded into a "Data Lake" (file storage), then into a PostgreSQL database serving as a data warehouse. dbt will handle cleaning and remodeling into a dimensional star schema, optimized for analytical queries.

### Key Business Questions

This pipeline is designed to answer key business questions, including:

*   What are the top 10 most frequently mentioned medical products or drugs across all channels?
*   How does the price or availability of a specific product vary across different channels?
*   Which channels have the most visual content (e.g., images of pills vs. creams)?
*   What are the daily and weekly trends in posting volume for health-related topics?

### Data Product Goals

This project aims to deliver a data product that:

*   Develops a reproducible project environment and secure pipeline.
*   Develops a data scraping and collection pipeline to populate a raw data lake.
*   Designs and implements a dimensional data model (star schema) in a PostgreSQL data warehouse.
*   Develops a data cleaning and transformation pipeline using dbt.
*   Enriches the data using object detection on images with YOLO.
*   Exposes the final, cleaned data through an analytical API using FastAPI.

## 2. Data and Features

The data for this project originates from public Telegram channels primarily focused on medical and pharmaceutical products within Ethiopia.

### Telegram Channels to Scrape

*   CheMed Telegram Channel
*   Lobelia Cosmetics: `https://t.me/lobelia4cosmetics`
*   Tikvah Pharma: `https://t.me/tikvahpharma`
*   Additional relevant channels from `https://et.tgstat.com/medicine` (e.g., specific pharmacies, medical supply groups).

### Data Fields Collected

For each Telegram message, the following fields are collected:

*   `message_id`: Unique identifier for each message.
*   `channel_name`: Name of the Telegram channel.
*   `message_date`: Timestamp of the message.
*   `message_text`: Full text content (including product names, prices, descriptions).
*   `has_media`: Boolean indicating if the message contains media.
*   `image_path`: Local file path to the downloaded image (if applicable).
*   `views`: Number of views on the message.
*   `forwards`: Number of times the message was forwarded.

## 3. Learning Outcomes

### Skills Acquired

*   Telegram API data extraction using `Telethon`.
*   Data Modeling: Designing and implementing a Star Schema.
*   ELT Pipeline Development: Building layered data pipelines (Raw -> Staging -> Marts).
*   Infrastructure as Code (IaC) and environment management using `Docker` and `requirements.txt`.
*   Data Transformation at scale using `dbt` (Data Build Tool).
*   Data Enrichment using Object Detection (`YOLOv8`).
*   Analytical API Development with `FastAPI`.
*   Data Pipeline Orchestration with `Dagster`.
*   Testing and validation of data systems.
*   Managing credentials and secrets using environment variables.

### Knowledge Gained

*   Principles of modern ELT vs. ETL architectures.
*   Layered data architecture (Data Lake, Staging, Data Marts).
*   Best practices in data cleaning, validation, and transformation.
*   Structuring data for efficient analytical queries (Dimensional Modeling).
*   Integrating unstructured data (like image detection results) into a structured warehouse.
*   Best practices for deploying and maintaining reproducible data pipelines.

### Communication

*   Documenting data architecture and modeling decisions.
*   Reporting on project outcomes and technical challenges.

## 4. Team

*   **Tutors:** Kerod, Mahbubah, Filimon, Smegnsh

## 5. Key Dates

*   **Challenge Introduction:** 10:30 AM UTC on Wednesday, 14 Jan 2026
*   **Interim Submission:** 8:00 PM UTC on Sunday, 18 Jan 2026
*   **Final Submission:** 8:00 PM UTC on Tuesday, 20 Jan 2026

## 6. Project Structure
```text
medical-telegram-warehouse/
├── .vscode/
│ └── settings.json
├── .github/
│ └── workflows/
│ └── unittests.yml 
├── .env 
├── .gitignore 
├── docker-compose.yml 
├── Dockerfile
├── requirements.txt
├── README.md 
├── data/ 
│ ├── raw/ 
│ │ ├── images/ 
│ │ └── telegram_messages/
├── logs/ 
├── medical_warehouse/
│ ├── dbt_project.yml
│ ├── profiles.yml
│ ├── models/ 
│ │ ├── staging/
│ │ └── marts/
│ └── tests/ 
├── src/ 
│ ├── api/ 
│ │ ├── init.py
│ │ ├── main.py 
│ │ ├── database.py
│ │ └── schemas.py 
│ ├── notebooks/
│ │ ├── init.py
│ ├── scraper.py 
│ ├── yolo_detect.py
│ ├── load_raw_to_postgres.py 
│ └── tests/ 
│ └── init.py
└── scripts/

```

## 7. Setup and Local Development

### Prerequisites

Before starting, ensure you have the following installed:

*   **Git**: For version control.
*   **Python 3.8+**: Recommended for development.
*   **Docker Desktop**: For containerization and running PostgreSQL.
*   **PoSh (PowerShell)**: Your chosen terminal environment.
```bash
git remote add origin https://github.com/Mullat-K/medical-telegram-warehouse.git
git branch -M main
git push -u origin main

```
# Shipping a Data Product: From Raw Telegram Data to an Analytical API

## Overview

This project is an **end-to-end data pipeline** designed to extract, transform, enrich, and expose data from public Telegram channels related to Ethiopian medical businesses. The goal is to provide actionable insights via an analytical API.

## Business Objective

* Identify top-mentioned medical products and drugs.
* Analyze price and availability variations across channels.
* Track visual content trends (e.g., images of pills vs. creams).
* Monitor daily and weekly posting trends for health-related topics.

## Tech Stack

* **Data Extraction:** Telethon (Python)
* **Data Lake:** Raw JSON storage for messages and images
* **Data Warehouse:** PostgreSQL
* **Data Transformation:** dbt
* **Data Enrichment:** YOLOv8 (object detection for images)
* **API Exposure:** FastAPI
* **Pipeline Orchestration:** Dagster

## Project Structure
`````bash
project-root/
├── data/
│ ├── raw/
│ │ ├── telegram_messages/
│ │ │ └── channel_name/YYYY_MM_DD.json
│ │ └── metadata/
│ └── logs/
├── dbt_project/
│ ├── models/
│ └── macros/
├── yolov8_enrichment/
│ └── detect_objects.py
├── api/
│ └── main.py
├── dagster_pipeline/
│ └── pipeline.py
├── scrapers/
│ └── telegram_scraper.py
└── README.md
`````
## Pipeline Overview
The pipeline consists of the following steps:

### Task 1: Telegram Data Scraping
* Collect messages and images from public Telegram channels using Telethon.
* Store data in **raw JSON files** in the data lake.
* Run the scraper manually:
python scrapers/telegram_scraper.py

### Task 2: Load Raw Data to PostgreSQL
* Load the raw JSON data into the PostgreSQL warehouse.
* Apply basic cleaning and formatting during ingestion.
* Run the loader:
python data_lake/load_raw_to_postgres.py

### Task 4: Data Enrichment with YOLOv8

* Apply object detection on images to extract visual insights.
* Store detected objects as structured features in the warehouse.
* Run YOLOv8 enrichment:
python yolov8_enrichment/detect_objects.py

### Task 5: Pipeline Orchestration with Dagster

* Automate the pipeline using Dagster.
* Define operations (ops) for scraping, loading, transforming, and enrichment.
* Example pipeline.py structure:

```
from dagster import job, op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(['python', 'scrapers/telegram_scraper.py'], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(['python', 'data_lake/load_raw_to_postgres.py'], check=True)

@op
def run_dbt_transformations():
    subprocess.run(['dbt', 'run', '--project-dir', 'dbt_project'], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(['python', 'yolov8_enrichment/detect_objects.py'], check=True)

@job
def telegram_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres()
    dbt = run_dbt_transformations()
    yolo = run_yolo_enrichment()

```
### Define execution order
    load.after(scrape)
    dbt.after(load)
    yolo.after(dbt)

* Launch Dagster UI and monitor runs:
dagster dev -f dagster_pipeline/pipeline.py

* Access the UI at http://localhost:3000.

* Schedule daily runs and monitor pipeline logs.


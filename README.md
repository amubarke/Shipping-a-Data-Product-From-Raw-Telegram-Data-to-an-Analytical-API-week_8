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

```
project-root/
├── data_lake/
│   ├── raw/
│   │   ├── telegram_messages/
│   │   │   └── channel_name/YYYY_MM_DD.json
│   │   └── metadata/
│   └── logs/
├── dbt_project/
│   ├── models/
│   └── macros/
├── yolov8_enrichment/
│   └── detect_objects.py
├── api/
│   └── main.py
├── dagster_pipeline/
│   └── pipeline.py
└── README.md
```

## Features

1. **Data Scraping:** Collects messages and images from public Telegram channels.
2. **Data Lake:** Stores raw, immutable data partitioned by channel and date.
3. **Star Schema Warehouse:** Dimensional modeling for analytical queries.
4. **Data Transformation:** Cleans and structures data with dbt.
5. **Data Enrichment:** Applies YOLOv8 for object detection in images.
6. **Analytical API:** Serves insights through FastAPI endpoints.
7. **Orchestration:** Dagster manages the workflow and schedules.

## Getting Started

1. **Clone the repository**

```bash
git clone <repo-url>
cd project-root
```

2. **Set up environment variables** for Telegram API credentials.

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run data scraping**

```bash
python data_lake/collect_telegram_data.py
```

5. **Run dbt transformations**

```bash
dbt run
```

6. **Run YOLOv8 enrichment**

```bash
python yolov8_enrichment/detect_objects.py
```

7. **Start FastAPI**

```bash
uvicorn api.main:app --reload
```

## Next Steps

* Apply **YOLOv8 object detection** to all images.
* Expand **API endpoints** for advanced analytical queries.
* Implement **Dagster orchestration** for automated pipeline runs.

## License

MIT License

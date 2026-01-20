from dagster import op,job, ScheduleDefinition
import subprocess
import sys
from pathlib import Path

@op
def scrape_telegram_data(context):
    context.log.info("Starting Telegram scraper...")

    project_root = Path(__file__).resolve().parent
    scraper_path = project_root / "src" / "scraper.py"

    if not scraper_path.exists():
        raise FileNotFoundError(f"Scraper not found at {scraper_path}")

    result = subprocess.run(
        [sys.executable, str(scraper_path)],
        capture_output=True,
        text=True
    )

    context.log.info(result.stdout)

    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception("Telegram scraper failed")

    context.log.info("Telegram scraping completed successfully")


@op
def load_raw_to_postgres(scrape_status: str):
    """
    Step 2: Load raw data into Postgres
    """
    subprocess.run(
        ["python", "loaders/load_raw_to_postgres.py"],
        check=True
    )
    return "load_done"


@op
def run_dbt_transformations(load_status: str):
    """
    Step 3: Run dbt models
    """
    subprocess.run(
        ["dbt", "run"],
        check=True
    )
    return "dbt_done"


@op
def run_yolo_enrichment(dbt_status: str):
    """
    Step 4: Run YOLO object detection
    """
    subprocess.run(
        ["python", "enrichment/run_yolo.py"],
        check=True
    )
    return "yolo_done"


@job
def telegram_data_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    run_yolo_enrichment(dbt)


daily_schedule = ScheduleDefinition(
    job=telegram_data_pipeline,
    cron_schedule="0 2 * * *"
)

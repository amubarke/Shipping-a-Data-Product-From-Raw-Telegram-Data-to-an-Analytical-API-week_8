# test_db.py
from sqlalchemy import create_engine, inspect, text
from api.database import get_db

# Define the tables and required columns to check
tables_to_check = {
    "fct_image_detections": [
        "message_id", "channel_key", "channel_name",
        "image_name", "detected_class", "confidence_score", "image_category"
    ],
    "fct_messages": ["message_id", "channel_key", "date_key"],
    "dim_channels": ["channel_key", "channel_name"],
    "dim_dates": ["date_key", "date", "weekday", "month", "year"]
}

def main():
    # Connect to database
    db = next(get_db())
    inspector = inspect(db.bind)

    for table_name, columns in tables_to_check.items():
        print(f"\n--- Checking table: {table_name} ---")

        # Check if table exists
        if table_name in inspector.get_table_names():
            print(f"✅ Table exists")
        else:
            print(f"❌ Table does NOT exist")
            continue  # Skip column checks if table doesn't exist

        # Check if all required columns exist
        existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
        missing_columns = [c for c in columns if c not in existing_columns]
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
        else:
            print(f"✅ All required columns are present")

        # Print first 5 rows as sample
        try:
            query = text(f"SELECT * FROM {table_name} LIMIT 5")
            rows = db.execute(query).fetchall()
            if rows:
                print(f"Sample rows:")
                for row in rows:
                    print(dict(row))
            else:
                print("⚠️ Table is empty")
        except Exception as e:
            print(f"❌ Error fetching sample rows: {e}")

if __name__ == "__main__":
    main()

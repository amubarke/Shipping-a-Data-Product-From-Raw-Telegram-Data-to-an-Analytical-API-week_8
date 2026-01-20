from sqlalchemy.orm import Session
from sqlalchemy import text

# Endpoint 1
def get_top_products(db: Session, limit: int):
    query = text("""
        SELECT detected_class, COUNT(*) AS total_mentions
        FROM analytics_marts.fct_image_detections
        WHERE detected_class IS NOT NULL
        GROUP BY detected_class
        ORDER BY total_mentions DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()


# Endpoint 2
def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT channel_name, COUNT(*) AS total_messages
        FROM analytics_marts.fct_messages
        WHERE channel_name = :channel_name
        GROUP BY channel_name
    """)
    return db.execute(query, {"channel_name": channel_name}).fetchone()


# Endpoint 3
def search_messages(db: Session, query_text: str, limit: int):
    query = text("""
        SELECT message_id, message_text
        FROM analytics_marts.fct_messages
        WHERE message_text ILIKE :query
        LIMIT :limit
    """)
    return db.execute(
        query, {"query": f"%{query_text}%", "limit": limit}
    ).fetchall()


# Endpoint 4
def get_visual_content_stats(db: Session):
    query = text("""
        SELECT image_category, COUNT(*) AS total_images
        FROM analytics_marts.fct_image_detections
        GROUP BY image_category
    """)
    return db.execute(query).fetchall()

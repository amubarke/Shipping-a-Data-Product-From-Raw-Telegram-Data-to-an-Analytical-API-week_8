

WITH yolo_detections AS (
    SELECT
        CAST(message_id AS BIGINT) AS message_id,
        image_name,
        detected_class,
        confidence_score,
        image_category
    FROM "medical_warehouse"."raw"."yolo_detections"
),

messages AS (
    SELECT
        message_id,
        channel_key,
        date_key
    FROM "medical_warehouse"."analytics_marts"."fct_messages"
),

channel_map AS (
    SELECT *
    FROM "medical_warehouse"."raw"."channel_mapping"
)

SELECT
    y.image_name,
    y.detected_class,
    y.confidence_score,
    y.image_category,
    m.message_id,
    m.channel_key,
    c.channel_name,
    m.date_key
FROM yolo_detections y
LEFT JOIN messages m
    ON y.message_id = m.message_id
LEFT JOIN channel_map c
    ON CAST(m.channel_key AS TEXT) = c.channel_key  -- fix type mismatch
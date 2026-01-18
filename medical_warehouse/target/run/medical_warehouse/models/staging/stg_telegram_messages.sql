
  create view "medical_warehouse"."analytics_staging"."stg_telegram_messages__dbt_tmp"
    
    
  as (
    select
    message_id,
    channel_name,
    message_text,
    message_date,
    length(message_text) as message_length,
    view_count,
    forward_count,
    has_media,
    image_path
from "medical_warehouse"."raw"."telegram_messages"
where message_text is not null
  );
select *
from "medical_warehouse"."analytics_staging"."stg_telegram_messages"
where message_date > current_timestamp
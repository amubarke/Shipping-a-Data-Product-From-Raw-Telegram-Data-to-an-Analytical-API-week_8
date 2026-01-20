
  
    

  create  table "medical_warehouse"."analytics_marts"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    

select
    s.message_id,
    dc.channel_key,
    dd.full_date as date_key,
    s.message_text,
    s.message_length,
    s.view_count,
    s.forward_count,
    s.has_media as has_image
from "medical_warehouse"."analytics_staging"."stg_telegram_messages" s
left join "medical_warehouse"."analytics_marts"."dim_channels" dc
    on s.channel_name = dc.channel_name
left join "medical_warehouse"."analytics_marts"."dim_dates" dd
    on cast(s.message_date as date) = dd.full_date
  );
  
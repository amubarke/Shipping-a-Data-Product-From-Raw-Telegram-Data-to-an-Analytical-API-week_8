{{ config(materialized='table') }}

select
    s.message_id,
    dc.channel_key,
    dd.full_date as date_key,
    s.message_text,
    s.message_length,
    s.view_count,
    s.forward_count,
    s.has_media as has_image
from {{ ref('stg_telegram_messages') }} s
left join {{ ref('dim_channels') }} dc
    on s.channel_name = dc.channel_name
left join {{ ref('dim_dates') }} dd
    on cast(s.message_date as date) = dd.full_date

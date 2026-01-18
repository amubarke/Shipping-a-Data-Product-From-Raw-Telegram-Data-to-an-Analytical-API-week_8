

select distinct
    cast(message_date as date) as full_date,
    extract(year from message_date)::int as year,
    extract(month from message_date)::int as month,
    extract(day from message_date)::int as day,
    extract(week from message_date)::int as week_of_year,
    extract(dow from message_date)::int as day_of_week,
    to_char(message_date, 'Day') as day_name,
    to_char(message_date, 'Month') as month_name,
    case when extract(dow from message_date) in (0,6) then true else false end as is_weekend
from "medical_warehouse"."analytics_staging"."stg_telegram_messages"
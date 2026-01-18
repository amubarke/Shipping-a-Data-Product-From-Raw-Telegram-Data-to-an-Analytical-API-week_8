
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "medical_warehouse"."analytics_staging"."stg_telegram_messages"
where message_date > current_timestamp
  
  
      
    ) dbt_internal_test
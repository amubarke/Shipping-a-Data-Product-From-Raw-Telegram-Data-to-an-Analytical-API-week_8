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
from {{ source('raw', 'telegram_messages') }}
where message_text is not null

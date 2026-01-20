with source as (
    select * from raw.telegram_messages
),

cleaned as (
    select
        message_id,
        channel_name,
        cast(message_date as date) as message_date,
        message_text,
        length(message_text) as message_length,
        coalesce(views, 0) as view_count,
        coalesce(forwards, 0) as forward_count,
        has_media as has_image,
        image_path
    from source
    where message_text is not null
)

select * from cleaned

select
    cast(d.message_id as bigint) as message_id,
    c.channel_key,
    dt.date_key,
    d.image_category,
    d.detected_objects,
    d.confidence_score
from raw.image_detections d
join {{ ref('dim_channels') }} c
    on d.channel_name = c.channel_name
join {{ ref('fct_messages') }} m
    on d.message_id = m.message_id
join {{ ref('dim_dates') }} dt
    on m.date_key = dt.date_key

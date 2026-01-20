select distinct
    cast(to_char(message_date, 'YYYYMMDD') as int) as date_key,
    message_date as full_date,
    extract(dow from message_date) as day_of_week,
    extract(week from message_date) as week_of_year,
    extract(month from message_date) as month,
    extract(year from message_date) as year
from {{ ref('stg_telegram_messages') }}

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from api.database import get_db
from api.schemas import (
    TopProduct,
    ChannelActivity,
    MessageSearchResult,
    VisualContentStat,
)

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytical API for Ethiopian medical Telegram data",
    version="1.0.0",
)

# --------------------------------------------------
# Endpoint 1: Top Products
# --------------------------------------------------
@app.get("/api/reports/top-products", response_model=list[TopProduct])
def top_products(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    query = text("""
        SELECT
            lower(word) AS product,
            COUNT(*) AS mentions
        FROM analytics.fct_messages,
        unnest(string_to_array(message_text, ' ')) AS word
        GROUP BY word
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"product": r[0], "mentions": r[1]} for r in result]

# --------------------------------------------------
# Endpoint 2: Channel Activity
# --------------------------------------------------
@app.get("/api/channels/{channel_name}/activity", response_model=list[ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            c.channel_name,
            d.full_date::text AS message_date,
            COUNT(*) AS total_posts
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c USING (channel_key)
        JOIN analytics.dim_dates d USING (date_key)
        WHERE c.channel_name = :channel
        GROUP BY c.channel_name, d.full_date
        ORDER BY d.full_date
    """)
    result = db.execute(query, {"channel": channel_name}).fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")

    return [
        {
            "channel_name": r[0],
            "message_date": r[1],
            "total_posts": r[2],
        }
        for r in result
    ]

# --------------------------------------------------
# Endpoint 3: Message Search
# --------------------------------------------------
@app.get("/api/search/messages", response_model=list[MessageSearchResult])
def search_messages(
    query: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    sql = text("""
        SELECT
            message_id,
            c.channel_name,
            message_text,
            view_count
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c USING (channel_key)
        WHERE message_text ILIKE :q
        ORDER BY view_count DESC
        LIMIT :limit
    """)
    result = db.execute(sql, {"q": f"%{query}%", "limit": limit}).fetchall()
    return [
        {
            "message_id": r[0],
            "channel_name": r[1],
            "message_text": r[2],
            "view_count": r[3],
        }
        for r in result
    ]

# --------------------------------------------------
# Endpoint 4: Visual Content Stats
# --------------------------------------------------
@app.get("/api/reports/visual-content", response_model=list[VisualContentStat])
def visual_content_stats(db: Session = Depends(get_db)):
    sql = text("""
        SELECT
            c.channel_name,
            d.image_category,
            COUNT(*) AS total_images
        FROM analytics.fct_image_detections d
        JOIN analytics.dim_channels c USING (channel_key)
        GROUP BY c.channel_name, d.image_category
        ORDER BY total_images DESC
    """)
    result = db.execute(sql).fetchall()
    return [
        {
            "channel_name": r[0],
            "image_category": r[1],
            "total_images": r[2],
        }
        for r in result
    ]

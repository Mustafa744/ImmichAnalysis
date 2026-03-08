# src/db_client.py
import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DB_URL

engine = create_engine(DB_URL)

def get_all_photos() -> pd.DataFrame:
    query = text("""
        SELECT
            a.id,
            a."localDateTime",
            a."fileCreatedAt",
            a."isFavorite",
            a."visibility",
            a."status",
            a."width",
            a."height",
            a."stackId",
            e.latitude,
            e.longitude,
            e.city,
            e.state,
            e.country,
            e.make,
            e.model,
            e."lensModel",
            e."focalLength",
            e."fNumber",
            e.iso,
            e."exposureTime",
            e."fileSizeInByte",
            e."dateTimeOriginal",
            e."rating"
        FROM asset a
        JOIN asset_exif e ON a.id = e."assetId"
        WHERE
            a.type = 'IMAGE'
            AND a."deletedAt" IS NULL
            AND a.visibility = 'timeline'
        ORDER BY a."localDateTime"
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def get_clip_embeddings() -> pd.DataFrame:
    query = text("""
        SELECT
            s."assetId",
            s.embedding::text AS embedding
        FROM smart_search s
        JOIN asset a ON s."assetId" = a.id
        WHERE
            a.type = 'IMAGE'
            AND a."deletedAt" IS NULL
            AND a.visibility = 'timeline'
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
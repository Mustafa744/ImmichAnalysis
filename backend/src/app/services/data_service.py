import pandas as pd
from typing import Optional
from app.api.deps import LocationFilter
from infrastructure.clients.database import get_all_photos
from infrastructure.persistence.cache import ThumbnailCache
from app.core.config import CACHE_PATH


class DataService:
    _df: Optional[pd.DataFrame] = None
    _cache: Optional[ThumbnailCache] = None

    @classmethod
    def get_analysis_cache(cls) -> ThumbnailCache:
        if cls._cache is None:
            cls._cache = ThumbnailCache(str(CACHE_PATH))
        return cls._cache

    @classmethod
    def get_df(cls) -> pd.DataFrame:
        if cls._df is None:
            df = get_all_photos()
            if not df.empty and "localDateTime" in df.columns:
                df["localDateTime"] = pd.to_datetime(
                    df["localDateTime"], errors="coerce"
                )
            cls._df = df
        return cls._df

    @classmethod
    def apply_filters(cls, df: pd.DataFrame, filters: LocationFilter) -> pd.DataFrame:
        if df.empty:
            return df

        filtered = df.copy()

        # Location filters rules:
        # 1. Cities take priority over countries if both provided
        if filters.cities:
            filtered = filtered[filtered["city"].isin(filters.cities)]
        elif filters.countries:
            filtered = filtered[filtered["country"].isin(filters.countries)]

        # Dates
        if filters.date_from:
            filtered = filtered[filtered["localDateTime"].dt.date >= filters.date_from]
        if filters.date_to:
            filtered = filtered[filtered["localDateTime"].dt.date <= filters.date_to]

        return filtered

    @classmethod
    def get_filtered_df(cls, filters: LocationFilter) -> pd.DataFrame:
        df = cls.get_df()
        return cls.apply_filters(df, filters)

    @staticmethod
    def format_photo_record(row: pd.Series) -> dict:
        """Helper to safely format a DataFrame row into a standard frontend dict."""
        record = {
            "id": str(row["id"]),
            "date": row["localDateTime"].isoformat()
            if pd.notnull(row.get("localDateTime"))
            else None,
            "city": row.get("city") if pd.notnull(row.get("city")) else None,
            "country": row.get("country") if pd.notnull(row.get("country")) else None,
        }
        if pd.notnull(row.get("latitude")) and pd.notnull(row.get("longitude")):
            record["coords"] = {
                "lat": float(row["latitude"]),
                "lng": float(row["longitude"]),
            }
        return record

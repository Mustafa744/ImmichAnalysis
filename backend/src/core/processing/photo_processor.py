import pandas as pd
from typing import Tuple, List, Optional
from pathlib import Path
from app.core.config import PHOTOS_CSV


def load_and_preprocess_photos(
    csv_path: str | Path = PHOTOS_CSV, home_countries: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads the photos csv, adds time features, and splits into full, travel, and home dataframes.

    Returns:
        Tuple of (df, travel_df, home_df)
    """
    if home_countries is None:
        home_countries = ["Egypt"]

    df = pd.read_csv(csv_path)
    df["localDateTime"] = pd.to_datetime(
        df["localDateTime"], format="ISO8601"
    ).dt.tz_convert(None)
    df["fileCreatedAt"] = pd.to_datetime(
        df["fileCreatedAt"], format="ISO8601"
    ).dt.tz_convert(None)

    # Time features
    df["hour"] = df["localDateTime"].dt.hour
    df["weekday"] = df["localDateTime"].dt.day_name()
    df["month"] = df["localDateTime"].dt.month
    df["year"] = df["localDateTime"].dt.year
    df["date"] = df["localDateTime"].dt.date

    # Split home vs travel
    travel = df[~df["country"].isin(home_countries) & df["country"].notna()].copy()
    home = df[df["country"].isin(home_countries)].copy()

    return df, travel, home

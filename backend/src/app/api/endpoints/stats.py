from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.api.deps import LocationFilter, location_filter
from app.services.data_service import DataService

router = APIRouter()


@router.get("/overview")
async def get_overview(
    loc: LocationFilter = Depends(location_filter),
) -> Dict[str, Any]:
    df = DataService.get_filtered_df(loc)

    if df.empty:
        return {
            "total_photos": 0,
            "countries": 0,
            "date_range": None,
            "most_active_country": None,
            "most_active_month": None,
        }

    total_photos = len(df)
    countries_count = df["country"].nunique() if "country" in df else 0

    date_range = (
        {
            "from": df["localDateTime"].dt.date.min(),
            "to": df["localDateTime"].dt.date.max(),
        }
        if "localDateTime" in df
        else None
    )

    most_active_country = (
        df["country"].mode()[0]
        if ("country" in df and not df["country"].dropna().empty)
        else None
    )

    if "localDateTime" in df and not df["localDateTime"].dropna().empty:
        most_active_month = (
            df["localDateTime"].dt.to_period("M").mode()[0].strftime("%Y-%m")
        )
    else:
        most_active_month = None

    return {
        "total_photos": total_photos,
        "countries": int(countries_count),
        "date_range": date_range,
        "most_active_country": most_active_country,
        "most_active_month": most_active_month,
    }

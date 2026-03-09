from fastapi import APIRouter, Depends, Path
from typing import Dict, Any, List

from app.api.deps import LocationFilter, location_filter
from app.services.data_service import DataService
import pandas as pd

router = APIRouter()


@router.get("/daily")
async def get_daily_timeline(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    df = DataService.get_filtered_df(loc)

    if df.empty or "localDateTime" not in df or df["localDateTime"].dropna().empty:
        return []

    # Get start and end date for zero-filling
    start_date = df["localDateTime"].dt.date.min()
    end_date = df["localDateTime"].dt.date.max()

    df["date_str"] = df["localDateTime"].dt.date.astype(str)
    daily_groups = df.groupby("date_str")

    # Generate all dates in range
    all_dates = pd.date_range(start=start_date, end=end_date, freq="D").strftime(
        "%Y-%m-%d"
    )

    result = []
    for date_str in all_dates:
        count = 0
        photos = []
        if date_str in daily_groups.groups:
            group_df = daily_groups.get_group(date_str)
            count = len(group_df)
            photos = [
                DataService.format_photo_record(row) for _, row in group_df.iterrows()
            ]

        result.append({"date": date_str, "count": count, "photos": photos})

    return result


@router.get("/hourly")
async def get_hourly_timeline(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    df = DataService.get_filtered_df(loc)

    if df.empty or "localDateTime" not in df or df["localDateTime"].dropna().empty:
        return []

    df["hour"] = df["localDateTime"].dt.hour
    hourly_groups = df.groupby("hour")

    result = []
    for hour in range(24):  # 0 to 23
        count = 0
        photos = []
        if hour in hourly_groups.groups:
            group_df = hourly_groups.get_group(hour)
            count = len(group_df)
            photos = [
                DataService.format_photo_record(row) for _, row in group_df.iterrows()
            ]

        result.append({"hour": hour, "count": count, "photos": photos})

    return result


@router.get("/trips")
async def get_trips(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    # Very basic trip detection logic based on GPS gap and date gap analysis
    df = DataService.get_filtered_df(loc)

    if df.empty or "localDateTime" not in df:
        return []

    # Sort
    df = df.sort_values(by="localDateTime").reset_index(drop=True)

    # Gap > 1.5 days or large distance
    # For simplicity, purely by time distance > 24 hours right now
    time_diff = df["localDateTime"].diff()
    trip_ids = (time_diff > pd.Timedelta(hours=48)).cumsum()
    df["trip_id"] = trip_ids

    trips = []

    for trip_id, trip_df in df.groupby("trip_id"):
        if len(trip_df) < 5:  # Arbitrary threshold to call it a trip
            continue

        start_date = trip_df["localDateTime"].min()
        end_date = trip_df["localDateTime"].max()

        # Primary location (most frequent city or country)
        city = (
            trip_df["city"].mode()[0]
            if "city" in trip_df and not trip_df["city"].dropna().empty
            else None
        )
        country = (
            trip_df["country"].mode()[0]
            if "country" in trip_df and not trip_df["country"].dropna().empty
            else None
        )

        trips.append(
            {
                "id": int(trip_id),
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "photos_count": len(trip_df),
                "city": city,
                "country": country,
            }
        )

    return trips


@router.get("/trips/{trip_id}")
async def get_trip_details(
    trip_id: int = Path(..., description="Trip ID"),
    loc: LocationFilter = Depends(location_filter),
) -> Dict[str, Any]:
    df = DataService.get_filtered_df(loc)

    if df.empty or "localDateTime" not in df:
        return {}

    df = df.sort_values(by="localDateTime").reset_index(drop=True)
    time_diff = df["localDateTime"].diff()
    trip_ids = (time_diff > pd.Timedelta(hours=48)).cumsum()
    df["trip_id"] = trip_ids

    trip_df = df[df["trip_id"] == trip_id]
    if trip_df.empty:
        return {}

    photos = []
    for _, row in trip_df.iterrows():
        photo_dict = {
            "id": str(row["id"]),
            "date": row["localDateTime"].isoformat()
            if pd.notnull(row["localDateTime"])
            else None,
        }
        if pd.notnull(row.get("latitude")) and pd.notnull(row.get("longitude")):
            photo_dict["coords"] = {
                "lat": float(row["latitude"]),
                "lng": float(row["longitude"]),
            }

        photos.append(photo_dict)

    return {"id": trip_id, "count": len(trip_df), "photos": photos}

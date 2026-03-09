from fastapi import APIRouter, Depends
from typing import Dict, Any, List
import pandas as pd

from app.api.deps import LocationFilter, location_filter
from app.services.data_service import DataService

router = APIRouter()


@router.get("/moments")
async def get_moments(loc: LocationFilter = Depends(location_filter)) -> Dict[str, Any]:
    df = DataService.get_filtered_df(loc)
    empty_result = {"count": 0, "photos": []}
    if df.empty or "localDateTime" not in df or df["localDateTime"].dropna().empty:
        return {
            "golden_hour": empty_result,
            "night": empty_result,
            "midday": empty_result,
            "morning": empty_result,
            "afternoon": empty_result,
        }

    hours = df["localDateTime"].dt.hour

    def _extract(mask):
        sub = df[mask]
        return {
            "count": len(sub),
            "photos": [
                DataService.format_photo_record(row) for _, row in sub.iterrows()
            ],
        }

    return {
        "golden_hour": _extract((hours >= 17) & (hours <= 19)),
        "night": _extract((hours >= 20) | (hours < 5)),
        "morning": _extract((hours >= 5) & (hours < 10)),
        "midday": _extract((hours >= 10) & (hours < 14)),
        "afternoon": _extract((hours >= 14) & (hours < 17)),
    }


@router.get("/shot-types")
async def get_shot_types(
    loc: LocationFilter = Depends(location_filter),
) -> Dict[str, Any]:
    df = DataService.get_filtered_df(loc)

    empty_result = {"count": 0, "photos": []}
    if df.empty or "width" not in df or "height" not in df:
        return {
            "landscape": empty_result,
            "portrait": empty_result,
            "square": empty_result,
            "macro": empty_result,
        }

    valid_dims = df.dropna(subset=["width", "height"])

    def _extract(mask_df):
        return {
            "count": len(mask_df),
            "photos": [
                DataService.format_photo_record(row) for _, row in mask_df.iterrows()
            ],
        }

    landscape = valid_dims[valid_dims["width"] > valid_dims["height"]]
    portrait = valid_dims[valid_dims["width"] < valid_dims["height"]]
    square = valid_dims[valid_dims["width"] == valid_dims["height"]]

    macro = None
    if "focalLength" in df:
        macro = df.dropna(subset=["focalLength"])
        macro = macro[macro["focalLength"] < 30]

    return {
        "landscape": _extract(landscape),
        "portrait": _extract(portrait),
        "square": _extract(square),
        "macro": _extract(macro) if macro is not None else empty_result,
    }


@router.get("/burst-clusters")
async def get_burst_clusters(
    loc: LocationFilter = Depends(location_filter),
) -> Dict[str, Any]:
    df = DataService.get_filtered_df(loc)

    if df.empty or "localDateTime" not in df:
        return {"burst_clusters": []}

    df = df.sort_values(by="localDateTime").reset_index(drop=True)
    time_diff = df["localDateTime"].diff()

    # Photos within 30s of each other
    burst_ids = (time_diff > pd.Timedelta(seconds=30)).cumsum()
    df["burst_id"] = burst_ids

    bursts = []
    # Identify groups with at least 3 photos to define a "burst cluster"
    for b_id, b_df in df.groupby("burst_id"):
        if len(b_df) >= 3:
            bursts.append(
                {
                    "id": int(b_id),
                    "count": len(b_df),
                    "start": b_df["localDateTime"].min().isoformat(),
                    "end": b_df["localDateTime"].max().isoformat(),
                }
            )

    return {"total_bursts": len(bursts), "burst_clusters": bursts}


@router.get("/top-locations")
async def get_top_locations(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    df = DataService.get_filtered_df(loc)

    if df.empty or "city" not in df or "country" not in df:
        return []

    # Count photos per city/country
    loc_counts = df.groupby(["country", "city"]).size().reset_index(name="count")
    loc_counts = loc_counts.sort_values(by="count", ascending=False).head(10)

    result = []
    for _, row in loc_counts.iterrows():
        country = row["country"]
        city = row["city"]
        count = row["count"]

        # Extract matching photos
        mask = (df["country"] == country) & (df["city"] == city)
        sub_df = df[mask]

        photos = [
            DataService.format_photo_record(p_row) for _, p_row in sub_df.iterrows()
        ]

        result.append(
            {"country": country, "city": city, "count": int(count), "photos": photos}
        )

    return result

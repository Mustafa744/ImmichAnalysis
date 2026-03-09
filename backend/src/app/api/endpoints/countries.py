from fastapi import APIRouter, Depends, Path
from typing import Dict, Any, List

from app.api.deps import LocationFilter, location_filter
from app.services.data_service import DataService

router = APIRouter()


@router.get("")
async def get_countries() -> List[Dict[str, Any]]:
    # Countries typically don't use the LocationFilter since this feeds the picker
    df = DataService.get_df()

    if df.empty or "country" not in df or df["country"].dropna().empty:
        return []

    # Get country counts and roughly median or average coordinates
    agg_df = (
        df.groupby("country")
        .agg(count=("id", "count"), lat=("latitude", "mean"), lng=("longitude", "mean"))
        .reset_index()
    )

    # Drop any nulls (if some photos don't have coords)
    agg_df = agg_df.dropna(subset=["lat", "lng"])

    result = []
    for _, row in agg_df.iterrows():
        result.append(
            {
                "country": row["country"],
                "count": int(row["count"]),
                "coords": {"lat": float(row["lat"]), "lng": float(row["lng"])},
            }
        )

    return result


@router.get("/{country}/cities")
async def get_cities(country: str = Path(..., description="Country name")) -> List[str]:
    df = DataService.get_df()
    if df.empty or "country" not in df or "city" not in df:
        return []

    country_df = df[df["country"] == country]
    if country_df.empty:
        return []

    cities = country_df["city"].dropna().unique().tolist()
    return sorted(cities)


@router.get("/{country}/heatmap")
async def get_heatmap(
    country: str = Path(..., description="Country name"),
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, float]]:
    # Apply global filters first, but ensure we also filter by the specific country path param
    # if it's not somehow part of the filter already. But usually we just filter the base dataframe.
    df = DataService.get_filtered_df(loc)

    if df.empty or "country" not in df or "latitude" not in df or "longitude" not in df:
        return []

    country_df = df[df["country"] == country]
    # Drop rows without coords
    country_df = country_df.dropna(subset=["latitude", "longitude"])

    heatmap = []
    for _, row in country_df.iterrows():
        heatmap.append({"lat": float(row["latitude"]), "lng": float(row["longitude"])})

    return heatmap

from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from app.api.deps import LocationFilter, location_filter
from app.services.data_service import DataService
from core.analysis.palette_analyzer import compute_location_palette

router = APIRouter()


def _collect_colors_for_ids(photo_ids: list[str], cache) -> list[dict]:
    """Collect all dominant_colors entries from cache for the given photo IDs."""
    all_colors: list[dict] = []
    for pid in photo_ids:
        pid_str = str(pid)
        if pid_str in cache:
            colors = cache[pid_str].get("dominant_colors")
            if colors:
                all_colors.extend(colors)
    return all_colors


@router.get("/by-country")
async def get_palettes_by_country(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    """
    Returns a representative 5-color palette for each country.
    Accepts standard LocationFilter to narrow results.
    """
    df = DataService.get_filtered_df(loc)

    if df.empty or "id" not in df or "country" not in df:
        return []

    cache = DataService.get_analysis_cache()
    results = []

    for country, group in df.groupby("country"):
        if not country or str(country) == "nan":
            continue

        photo_ids = group["id"].tolist()
        all_colors = _collect_colors_for_ids(photo_ids, cache)

        if not all_colors:
            continue

        palette = compute_location_palette(all_colors, k=5)
        results.append({
            "country": str(country),
            "count": len(photo_ids),
            "palette": palette,
        })

    # Sort by photo count descending
    results.sort(key=lambda x: x["count"], reverse=True)
    return results


@router.get("/by-city")
async def get_palettes_by_city(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    """
    Returns a representative 5-color palette for each city.
    Accepts standard LocationFilter to narrow results.
    """
    df = DataService.get_filtered_df(loc)

    if df.empty or "id" not in df or "city" not in df:
        return []

    cache = DataService.get_analysis_cache()
    results = []

    for (city, country), group in df.groupby(["city", "country"]):
        if not city or str(city) == "nan":
            continue

        photo_ids = group["id"].tolist()
        all_colors = _collect_colors_for_ids(photo_ids, cache)

        if not all_colors:
            continue

        palette = compute_location_palette(all_colors, k=5)
        results.append({
            "city": str(city),
            "country": str(country) if country and str(country) != "nan" else None,
            "count": len(photo_ids),
            "palette": palette,
        })

    results.sort(key=lambda x: x["count"], reverse=True)
    return results

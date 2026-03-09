from fastapi import APIRouter, Depends
from typing import Dict, Any, List
import numpy as np

from app.api.deps import LocationFilter, location_filter
from app.services.data_service import DataService

router = APIRouter()


@router.get("/histograms")
async def get_histograms(
    loc: LocationFilter = Depends(location_filter),
) -> Dict[str, Any]:
    """Returns aggregated 32-bin color histogram curves and average IRQ metrics for the selected photos"""
    df = DataService.get_filtered_df(loc)
    empty_hist = [0] * 32

    if df.empty or "id" not in df:
        return {
            "r_hist": empty_hist,
            "g_hist": empty_hist,
            "b_hist": empty_hist,
            "brightness": 0.0,
            "colorfulness": 0.0,
            "warmth": 0.0,
            "sky_score": 0.0,
            "count": 0,
        }

    cache = DataService.get_analysis_cache()

    r_sum = np.zeros(32)
    g_sum = np.zeros(32)
    b_sum = np.zeros(32)

    metrics_sum = {
        "brightness": 0.0,
        "colorfulness": 0.0,
        "warmth": 0.0,
        "sky_score": 0.0,
    }

    valid_count = 0

    for _, row in df.iterrows():
        pid = str(row["id"])
        if pid in cache:
            analysis = cache[pid]
            # Assumes BINS = 32 based on image_analyzer.py
            r_sum += np.array(analysis.get("r_hist", empty_hist))
            g_sum += np.array(analysis.get("g_hist", empty_hist))
            b_sum += np.array(analysis.get("b_hist", empty_hist))

            # Aggregate IRQ metrics
            for key in metrics_sum.keys():
                metrics_sum[key] += float(analysis.get(key, 0.0))

            valid_count += 1

    if valid_count > 0:
        # Normalize to average curves and average metrics
        r_sum = r_sum / valid_count
        g_sum = g_sum / valid_count
        b_sum = b_sum / valid_count

        for key in metrics_sum.keys():
            metrics_sum[key] = round(metrics_sum[key] / valid_count, 2)

    return {
        "r_hist": r_sum.tolist(),
        "g_hist": g_sum.tolist(),
        "b_hist": b_sum.tolist(),
        "brightness": metrics_sum["brightness"],
        "colorfulness": metrics_sum["colorfulness"],
        "warmth": metrics_sum["warmth"],
        "sky_score": metrics_sum["sky_score"],
        "count": valid_count,
    }


@router.get("/palette")
async def get_color_palette(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    # TBD: Dynamic K-Means on pixels returning Hex
    return [
        {"color": "#FFFFFF", "percentage": 15},
        {"color": "#000000", "percentage": 10},
        {"color": "#4A90E2", "percentage": 75},
    ]


@router.get("/trending")
async def get_trending_colors(
    loc: LocationFilter = Depends(location_filter),
) -> List[Dict[str, Any]]:
    # TBD: Chronological mood shifts
    return [
        {"month": "2024-01", "dominant_color": "#FFFFFF"},
        {"month": "2024-02", "dominant_color": "#000000"},
        {"month": "2024-03", "dominant_color": "#4A90E2"},
    ]

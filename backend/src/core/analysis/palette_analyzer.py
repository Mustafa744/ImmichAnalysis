"""
palette_analyzer.py

Aggregates per-photo swatches into a definitive location color signature.
Executes Agglomerative Clustering in CIELAB space to extract the top 3 
dominant, true-to-life colors per swatch category, avoiding muddy averages.
"""

from __future__ import annotations

from collections import defaultdict
import numpy as np
from skimage.color import rgb2lab, lab2rgb
from sklearn.cluster import AgglomerativeClustering

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Canonical Vibrant swatch types in display order (vivid → muted).
SWATCH_TYPES: list[str] = [
    "vibrant",
    "light_vibrant",
    "dark_vibrant",
    "muted",
    "light_muted",
    "dark_muted",
]

# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_str: str) -> list[int]:
    """Convert '#AABBCC' → [170, 187, 204]."""
    h = hex_str.lstrip("#")
    return [int(h[i : i + 2], 16) for i in (0, 2, 4)]

def _extract_rgb(c: dict) -> list[int] | None:
    """Pull rgb out of a swatch dict; return None on bad input."""
    if "rgb" in c:
        return c["rgb"]
    elif "hex" in c:
        return _hex_to_rgb(c["hex"])
    return None

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_location_palette(all_colors: list[dict]) -> dict[str, list[str]]:
    """
    Executes the Top-3 Agglomerative Format:
    1. Isolate by Category: pool all swatches of each type.
    2. Convert to LAB Space: convert pooled RGBs to CIELAB using skimage.
    3. Cluster: run Agglomerative Clustering with strict color boundaries.
    4. Extract: find the median color of the largest clusters.
    5. Assemble: return the top 3 hex codes for each swatch.

    Args:
        all_colors: Flat list of swatch dicts pooled from every photo in the location.

    Returns:
        Dictionary mapping each swatch type to a list of up to 3 Hex strings.
    """
    if not all_colors:
        return {}

    # 1. Isolate by Category
    buckets: dict[str, list[list[int]]] = defaultdict(list)

    for c in all_colors:
        rgb = _extract_rgb(c)
        if rgb is None:
            continue
            
        swatch_type = c.get("swatch_type")
        if swatch_type in SWATCH_TYPES:
            buckets[swatch_type].append(rgb)

    final_palette: dict[str, list[str]] = {}

    for swatch_type in SWATCH_TYPES:
        if swatch_type not in buckets or not buckets[swatch_type]:
            final_palette[swatch_type] = []
            continue

        rgb_array = np.array(buckets[swatch_type], dtype=np.float32) / 255.0

        # 2. Convert to LAB Space
        lab_array = rgb2lab(rgb_array.reshape(-1, 1, 3)).reshape(-1, 3)

        # 3. Calculate Representative Colors via Agglomerative Clustering
        if len(lab_array) < 3:
            # If we have fewer than 3 colors total, just use them directly
            unique_labels = np.arange(len(lab_array))
            labels = unique_labels
            counts = np.ones(len(lab_array), dtype=int)
        else:
            agglo = AgglomerativeClustering(
                n_clusters=None, 
                distance_threshold=22, 
                linkage='complete'
            )
            labels = agglo.fit_predict(lab_array)
            unique_labels, counts = np.unique(labels, return_counts=True)

        # 4. Extract Medians of the clusters
        lab_centers = []
        for label in unique_labels:
            cluster_points = lab_array[labels == label]
            lab_centers.append(np.median(cluster_points, axis=0))
            
        lab_centers = np.array(lab_centers)

        # Convert medians back to 0-1 RGB
        rgb_centers = lab2rgb(lab_centers.reshape(-1, 1, 3)).reshape(-1, 3)

        # 5. Extract Top 3 and Assemble Hex Codes
        sorted_indices = np.argsort(counts)[::-1]
        top_3_hex_codes = []
        
        for idx in sorted_indices[:3]:
            rank_rgb = rgb_centers[idx]
            r, g, b = (np.clip(rank_rgb, 0, 1) * 255).astype(int)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            top_3_hex_codes.append(hex_color)

        final_palette[swatch_type] = top_3_hex_codes

    return final_palette
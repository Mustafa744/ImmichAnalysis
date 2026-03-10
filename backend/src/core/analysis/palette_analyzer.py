import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

# How aggressively to boost saturated colors during aggregation.
# weight_i *= (1 + SATURATION_BOOST * S_norm), so at S=255 → ~3× boost.
_SATURATION_BOOST = 5.0


def _hex_to_rgb(hex_str: str) -> list[int]:
    """Convert '#AABBCC' to [170, 187, 204]."""
    h = hex_str.lstrip("#")
    return [int(h[i : i + 2], 16) for i in (0, 2, 4)]


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))


def _saturation_boost_weights(
    rgb_array: np.ndarray,
    base_weights: np.ndarray,
    boost: float = _SATURATION_BOOST,
) -> np.ndarray:
    """
    Multiply each sample weight by a saturation-based boost factor.

    Factor = 1 + boost * (S / 255), where S is the HSV saturation.
    Low-saturation (muddy) colors keep factor ≈ 1,
    high-saturation (vivid) colors get factor up to 1 + boost.
    """
    hsv_row = cv2.cvtColor(rgb_array.reshape(1, -1, 3), cv2.COLOR_RGB2HSV)
    sat = hsv_row.reshape(-1, 3)[:, 1].astype(np.float32) / 255.0  # 0-1
    factor = 1.0 + boost * sat
    return base_weights * factor


def compute_location_palette(
    all_colors: list[dict],
    k: int = 5,
) -> list[dict]:
    """
    Aggregate per-photo dominant colors into a single location palette.

    Pipeline:
      1. Collect RGB + proportion from every photo's dominant colors.
      2. Boost weights by saturation so vivid colors dominate over muddy tones.
      3. Cluster in CIELAB (perceptually uniform) with boosted weights.
      4. Convert centroids back to RGB for output.

    Args:
        all_colors: flat list of {"hex", "rgb", "proportion"} dicts
                    pooled from every photo in the location.
        k: number of palette colors to return.

    Returns:
        Sorted list of [{"hex": "#...", "rgb": [...], "proportion": float}]
    """
    if not all_colors:
        return []

    rgb_array = np.array([c["rgb"] for c in all_colors], dtype=np.uint8)
    base_weights = np.array(
        [c.get("proportion", c.get("percentage", 1.0)) for c in all_colors],
        dtype=float,
    )

    n_unique = len(np.unique(rgb_array, axis=0))
    effective_k = min(k, n_unique)
    if effective_k == 0:
        return []

    # Boost vivid colors so they outweigh muddy earth tones
    weights = _saturation_boost_weights(rgb_array, base_weights)

    # Convert RGB → LAB for perceptually uniform clustering
    lab_row = cv2.cvtColor(rgb_array.reshape(1, -1, 3), cv2.COLOR_RGB2LAB)
    lab_array = lab_row.reshape(-1, 3).astype(np.float32)

    km = MiniBatchKMeans(
        n_clusters=effective_k, random_state=42, n_init=3, batch_size=256
    )
    labels = km.fit_predict(lab_array, sample_weight=weights)
    centroids_lab = km.cluster_centers_

    # Convert LAB centroids → RGB
    lab_centroids_img = centroids_lab.reshape(1, -1, 3).astype(np.uint8)
    rgb_centroids = cv2.cvtColor(lab_centroids_img, cv2.COLOR_LAB2RGB).reshape(-1, 3)

    # Weight-aware proportion per cluster (use boosted weights for consistency)
    cluster_weights = np.zeros(effective_k)
    for i, label in enumerate(labels):
        cluster_weights[label] += weights[i]
    total_weight = cluster_weights.sum()
    proportions = (
        (cluster_weights / total_weight) * 100
        if total_weight > 0
        else np.zeros(effective_k)
    )

    order = np.argsort(-proportions)

    palette = []
    for idx in order:
        r, g, b = rgb_centroids[idx]
        palette.append(
            {
                "hex": _rgb_to_hex(r, g, b),
                "rgb": [int(r), int(g), int(b)],
                "proportion": round(float(proportions[idx]), 1),
            }
        )

    return palette

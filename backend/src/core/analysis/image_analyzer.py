import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

BINS = 32  # per channel histogram bins
_THUMB_SIZE = (100, 100)

# HSV filter thresholds (0-255 OpenCV scale)
_MIN_SATURATION = 40
_MIN_VALUE = 30
_MAX_VALUE = 240
_MIN_SURVIVING_PIXELS = 10

# Saturation boost: weight_i *= (1 + _SAT_BOOST * S/255)
# Matches palette_analyzer._SATURATION_BOOST
_SAT_BOOST = 3.0


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB integers to a hex color string."""
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"


def _resize_rgb(img: np.ndarray) -> np.ndarray:
    """Resize an RGB numpy array to the standard thumbnail size."""
    return cv2.resize(img, _THUMB_SIZE, interpolation=cv2.INTER_AREA)


def _filter_pixels_hsv(
    pixels_rgb: np.ndarray,
    min_s: int = _MIN_SATURATION,
    min_v: int = _MIN_VALUE,
    max_v: int = _MAX_VALUE,
) -> tuple[np.ndarray, np.ndarray] | None:
    """
    Filter out unsaturated / too-dark / blown-out pixels.

    Args:
        pixels_rgb: (N, 3) uint8 RGB array
        min_s: Minimum saturation (0-255). Tunable:
               25 → inclusive (deserts, stone cities)
               40 → balanced default
               80 → strict, only vivid colors
        min_v: Minimum brightness value
        max_v: Maximum brightness value

    Returns:
        (filtered_rgb, saturation) tuple — both (M, 3)/(M,) uint8 arrays,
        or None if fewer than _MIN_SURVIVING_PIXELS survive.
    """
    # Reshape into a 1-row image so cvtColor works
    img_row = pixels_rgb.reshape(1, -1, 3).astype(np.uint8)
    hsv_row = cv2.cvtColor(img_row, cv2.COLOR_RGB2HSV)
    hsv = hsv_row.reshape(-1, 3)

    mask = (hsv[:, 1] > min_s) & (hsv[:, 2] > min_v) & (hsv[:, 2] < max_v)
    filtered = pixels_rgb[mask]

    if len(filtered) < _MIN_SURVIVING_PIXELS:
        return None
    return filtered, hsv[mask, 1]  # return saturation channel too


def _rgb_pixels_to_lab(pixels_rgb: np.ndarray) -> np.ndarray:
    """Convert (N, 3) uint8 RGB pixels to LAB float32."""
    img_row = pixels_rgb.reshape(1, -1, 3).astype(np.uint8)
    lab_row = cv2.cvtColor(img_row, cv2.COLOR_RGB2LAB)
    return lab_row.reshape(-1, 3).astype(np.float32)


def _lab_centroids_to_rgb(centroids_lab: np.ndarray) -> np.ndarray:
    """Convert (K, 3) LAB centroids back to uint8 RGB."""
    lab_row = centroids_lab.reshape(1, -1, 3).astype(np.uint8)
    rgb_row = cv2.cvtColor(lab_row, cv2.COLOR_LAB2RGB)
    return rgb_row.reshape(-1, 3)


def extract_dominant_colors_from_pixels(
    pixels: np.ndarray,
    k: int = 5,
    min_saturation: int = _MIN_SATURATION,
) -> list[dict]:
    """
    Extract k dominant colors using HSV filtering + saturation-weighted
    LAB-space KMeans.

    Pipeline:
      1. Filter pixels in HSV (remove unsaturated / dark / blown-out)
      2. Compute saturation-based sample weights (vivid pixels count more)
      3. Convert surviving pixels to CIELAB
      4. MiniBatchKMeans in LAB with saturation weights
      5. Convert centroids back to RGB for output

    Returns a list sorted by weighted dominance (largest cluster first):
        [{"hex": "#AABBCC", "rgb": [170, 187, 204], "proportion": 35.2}, ...]
    """
    # Ensure uint8 for cv2 conversions
    px_u8 = np.clip(pixels, 0, 255).astype(np.uint8)

    result = _filter_pixels_hsv(px_u8, min_s=min_saturation)
    if result is None:
        return []  # grayscale image, skip
    filtered, sat = result

    # Saturation-based sample weights: vivid pixels pull centroids harder
    sat_norm = sat.astype(np.float32) / 255.0
    sample_weights = 1.0 + _SAT_BOOST * sat_norm

    # Convert to LAB for perceptually uniform clustering
    lab_pixels = _rgb_pixels_to_lab(filtered)

    n_unique = len(np.unique(lab_pixels, axis=0))
    effective_k = min(k, n_unique)
    if effective_k == 0:
        return []

    km = MiniBatchKMeans(
        n_clusters=effective_k, random_state=42, n_init=3, batch_size=256
    )
    labels = km.fit_predict(lab_pixels, sample_weight=sample_weights)
    centroids_lab = km.cluster_centers_

    # Convert LAB centroids → RGB
    centroids_rgb = _lab_centroids_to_rgb(centroids_lab)

    # Weighted proportion per cluster
    cluster_weights = np.zeros(effective_k)
    for i, label in enumerate(labels):
        cluster_weights[label] += sample_weights[i]
    total = cluster_weights.sum()
    percentages = (
        (cluster_weights / total) * 100.0 if total > 0 else np.zeros(effective_k)
    )

    # Sort by dominance descending
    order = np.argsort(-percentages)
    sorted_centroids = centroids_rgb[order]
    sorted_pcts = percentages[order]

    return [
        {
            "hex": _rgb_to_hex(c[0], c[1], c[2]),
            "rgb": [int(c[0]), int(c[1]), int(c[2])],
            "proportion": round(float(p), 1),
        }
        for c, p in zip(sorted_centroids, sorted_pcts)
    ]


def extract_dominant_colors(
    img: np.ndarray,
    k: int = 5,
    min_saturation: int = _MIN_SATURATION,
) -> list[dict]:
    """Public convenience: accepts full RGB image, resizes, then extracts."""
    small = _resize_rgb(img)
    pixels = small.reshape(-1, 3)
    return extract_dominant_colors_from_pixels(pixels, k, min_saturation)


def analyze_thumbnail(img: np.ndarray) -> dict:
    """
    Analyze an RGB numpy array thumbnail.
    Computes histograms, IRQ metrics, and dominant colors in a single pass
    over the resized pixel matrix.
    """
    small = _resize_rgb(img)
    # float32 for vectorized math
    pixels = small.reshape(-1, 3).astype(np.float32)

    # --- Vectorized channel means & std ---
    channel_means = pixels.mean(axis=0)  # [R_mean, G_mean, B_mean]
    brightness = float(pixels.mean())
    colorfulness = float(pixels.std())
    warmth = float(channel_means[0] - channel_means[2])  # R - B

    # Sky score: blue minus red in top third
    top_third = small[:33, :, :]
    sky_score = float(top_third[:, :, 2].mean() - top_third[:, :, 0].mean())

    # --- cv2.calcHist is C-optimized, much faster than np.histogram ---
    # Convert to uint8 single-channel views for cv2.calcHist
    small_u8 = small  # already uint8 from cv2.resize
    r_hist = cv2.calcHist([small_u8], [0], None, [BINS], [0, 256]).flatten()
    g_hist = cv2.calcHist([small_u8], [1], None, [BINS], [0, 256]).flatten()
    b_hist = cv2.calcHist([small_u8], [2], None, [BINS], [0, 256]).flatten()

    # Normalize to density (matches original np.histogram(density=True) behavior)
    n_pixels = float(pixels.shape[0])
    bin_width = 256.0 / BINS
    r_hist = r_hist / (n_pixels * bin_width)
    g_hist = g_hist / (n_pixels * bin_width)
    b_hist = b_hist / (n_pixels * bin_width)

    # Dominant colors — reuse the already-resized float pixel matrix
    dominant = extract_dominant_colors_from_pixels(pixels, k=5)

    return {
        "brightness": round(brightness, 2),
        "colorfulness": round(colorfulness, 2),
        "sky_score": round(sky_score, 2),
        "warmth": round(warmth, 2),
        "r_hist": r_hist.tolist(),
        "g_hist": g_hist.tolist(),
        "b_hist": b_hist.tolist(),
        "dominant_colors": dominant,
    }


def extract_feature_vector(entry: dict) -> np.ndarray:
    """Flatten all numeric fields into a single vector for clustering."""
    scalar = [
        entry["brightness"],
        entry["colorfulness"],
        entry["sky_score"],
        entry["warmth"],
    ]
    hist = entry["r_hist"] + entry["g_hist"] + entry["b_hist"]  # 96 dims
    return np.array(scalar + hist, dtype=np.float32)

import numpy as np
from PIL import Image

BINS = 32  # per channel histogram bins


def analyze_thumbnail(img: Image.Image) -> dict:
    img_small = img.resize((100, 100))
    pixels    = np.array(img_small).reshape(-1, 3).astype(float)
    top_third = np.array(img_small)[:33, :, :]

    r_hist, _ = np.histogram(pixels[:, 0], bins=BINS, range=(0, 256), density=True)
    g_hist, _ = np.histogram(pixels[:, 1], bins=BINS, range=(0, 256), density=True)
    b_hist, _ = np.histogram(pixels[:, 2], bins=BINS, range=(0, 256), density=True)

    return {
        "brightness":   round(float(pixels.mean()), 2),
        "colorfulness": round(float(pixels.std()), 2),
        "sky_score":    round(float(top_third[:, :, 2].mean() - top_third[:, :, 0].mean()), 2),
        "warmth":       round(float(pixels[:, 0].mean() - pixels[:, 2].mean()), 2),
        "r_hist":       r_hist.tolist(),
        "g_hist":       g_hist.tolist(),
        "b_hist":       b_hist.tolist(),
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
    return np.array(scalar + hist, dtype=float)

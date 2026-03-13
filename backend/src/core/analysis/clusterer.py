import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def extract_feature_vector(entry: dict) -> np.ndarray:
    """Flatten all numeric fields into a single vector for clustering."""
    scalar = [
        entry.get("brightness", 0),
        entry.get("colorfulness", 0),
        entry.get("sky_score", 0),
        entry.get("warmth", 0),
    ]
    empty_hist = [0] * 32
    hist = (
        entry.get("r_hist", empty_hist) + 
        entry.get("g_hist", empty_hist) + 
        entry.get("b_hist", empty_hist)
    )
    return np.array(scalar + hist, dtype=np.float32)

def build_feature_matrix(results: dict, ids: list[str]) -> tuple[np.ndarray, list[str]]:
    valid_ids = [i for i in ids if i in results]
    matrix = np.array([extract_feature_vector(results[i]) for i in valid_ids])
    return matrix, valid_ids


def cluster_photos(
    results: dict,
    ids: list[str],
    n_clusters: int = 8,
    random_state: int = 42,
) -> dict[str, int]:
    """Returns {asset_id: cluster_label}."""
    matrix, valid_ids = build_feature_matrix(results, ids)
    scaled = StandardScaler().fit_transform(matrix)
    labels = KMeans(
        n_clusters=n_clusters, random_state=random_state, n_init="auto"
    ).fit_predict(scaled)
    return dict(zip(valid_ids, labels.tolist()))


def build_country_profiles(
    travel: pd.DataFrame,
    results: dict,
    id_col: str = "id",
    country_col: str = "country",
) -> pd.DataFrame:
    """
    Returns a DataFrame indexed by country with mean values
    for all scalar metrics.
    """
    SCALAR_METRICS = ["brightness", "colorfulness", "sky_score", "warmth"]
    rows = []

    for country, group in travel.groupby(country_col):
        ids = group[id_col].tolist()
        values = [results[i] for i in ids if i in results]
        if not values:
            continue
        row = {"country": country, "n_photos": len(values)}
        for m in SCALAR_METRICS:
            row[m] = round(np.mean([v[m] for v in values]), 3)
        rows.append(row)

    return pd.DataFrame(rows).set_index("country")

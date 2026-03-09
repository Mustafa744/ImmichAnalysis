from typing import List
from pydantic import BaseModel


class ImageAnalysis(BaseModel):
    brightness: float
    colorfulness: float
    sky_score: float
    warmth: float
    r_hist: List[float]
    g_hist: List[float]
    b_hist: List[float]


class ClusterResult(BaseModel):
    asset_id: str
    cluster_label: int

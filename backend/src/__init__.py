# src/__init__.py
# Expose main components for easier access

from .infrastructure.clients.immich import ImmichClient
from .infrastructure.persistence.cache import ThumbnailCache
from .core.analysis.pipeline import BatchAnalyzer, AnalysisStep
from .core.analysis.clusterer import cluster_photos
from .core.visualization.travel_visualizer import TravelVisualizer

__all__ = [
    "ImmichClient",
    "ThumbnailCache",
    "BatchAnalyzer",
    "AnalysisStep",
    "cluster_photos",
    "TravelVisualizer",
]

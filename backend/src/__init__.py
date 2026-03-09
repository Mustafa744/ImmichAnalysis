# src/__init__.py
# Expose main components for easier access

from .infrastructure.clients.immich import ImmichClient
from .core.analysis.image_analyzer import analyze_thumbnail
from .infrastructure.persistence.cache import ThumbnailCache
from .core.analysis.clusterer import cluster_photos
from .core.visualization.travel_visualizer import TravelVisualizer
from .core.processing.photo_processor import load_and_preprocess_photos
from .app.core.config import CACHE_PATH

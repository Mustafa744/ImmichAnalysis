import pandas as pd
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from app.core.config import IMMICH_URL, API_KEY, CACHE_PATH, MAX_WORKERS
from infrastructure.clients.immich import ImmichClient
from infrastructure.clients.database import get_all_photos
from infrastructure.persistence.cache import ThumbnailCache
from core.analysis.image_analyzer import analyze_thumbnail
from core.analysis.clusterer import cluster_photos
from core.processing.photo_processor import load_and_preprocess_photos


class PhotoService:
    def __init__(self):
        self.immich_client = ImmichClient(IMMICH_URL, API_KEY)
        self.cache = ThumbnailCache(str(CACHE_PATH))

    def get_photos_dataframe(self) -> pd.DataFrame:
        """Fetch all photos from database."""
        return get_all_photos()

    def process_and_analyze(self, force_refresh: bool = False):
        """Main pipeline: download thumbnails and analyze."""
        df = self.get_photos_dataframe()
        all_ids = df["id"].tolist()

        missing_ids = self.cache.missing_from(all_ids)
        if not missing_ids:
            print("All photos already analyzed and cached.")
            return self.cache.data

        print(f"Analyzing {len(missing_ids)} missing photos...")

        def process_one(asset_id: str):
            img = self.immich_client.get_thumbnail(asset_id)
            if img:
                return asset_id, analyze_thumbnail(img)
            return asset_id, None

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(
                tqdm(
                    executor.map(process_one, missing_ids),
                    total=len(missing_ids),
                    desc="Analyzing",
                )
            )

        for asset_id, analysis in results:
            if analysis:
                self.cache[asset_id] = analysis

        self.cache.save()
        return self.cache.data

    def get_clusters(self, n_clusters: int = 8):
        """Cluster photos based on cached analysis."""
        df = self.get_photos_dataframe()
        return cluster_photos(self.cache.data, df["id"].tolist(), n_clusters=n_clusters)

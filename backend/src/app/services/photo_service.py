import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from app.core.config import IMMICH_URL, API_KEY, CACHE_PATH, MAX_WORKERS
from infrastructure.clients.immich import ImmichClient
from infrastructure.clients.database import get_all_photos
from infrastructure.persistence.cache import ThumbnailCache
from core.analysis.image_analyzer import analyze_thumbnail, extract_dominant_colors
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

    def backfill_dominant_colors(self):
        """
        Backfill existing cache entries that are missing the 'dominant_colors' key.
        Re-downloads thumbnails only for those entries and extracts dominant colors.
        """
        needs_backfill = [
            aid for aid, data in self.cache.data.items()
            if "dominant_colors" not in data
        ]

        if not needs_backfill:
            print("All cache entries already have dominant_colors.")
            return

        print(f"Backfilling dominant_colors for {len(needs_backfill)} entries...")

        def backfill_one(asset_id: str):
            img = self.immich_client.get_thumbnail(asset_id)
            if img:
                return asset_id, extract_dominant_colors(img)
            return asset_id, None

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(
                tqdm(
                    executor.map(backfill_one, needs_backfill),
                    total=len(needs_backfill),
                    desc="Backfilling colors",
                )
            )

        updated = 0
        for asset_id, colors in results:
            if colors and asset_id in self.cache:
                self.cache[asset_id]["dominant_colors"] = colors
                updated += 1

        self.cache.save()
        print(f"Backfilled {updated} entries with dominant_colors.")

    def get_clusters(self, n_clusters: int = 8):
        """Cluster photos based on cached analysis."""
        df = self.get_photos_dataframe()
        return cluster_photos(self.cache.data, df["id"].tolist(), n_clusters=n_clusters)

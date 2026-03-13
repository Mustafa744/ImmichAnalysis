import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from app.core.config import IMMICH_URL, API_KEY, CACHE_PATH, MAX_WORKERS
from infrastructure.clients.immich import ImmichClient
from infrastructure.clients.database import get_all_photos
from infrastructure.persistence.cache import ThumbnailCache
from core.analysis.pipeline import (
    BatchAnalyzer,
    HistogramAnalysis,
    MetricsAnalysis,
    ColorPaletteAnalysis,
)
from core.analysis.clusterer import cluster_photos


class PhotoService:
    """
    A service class that orchestrates downloading images from Immich
    and passing them through the analysis pipeline. It integrates caching
    to prevent re-analyzing images on subsequent runs.
    """

    def __init__(self):
        self.immich_client = ImmichClient(IMMICH_URL, API_KEY)
        self.cache = ThumbnailCache(str(CACHE_PATH))
        self.analyzer = BatchAnalyzer(
            [HistogramAnalysis(), MetricsAnalysis(), ColorPaletteAnalysis()]
        )

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
            if img is not None:
                return asset_id, self.analyzer.analyze_single(img)
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

    def backfill_color_palette(self):
        """
        Backfill existing cache entries that are missing the 'color_palette' key.
        Re-downloads thumbnails only for those entries and extracts the palette.
        """
        needs_backfill = [
            aid for aid, data in self.cache.data.items() if "color_palette" not in data
        ]

        if not needs_backfill:
            print("All cache entries already have color_palette.")
            return

        print(f"Backfilling color_palette for {len(needs_backfill)} entries...")
        palette_analyzer = BatchAnalyzer([ColorPaletteAnalysis()])

        def backfill_one(asset_id: str):
            img = self.immich_client.get_thumbnail(asset_id)
            if img is not None:
                return asset_id, palette_analyzer.analyze_single(img)
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
        for asset_id, res in results:
            if res and asset_id in self.cache:
                self.cache[asset_id].update(res)
                updated += 1

        self.cache.save()
        print(f"Backfilled {updated} entries with color_palette.")

    def get_clusters(self, n_clusters: int = 8) -> dict[str, int]:
        """
        Groups photos into chronological or semantic clusters based on their cached
        feature analysis (brightness, colorfulness, warmth, sky score, and histograms).

        Args:
            n_clusters (int): The number of clusters to generate.

        Returns:
            dict[str, int]: A mapping of asset_id to its assigned cluster label.
        """
        df = self.get_photos_dataframe()
        return cluster_photos(self.cache.data, df["id"].tolist(), n_clusters=n_clusters)

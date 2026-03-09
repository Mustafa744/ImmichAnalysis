from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any, Dict

from app.services.photo_service import PhotoService

router = APIRouter()


def get_photo_service() -> PhotoService:
    return PhotoService()


@router.post("/analyze", summary="Analyze photos")
def analyze_photos(
    force_refresh: bool = Query(False, description="Force re-analyzing even if cached"),
    service: PhotoService = Depends(get_photo_service),
) -> Dict[str, Any]:
    """
    Download thumbnails from Immich and run content analysis if not already cached.
    """
    try:
        results = service.process_and_analyze(force_refresh=force_refresh)
        return {"status": "success", "analyzed_count": len(results) if results else 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clusters", summary="Get clustered photos")
def get_clusters(
    n_clusters: int = Query(
        8, ge=2, le=50, description="Number of clusters to generate"
    ),
    service: PhotoService = Depends(get_photo_service),
) -> Dict[str, Any]:
    """
    Returns image clusters based on similarities in brightness, colorfulness, warmth, etc.
    """
    try:
        clusters = service.get_clusters(n_clusters=n_clusters)
        return {"status": "success", "n_clusters": n_clusters, "clusters": clusters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

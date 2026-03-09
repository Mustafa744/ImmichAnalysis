from fastapi import APIRouter

from app.api.endpoints import photos, stats, countries, timeline, colors, insights

api_router = APIRouter()
api_router.include_router(photos.router, prefix="/photos", tags=["photos"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(colors.router, prefix="/colors", tags=["colors"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])

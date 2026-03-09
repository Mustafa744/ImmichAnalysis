from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class PhotoBase(BaseModel):
    id: str
    localDateTime: datetime
    fileCreatedAt: datetime
    isFavorite: bool
    visibility: str
    status: str
    width: Optional[int] = None
    height: Optional[int] = None


class PhotoExif(PhotoBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    lensModel: Optional[str] = None
    focalLength: Optional[float] = None
    fNumber: Optional[float] = None
    iso: Optional[int] = None
    exposureTime: Optional[str] = None
    fileSizeInByte: Optional[int] = None
    dateTimeOriginal: Optional[datetime] = None
    rating: Optional[int] = None


class PhotoInfo(PhotoExif):
    # Additional computed fields can go here
    pass

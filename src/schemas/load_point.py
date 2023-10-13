from typing import Optional
from pydantic import BaseModel


class ReadLoadPoint(BaseModel):
    GI: str
    total_load_point: int

class ReadLoadDensity(BaseModel):
    GI: str
    load_point_density_per_km2: Optional[float]

class GIRecommendation(BaseModel):
    GI: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
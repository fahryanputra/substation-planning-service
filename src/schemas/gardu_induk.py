from typing import Optional

from geoalchemy2 import Geometry
from pydantic import BaseModel


class GarduIndukBase(BaseModel):
    id: Optional[int]
    GI: Optional[str]
    Alamat: Optional[str]
    y: Optional[float]
    x: Optional[float]
    status: Optional[str]
    nama_group: Optional[str]


class ReadGarduInduk(BaseModel):
    available: list[str]


class GarduIndukLocation(BaseModel):
    GI: str
    latitude: float
    longitude: float

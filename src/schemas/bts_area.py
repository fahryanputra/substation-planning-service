from geoalchemy2 import Geometry
from pydantic import BaseModel


class BtsAreaBase(BaseModel):
    id: int
    nama_kp: str
    aj: str
    nama_area: str
    kd_kp: str
    kd_area: str
    geometry: Geometry

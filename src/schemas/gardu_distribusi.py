from geoalchemy2 import Geometry
from pydantic import BaseModel


class GarduBase(BaseModel):
    id: int
    kdarea: int
    nama_area: str
    kode_aset_: str
    nama_gi: str
    kode_ase_1: str
    nama_penyu: str
    kode_ase_2: int
    gardu: str
    alamat1: str
    gps_x: float
    gps_y: float
    status_rc: str
    fungsi_gar: str
    # geometry: Geometry

class GarduList(BaseModel):
    gardu: list[GarduBase]
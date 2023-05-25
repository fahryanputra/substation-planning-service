from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from src.models import models


def get_gardu(db: Session, gardu: str = None, nama_area: str = None, limit: int = 10):
    result = db.query(models.GarduDistribusi)

    if gardu is not None:
        result = result.filter(models.GarduDistribusi.gardu == gardu)
    if nama_area is not None:
        result = result.filter(models.GarduDistribusi.nama_area == nama_area)
    result = result.limit(limit).all()
    result = [item.__dict__ for item in result]
    
    return result

from sqlalchemy.orm import Session

from src.models import models


def get_gardu_induk(db: Session):
    result = db.query(models.GarduInduk).all()
    result = [item.GI for item in result]
    return result

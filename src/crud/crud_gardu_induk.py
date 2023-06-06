from sqlalchemy.orm import Session

from src.models import models


def get_gardu_induk(db: Session):
    result = db.query(models.GarduInduk).all()
    result = [item.GI for item in result]
    return result


def get_gardu_induk_location(db: Session, gi_name: str):
    result = db.query(models.GarduInduk).where(models.GarduInduk.GI == gi_name).first()

    if result is None:
        return {}

    return {"x": result.x, "y": result.y}


def get_all_gardu_induk(db: Session):
    result = db.query(models.GarduInduk).all()
    result = [item.__dict__ for item in result]
    return result
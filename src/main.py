from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .config import Settings
from .database import SessionLocal, engine
from .models import models
from .crud import crud_gardu_distribusi, crud_region, crud_gardu_induk
from .schemas import area, gardu_distribusi, gardu_induk

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
settings = Settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all-gardu-induk", response_model=gardu_induk.AllGardu)
async def all_gardu_induk_list(db: Session = Depends(get_db)):
    result = crud_gardu_induk.get_all_gardu_induk(db)

    print(result)

    data = {
        "gardu_induk": result,
    }
    return gardu_induk.AllGardu(**data)


@app.get("/all-gardu-distribusi", response_model=gardu_distribusi.AllGardu)
async def all_gardu_distribusi_list(db: Session = Depends(get_db)):
    result = crud_gardu_distribusi.get_all_gardu(db)

    data = {
        "gardu": result,
    }
    return gardu_distribusi.AllGardu(**data)


@app.get("/available-gardu-induk", response_model=gardu_induk.ReadGarduInduk)
async def gardu_induk_name_list(db: Session = Depends(get_db)):
    result = crud_gardu_induk.get_gardu_induk(db)

    data = {
        "available": result,
    }

    return gardu_induk.ReadGarduInduk(**data)


@app.get("/gardu-induk-location", response_model=gardu_induk.GarduIndukLocation)
async def gardu_induk_location(area_name: str, db: Session = Depends(get_db)):
    result = crud_gardu_induk.get_gardu_induk_location(db, gi_name=area_name)

    if not result:
        result["x"] = 0
        result["y"] = 0

    data = {
        "GI": area_name,
        "latitude": result["y"],
        "longitude": result["x"],
    }


    return gardu_induk.GarduIndukLocation(**data)


@app.get("/gardu-distribusi", response_model=gardu_distribusi.GarduList)
async def gardu_distribusi_list(gardu: str = None, nama_area: str = None, nama_gi: str = None, limit: int = 10, db: Session = Depends(get_db)):
    result = crud_gardu_distribusi.get_gardu(db, gardu, nama_area, nama_gi, limit)

    data = {
        "gardu": result,
    }
    
    return gardu_distribusi.GarduList(**data)


@app.get("/area", response_model=area.ReadArea)
async def main_substation_area(method: str, area_name: str, db: Session = Depends(get_db)):
    area_result = crud_region.calculate_gi_region(db, gi_name=area_name, calc_method=method)

    data = {
        "GI": area_name,
        "area": area_result,
    }

    return area.ReadArea(**data)


# TODO
@app.get("/total")
async def load_point_total():
    return {"message": "Endpoint Total Titik Beban"}


# TODO
@app.get("/capacity")
async def load_point_capacity():
    return {"message": "Endpoint Rekap Titik Beban"}


# TODO
@app.get("/density")
async def main_substation_density():
    return {"message": "Endpoint Kerapatan GI"}

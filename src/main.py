from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .config import Settings
from .database import SessionLocal, engine
from .models import models
from .crud import crud_calc_method, crud_gardu_distribusi, crud_gardu_induk, crud_load_point
from .schemas import area, gardu_distribusi, gardu_induk, calc_method, load_point

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
    return {"status": "Server is up"}


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


@app.get("/calc-methods")
async def all_calc_method_list(db: Session = Depends(get_db)):
    result = crud_calc_method.get_all_calc_method(db)

    print(result)

    data = {
        "methods": result,
    }
    return data


@app.post("/calc-method", response_model=calc_method.CalcMethodBase)
async def create_calc_method(calc_method:str, db: Session = Depends(get_db)):
    db_calc_method = crud_calc_method.get_calc_method_by_name(db, calc_method)
    if db_calc_method:
        raise HTTPException(status_code=400, detail="Calculation method already exists")
    return crud_calc_method.create_calc_method(db=db, calc_method=calc_method)


@app.put("/calc-method/{id}")
async def update_calc_method(id, db: Session = Depends(get_db)):
    return crud_calc_method.update_calc_method(db=db, id=id)


@app.delete("/calc-method/{id}")
async def delete_calc_method(id, db: Session = Depends(get_db)):
    return crud_calc_method.delete_calc_method(db=db, id=id)


@app.get("/area", response_model=area.ReadArea)
async def main_substation_area(method: str, area_name: str, db: Session = Depends(get_db)):
    area_result = crud_calc_method.get_area(db, gi_name=area_name, calc_method=method)

    data = {
        "GI": area_name,
        "area": area_result,
    }
    return area.ReadArea(**data)


@app.get("/recommendation", response_model=load_point.GIRecommendation)
async def get_gi_recommendation(method: str, area_name: str, db: Session = Depends(get_db)):
    result = crud_load_point.get_gi_recommendation(db=db, gi_name=area_name, calc_method=method)

    if not result:
        result["x"] = 0
        result["y"] = 0

    data = {
        "GI": area_name,
        "latitude": result["y"],
        "longitude": result["x"],
    }

    return load_point.GIRecommendation(**data)


@app.get("/total", response_model=load_point.ReadLoadPoint)
async def load_point_total(gi_name: str, calc_method: str, db: Session = Depends(get_db)):
    total_load_point = crud_load_point.get_load_points(gi_name=gi_name, calc_method=calc_method, db=db)
    print(total_load_point)
    data = {
        "GI": gi_name,
        "total_load_point": total_load_point,
    }
    return load_point.ReadLoadPoint(**data)


@app.get("/density", response_model=load_point.ReadLoadDensity)
async def main_substation_density(gi_name: str, calc_method: str, db: Session = Depends(get_db)):
    load_point_density = crud_load_point.get_load_density(gi_name=gi_name, calc_method=calc_method, db=db)
    print(load_point_density)
    data = {
        "GI": gi_name,
        "load_point_density_per_km2": "{:.3f}".format(load_point_density),
    }
    return load_point.ReadLoadDensity(**data)


# TODO
# @app.get("/capacity")
# async def load_point_capacity():
#     return {"message": "Endpoint Rekap Titik Beban"}


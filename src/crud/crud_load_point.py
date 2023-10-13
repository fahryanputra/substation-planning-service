import geojson

from shapely import Polygon
from fastapi import HTTPException
from src.models import models
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import shape
from geoalchemy2 import func
from pyproj import Geod


def __get_gi_area(db: Session, gi_name: str, calc_method: str):
    selected_gi = db.query(models.GarduInduk).filter(models.GarduInduk.GI == gi_name).first()
    if selected_gi is None:
            return 0
    
    result = None
    selected_gi = to_shape(selected_gi.geometry)
    gi_region_query = db.query(models.RegionGI.geometry).filter(models.RegionGI.calc_method == calc_method).first()

    if gi_region_query is None:
         raise HTTPException(status_code=400, detail="Calculation method is not implemented")
    
    gi_region = geojson.loads(gi_region_query[0])
    for polygon in gi_region.geometries:
        polygon: Polygon = shape(polygon)
        if polygon.contains(selected_gi):
            result = polygon
            break
    return result

def get_load_points(db: Session, gi_name: str, calc_method: str):
    result = None
    
    selected_gi = __get_gi_area(db=db, gi_name=gi_name, calc_method=calc_method)
    area = from_shape(selected_gi, srid=4326)
    result = db.query(models.GarduDistribusi).filter(func.ST_Contains(area, models.GarduDistribusi.geometry)).count()
    return result

def get_load_density(db: Session, gi_name: str, calc_method: str):
    result = None

    selected_gi = __get_gi_area(db=db, gi_name=gi_name, calc_method=calc_method)
    geod = Geod(ellps="WGS84")
    area, perimeter = geod.geometry_area_perimeter(selected_gi)
    area = round(abs(area) / 10**6)
    load_point = get_load_points(db=db, gi_name=gi_name, calc_method=calc_method)

    result = load_point / area

    return result

def get_gi_recommendation(db: Session, gi_name: str, calc_method:str):
    selected_gi = __get_gi_area(db=db, gi_name=gi_name, calc_method=calc_method)
    area = from_shape(selected_gi, srid=4326)
    load_points = db.query(func.ST_Collect(models.GarduDistribusi.geometry)).filter(func.ST_Contains(area, models.GarduDistribusi.geometry))
    result = db.query(func.ST_Centroid(load_points)).first()
    result_x = db.query(func.ST_X(result[0])).first()
    result_y = db.query(func.ST_Y(result[0])).first()
    if result is None:
        return {}

    return {"x": result_x[0], "y": result_y[0]}
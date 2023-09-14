import pandas as pd
import geopandas as gpd
import geojson

from fastapi import HTTPException
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from shapely import GeometryCollection, Polygon
from shapely.geometry import shape
from shapely.wkt import loads
from sqlalchemy.orm import Session
from geoalchemy2 import func
from pyproj import Geod
from geojson import GeometryCollection

from src.models import models
from src.schemas import area

def __get_gi_region(db:Session, calc_method:str):
    result = None
    if calc_method == "voronoi":
        voronoi_query = db.query(func.ST_VoronoiPolygons(func.ST_Collect(models.GarduInduk.geometry), 0.0)).first()
        voronoi_polygons: WKBElement = voronoi_query[0]

        shapely_polygons: GeometryCollection = to_shape(voronoi_polygons)
        result = GeometryCollection(list(shapely_polygons.geoms))

        return result
    elif calc_method == "convex_hull":
        sql = db.execute("""   
        SELECT gi_terdekat.id AS gi_id, ST_AsText(gardu.geometry) AS geometry
        FROM gardu
        CROSS JOIN LATERAL(
            SELECT id, "GI", ST_Distance(gardu.geometry, gardu_induk.geometry) as dist
	        FROM gardu_induk
	        WHERE ST_DWithin(gardu_induk.geometry, gardu.geometry, 0.5)
	        ORDER BY ST_Distance(gardu_induk.geometry, gardu.geometry)
	        LIMIT 1
        ) AS gi_terdekat 
        """)

        new_area = gpd.GeoDataFrame(pd.DataFrame.from_records(sql.mappings().all()))
        new_area.geometry = new_area['geometry'].apply(loads)
        convex_hull = new_area.dissolve("gi_id").convex_hull.reset_index()
        result = GeometryCollection(list(convex_hull.geometry))

        return result
    else:
        raise HTTPException(status_code=400, detail="Method not available")
    
def get_area_by_name(db: Session, calc_method: str):
    return db.query(models.RegionGI).filter(models.RegionGI.calc_method == calc_method).first()

def create_area(db: Session, calc_method: str):
    db_geom = __get_gi_region(db=db, calc_method=calc_method)
    db_area = models.RegionGI(calc_method = calc_method, geometry = geojson.dumps(db_geom))
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area
        
def get_area(db: Session, gi_name: str, calc_method: str):
    result = None
    selected_gi = db.query(models.GarduInduk).filter(models.GarduInduk.GI == gi_name).first()
    if selected_gi is None:
            return 0

    new_polygon = None
    selected_gi = to_shape(selected_gi.geometry)
    gi_region_query = db.query(models.RegionGI.geometry).filter(models.RegionGI.calc_method == calc_method).first()

    if gi_region_query is None:
         raise HTTPException(status_code=400, detail="Calculation method is not implemented")
    
    gi_region = geojson.loads(gi_region_query[0])
    for polygon in gi_region.geometries:
        polygon: Polygon = shape(polygon)
        if polygon.contains(selected_gi):
            new_polygon = polygon
            break

    geod = Geod(ellps="WGS84")
    area, perimeter = geod.geometry_area_perimeter(new_polygon)
    result = round(abs(area))
    
    return result
import pandas as pd
import geopandas as gpd

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from shapely import GeometryCollection
from shapely.wkt import loads
from sqlalchemy.orm import Session
from geoalchemy2 import func
from pyproj import Geod

from src.models import models


def calculate_gi_region(db: Session, gi_name: str, calc_method: str):
    result = None
    if calc_method == "voronoi":
        voronoi_query = db.query(func.ST_VoronoiPolygons(func.ST_Collect(models.GarduInduk.geometry), 0.0)).first()
        voronoi_polygons: WKBElement = voronoi_query[0]

        shapely_polygons: GeometryCollection = to_shape(voronoi_polygons)

        selected_gi = db.query(models.GarduInduk).filter(models.GarduInduk.GI == gi_name).first()
        if selected_gi is None:
            return 0

        selected_gi = to_shape(selected_gi.geometry)
        voronoi_polygon = None
        for polygon in shapely_polygons.geoms:
            if polygon.contains(selected_gi):
                voronoi_polygon = polygon
                break

        # Voronoi Area
        geod = Geod(ellps="WGS84")
        area, perimeter = geod.geometry_area_perimeter(voronoi_polygon)
        result = round(abs(area))
    elif calc_method == "convex_hull":
        result = None
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
        # new_area = sql.mappings().all()
        # convex_hull = db.query(func.ST_Convex_Hull(func.ST_Collect(new_area['geometry']))).group_by(new_area['gi_id'])

        new_area = gpd.GeoDataFrame(pd.DataFrame.from_records(sql.mappings().all()))
        new_area.geometry = new_area['geometry'].apply(loads)
        new_area = new_area.set_crs('epsg:4326')
        convex_hull = new_area.dissolve("gi_id").convex_hull.reset_index()
        new_area = new_area.set_crs('epsg:4326')

        
        # convex_hull_polygons: WKBElement = convex_hull[0]
        
        # shapely_polygons: GeometryCollection = to_shape(convex_hull_polygons)

        selected_gi = db.query(models.GarduInduk).filter(models.GarduInduk.GI == gi_name).first()
        if selected_gi is None:
            return 0

        selected_gi = to_shape(selected_gi.geometry)
        convex_hull_polygon = None
        for polygon in convex_hull.geometry:
            if polygon.contains(selected_gi):
                convex_hull_polygon = polygon
                break

        # Convex Hull Area
        geod = Geod(ellps="WGS84")
        area, perimeter = geod.geometry_area_perimeter(convex_hull_polygon)
        result = round(abs(area))
    else:
        NotImplementedError("Calculation method not implemented")

    return result

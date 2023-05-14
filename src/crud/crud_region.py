import pyproj
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from shapely import GeometryCollection
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
        # TODO
        pass
    else:
        NotImplementedError("Calculation method not implemented")

    return result

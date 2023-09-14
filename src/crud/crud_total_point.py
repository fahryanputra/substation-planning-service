from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from shapely import GeometryCollection
from sqlalchemy.orm import Session
from geoalchemy2 import func
from pyproj import Geod

from src.models import models

def get_area_load_total():
    return


# def gd_in_voronoi_gi(item, gi):
#     result = gi['geom_poly'].contains(item)
    
#     if result.any():
#         # GD already covered by a voronoi polygon
#         result = gi[result]
#         return result['GI'].iloc[0]
#     else:
#         # no matching voronoi polygons
#         return "-"

# temp = gd_gdf['geometry'].apply(lambda i: gd_in_voronoi_gi(i, gi_gdf))

# gd_gdf['gi_voronoi'] = temp
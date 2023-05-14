from shapely import Polygon
from sqlalchemy import BigInteger, CheckConstraint, Column, Float, Integer, String, Table, Text
from geoalchemy2.types import Geometry

from src.database import Base

metadata = Base.metadata


class BtsArea(Base):
    __tablename__ = 'bts_area'

    id = Column(BigInteger, primary_key=True)
    nama_kp = Column(Text)
    aj = Column(Text)
    nama_area = Column(Text)
    kd_kp = Column(Text)
    kd_area = Column(Text)
    geometry = Column(Geometry(srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)


class Gardu(Base):
    __tablename__ = 'gardu'

    id = Column(BigInteger, primary_key=True)
    kdarea = Column(BigInteger)
    nama_area = Column(Text)
    kode_aset_ = Column(Text)
    nama_gi = Column(Text)
    kode_ase_1 = Column(Text)
    nama_penyu = Column(Text)
    kode_ase_2 = Column(BigInteger)
    gardu = Column(Text)
    alamat1 = Column(Text)
    gps_x = Column(Float(53))
    gps_y = Column(Float(53))
    status_rc = Column(Text)
    fungsi_gar = Column(Text)
    geometry = Column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)


class GarduInduk(Base):
    __tablename__ = 'gardu_induk'

    id = Column(BigInteger, primary_key=True)
    GI = Column(Text)
    Alamat = Column(Text)
    y = Column(Float(53))
    x = Column(Float(53))
    status = Column(Text)
    nama_group = Column(Text)
    geometry = Column(Geometry('POINT', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)


class RegionGI(Base):
    __tablename__ = 'gardu_induk_region'

    id = Column(BigInteger, primary_key=True)
    GI = Column(Text)
    calc_method = Column(Text)
    geometry = Column(Geometry('POLYGON', 4326, from_text='ST_GeomFromEWKT', name='geometry'), index=True)


t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)

t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


class SpatialRefSys(Base):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        CheckConstraint('(srid > 0) AND (srid <= 998999)'),
    )

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))

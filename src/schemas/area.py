from pydantic import BaseModel


class ReadArea(BaseModel):
    GI: str
    area: float
    
# class CreateArea(BaseModel):
#     id: int
#     calc_method: str
#     geometry: str

#     class Config:
#         orm_mode = True

# class AllArea(BaseModel):
#     calc_method: list[AreaBase]

# class LoadTotal(BaseModel):
#     GI: str
#     load_total: int

# class LoadCapacity(BaseModel):
#     GI: str
#     load_capacity: float

# class LoadDensity(BaseModel):
#     GI: str
#     load_density: float
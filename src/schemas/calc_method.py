from typing import Optional
from pydantic import BaseModel

class CalcMethodBase(BaseModel):
    id: Optional[int]
    calc_method: Optional[str]
    geometry: Optional[str]

    class Config:
        orm_mode = True

class AllCalcMethod(BaseModel):
    calc_method_list: list[str]

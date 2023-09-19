from pydantic import BaseModel


class ReadArea(BaseModel):
    GI: str
    area: float
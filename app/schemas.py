from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Base64Str, Field
from enum import Enum

from app.models import Category, DamageClass


class DefectBase(BaseModel):
    image: str
    latitude: float
    longitude: float
    size: float
    category: Category
    damage_class: DamageClass
    is_open: bool = True


class DefectCreate(DefectBase):
    pass


class DefectUpdate(BaseModel):
    image: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    size: Optional[float] = None
    category: Optional[Category] = None
    damage_class: Optional[DamageClass] = None
    is_open: Optional[bool] = True

    class Config:
        use_enum_values = True


class DefectRead(DefectBase):
    id: str
    pass

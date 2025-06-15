from enum import Enum
from beanie import Document, PydanticObjectId
from bson import Decimal128


class Category(str, Enum):
    POTHOLE = 'pothole'
    CRACK = 'crack'

class DamageClass(str, Enum):
    MINOR = 'minor'
    MAJOR = 'major'
    CRITICAL = 'critical'

class Defect(Document):
    image: str
    latitude: float
    longitude: float
    size: float
    category: Category
    damage_class: DamageClass
    is_open: bool = True

    class Settings:
        name = 'defects'
        use_enum_values = True
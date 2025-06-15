from typing import Optional, List
from beanie import PydanticObjectId

from app.models import Defect
from app.schemas import DefectCreate, DefectUpdate


async def create_defect(defect_in: DefectCreate) -> Defect:
    defect = Defect(**defect_in.model_dump())
    await defect.insert()
    return defect


async def get_defects(
        category: Optional[str] = None,
        damage_class: Optional[str] = None,
        is_open: Optional[bool] = None
) -> List[Defect]:
    filter_query = {}
    if category is not None:
        filter_query['category'] = category
    if damage_class is not None:
        filter_query['damage_class'] = damage_class
    if is_open is not None:
        filter_query['is_open'] = is_open
    return await Defect.find(filter_query).to_list()


async def get_defect(defect_id: PydanticObjectId) -> Optional[Defect]:
    return await Defect.get(defect_id)


async def update_defect(defect_id: PydanticObjectId, defect_in: DefectUpdate) -> Optional[Defect]:
    defect = await Defect.get(defect_id)
    if not defect:
        return None
    update_data = defect_in.model_dump(exclude_unset=True)
    await defect.set(update_data)
    return defect


async def delete_defect(defect_id: PydanticObjectId) -> bool:
    defect = await Defect.get(defect_id)
    if not defect:
        return False
    await defect.delete()
    return True

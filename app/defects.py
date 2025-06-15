from fastapi import APIRouter, HTTPException, status, Query, Request
from typing import List, Optional
from beanie import PydanticObjectId

from app.schemas import DefectCreate, DefectRead, DefectUpdate
from app.crud import (
    create_defect, get_defects, get_defect,
    update_defect, delete_defect
)

router = APIRouter()


@router.post('/', response_model=DefectRead, name='Создать запись', status_code=status.HTTP_201_CREATED)
async def create_record(defect_in: DefectCreate):
    defect = await create_defect(defect_in)
    return DefectRead(**defect.model_dump(exclude={'id'}), id=str(defect.id))


@router.get('/', response_model=List[DefectRead], name='Получить все записи')
async def find_records(
        category: Optional[str] = Query(None),
        damage_class: Optional[str] = Query(None),
        is_open: Optional[bool] = Query(None)
):
    defects = await get_defects(category, damage_class, is_open)
    return [DefectRead(**defect.model_dump(exclude={'id'}), id=str(defect.id)) for defect in defects]


@router.get('/{defect_id}', response_model=DefectRead, name='Получить запись')
async def find_record(defect_id: PydanticObjectId):
    defect = await get_defect(defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail='Record not found')
    return DefectRead(**defect.model_dump(exclude={'id'}), id=str(defect.id))


@router.patch('/{defect_id}', response_model=DefectRead, name='Изменить запись')
async def update_record(defect_id: PydanticObjectId, defect_in: DefectUpdate):
    defect = await update_defect(defect_id, defect_in)
    if not defect:
        raise HTTPException(status_code=404, detail='Record not found')
    return DefectRead(**defect.model_dump(exclude={'id'}), id=str(defect.id))


@router.delete('/{defect_id}', name='Удалить запись', status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(defect_id: PydanticObjectId):
    success = await delete_defect(defect_id)
    if not success:
        raise HTTPException(status_code=404, detail='Record not found')
    return

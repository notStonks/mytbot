from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select, inspect, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Medicine, Time
from api.schemas import Medicine as MedCreate, UserBase
from api.utils import get_current_active_user

app = APIRouter(tags=["medicines"])

@app.get("/medicines/")
async def get_item(medicine_id: int | None = None, session: AsyncSession = Depends(get_async_session), current_user: UserBase = Depends(get_current_active_user)):
    """
    Получение записи по id из бд или всех записей без указания id
    :return:
    """
    if medicine_id is None:
        stmt = select(Medicine.id, Medicine.user_id, Medicine.name, Medicine.number_of_receptions, Time.reception_time,
                      Medicine.notifications).where(Medicine.id == Time.medicine_id)
    else:
        stmt = select(Medicine.id, Medicine.user_id, Medicine.name, Medicine.number_of_receptions, Time.reception_time,
                      Medicine.notifications).where(Medicine.id == Time.medicine_id, Medicine.id == medicine_id)
    result = await session.execute(stmt)
    result.unique()
    dict_result = [row._mapping for row in result.all()]
    return dict_result


@app.delete("/medecines/")
async def del_item(session: Annotated[AsyncSession, Depends(get_async_session)], current_user: Annotated[UserBase, Depends(get_current_active_user)], medicine_id: int | None = None, user_id: int | None = None):
    """
    Удаление записей или записи по id
    :param medicine_id: id лекарства
    :param session: объект сессии
    :return:
    """
    if medicine_id is None and user_id is None:
        stmt = delete(Medicine)
    elif medicine_id is not None:
        stmt = delete(Medicine).where(Medicine.id == medicine_id)
    elif user_id is not None:
        stmt = delete(Medicine).where(Medicine.user_id == user_id)

    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@app.post("/medicines/")
async def add_item(medicine: MedCreate, session: AsyncSession = Depends(get_async_session), current_user: UserBase = Depends(get_current_active_user)):
    if medicine.number_of_receptions != len(medicine.times):
        return {"status": "error", "details": "number of receptions must be equal len of times"}
    new_medicine = Medicine(
        name=medicine.name,
        user_id=medicine.user_id,
        number_of_receptions=medicine.number_of_receptions,
        time_of_reception=medicine.time_of_reception
    )
    session.add(new_medicine)
    await session.flush()
    await session.refresh(new_medicine)
    times = []
    for time in medicine.times:
        new_time = Time(
            reception_time=time,
            medicine_id=new_medicine.id,
            medicine=new_medicine
        )
        times.append(new_time)
    session.add_all(times)
    await session.commit()
    return {"status": "success"}
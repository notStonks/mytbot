from sqlalchemy import select, delete, update, case
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine
from models.models import Medicine, Time
from datetime import time


async def db_read(user_id=None, flag=False):
    async with AsyncSession(bind=engine) as session:
        if user_id is None:
            stmt = select(Medicine.id, Medicine.user_id, Medicine.name, Medicine.time_of_reception,
                          Time.reception_time).where(Time.medicine_id == Medicine.id, Medicine.notifications is True)
        elif flag:
            stmt = select(Medicine.id, Medicine.user_id, Medicine.name, Medicine.time_of_reception,
                          Time.reception_time).where(Medicine.user_id == user_id, Time.medicine_id == Medicine.id)
        else:
            stmt = select(Medicine.id, Medicine.name, Medicine.number_of_receptions).where(Medicine.user_id == user_id)
        return await session.execute(stmt)


async def db_add(state):
    async with AsyncSession(bind=engine) as session:
        async with state.proxy() as data:
            try:
                m = Medicine(
                    name=data["name"],
                    user_id=int(data["user_id"]),
                    number_of_receptions=int(data["number"]),
                    time_of_reception=int(data["time"])
                )

                session.add(m)
                await session.flush()
                await session.refresh(m)
                m_id = m.id
                times = []
                for t in data["times"]:
                    # h, min = t.split(":")
                    tel = Time(
                        # reception_time=datetime.datetime.strptime(t, '%H:%M').time(),
                        # reception_time=time(hour=int(h), minute=int(min)),
                        reception_time=t,
                        medicine_id=m_id
                    )
                    times.append(tel)

                session.add_all(times)
                await session.commit()
                return m_id
            except ValueError as e:
                print(e)


async def db_del(id: int):
    async with AsyncSession(bind=engine) as session:
        await session.execute(delete(Medicine).where(Medicine.id == id))
        await session.commit()


async def deb_del_all(user_id: int):
    async with AsyncSession(bind=engine) as session:
        await session.execute(delete(Medicine).where(Medicine.user_id == user_id))
        await session.commit()


async def db_edit_notify(user_id, flag):
    async with AsyncSession(bind=engine) as session:
        stmt = select(Medicine.notifications).where(Medicine.user_id == user_id).limit(1)
        result = await session.execute(stmt)
        if result.all()[0][0] != flag:
            stmt = update(Medicine).where(Medicine.user_id == user_id).values(notifications=flag)
            await session.execute(stmt)
            await session.commit()
        else:
            return False
        # stmt = update(Medicine).where(
        #     case(
        #         (Medicine.notifications != flag, flag)
        #     ), Medicine.user_id == user_id).values(notifications=flag)
        # res = await session.execute(stmt)


from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import engine
from models.models import Medicine, Time


async def db_read(user_id=None, flag=False):
    async with AsyncSession(bind=engine) as session:
        if user_id is None:
            stmt = select(Medicine.id, Medicine.user_id, Medicine.name, Medicine.time_of_reception,
                          Time.reception_time).where(Time.medicine_id == Medicine.id, Medicine.notifications == True)
        elif flag:
            stmt = select(Medicine.id, Medicine.user_id, Medicine.name, Medicine.time_of_reception,
                          Time.reception_time).where(Medicine.user_id == user_id, Time.medicine_id == Medicine.id)
        else:
            stmt = select(Medicine).where(Medicine.user_id == user_id)
        res = await session.execute(stmt)
        res.unique()
        return res


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
                    tel = Time(
                        reception_time=t,
                        medicine_id=m_id,
                        medicine=m
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
        if result.scalar() != flag:
            stmt = update(Medicine).where(Medicine.user_id == user_id).values(notifications=flag)
            await session.execute(stmt)
            await session.commit()
            return True
        else:
            return False

import datetime
from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from sqlalchemy import Table, Integer, String, Column, ForeignKey, Time, Boolean
from database import Base

import enum


# class time_of_receptionsEnum(enum.Enum):
#     before = 0
#     during_a_meal = 1
#     after = 2
#     regardless = 3


class Medicine(Base):
    __tablename__ = 'medicine'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    number_of_receptions: Mapped[int] = mapped_column(nullable=False)
    time_of_reception: Mapped[int] = mapped_column(nullable=False)  # время приема (в зависимости от пищи, до, во время или после нее) 0-3
    notifications: Mapped[bool] = mapped_column(default=True)
    times: Mapped[List["Time"]] = relationship('Time', backref="medicine", uselist=True, cascade="all, delete", passive_deletes=True, lazy="joined")


class Time(Base):
    __tablename__ = 'time'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reception_time: Mapped[datetime.time] = mapped_column(nullable=False)
    medicine_id: Mapped[int] = mapped_column(ForeignKey('medicine.id', ondelete="CASCADE"))


from sqlalchemy.orm import relationship


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

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    number_of_receptions = Column(Integer, nullable=False)
    time_of_reception = Column(Integer, nullable=False)  # время приема (в зависимости от пищи, до, во время или после нее) 0-3
    notifications = Column(Boolean, default=True)
    times = relationship('Time', cascade="all, delete", passive_deletes=True)


class Time(Base):
    __tablename__ = 'time'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reception_time = Column(Time, nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicine.id', ondelete="CASCADE"))


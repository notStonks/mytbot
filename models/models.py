from database import metadata

from sqlalchemy import Table, Integer, String, Column, ForeignKey, TIMESTAMP

medicine = Table(
    'medicine',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id', Integer(), nullable=False),
    Column('name', String(), nullable=False)
)

receive = Table(
    'receive',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('medicine_id', Integer(), ForeignKey('medicine.id')),
    Column('number_of_receptions', Integer()),
    Column("number_of_reception", Integer())  #  время приема (в зависимости от пищи, до, во время или после нее) 0-3
)

time = Table(
    'time',
    metadata,
    Column('id', Integer(), ForeignKey('receive.id')),
    Column('reception_time', TIMESTAMP)
)
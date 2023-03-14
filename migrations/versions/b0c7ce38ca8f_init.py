"""init

Revision ID: b0c7ce38ca8f
Revises: 
Create Date: 2023-03-10 20:46:46.296453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0c7ce38ca8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medicine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('number_of_receptions', sa.Integer(), nullable=False),
    sa.Column('time_of_reception', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('time',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reception_time', sa.Time(), nullable=False),
    sa.Column('medicine_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicine.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time')
    op.drop_table('medicine')
    # ### end Alembic commands ###
"""add partners table

Revision ID: 2f2c4f135723
Revises: 8c4e270b5bc0
Create Date: 2022-09-28 19:24:30.477174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f2c4f135723'
down_revision = '8c4e270b5bc0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('partners',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=400), nullable=False),
    sa.Column('address', sa.String(length=400), nullable=True),
    sa.Column('dni', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=8), nullable=True),
    sa.Column('mobile', sa.String(length=8), nullable=True),
    sa.Column('nit', sa.String(length=11), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_provider', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(length=50), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='partner'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('partners', schema='partner')
    # ### end Alembic commands ###

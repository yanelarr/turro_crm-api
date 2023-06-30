"""modificaciones en atributo measure de las entidades

Revision ID: dfd26e8b86c4
Revises: aef0ac579a04
Create Date: 2022-11-30 16:34:20.525432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfd26e8b86c4'
down_revision = 'aef0ac579a04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movements', sa.Column('measure_id', sa.Integer(), nullable=False), schema='stock')
    op.create_foreign_key(None, 'movements', 'measure', ['measure_id'], ['id'], source_schema='stock', referent_schema='stock')
    op.drop_column('movements', 'measurement', schema='stock')
    op.add_column('products', sa.Column('measure_id', sa.Integer(), nullable=False), schema='stock')
    op.create_foreign_key(None, 'products', 'measure', ['measure_id'], ['id'], source_schema='stock', referent_schema='stock')
    op.drop_column('products', 'measurement', schema='stock')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('measurement', sa.VARCHAR(), autoincrement=False, nullable=False), schema='stock')
    op.drop_constraint(None, 'products', schema='stock', type_='foreignkey')
    op.drop_column('products', 'measure_id', schema='stock')
    op.add_column('movements', sa.Column('measurement', sa.VARCHAR(), autoincrement=False, nullable=True), schema='stock')
    op.drop_constraint(None, 'movements', schema='stock', type_='foreignkey')
    op.drop_column('movements', 'measure_id', schema='stock')
    # ### end Alembic commands ###

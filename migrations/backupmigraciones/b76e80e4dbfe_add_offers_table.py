"""add offers table

Revision ID: b76e80e4dbfe
Revises: c70b7ace77a0
Create Date: 2023-06-04 23:05:00.949598

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b76e80e4dbfe'
down_revision = 'c70b7ace77a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('code', sa.String(length=24), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('cost_price', sa.Float(), nullable=True),
    sa.Column('sale_price', sa.Float(), nullable=True),
    sa.Column('ledger_account', sa.String(length=250), nullable=True),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(length=50), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='offer'
    )
    op.create_table('offer_products',
    sa.Column('offer_id', sa.String(), nullable=False),
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(length=50), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.offers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['stock.products.id'], ),
    sa.PrimaryKeyConstraint('offer_id', 'product_id'),
    schema='offer'
    )
    op.drop_table('partners_versat', schema='partner')
    op.drop_table('partner_v', schema='partner')
    op.drop_table('torneos', schema='enterprise')
    op.drop_table('invoice_f', schema='invoice')
    op.drop_constraint('users_dni_key', 'users', schema='enterprise', type_='unique')
    op.drop_constraint('users_email_key', 'users', schema='enterprise', type_='unique')
    op.drop_constraint('users_phone_key', 'users', schema='enterprise', type_='unique')
    op.create_foreign_key(None, 'movements', 'status_element', ['status_id'], ['id'], source_schema='stock', referent_schema='resources')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movements', schema='stock', type_='foreignkey')
    op.create_unique_constraint('users_phone_key', 'users', ['phone'], schema='enterprise')
    op.create_unique_constraint('users_email_key', 'users', ['email'], schema='enterprise')
    op.create_unique_constraint('users_dni_key', 'users', ['dni'], schema='enterprise')
    op.create_table('invoice_f',
    sa.Column('idfactura', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('numero', sa.VARCHAR(length=65), autoincrement=False, nullable=True),
    sa.Column('fecha', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('idestado', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idtipo', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('identidad', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idunidad', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idusuario', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('porcarancel', sa.NUMERIC(precision=18, scale=2), autoincrement=False, nullable=True),
    sa.Column('imparancelmn', sa.NUMERIC(precision=18, scale=2), autoincrement=False, nullable=True),
    sa.Column('imparancelmlc', sa.NUMERIC(precision=18, scale=2), autoincrement=False, nullable=True),
    sa.Column('observacion', sa.VARCHAR(length=2005), autoincrement=False, nullable=True),
    sa.Column('idcontratovta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('importemn', sa.NUMERIC(precision=18, scale=2), autoincrement=False, nullable=True),
    sa.Column('importemlc', sa.NUMERIC(precision=18, scale=2), autoincrement=False, nullable=True),
    sa.Column('idconceptooblig', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('idperiodo', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ctabcomn', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ctabcomlc', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idempresa', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('precioest', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('idforma', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('idunidademitida', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('numcons', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('resumen', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('confirmo', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('termino', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('creaoblig', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('idoperacion', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('idregistrotalon', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('vtacadena', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('creadescuento', postgresql.BIT(length=1), autoincrement=False, nullable=True),
    sa.Column('crearetencion', postgresql.BIT(length=1), autoincrement=False, nullable=True),
    sa.Column('crc', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('chkcontrol', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('chkdate', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('factelect', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    schema='invoice'
    )
    op.create_table('torneos',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('nombre', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('estado', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), autoincrement=False, nullable=True),
    schema='enterprise'
    )
    op.create_table('partner_v',
    sa.Column('identidad', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('codigo', sa.VARCHAR(length=11), autoincrement=False, nullable=True),
    sa.Column('codigoreu', sa.VARCHAR(length=19), autoincrement=False, nullable=True),
    sa.Column('nombre', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('abreviatura', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('direccion', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('activo', postgresql.BIT(length=1), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('telefono', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('nit', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('ircc', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('provincia', sa.VARCHAR(length=150), autoincrement=False, nullable=True),
    sa.Column('pais', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    schema='partner'
    )
    op.create_table('partners_versat',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=400), autoincrement=False, nullable=False),
    sa.Column('id_versat', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('cod_reup', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='partners_review_pkey1'),
    schema='partner'
    )
    op.drop_table('offer_products', schema='offer')
    op.drop_table('offers', schema='offer')
    # ### end Alembic commands ###

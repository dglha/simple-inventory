"""Add transfer money (digicoin) table

Revision ID: a9e3b93b14d6
Revises: 39dbce1c181c
Create Date: 2021-08-24 16:28:07.697665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e3b93b14d6'
down_revision = '39dbce1c181c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfer',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('sender', sa.String(length=64), nullable=False),
    sa.Column('receiver', sa.String(length=64), nullable=False),
    sa.Column('currency', sa.String(length=64), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('method', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('order_detail', 'price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=15),
               existing_nullable=False)
    op.alter_column('product', 'unit_quoted_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=15),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'unit_quoted_price',
               existing_type=sa.Float(precision=15),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('order_detail', 'price',
               existing_type=sa.Float(precision=15),
               type_=sa.REAL(),
               existing_nullable=False)
    op.drop_table('transfer')
    # ### end Alembic commands ###

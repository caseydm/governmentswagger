"""empty message

Revision ID: 6914f620c8d1
Revises: 04e0bd0e09c7
Create Date: 2016-05-10 21:25:14.233765

"""

# revision identifiers, used by Alembic.
revision = '6914f620c8d1'
down_revision = '04e0bd0e09c7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('self_parking_cost', sa.Numeric(precision=10, scale=2), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hotels', 'self_parking_cost')
    ### end Alembic commands ###

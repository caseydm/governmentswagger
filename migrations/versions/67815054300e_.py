"""empty message

Revision ID: 67815054300e
Revises: 2492e8cc8190
Create Date: 2016-05-10 21:21:16.954115

"""

# revision identifiers, used by Alembic.
revision = '67815054300e'
down_revision = '2492e8cc8190'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hotels', 'self_parking_cost')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('self_parking_cost', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    ### end Alembic commands ###

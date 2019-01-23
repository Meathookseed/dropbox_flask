"""empty message

Revision ID: 33fec3cea088
Revises: ee6c0bf3750c
Create Date: 2019-01-04 02:39:48.064551

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '33fec3cea088'
down_revision = 'ee6c0bf3750c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('vault_title_key', 'vault', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('vault_title_key', 'vault', ['title'])
    # ### end Alembic commands ###

"""empty message

Revision ID: ac89a0774aa9
Revises: e26eee94f8df
Create Date: 2018-12-10 09:18:53.714728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac89a0774aa9'
down_revision = 'e26eee94f8df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vault', type_='foreignkey')
    op.create_foreign_key(None, 'vault', 'user', ['owner_id'], ['public_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vault', type_='foreignkey')
    op.create_foreign_key(None, 'vault', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###
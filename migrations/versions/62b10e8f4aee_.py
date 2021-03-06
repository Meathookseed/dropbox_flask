"""empty message

Revision ID: 62b10e8f4aee
Revises: 
Create Date: 2019-01-31 10:07:08.479193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b10e8f4aee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stripe',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stripe_id', sa.String(length=150), autoincrement=False, nullable=False),
    sa.Column('token', sa.String(length=150), nullable=False),
    sa.Column('user_id', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('stripe_id'),
    sa.UniqueConstraint('token')
    )
    op.drop_table('stripe_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stripe_data',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('stripe_id', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('token', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='stripe_data_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='stripe_data_pkey'),
    sa.UniqueConstraint('stripe_id', name='stripe_data_stripe_id_key'),
    sa.UniqueConstraint('token', name='stripe_data_token_key')
    )
    op.drop_table('stripe')
    # ### end Alembic commands ###

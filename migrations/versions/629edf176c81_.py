"""empty message

Revision ID: 629edf176c81
Revises: 20469cbb9d87
Create Date: 2020-07-21 09:26:36.507938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '629edf176c81'
down_revision = '20469cbb9d87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('total', sa.Integer(), nullable=True))
    op.drop_column('data', 'completed')
    op.drop_column('data', 'carb_content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('carb_content', sa.INTEGER(), nullable=True))
    op.add_column('data', sa.Column('completed', sa.INTEGER(), nullable=True))
    op.drop_column('data', 'total')
    # ### end Alembic commands ###

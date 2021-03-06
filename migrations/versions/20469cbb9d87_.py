"""empty message

Revision ID: 20469cbb9d87
Revises: 4ae2b14cd321
Create Date: 2020-07-20 23:34:43.203272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20469cbb9d87'
down_revision = '4ae2b14cd321'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('carbs', sa.Integer(), default = 0))
    op.add_column('data', sa.Column('fats', sa.Integer(), default = 0))
    op.add_column('data', sa.Column('proteins', sa.Integer(), default = 0))
    op.drop_column('data', 'completed')
    op.drop_column('data', 'carb_content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('carb_content', sa.INTEGER(), nullable=True))
    op.add_column('data', sa.Column('completed', sa.INTEGER(), nullable=True))
    op.drop_column('data', 'proteins')
    op.drop_column('data', 'fats')
    op.drop_column('data', 'carbs')
    # ### end Alembic commands ###

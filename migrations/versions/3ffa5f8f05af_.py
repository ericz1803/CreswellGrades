"""empty message

Revision ID: 3ffa5f8f05af
Revises: 2a9d46e6a8d2
Create Date: 2019-08-18 14:31:52.705530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ffa5f8f05af'
down_revision = '2a9d46e6a8d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gradefactor', sa.Column('category1_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category2_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category3_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category4_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category5_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category6_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category7_drop', sa.Integer(), nullable=True))
    op.add_column('gradefactor', sa.Column('category8_drop', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gradefactor', 'category8_drop')
    op.drop_column('gradefactor', 'category7_drop')
    op.drop_column('gradefactor', 'category6_drop')
    op.drop_column('gradefactor', 'category5_drop')
    op.drop_column('gradefactor', 'category4_drop')
    op.drop_column('gradefactor', 'category3_drop')
    op.drop_column('gradefactor', 'category2_drop')
    op.drop_column('gradefactor', 'category1_drop')
    # ### end Alembic commands ###

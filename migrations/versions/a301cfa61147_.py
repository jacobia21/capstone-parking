"""empty message

Revision ID: a301cfa61147
Revises: 1f79765c8269
Create Date: 2020-10-24 02:30:20.698366

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a301cfa61147'
down_revision = '1f79765c8269'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('control_points', 'height',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('control_points', 'start_x',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('control_points', 'start_y',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('control_points', 'width',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'height',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'start_x',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'start_y',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'width',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('space_dimensions', 'width',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'start_y',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'start_x',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('space_dimensions', 'height',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('control_points', 'width',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('control_points', 'start_y',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('control_points', 'start_x',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('control_points', 'height',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###

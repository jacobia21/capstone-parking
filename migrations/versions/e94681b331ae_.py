"""empty message

Revision ID: e94681b331ae
Revises: ba46f4c910e3
Create Date: 2020-10-15 20:01:32.011060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e94681b331ae'
down_revision = 'ba46f4c910e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('logs', 'type',
               existing_type=mysql.ENUM('WEBSITE', 'DATBASE', 'HARDWARE'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('logs', 'type',
               existing_type=mysql.ENUM('WEBSITE', 'DATBASE', 'HARDWARE'),
               nullable=True)
    # ### end Alembic commands ###

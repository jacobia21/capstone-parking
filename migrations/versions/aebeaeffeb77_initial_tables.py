"""removing username from users table

Revision ID: aebeaeffeb77
Revises: 
Create Date: 2020-09-07 21:55:27.987537

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aebeaeffeb77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_username', table_name='user')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', mysql.VARCHAR(length=64), nullable=True))
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    # ### end Alembic commands ###
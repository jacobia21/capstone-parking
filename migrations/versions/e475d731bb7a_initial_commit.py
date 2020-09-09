"""initial commit

Revision ID: e475d731bb7a
Revises: 
Create Date: 2020-09-08 21:20:42.770684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e475d731bb7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lot_name'), 'lot', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('middle_initial', sa.String(length=1), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('first_name', 'last_name', 'middle_initial')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_middle_initial'), 'user', ['middle_initial'], unique=False)
    op.create_table('zone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('color', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_zone_color'), 'zone', ['color'], unique=True)
    op.create_index(op.f('ix_zone_name'), 'zone', ['name'], unique=True)
    op.create_table('camera',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('ON', 'OFF', name='camerastatus'), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lotzone',
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.Column('zone_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.ForeignKeyConstraint(['zone_id'], ['zone.id'], ),
    sa.PrimaryKeyConstraint('lot_id', 'zone_id')
    )
    op.create_table('space',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('availability', sa.String(length=100), nullable=True),
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.Column('zone_id', sa.Integer(), nullable=False),
    sa.Column('camera_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['camera_id'], ['camera.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lotzone.lot_id'], ),
    sa.ForeignKeyConstraint(['zone_id'], ['lotzone.zone_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('space')
    op.drop_table('lotzone')
    op.drop_table('camera')
    op.drop_index(op.f('ix_zone_name'), table_name='zone')
    op.drop_index(op.f('ix_zone_color'), table_name='zone')
    op.drop_table('zone')
    op.drop_index(op.f('ix_user_middle_initial'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_lot_name'), table_name='lot')
    op.drop_table('lot')
    # ### end Alembic commands ###

"""empty message

Revision ID: b3f87384998e
Revises: 30aff9aae825
Create Date: 2020-10-15 21:19:36.572770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3f87384998e'
down_revision = '30aff9aae825'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('lotzone_ibfk_1', 'lotzone', type_='foreignkey')
    op.drop_constraint('lotzone_ibfk_2', 'lotzone', type_='foreignkey')
    op.create_foreign_key(None, 'lotzone', 'lot', ['lot_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'lotzone', 'zone', ['zone_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'lotzone', type_='foreignkey')
    op.drop_constraint(None, 'lotzone', type_='foreignkey')
    op.create_foreign_key('lotzone_ibfk_2', 'lotzone', 'zone', ['zone_id'], ['id'])
    op.create_foreign_key('lotzone_ibfk_1', 'lotzone', 'lot', ['lot_id'], ['id'])
    # ### end Alembic commands ###
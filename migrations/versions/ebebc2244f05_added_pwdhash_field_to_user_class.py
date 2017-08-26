"""Added pwdhash field to user class

Revision ID: ebebc2244f05
Revises: 87f8840137a3
Create Date: 2017-08-03 23:11:52.272561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebebc2244f05'
down_revision = '87f8840137a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pwdhash', sa.String(length=54), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pwdhash')
    # ### end Alembic commands ###

"""模型更新

Revision ID: 3e99d77c88d8
Revises: 
Create Date: 2023-09-21 15:01:38.364812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e99d77c88d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.String(length=200), nullable=False))
        batch_op.add_column(sa.Column('completed', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('pub_date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('pub_date')
        batch_op.drop_column('completed')
        batch_op.drop_column('content')

    # ### end Alembic commands ###

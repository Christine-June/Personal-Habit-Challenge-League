"""Fix message model: sender/receiver

Revision ID: bc1f27046b73
Revises: 44f52ca06683
Create Date: 2025-06-25 21:53:38.329106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1f27046b73'
down_revision = '44f52ca06683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sender_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('receiver_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('fk_messages_user_id_users', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_messages_receiver_id_users'), 'users', ['receiver_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_messages_sender_id_users'), 'users', ['sender_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(batch_op.f('fk_messages_sender_id_users'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_messages_receiver_id_users'), type_='foreignkey')
        batch_op.create_foreign_key('fk_messages_user_id_users', 'users', ['user_id'], ['id'])
        batch_op.drop_column('receiver_id')
        batch_op.drop_column('sender_id')

    # ### end Alembic commands ###

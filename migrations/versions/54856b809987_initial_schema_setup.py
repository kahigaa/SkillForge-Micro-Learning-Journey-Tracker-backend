"""Initial schema setup

Revision ID: 54856b809987
Revises: 
Create Date: 2025-07-01 14:46:31.560715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54856b809987'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_blocklist_jti'), ['jti'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('journeys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('steps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_complete', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('journey_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['journey_id'], ['journeys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('steps')
    op.drop_table('journeys')
    op.drop_table('users')
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blocklist_jti'))

    op.drop_table('token_blocklist')
    # ### end Alembic commands ###

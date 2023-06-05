"""elimino relaciones

Revision ID: 0ff5fa42eeb9
Revises: cb220de6c984
Create Date: 2023-06-05 16:34:27.427960

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '0ff5fa42eeb9'
down_revision = 'cb220de6c984'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasksowners')
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_column('notes', 'task_id')
    op.drop_column('notes', 'user_id')
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'started_by_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('started_by_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'users', ['started_by_id'], ['id'])
    op.add_column('notes', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.add_column('notes', sa.Column('task_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'notes', 'tasks', ['task_id'], ['id'])
    op.create_foreign_key(None, 'notes', 'users', ['user_id'], ['id'])
    op.create_table('tasksowners',
    sa.Column('task_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('task_id', 'user_id')
    )
    # ### end Alembic commands ###
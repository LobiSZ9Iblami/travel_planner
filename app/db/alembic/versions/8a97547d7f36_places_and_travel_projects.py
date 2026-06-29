"""places and travel projects

Revision ID: 8a97547d7f36
Revises: 
Create Date: 2026-06-29 21:59:06.840880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a97547d7f36'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('travel_projects',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('create_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('update_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_travel_projects_id'), 'travel_projects', ['id'], unique=False)

    op.create_table('travel_places',
        sa.Column('travel_project_id', sa.Integer(), nullable=False),
        sa.Column('external_place_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('visited', sa.Boolean(), nullable=False),
        sa.Column('visited_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('create_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('update_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['travel_project_id'], ['travel_projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_travel_places_id'), 'travel_places', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_travel_places_id'), table_name='travel_places')
    op.drop_table('travel_places')
    op.drop_index(op.f('ix_travel_projects_id'), table_name='travel_projects')
    op.drop_table('travel_projects')

"""add content column to posts table

Revision ID: 8560c6245b7c
Revises: da205554e7dd
Create Date: 2022-06-28 17:45:38.546088

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8560c6245b7c'
down_revision = 'da205554e7dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String(20), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass

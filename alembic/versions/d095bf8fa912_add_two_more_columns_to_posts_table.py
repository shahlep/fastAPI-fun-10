"""add two more columns to posts table

Revision ID: d095bf8fa912
Revises: 134b81651e7d
Create Date: 2022-06-28 18:47:23.085904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd095bf8fa912'
down_revision = '134b81651e7d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column(
                      "created_at",
                      sa.TIMESTAMP(timezone=True),
                      server_default=sa.text("now()"),
                      nullable=False,
                  ),)
    op.add_column("posts",
                  sa.Column(
                      "published",
                      sa.Boolean,
                      server_default='True',
                      nullable=False,
                  ), )
    pass


def downgrade() -> None:

    pass

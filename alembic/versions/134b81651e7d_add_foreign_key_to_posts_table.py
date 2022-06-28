"""add foreign key to posts table

Revision ID: 134b81651e7d
Revises: f8274cad2e1c
Create Date: 2022-06-28 18:32:21.957255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '134b81651e7d'
down_revision = 'f8274cad2e1c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("owner_id",sa.Integer,nullable=False))
    op.create_foreign_key("posts_users_fk",
                          source_table="posts",referent_table="users",
                          local_cols="owner_id",remote_cols="id",
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_column("posts","owner_id")
    pass

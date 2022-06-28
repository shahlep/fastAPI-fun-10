"""create users table

Revision ID: f8274cad2e1c
Revises: 8560c6245b7c
Create Date: 2022-06-28 18:16:50.046357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8274cad2e1c'
down_revision = '8560c6245b7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer,nullable=False),
                    sa.Column("email",sa.String,nullable=False),
                    sa.Column("password",sa.String,nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

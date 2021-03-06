"""adding votes table

Revision ID: 52929d64f58e
Revises: d095bf8fa912
Create Date: 2022-06-28 19:01:11.286614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52929d64f58e"
down_revision = "d095bf8fa912"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("votes")
    # ### end Alembic commands ###

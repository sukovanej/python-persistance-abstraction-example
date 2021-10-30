"""initial revision

Revision ID: 5aadb6e74421
Revises: 
Create Date: 2021-10-29 23:23:36.435039

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "5aadb6e74421"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")

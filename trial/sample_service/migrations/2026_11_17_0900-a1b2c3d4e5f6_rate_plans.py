"""create rate_plans

Revision ID: a1b2c3d4e5f6
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = None


def upgrade() -> None:
    conn = op.get_bind()
    if "rate_plans" in sa.inspect(conn).get_table_names():
        return
    op.create_table(
        "rate_plans",
        sa.Column("id", sa.BigInteger, sa.Identity(), primary_key=True),
        sa.Column("property_id", sa.BigInteger, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("currency", sa.String(255), nullable=False),
        sa.Column("contact", sa.String(100), nullable=False),
        sa.Column("contact_2", sa.String(100), nullable=True),
        sa.Column("created", sa.TIMESTAMP(timezone=False), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("rate_plans")

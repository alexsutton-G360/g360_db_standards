"""add details to rate_plans

Revision ID: b2c3d4e5f6a1
Revises: a1b2c3d4e5f6
"""
import sqlalchemy as sa
from alembic import op

revision = "b2c3d4e5f6a1"
down_revision = "a1b2c3d4e5f6"


def upgrade() -> None:
    op.add_column("rate_plans", sa.Column("website", sa.Text, nullable=True))
    op.add_column("rate_plans", sa.Column("notify_emails", sa.String(500), nullable=True))
    op.add_column("rate_plans", sa.Column("approved_on", sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column("rate_plans", sa.Column("room_count", sa.Integer, nullable=True))
    op.add_column("rate_plans", sa.Column("status", sa.Text, nullable=True))


def downgrade() -> None:
    for name in ("status", "room_count", "approved_on", "notify_emails", "website"):
        op.drop_column("rate_plans", name)

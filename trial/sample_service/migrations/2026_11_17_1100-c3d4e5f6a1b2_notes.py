"""create notes (control: written to follow the standards)

Revision ID: c3d4e5f6a1b2
Revises: b2c3d4e5f6a1
"""
import sqlalchemy as sa
from alembic import op

revision = "c3d4e5f6a1b2"
down_revision = "b2c3d4e5f6a1"


def upgrade() -> None:
    conn = op.get_bind()
    if "notes" in sa.inspect(conn).get_table_names():
        return
    op.create_table(
        "notes",
        sa.Column("id", sa.BigInteger, sa.Identity(), nullable=False),
        sa.Column("guid", sa.UUID, nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("property_id", sa.BigInteger, sa.ForeignKey("properties.id", name="fk_notes_property_id"), nullable=False),
        sa.Column("body", sa.String(2000), nullable=False),
        sa.Column("currency_code", sa.String(3), nullable=False),
        sa.Column("quoted_amount_minor_units", sa.BigInteger, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_notes"),
        sa.UniqueConstraint("guid", name="ctx_notes_guid_unique"),
    )
    op.create_index("idx_notes_property_id", "notes", ["property_id"])


def downgrade() -> None:
    op.drop_index("idx_notes_property_id", table_name="notes")
    op.drop_table("notes")

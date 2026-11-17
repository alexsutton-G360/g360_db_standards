"""Data model for rate_plans (mirrors the two rate_plans migrations)."""
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RatePlan(Base):
    __tablename__ = "rate_plans"

    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    property_id: Mapped[int] = mapped_column(sa.BigInteger)
    price: Mapped[float] = mapped_column(sa.Float)
    currency: Mapped[str] = mapped_column(sa.String(255))
    contact: Mapped[str] = mapped_column(sa.String(100))
    contact_2: Mapped[str | None] = mapped_column(sa.String(100))
    created: Mapped[str] = mapped_column(sa.TIMESTAMP(timezone=False))
    website: Mapped[str | None] = mapped_column(sa.Text)
    notify_emails: Mapped[str | None] = mapped_column(sa.String(500))
    approved_on: Mapped[str | None] = mapped_column(sa.TIMESTAMP(timezone=True))
    room_count: Mapped[int | None] = mapped_column(sa.Integer)
    status: Mapped[str | None] = mapped_column(sa.Text)

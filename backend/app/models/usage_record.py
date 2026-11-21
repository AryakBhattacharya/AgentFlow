import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class UsageRecord(BaseModel):
    """Tracks AI model usage and estimated costs."""

    __tablename__ = "usage_records"

    __table_args__ = (
        CheckConstraint(
            "input_tokens >= 0 AND output_tokens >= 0",
            name="valid_token_counts",
        ),
        CheckConstraint(
            "estimated_cost >= 0",
            name="valid_estimated_cost",
        ),
    )

    execution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("executions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    node_execution_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("node_executions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    estimated_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )
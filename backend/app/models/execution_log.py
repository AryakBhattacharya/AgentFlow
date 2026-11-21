import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class ExecutionLog(BaseModel):
    """Stores chronological events generated during workflow execution."""

    __tablename__ = "execution_logs"

    __table_args__ = (
        CheckConstraint(
            "level IN ('debug', 'info', 'warning', 'error')",
            name="valid_execution_log_level",
        ),
        # Optimizes retrieving an execution's logs chronologically.
        Index(
            "ix_execution_logs_execution_created",
            "execution_id",
            "created_at",
        ),
    )

    execution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("executions.id", ondelete="CASCADE"),
        nullable=False,
    )

    node_execution_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("node_executions.id", ondelete="SET NULL"),
        nullable=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="info",
        server_default="info",
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    details: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
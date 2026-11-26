
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class NodeExecution(BaseModel):
    """Tracks an individual node execution within a workflow execution."""

    __tablename__ = "node_executions"

    __table_args__ = (
        UniqueConstraint(
            "execution_id",
            "workflow_node_id",
            "attempt_number",
            name="uq_node_executions_attempt",
        ),
        ForeignKeyConstraint(
            ["execution_id", "workflow_version_id"],
            ["executions.id", "executions.workflow_version_id"],
            ondelete="CASCADE",
            name="fk_node_executions_execution_version",
        ),
        ForeignKeyConstraint(
            ["workflow_node_id", "workflow_version_id"],
            ["workflow_nodes.id", "workflow_nodes.workflow_version_id"],
            ondelete="RESTRICT",
            name="fk_node_executions_node_version",
        ),
        CheckConstraint(
            "status IN ('pending', 'running', 'paused', "
            "'completed', 'failed', 'skipped', 'cancelled')",
            name="valid_node_execution_status",
        ),
        CheckConstraint(
            "attempt_number >= 1",
            name="valid_attempt_number",
        ),
        CheckConstraint(
            "completed_at IS NULL OR started_at IS NULL "
            "OR completed_at >= started_at",
            name="valid_node_execution_timestamps",
        ),
        Index(
            "ix_node_executions_execution_version",
            "execution_id",
            "workflow_version_id",
        ),
        Index(
            "ix_node_executions_node_version",
            "workflow_node_id",
            "workflow_version_id",
        ),
    )

    execution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    workflow_node_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    workflow_version_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )

    input_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    output_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

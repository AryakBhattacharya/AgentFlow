import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class WorkflowNode(BaseModel):
    """Represents an individual node in a workflow version."""

    __tablename__ = "workflow_nodes"

    __table_args__ = (
        UniqueConstraint(
            "workflow_version_id",
            "node_key",
            name="uq_workflow_nodes_version_node_key",
        ),
        CheckConstraint(
            "node_type IN ('start', 'agent', 'llm', 'tool', "
            "'condition', 'human_approval', 'delay', 'output')",
            name="valid_workflow_node_type",
        ),
    )

    workflow_version_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("workflow_versions.id", ondelete="CASCADE"),
        nullable=False,
    )

    node_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    node_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    position_x: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    position_y: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    configuration: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
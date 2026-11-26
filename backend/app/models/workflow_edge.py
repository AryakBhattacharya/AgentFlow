import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class WorkflowEdge(BaseModel):
    """Represents a connection between two nodes in a workflow version."""

    __tablename__ = "workflow_edges"

    __table_args__ = (
        CheckConstraint(
            "source_node_key <> target_node_key",
            name="ck_workflow_edges_no_self_loop",
        ),
        UniqueConstraint(
            "workflow_version_id",
            "source_node_key",
            "target_node_key",
            name="uq_workflow_edges_version_connection",
        ),
        ForeignKeyConstraint(
            ["workflow_version_id", "source_node_key"],
            [
                "workflow_nodes.workflow_version_id",
                "workflow_nodes.node_key",
            ],
            ondelete="CASCADE",
            name="fk_workflow_edges_source_node",
        ),
        ForeignKeyConstraint(
            ["workflow_version_id", "target_node_key"],
            [
                "workflow_nodes.workflow_version_id",
                "workflow_nodes.node_key",
            ],
            ondelete="CASCADE",
            name="fk_workflow_edges_target_node",
        ),
        Index(
            "ix_workflow_edges_target_node",
            "workflow_version_id",
            "target_node_key",
        ),
    )

    workflow_version_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    source_node_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_node_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    edge_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="default",
        server_default="default",
    )

    configuration: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class WorkflowVersion(BaseModel):
    """Stores a versioned snapshot of a workflow definition."""

    __tablename__ = "workflow_versions"

    __table_args__ = (
        UniqueConstraint(
            "workflow_id",
            "version_number",
            name="uq_workflow_versions_workflow_version",
        ),
        UniqueConstraint(
            "id",
            "workspace_id",
            name="uq_workflow_versions_id_workspace",
        ),
        ForeignKeyConstraint(
            ["workflow_id", "workspace_id"],
            ["workflows.id", "workflows.workspace_id"],
            ondelete="CASCADE",
            name="fk_workflow_versions_workflow_workspace",
        ),
        CheckConstraint(
            "status IN ('draft', 'published', 'archived')",
            name="valid_workflow_version_status",
        ),
    )

    workflow_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Immutable snapshot of the workflow graph.
    graph_definition: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # Optional description of this version.
    change_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
        server_default="draft",
    )

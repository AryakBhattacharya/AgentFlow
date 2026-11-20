import uuid
from sqlalchemy import Uuid

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class Agent(BaseModel):
    """Stores reusable AI agent configurations within a workspace."""

    __tablename__ = "agents"

    # Every agent belongs to a workspace.
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Defines the agent's instructions and behavior.
    system_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Stores provider-specific model configuration.
    model_settings: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )
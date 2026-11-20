from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class Workspace(BaseModel):
    """Represents an organization or team within AgentFlow."""

    __tablename__ = "workspaces"

    # Workspace display name.
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # URL-friendly identifier, unique across workspaces.
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    # Optional workspace description.
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Allows administrators to deactivate a workspace.
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )
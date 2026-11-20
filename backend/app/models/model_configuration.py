import uuid

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class ModelConfiguration(BaseModel):
    """Stores workspace-specific AI model provider configurations."""

    __tablename__ = "model_configurations"

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

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # Reference to the encrypted API credential.
    secret_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Stores non-secret provider-specific parameters.
    settings: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
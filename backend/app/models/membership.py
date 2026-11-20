import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseModel


class Membership(BaseModel):
    """Associates users with workspaces and defines their roles."""

    __tablename__ = "memberships"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "workspace_id",
            name="uq_memberships_user_workspace",
        ),
        CheckConstraint(
            "role IN ('owner', 'admin', 'member', 'viewer')",
            name="valid_membership_role",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="member",
        server_default="member",
    )
"""add workflow version status constraint

Revision ID: 966f25b8c54f
Revises: bdd8191471b8
Create Date: 2026-11-26 20:16:25.327533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '966f25b8c54f'
down_revision: Union[str, Sequence[str], None] = 'bdd8191471b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_workflow_versions_valid_workflow_version_status",
        "workflow_versions",
        "status IN ('draft', 'published', 'archived')",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_workflow_versions_valid_workflow_version_status",
        "workflow_versions",
        type_="check",
    )

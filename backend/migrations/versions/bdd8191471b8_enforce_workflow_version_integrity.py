"""enforce workflow version integrity

Revision ID: bdd8191471b8
Revises: 272dd12684be
Create Date: 2026-11-21 15:20:59.648713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdd8191471b8'
down_revision: Union[str, Sequence[str], None] = '272dd12684be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema with safe data backfills."""

    # 1. Add new columns as nullable.
    op.add_column(
        "workflow_versions",
        sa.Column("workspace_id", sa.Uuid(), nullable=True),
    )

    op.add_column(
        "node_executions",
        sa.Column("workflow_version_id", sa.Uuid(), nullable=True),
    )

    # 2. Backfill workflow_versions.workspace_id.
    op.execute(
        sa.text("""
            UPDATE workflow_versions AS wv
            SET workspace_id = w.workspace_id
            FROM workflows AS w
            WHERE wv.workflow_id = w.id
        """)
    )

    # 3. Backfill node_executions.workflow_version_id.
    op.execute(
        sa.text("""
            UPDATE node_executions AS ne
            SET workflow_version_id = e.workflow_version_id
            FROM executions AS e
            WHERE ne.execution_id = e.id
        """)
    )

    # 4. Enforce NOT NULL after backfilling.
    op.alter_column(
        "workflow_versions",
        "workspace_id",
        existing_type=sa.Uuid(),
        nullable=False,
    )

    op.alter_column(
        "node_executions",
        "workflow_version_id",
        existing_type=sa.Uuid(),
        nullable=False,
    )

    # 5. Create referenced unique constraints first.
    op.create_unique_constraint(
        "uq_workflows_id_workspace",
        "workflows",
        ["id", "workspace_id"],
    )

    op.create_unique_constraint(
        "uq_workflow_versions_id_workspace",
        "workflow_versions",
        ["id", "workspace_id"],
    )

    op.create_unique_constraint(
        "uq_executions_id_version",
        "executions",
        ["id", "workflow_version_id"],
    )

    op.create_unique_constraint(
        "uq_workflow_nodes_id_version",
        "workflow_nodes",
        ["id", "workflow_version_id"],
    )

    # 6. Replace workflow_versions foreign key.
    op.drop_constraint(
        op.f("fk_workflow_versions_workflow_id_workflows"),
        "workflow_versions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_workflow_versions_workflow_workspace",
        "workflow_versions",
        "workflows",
        ["workflow_id", "workspace_id"],
        ["id", "workspace_id"],
        ondelete="CASCADE",
    )

    # 7. Remove redundant workflow_id index.
    op.drop_index(
        op.f("ix_workflow_versions_workflow_id"),
        table_name="workflow_versions",
    )

    # 8. Replace executions foreign key.
    op.drop_constraint(
        op.f("fk_executions_workflow_version_id_workflow_versions"),
        "executions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_executions_workflow_version_workspace",
        "executions",
        "workflow_versions",
        ["workflow_version_id", "workspace_id"],
        ["id", "workspace_id"],
        ondelete="RESTRICT",
    )

    # 9. Replace node_executions foreign keys.
    op.drop_constraint(
        op.f("fk_node_executions_execution_id_executions"),
        "node_executions",
        type_="foreignkey",
    )

    op.drop_constraint(
        op.f("fk_node_executions_workflow_node_id_workflow_nodes"),
        "node_executions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_node_executions_execution_version",
        "node_executions",
        "executions",
        ["execution_id", "workflow_version_id"],
        ["id", "workflow_version_id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "fk_node_executions_node_version",
        "node_executions",
        "workflow_nodes",
        ["workflow_node_id", "workflow_version_id"],
        ["id", "workflow_version_id"],
        ondelete="RESTRICT",
    )



def downgrade() -> None:
    """Revert workflow version integrity constraints."""

    # 1. Restore node execution foreign keys.
    op.drop_constraint(
        "fk_node_executions_node_version",
        "node_executions",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_node_executions_execution_version",
        "node_executions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("fk_node_executions_workflow_node_id_workflow_nodes"),
        "node_executions",
        "workflow_nodes",
        ["workflow_node_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        op.f("fk_node_executions_execution_id_executions"),
        "node_executions",
        "executions",
        ["execution_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_column("node_executions", "workflow_version_id")

    # 2. Restore execution foreign key.
    op.drop_constraint(
        "fk_executions_workflow_version_workspace",
        "executions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("fk_executions_workflow_version_id_workflow_versions"),
        "executions",
        "workflow_versions",
        ["workflow_version_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.drop_constraint(
        "uq_executions_id_version",
        "executions",
        type_="unique",
    )

    # Preserve ix_executions_workflow_version_id.
    # It was never dropped by upgrade().

    # 3. Restore workflow version foreign key.
    op.drop_constraint(
        "fk_workflow_versions_workflow_workspace",
        "workflow_versions",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("fk_workflow_versions_workflow_id_workflows"),
        "workflow_versions",
        "workflows",
        ["workflow_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "uq_workflow_versions_id_workspace",
        "workflow_versions",
        type_="unique",
    )

    op.create_index(
        op.f("ix_workflow_versions_workflow_id"),
        "workflow_versions",
        ["workflow_id"],
        unique=False,
    )

    op.drop_column("workflow_versions", "workspace_id")

    # 4. Remove remaining composite unique constraints.
    op.drop_constraint(
        "uq_workflow_nodes_id_version",
        "workflow_nodes",
        type_="unique",
    )

    op.drop_constraint(
        "uq_workflows_id_workspace",
        "workflows",
        type_="unique",
    )

"""add anomaly fields to processed_logs

Revision ID: 2cc4d8f1b73d
Revises: e75853ce4586
Create Date: 2026-02-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "2cc4d8f1b73d"
down_revision = "e75853ce4586"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("processed_logs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("anomaly_score", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("risk_level", sa.String(length=20), nullable=True))
        batch_op.create_index("ix_processed_logs_is_anomaly", ["is_anomaly"], unique=False)
        batch_op.create_index("ix_processed_logs_risk_level", ["risk_level"], unique=False)


def downgrade():
    with op.batch_alter_table("processed_logs", schema=None) as batch_op:
        batch_op.drop_index("ix_processed_logs_risk_level")
        batch_op.drop_index("ix_processed_logs_is_anomaly")
        batch_op.drop_column("risk_level")
        batch_op.drop_column("anomaly_score")

"""activitylogidx

Revision ID: 541e5e89943c
Revises: 1ab9cc1d1843
Create Date: 2022-12-04 16:51:53.925604

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "541e5e89943c"
down_revision = "1ab9cc1d1843"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "activity_log_post_interaction_idx", "activity_log", ["post_id", "interaction_type"], unique=False
    )


def downgrade():
    op.drop_index("activity_log_post_interaction_idx", table_name="activity_log")

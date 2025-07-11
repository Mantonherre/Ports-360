"""create snapshot tables"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "sensor_snapshot",
        sa.Column("id", sa.Text, nullable=False),
        sa.Column(
            "ts",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("measuredproperty", sa.Text, nullable=True),
        sa.Column("value", sa.Float, nullable=True),
        sa.Column("geom", Geometry("POINT", srid=4326), nullable=True),
    )
    op.execute("SELECT create_hypertable('sensor_snapshot','ts');")

    op.create_table(
        "energy_snapshot",
        sa.Column("id", sa.Text, nullable=False),
        sa.Column(
            "ts",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("soc", sa.Float, nullable=True),
        sa.Column("power_kw", sa.Float, nullable=True),
    )
    op.execute("SELECT create_hypertable('energy_snapshot','ts');")

    op.create_table(
        "bathy_snapshot",
        sa.Column("id", sa.Text, nullable=False),
        sa.Column("ts", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("depth_m", sa.Float, nullable=True),
        sa.Column("geom", Geometry("POINT", srid=4326), nullable=True),
    )
    op.execute("SELECT create_hypertable('bathy_snapshot','ts');")


def downgrade() -> None:
    op.drop_table("bathy_snapshot")
    op.drop_table("energy_snapshot")
    op.drop_table("sensor_snapshot")

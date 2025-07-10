from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, TIMESTAMP, Float, text
from geoalchemy2 import Geometry


class Base(DeclarativeBase):
    pass


class SensorSnapshot(Base):
    __tablename__ = "sensor_snapshot"

    id: Mapped[str] = mapped_column(Text)
    ts: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), primary_key=True
    )
    measuredproperty: Mapped[str | None] = mapped_column(Text)
    value: Mapped[float | None] = mapped_column(Float)
    geom: Mapped[Any] = mapped_column(Geometry("POINT", srid=4326))


class EnergySnapshot(Base):
    __tablename__ = "energy_snapshot"

    id: Mapped[str] = mapped_column(Text)
    ts: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), primary_key=True
    )
    soc: Mapped[float | None] = mapped_column(Float)
    power_kw: Mapped[float | None] = mapped_column(Float)


class BathySnapshot(Base):
    __tablename__ = "bathy_snapshot"

    id: Mapped[str] = mapped_column(Text)
    ts: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), primary_key=True)
    depth_m: Mapped[float | None] = mapped_column(Float)
    geom: Mapped[Any] = mapped_column(Geometry("POINT", srid=4326))

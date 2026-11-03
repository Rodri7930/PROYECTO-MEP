"""Modelos ORM de proveedores, servicios y tarifas referenciales.

Proyecto: Magic Experiences Perú.
Los precios y la disponibilidad deben confirmarse con cada proveedor.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base declarativa para los modelos del módulo de proveedores."""


class Proveedor(Base):
    """Contacto habitual o potencial para prestar servicios turísticos."""

    __tablename__ = "proveedores"

    # Se conserva el identificador usado en PBI-05 y PBI-06 (ej. PROV001).
    id_proveedor: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    ruc: Mapped[str | None] = mapped_column(String(11), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)
    tipo_servicio: Mapped[str] = mapped_column(String(60), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    servicios: Mapped[list["Servicio"]] = relationship(
        back_populates="proveedor",
        cascade="all, delete-orphan",
    )


class Servicio(Base):
    """Servicio de alojamiento, alimentación, transporte u otro tipo."""

    __tablename__ = "servicios"

    id_servicio: Mapped[int] = mapped_column(Integer, primary_key=True)
    proveedor_id: Mapped[str] = mapped_column(
        ForeignKey("proveedores.id_proveedor"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    categoria: Mapped[str] = mapped_column(String(60), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    proveedor: Mapped[Proveedor] = relationship(back_populates="servicios")
    tarifas: Mapped[list["Tarifa"]] = relationship(
        back_populates="servicio",
        cascade="all, delete-orphan",
    )


class Tarifa(Base):
    """Precio referencial negociado, susceptible de cambios por demanda."""

    __tablename__ = "tarifas"
    __table_args__ = (
        CheckConstraint("precio_referencial >= 0", name="ck_tarifa_precio"),
        CheckConstraint("personas_min >= 1", name="ck_tarifa_personas_min"),
        CheckConstraint(
            "personas_max IS NULL OR personas_max >= personas_min",
            name="ck_tarifa_personas_rango",
        ),
        CheckConstraint(
            "descuento_pct >= 0 AND descuento_pct <= 100",
            name="ck_tarifa_descuento",
        ),
    )

    id_tarifa: Mapped[int] = mapped_column(Integer, primary_key=True)
    servicio_id: Mapped[int] = mapped_column(
        ForeignKey("servicios.id_servicio"), nullable=False
    )
    precio_referencial: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    moneda: Mapped[str] = mapped_column(String(3), nullable=False)
    temporada: Mapped[str] = mapped_column(String(30), nullable=False)
    personas_min: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    personas_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    descuento_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("0.00"), nullable=False
    )
    vigencia_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    vigencia_fin: Mapped[date | None] = mapped_column(Date, nullable=True)

    servicio: Mapped[Servicio] = relationship(back_populates="tarifas")

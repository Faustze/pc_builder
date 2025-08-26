from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AssemblyComponentAssociation(Base):
    __tablename__ = "assembly_component_association"

    assembly_id: Mapped[int] = mapped_column(
        ForeignKey("assemblies.id", ondelete="CASCADE"), primary_key=True
    )
    component_id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)

    assembly: Mapped["Assembly"] = relationship(back_populates="components_association")
    component: Mapped["Component"] = relationship(
        back_populates="assemblies_association"
    )


class MemoryType(Base):
    __tablename__ = "memory_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    rams: Mapped[list["RAM"]] = relationship(back_populates="memory_type_rel")
    motherboards: Mapped[list["Motherboard"]] = relationship(
        back_populates="memory_type_rel"
    )


class SocketType(Base):
    __tablename__ = "socket_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    cpus: Mapped[list["CPU"]] = relationship(back_populates="socket_type_rel")
    motherboards: Mapped[list["Motherboard"]] = relationship(
        back_populates="socket_type_rel"
    )


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    component_type: Mapped[str] = mapped_column(String(50), nullable=False)

    components: Mapped[list["Component"]] = relationship(back_populates="brand_rel")


class Assembly(Base):
    __tablename__ = "assemblies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    components_association: Mapped[list["AssemblyComponentAssociation"]] = relationship(
        back_populates="assembly",
        cascade="all, delete-orphan",
    )
    components = association_proxy(
        "components_association",
        "component",
        creator=lambda component: AssemblyComponentAssociation(component=component),
    )


class Component(Base):
    __tablename__ = "components"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id", ondelete="CASCADE"), nullable=False
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    component_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __mapper_args__ = {
        "polymorphic_on": component_type,
        "polymorphic_identity": "component",
    }

    brand_rel: Mapped["Brand"] = relationship(
        back_populates="components", lazy="joined"
    )

    assemblies_association: Mapped[list["AssemblyComponentAssociation"]] = relationship(
        back_populates="component",
        cascade="all, delete-orphan",
    )
    assemblies = association_proxy("assemblies_association", "assembly")


class Motherboard(Component):
    __tablename__ = "motherboards"

    id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )
    socket_type_id: Mapped[int] = mapped_column(
        ForeignKey("socket_types.id"), nullable=False
    )
    memory_type_id: Mapped[int] = mapped_column(
        ForeignKey("memory_types.id"), nullable=False
    )
    has_integrated_graphics: Mapped[bool] = mapped_column(Boolean, default=False)

    socket_type_rel: Mapped["SocketType"] = relationship(
        back_populates="motherboards", lazy="joined"
    )
    memory_type_rel: Mapped["MemoryType"] = relationship(
        back_populates="motherboards", lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_identity": "motherboard",
    }


class CPU(Component):
    __tablename__ = "cpus"

    id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )
    socket_type_id: Mapped[int] = mapped_column(
        ForeignKey("socket_types.id"), nullable=False
    )
    cores: Mapped[int] = mapped_column(nullable=False)
    threads: Mapped[int] = mapped_column(nullable=False)
    has_integrated_graphics: Mapped[bool] = mapped_column(default=False)

    socket_type_rel: Mapped["SocketType"] = relationship(
        back_populates="cpus", lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_identity": "cpu",
    }


class GPU(Component):
    __tablename__ = "gpus"

    id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )
    vram: Mapped[int] = mapped_column(nullable=False)
    temperature: Mapped[int] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "gpu",
    }


class Soundcard(Component):
    __tablename__ = "soundcards"

    id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )
    channels_quantity: Mapped[int] = mapped_column(nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "soundcard",
    }


class RAM(Component):
    __tablename__ = "rams"

    id: Mapped[int] = mapped_column(
        ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )
    memory_type_id: Mapped[int] = mapped_column(
        ForeignKey("memory_types.id"), nullable=False
    )
    capacity: Mapped[int] = mapped_column(nullable=False)
    frequency: Mapped[int] = mapped_column(nullable=False)

    memory_type_rel: Mapped["MemoryType"] = relationship(
        back_populates="rams", lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_identity": "ram",
    }

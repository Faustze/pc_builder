from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        text)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .database import Base


class AssemblyComponentAssociation(Base):
    __tablename__ = "assembly_component_association"

    assembly_id = Column(Integer, ForeignKey('assemblies.id', ondelete='CASCADE'), primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)

    assembly = relationship("Assembly", back_populates="components_association")
    component = relationship("Component", back_populates="assemblies_association")


class MemoryType(Base):
    __tablename__ = 'memory_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    rams = relationship("RAM", back_populates="memory_type_rel")
    motherboards = relationship("Motherboard",
                                back_populates="memory_type_rel")


class SocketType(Base):
    __tablename__ = 'socket_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    cpus = relationship("CPU", back_populates="socket_type_rel")
    motherboards = relationship("Motherboard",
                                back_populates="socket_type_rel")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    component_type = Column(String, nullable=False)

    components = relationship("Component", back_populates="brand_rel")


class Assembly(Base):
    __tablename__ = "assemblies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    components_association = relationship("AssemblyComponentAssociation", back_populates="assembly", cascade="all, delete-orphan")
    components = association_proxy(
        'components_association',
        'component',
        creator=lambda component: AssemblyComponentAssociation(component=component)
    )


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey('brands.id', ondelete='CASCADE'),
                      nullable=False)
    model = Column(String(100), nullable=False, unique=True)
    quantity = Column(Integer, default=1)
    component_type = Column(String(20), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"))
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    __mapper_args__ = {
        "polymorphic_on": component_type,
        "polymorphic_identity": "component",
    }

    brand_rel = relationship("Brand",
                             back_populates="components", lazy='joined')

    assemblies_association = relationship("AssemblyComponentAssociation", back_populates="component", cascade="all, delete-orphan")
    assemblies = association_proxy('assemblies_association', 'assembly')


class Motherboard(Component):
    __tablename__ = "motherboards"

    id = Column(Integer, ForeignKey("components.id", ondelete='CASCADE'),
                primary_key=True)
    socket_type_id = Column(Integer, ForeignKey('socket_types.id'), nullable=False)
    memory_type_id = Column(Integer, ForeignKey('memory_types.id'), nullable=False)
    has_integrated_graphics = Column(Boolean, default=False)

    socket_type_rel = relationship("SocketType",
                                   back_populates="motherboards", lazy='joined')
    memory_type_rel = relationship("MemoryType",
                                   back_populates="motherboards", lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "motherboard",
    }


class CPU(Component):
    __tablename__ = "cpus"

    id = Column(Integer, ForeignKey("components.id", ondelete='CASCADE'),
                primary_key=True)
    socket_type_id = Column(Integer, ForeignKey('socket_types.id'), nullable=False)
    cores = Column(Integer, nullable=False)
    threads = Column(Integer, nullable=False)
    has_integrated_graphics = Column(Boolean, default=False)

    socket_type_rel = relationship("SocketType",
                                   back_populates="cpus", lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "cpu",
    }


class GPU(Component):
    __tablename__ = "gpus"

    id = Column(Integer, ForeignKey("components.id", ondelete='CASCADE'),
                primary_key=True)
    vram = Column(Integer, nullable=False)
    temperature = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "gpu",
    }


class Soundcard(Component):
    __tablename__ = "soundcards"

    id = Column(Integer, ForeignKey("components.id", ondelete='CASCADE'),
                primary_key=True)
    channels_quantity = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "soundcard",
    }


class RAM(Component):
    __tablename__ = "rams"

    id = Column(Integer, ForeignKey("components.id", ondelete='CASCADE'),
                primary_key=True)
    memory_type_id = Column(Integer, ForeignKey('memory_types.id'), nullable=False)
    capacity = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)

    memory_type_rel = relationship("MemoryType", back_populates="rams", lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "ram",
    }

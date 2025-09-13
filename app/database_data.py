from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from app.database import session_factory
from app.models import (
    CPU,
    GPU,
    RAM,
    Assembly,
    AssemblyComponentAssociation,
    Brand,
    MemoryType,
    Motherboard,
    SocketType,
    Soundcard,
)


def seed_data():
    with session_factory() as session:
        try:
            # Seed socket types
            socket_types = ["LGA1151", "LGA1700", "LGA1200", "AM4", "AM5"]
            for name in socket_types:
                if not session.query(SocketType).filter_by(name=name).first():
                    session.add(SocketType(name=name))
            session.commit()

            # Seed memory types
            memory_types = ["DDR3", "DDR4", "DDR5"]
            for name in memory_types:
                if not session.query(MemoryType).filter_by(name=name).first():
                    session.add(MemoryType(name=name))
            session.commit()

            # Seed brands
            brands = [
                {"name": "ASUS", "type": "motherboard"},
                {"name": "MSI", "type": "motherboard"},
                {"name": "GIGABYTE", "type": "motherboard"},
                {"name": "INTEL", "type": "cpu"},
                {"name": "AMD", "type": "cpu"},
                {"name": "NVIDIA", "type": "gpu"},
                {"name": "ZOTAC", "type": "gpu"},
                {"name": "CORSAIR", "type": "ram"},
                {"name": "KINGSTON", "type": "ram"},
                {"name": "G.SKILL", "type": "ram"},
                {"name": "CREATIVE", "type": "soundcard"},
                {"name": "BEHRINGER", "type": "soundcard"},
                {"name": "FOCUSRITE", "type": "soundcard"},
            ]
            for brand in brands:
                if not session.query(Brand).filter_by(name=brand["name"]).first():
                    session.add(Brand(name=brand["name"], component_type=brand["type"]))
            session.commit()

            # Helper functions
            def get_id(model, name):
                item = session.query(model).filter_by(name=name).first()
                return item.id if item else None

            # Seed motherboards
            motherboards = [
                {
                    "brand": "ASUS",
                    "model": "ROG Strix Z790-E",
                    "socket": "LGA1700",
                    "memory": "DDR5",
                    "graphics": True,
                    "quantity": 10,
                },
                {
                    "brand": "MSI",
                    "model": "MAG B550 Tomahawk",
                    "socket": "AM4",
                    "memory": "DDR4",
                    "graphics": False,
                    "quantity": 7,
                },
                {
                    "brand": "GIGABYTE",
                    "model": "Z490 AORUS ULTRA",
                    "socket": "LGA1200",
                    "memory": "DDR4",
                    "graphics": True,
                    "quantity": 5,
                },
                {
                    "brand": "ASUS",
                    "model": "PRIME B650M-A WIFI",
                    "socket": "AM5",
                    "memory": "DDR5",
                    "graphics": True,
                    "quantity": 5,
                },
                {
                    "brand": "MSI",
                    "model": "B550M PRO-VDH WIFI",
                    "socket": "AM4",
                    "memory": "DDR4",
                    "graphics": False,
                    "quantity": 5,
                },
                {
                    "brand": "GIGABYTE",
                    "model": "B650 AORUS Elite AX",
                    "socket": "AM5",
                    "memory": "DDR5",
                    "graphics": True,
                    "quantity": 5,
                },
                {
                    "brand": "MSI",
                    "model": "B650E Tomahawk WIFI",
                    "socket": "AM5",
                    "memory": "DDR5",
                    "graphics": False,
                    "quantity": 5,
                },
                {
                    "brand": "ASUS",
                    "model": "ROG Crosshair X670E Hero",
                    "socket": "AM5",
                    "memory": "DDR5",
                    "graphics": True,
                    "quantity": 4,
                },
                {
                    "brand": "MSI",
                    "model": "Z790 ACE",
                    "socket": "LGA1700",
                    "memory": "DDR5",
                    "graphics": True,
                    "quantity": 3,
                },
                {
                    "brand": "GIGABYTE",
                    "model": "B650M DS3H",
                    "socket": "AM5",
                    "memory": "DDR5",
                    "graphics": True,
                    "quantity": 3,
                },
            ]
            motherboard_objects = [
                Motherboard(
                    component_type="motherboard",
                    brand_id=get_id(Brand, m["brand"]),
                    model=m["model"],
                    socket_type_id=get_id(SocketType, m["socket"]),
                    memory_type_id=get_id(MemoryType, m["memory"]),
                    has_integrated_graphics=m["graphics"],
                    quantity=m["quantity"],
                )
                for m in motherboards
            ]
            session.add_all(motherboard_objects)
            session.commit()

            # Seed CPUs
            cpus = [
                {
                    "brand": "INTEL",
                    "model": "Core i7-12700K",
                    "socket": "LGA1700",
                    "cores": 12,
                    "threads": 20,
                    "graphics": True,
                    "quantity": 15,
                },
                {
                    "brand": "AMD",
                    "model": "Ryzen 5 5600X",
                    "socket": "AM4",
                    "cores": 6,
                    "threads": 12,
                    "graphics": False,
                    "quantity": 20,
                },
                {
                    "brand": "INTEL",
                    "model": "Core i9-10900K",
                    "socket": "LGA1200",
                    "cores": 10,
                    "threads": 20,
                    "graphics": True,
                    "quantity": 10,
                },
                {
                    "brand": "AMD",
                    "model": "Ryzen 5 8500G",
                    "socket": "AM5",
                    "cores": 6,
                    "threads": 12,
                    "graphics": True,
                    "quantity": 5,
                },
                {
                    "brand": "AMD",
                    "model": "Ryzen 5 7600",
                    "socket": "AM4",
                    "cores": 6,
                    "threads": 12,
                    "graphics": True,
                    "quantity": 4,
                },
                {
                    "brand": "INTEL",
                    "model": "Core i5-13400F",
                    "socket": "LGA1700",
                    "cores": 10,
                    "threads": 16,
                    "graphics": False,
                    "quantity": 3,
                },
            ]
            cpu_objects = [
                CPU(
                    component_type="cpu",
                    brand_id=get_id(Brand, c["brand"]),
                    model=c["model"],
                    socket_type_id=get_id(SocketType, c["socket"]),
                    cores=c["cores"],
                    threads=c["threads"],
                    has_integrated_graphics=c["graphics"],
                    quantity=c["quantity"],
                )
                for c in cpus
            ]
            session.add_all(cpu_objects)
            session.commit()

            # Seed GPUs
            gpus = [
                {"brand": "NVIDIA", "model": "RTX 3080", "vram": 10, "quantity": 8},
                {"brand": "NVIDIA", "model": "RTX 3070", "vram": 8, "quantity": 10},
                {"brand": "NVIDIA", "model": "GTX 1660", "vram": 6, "quantity": 12},
                {"brand": "NVIDIA", "model": "RTX 4060", "vram": 8, "quantity": 10},
                {"brand": "AMD", "model": "Radeon RX 7700 XT", "vram": 12, "quantity": 5},
                {"brand": "AMD", "model": "Radeon RX 7900 XTX", "vram": 24, "quantity": 7},
                {"brand": "AMD", "model": "Radeon RX 7800 XT", "vram": 16, "quantity": 6},
                {"brand": "AMD", "model": "Radeon RX 7600", "vram": 8, "quantity": 3},
            ]
            gpu_objects = [
                GPU(
                    component_type="gpu",
                    brand_id=get_id(Brand, g["brand"]),
                    model=g["model"],
                    vram=g["vram"],
                    quantity=g["quantity"],
                )
                for g in gpus
            ]
            session.add_all(gpu_objects)
            session.commit()

            # Seed RAMs
            rams = [
                {
                    "brand": "CORSAIR",
                    "model": "Vengeance LPX",
                    "memory": "DDR4",
                    "capacity": 16,
                    "frequency": 3200,
                    "quantity": 30,
                },
                {
                    "brand": "KINGSTON",
                    "model": "HyperX Fury",
                    "memory": "DDR4",
                    "capacity": 8,
                    "frequency": 2666,
                    "quantity": 25,
                },
                {
                    "brand": "CORSAIR",
                    "model": "Dominion Platinum",
                    "memory": "DDR5",
                    "capacity": 32,
                    "frequency": 5200,
                    "quantity": 10,
                },
                {
                    "brand": "G.SKILL",
                    "model": "Trident Z5 Neo",
                    "memory": "DDR5",
                    "capacity": 32,
                    "frequency": 600,
                    "quantity": 15,
                },
                {
                    "brand": "G.SKILL",
                    "model": "Ripjaws S5",
                    "memory": "DDR5",
                    "capacity": 32,
                    "frequency": 6400,
                    "quantity": 10,
                },
            ]
            ram_objects = [
                RAM(
                    component_type="ram",
                    brand_id=get_id(Brand, r["brand"]),
                    model=r["model"],
                    memory_type_id=get_id(MemoryType, r["memory"]),
                    capacity=r["capacity"],
                    frequency=r["frequency"],
                    quantity=r["quantity"],
                )
                for r in rams
            ]
            session.add_all(ram_objects)
            session.commit()

            # Seed soundcards
            soundcards = [
                {"brand": "CREATIVE", "model": "Sound BlasterX AE-5", "channels": 5, "quantity": 15},
                {"brand": "BEHRINGER", "model": "U-PHORIA UMC404HD", "channels": 4, "quantity": 12},
                {"brand": "CREATIVE", "model": "Sound Blaster Z", "channels": 5, "quantity": 10},
                {"brand": "BEHRINGER", "model": "U-PHORIA UMC22", "channels": 2, "quantity": 20},
                {"brand": "FOCUSRITE", "model": "Scarlett 2i2", "channels": 2, "quantity": 15},
            ]
            soundcard_objects = [
                Soundcard(
                    component_type="soundcard",
                    brand_id=get_id(Brand, s["brand"]),
                    model=s["model"],
                    channels_quantity=s["channels"],
                    quantity=s["quantity"],
                )
                for s in soundcards
            ]
            session.add_all(soundcard_objects)
            session.commit()

            # Seed assemblies
            assemblies = [
                {
                    "name": "Gaming Build",
                    "quantity": 3,
                    "components": [
                        (motherboard_objects[0], 1),
                        (cpu_objects[0], 1),
                        (gpu_objects[0], 1),
                        (ram_objects[2], 2),
                        (soundcard_objects[0], 1),
                    ],
                },
                {
                    "name": "Budget Build",
                    "quantity": 5,
                    "components": [
                        (motherboard_objects[1], 1),
                        (cpu_objects[1], 1),
                        (gpu_objects[2], 1),
                        (ram_objects[0], 2),
                        (soundcard_objects[1], 1),
                    ],
                },
                {
                    "name": "Workstation Build",
                    "quantity": 2,
                    "components": [
                        (motherboard_objects[2], 1),
                        (cpu_objects[2], 1),
                        (gpu_objects[1], 1),
                        (ram_objects[1], 4),
                        (soundcard_objects[0], 1),
                    ],
                },
            ]
            for assembly_data in assemblies:
                assembly = Assembly(name=assembly_data["name"], quantity=assembly_data["quantity"])
                assembly.components_association.extend(
                    [
                        AssemblyComponentAssociation(component=comp, quantity=qty)
                        for comp, qty in assembly_data["components"]
                    ]
                )
                session.add(assembly)
            session.commit()

            logger.info("Seed data and compatible assemblies added successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error during seeding: {e}")

from .database import session_factory
from .models import (
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
            socket_types = ["LGA1151", "LGA1700", "LGA1200", "AM4", "AM5"]
            for name in socket_types:
                if not session.query(SocketType).filter_by(name=name).first():
                    session.add(SocketType(name=name))
            session.commit()

            memory_types = ["DDR3", "DDR4", "DDR5"]
            for name in memory_types:
                if not session.query(MemoryType).filter_by(name=name).first():
                    session.add(MemoryType(name=name))
            session.commit()

            brand_data = [
                ("ASUS", "motherboard"),
                ("MSI", "motherboard"),
                ("GIGABYTE", "motherboard"),
                ("INTEL", "cpu"),
                ("AMD", "cpu"),
                ("NVIDIA", "gpu"),
                ("ZOTAC", "gpu"),
                ("CORSAIR", "ram"),
                ("KINGSTON", "ram"),
                ("CREATIVE", "soundcard"),
                ("BEHRINGER", "soundcard"),
            ]
            for name, ctype in brand_data:
                if not session.query(Brand).filter_by(name=name).first():
                    session.add(Brand(name=name, component_type=ctype))
            session.commit()

            def get_brand_id(brand_name):
                brand = session.query(Brand).filter_by(name=brand_name).first()
                return brand.id if brand else None

            def get_socket_id(socket_name):
                socket = session.query(SocketType).filter_by(name=socket_name).first()
                return socket.id if socket else None

            def get_memory_id(memory_name):
                memory_type = (
                    session.query(MemoryType).filter_by(name=memory_name).first()
                )
                return memory_type.id if memory_type else None

            motherboards = [
                Motherboard(
                    component_type="motherboard",
                    brand_id=get_brand_id("ASUS"),
                    model="ROG Strix Z790-E",
                    socket_type_id=get_socket_id("LGA1700"),
                    memory_type_id=get_memory_id("DDR5"),
                    has_integrated_graphics=True,
                    quantity=10,
                ),
                Motherboard(
                    component_type="motherboard",
                    brand_id=get_brand_id("MSI"),
                    model="MAG B550 Tomahawk",
                    socket_type_id=get_socket_id("AM4"),
                    memory_type_id=get_memory_id("DDR4"),
                    has_integrated_graphics=False,
                    quantity=7,
                ),
                Motherboard(
                    component_type="motherboard",
                    brand_id=get_brand_id("GIGABYTE"),
                    model="Z490 AORUS ULTRA",
                    socket_type_id=get_socket_id("LGA1200"),
                    memory_type_id=get_memory_id("DDR4"),
                    has_integrated_graphics=True,
                    quantity=5,
                ),
            ]
            session.add_all(motherboards)
            session.commit()

            cpus = [
                CPU(
                    component_type="cpu",
                    brand_id=get_brand_id("INTEL"),
                    model="Core i7-12700K",
                    socket_type_id=get_socket_id("LGA1700"),
                    cores=12,
                    threads=20,
                    has_integrated_graphics=True,
                    quantity=15,
                ),
                CPU(
                    component_type="cpu",
                    brand_id=get_brand_id("AMD"),
                    model="Ryzen 5 5600X",
                    socket_type_id=get_socket_id("AM4"),
                    cores=6,
                    threads=12,
                    has_integrated_graphics=False,
                    quantity=20,
                ),
                CPU(
                    component_type="cpu",
                    brand_id=get_brand_id("INTEL"),
                    model="Core i9-10900K",
                    socket_type_id=get_socket_id("LGA1200"),
                    cores=10,
                    threads=20,
                    has_integrated_graphics=True,
                    quantity=10,
                ),
            ]
            session.add_all(cpus)
            session.commit()

            gpus = [
                GPU(
                    component_type="gpu",
                    brand_id=get_brand_id("NVIDIA"),
                    model="RTX 3080",
                    vram=10,
                    quantity=8,
                ),
                GPU(
                    component_type="gpu",
                    brand_id=get_brand_id("ZOTAC"),
                    model="RTX 3070",
                    vram=8,
                    quantity=10,
                ),
                GPU(
                    component_type="gpu",
                    brand_id=get_brand_id("NVIDIA"),
                    model="GTX 1660",
                    vram=6,
                    quantity=12,
                ),
            ]
            session.add_all(gpus)
            session.commit()

            rams = [
                RAM(
                    component_type="ram",
                    brand_id=get_brand_id("CORSAIR"),
                    model="Vengeance LPX",
                    memory_type_id=get_memory_id("DDR4"),
                    capacity=16,
                    frequency=3200,
                    quantity=30,
                ),
                RAM(
                    component_type="ram",
                    brand_id=get_brand_id("KINGSTON"),
                    model="HyperX Fury",
                    memory_type_id=get_memory_id("DDR4"),
                    capacity=8,
                    frequency=2666,
                    quantity=25,
                ),
                RAM(
                    component_type="ram",
                    brand_id=get_brand_id("CORSAIR"),
                    model="Dominion Platinum",
                    memory_type_id=get_memory_id("DDR5"),
                    capacity=32,
                    frequency=5200,
                    quantity=10,
                ),
            ]
            session.add_all(rams)
            session.commit()

            soundcards = [
                Soundcard(
                    component_type="soundcard",
                    brand_id=get_brand_id("CREATIVE"),
                    model="Sound BlasterX AE-5",
                    channels_quantity=5,
                    quantity=15,
                ),
                Soundcard(
                    component_type="soundcard",
                    brand_id=get_brand_id("BEHRINGER"),
                    model="U-PHORIA UMC404HD",
                    channels_quantity=4,
                    quantity=12,
                ),
            ]
            session.add_all(soundcards)
            session.commit()

            assemblies = []

            assembly1 = Assembly(name="Gaming Build 1", quantity=3)
            assembly1.components_association.extend(
                [
                    AssemblyComponentAssociation(component=motherboards[0], quantity=1),
                    AssemblyComponentAssociation(component=cpus[0], quantity=1),
                    AssemblyComponentAssociation(component=gpus[0], quantity=1),
                    AssemblyComponentAssociation(component=rams[2], quantity=2),
                    AssemblyComponentAssociation(component=soundcards[0], quantity=1),
                ]
            )
            assemblies.append(assembly1)

            assembly2 = Assembly(name="Budget Build", quantity=5)
            assembly2.components_association.extend(
                [
                    AssemblyComponentAssociation(component=motherboards[1], quantity=1),
                    AssemblyComponentAssociation(component=cpus[1], quantity=1),
                    AssemblyComponentAssociation(component=gpus[2], quantity=1),
                    AssemblyComponentAssociation(component=rams[0], quantity=2),
                    AssemblyComponentAssociation(component=soundcards[1], quantity=1),
                ]
            )
            assemblies.append(assembly2)

            assembly3 = Assembly(name="Workstation Build", quantity=2)
            assembly3.components_association.extend(
                [
                    AssemblyComponentAssociation(component=motherboards[2], quantity=1),
                    AssemblyComponentAssociation(component=cpus[2], quantity=1),
                    AssemblyComponentAssociation(component=gpus[1], quantity=1),
                    AssemblyComponentAssociation(component=rams[1], quantity=4),
                    AssemblyComponentAssociation(component=soundcards[0], quantity=1),
                ]
            )
            assemblies.append(assembly3)

            assembly4 = Assembly(name="Streaming PC", quantity=4)
            assembly4.components_association.extend(
                [
                    AssemblyComponentAssociation(component=motherboards[0], quantity=1),
                    AssemblyComponentAssociation(component=cpus[0], quantity=1),
                    AssemblyComponentAssociation(component=gpus[1], quantity=1),
                    AssemblyComponentAssociation(component=rams[2], quantity=4),
                    AssemblyComponentAssociation(component=soundcards[1], quantity=1),
                ]
            )
            assemblies.append(assembly4)

            assembly5 = Assembly(name="Editing Rig", quantity=1)
            assembly5.components_association.extend(
                [
                    AssemblyComponentAssociation(component=motherboards[1], quantity=1),
                    AssemblyComponentAssociation(component=cpus[1], quantity=1),
                    AssemblyComponentAssociation(component=gpus[0], quantity=1),
                    AssemblyComponentAssociation(component=rams[0], quantity=2),
                    AssemblyComponentAssociation(component=soundcards[0], quantity=1),
                ]
            )
            assemblies.append(assembly5)

            session.add_all(assemblies)
            session.commit()

            print("Seed data and compatible assemblies added successfully.")

        except Exception as e:
            session.rollback()
            print(f"Error during seed data: {e}")

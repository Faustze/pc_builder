import json
import xml.etree.ElementTree as Et

from flask import (
    Response,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_wtf.csrf import generate_csrf
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, with_polymorphic

from .database import session_factory
from .forms import (
    AssemblySelectForm,
    BrandForm,
    CPUForm,
    GPUForm,
    MemoryTypeForm,
    MotherboardForm,
    RAMForm,
    SocketForm,
    SoundcardForm,
    get_memory_type_choices,
)
from .models import (
    CPU,
    GPU,
    RAM,
    Assembly,
    AssemblyComponentAssociation,
    Brand,
    Component,
    MemoryType,
    Motherboard,
    SocketType,
    Soundcard,
)


def populate_component_choices(form, session, selected_ids=None):
    selected_ids = selected_ids or {}

    def move_selected_first(items, selected_id):
        if not selected_id:
            return items
        return sorted(items, key=lambda x: 0 if x[0] == selected_id else 1)

    motherboards = session.query(Motherboard).all()
    mb_choices = [
        (
            mb.id,
            f"{mb.brand_rel.name} {mb.model} | Socket: {mb.socket_type_rel.name} | RAM: {mb.memory_type_rel.name}",
        )
        for mb in motherboards
    ]
    form.motherboard_id.choices = move_selected_first(
        mb_choices, selected_ids.get("motherboard_id")
    )

    cpus = session.query(CPU).all()
    cpu_choices = [
        (
            cpu.id,
            f"{cpu.brand_rel.name} {cpu.model} | Socket: {cpu.socket_type_rel.name} | "
            f"Cores: {cpu.cores} | Threads: {cpu.threads} | iGPU: {'Yes' if cpu.has_integrated_graphics else 'No'}",
        )
        for cpu in cpus
    ]
    form.cpu_id.choices = move_selected_first(cpu_choices, selected_ids.get("cpu_id"))

    gpus = session.query(GPU).all()
    gpu_choices = [
        (gpu.id, f"{gpu.brand_rel.name} {gpu.model} | VRAM: {gpu.vram}GB")
        for gpu in gpus
    ]
    form.gpu_id.choices = move_selected_first(gpu_choices, selected_ids.get("gpu_id"))

    rams = session.query(RAM).all()
    ram_choices = [
        (
            ram.id,
            f"{ram.brand_rel.name} {ram.model} | {ram.memory_type_rel.name} | "
            f"{ram.capacity}GB @ {ram.frequency}MHz",
        )
        for ram in rams
    ]
    form.ram_id.choices = move_selected_first(ram_choices, selected_ids.get("ram_id"))

    soundcards = session.query(Soundcard).all()
    sound_choices = [
        (sc.id, f"{sc.brand_rel.name} {sc.model} | Channels: {sc.channels_quantity}")
        for sc in soundcards
    ]
    form.soundcard_id.choices = move_selected_first(
        sound_choices, selected_ids.get("soundcard_id")
    )


def check_compatibility(form, session):
    errors = []

    motherboard_id = form.motherboard_id.data
    cpu_id = form.cpu_id.data
    ram_id = form.ram_id.data

    motherboard = session.get(Component, motherboard_id) if motherboard_id else None
    cpu = session.get(Component, cpu_id) if cpu_id else None
    ram = session.get(Component, ram_id) if ram_id else None

    if cpu and motherboard:
        if cpu.socket_type_id != motherboard.socket_type_id:
            errors.append("❌ CPU and Motherboard have incompatible sockets.")

    if ram and motherboard:
        if ram.memory_type_id != motherboard.memory_type_id:
            errors.append("❌ RAM and Motherboard have incompatible memory types.")

    return len(errors) == 0, errors


def get_selected_components_from_form(form, component_names):
    return [
        (getattr(form, f"{name}_id").data, getattr(form, f"{name}_quantity").data)
        for name in component_names
    ]


def populate_assembly_components(session, assembly, selected_components):
    component_ids = [cid for cid, _ in selected_components]

    components = session.query(Component).filter(Component.id.in_(component_ids)).all()
    id_to_qty = dict(selected_components)

    for component in components:
        quantity = id_to_qty.get(component.id, 1)
        assoc = AssemblyComponentAssociation(component=component, quantity=quantity)
        assembly.components_association.append(assoc)


def init_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def home():
        return render_template("home.html")

    @app.route("/components")
    def get_components_page():
        component_type_filter = request.args.get("component_type")
        brand_id_filter = request.args.get("brand_id")

        component_entities = with_polymorphic(
            Component, [Motherboard, CPU, GPU, RAM, Soundcard]
        )

        with session_factory() as session:
            query = session.query(component_entities)

            if component_type_filter:
                query = query.filter(
                    component_entities.component_type == component_type_filter
                )

            if brand_id_filter:
                query = query.filter(
                    component_entities.brand_id == int(brand_id_filter)
                )

            components = query.order_by(
                component_entities.component_type,
                component_entities.brand_id,
                component_entities.model,
            ).all()

            all_brands = session.query(Brand).order_by(Brand.name).all()

        return render_template(
            "components/components.html",
            components=components,
            brands=all_brands,
            selected_type=component_type_filter,
            selected_brand=brand_id_filter,
            csrf_token=generate_csrf(),
            active_page="components",
        )

    @app.route("/components/add", methods=["GET", "POST"])
    def add_component():
        return render_template("components/add_component.html")

    @app.route("/components/add/motherboard", methods=["GET", "POST"])
    def add_component_motherboard():
        form = MotherboardForm()

        with session_factory() as session:
            motherboard_brands = (
                session.query(Brand)
                .filter_by(component_type="motherboard")
                .order_by(Brand.name)
                .all()
            )
            socket_types = session.query(SocketType).all()
            memory_types = session.query(MemoryType).all()

            form.brand_id.choices = [(b.id, b.name) for b in motherboard_brands]
            form.socket_type_id.choices = [(s.id, s.name) for s in socket_types]
            form.memory_type_id.choices = [(m.id, m.name) for m in memory_types]

        if form.validate_on_submit():
            try:
                with session_factory() as session:
                    motherboard = Motherboard(
                        brand_id=form.brand_id.data,
                        model=form.model.data,
                        quantity=form.quantity.data,
                        socket_type_id=form.socket_type_id.data,
                        memory_type_id=form.memory_type_id.data,
                        has_integrated_graphics=bool(form.has_integrated_graphics.data),
                    )
                    session.add(motherboard)
                    session.commit()
                    flash("Motherboard added successfully", "success")
                    return redirect(url_for("get_components_page"))
            except IntegrityError as e:
                session.rollback()

                if "unique constraint" in str(e.orig).lower():
                    flash(
                        f'Error: Component with model "{form.model.data}" already exists.',
                        "danger",
                    )
                else:
                    flash(f"Database error: {e}", "danger")
            except Exception as e:
                flash(f"Error: {e}", "danger")
        else:
            print("❌ Form validation failed")
            print(form.errors)

        return render_template("components/add_component_motherboard.html", form=form)

    @app.route("/components/add/cpu", methods=["GET", "POST"])
    def add_component_cpu():
        form = CPUForm()
        with session_factory() as session:
            cpu_brands = (
                session.query(Brand)
                .filter_by(component_type="cpu")
                .order_by(Brand.name)
                .all()
            )
            socket_types = session.query(SocketType).all()

            form.brand_id.choices = [(b.id, b.name) for b in cpu_brands]
            form.socket_type_id.choices = [(s.id, s.name) for s in socket_types]

        if request.method == "POST":
            if form.validate_on_submit():
                try:
                    with session_factory() as session:
                        cpu = CPU(
                            brand_id=int(form.brand_id.data),
                            model=form.model.data,
                            quantity=(
                                int(form.quantity.data) if form.quantity.data else 1
                            ),
                            socket_type_id=int(form.socket_type_id.data),
                            cores=int(form.cores.data),
                            threads=int(form.threads.data),
                            has_integrated_graphics=bool(
                                form.has_integrated_graphics.data
                            ),
                        )
                        session.add(cpu)
                        session.commit()
                        flash("CPU added successfully", "success")
                        return redirect(url_for("get_components_page"))
                except Exception as e:
                    flash(f"Error: {e}", "danger")
            else:
                print("❌ Form validation failed")
                print(form.errors)

        return render_template("components/add_component_cpu.html", form=form)

    @app.route("/components/add/gpu", methods=["GET", "POST"])
    def add_component_gpu():
        form = GPUForm()

        with session_factory() as session:
            gpu_brands = (
                session.query(Brand)
                .filter_by(component_type="gpu")
                .order_by(Brand.name)
                .all()
            )

            form.brand_id.choices = [(b.id, b.name) for b in gpu_brands]

        if request.method == "POST":
            if form.validate_on_submit():
                try:
                    with session_factory() as session:
                        gpu = GPU(
                            brand_id=int(form.brand_id.data),
                            model=form.model.data,
                            quantity=(
                                int(form.quantity.data) if form.quantity.data else 1
                            ),
                            vram=int(form.vram.data),
                        )
                        session.add(gpu)
                        session.commit()
                        flash("GPU added successfully", "success")
                        return redirect(url_for("get_components_page"))
                except Exception as e:
                    flash(f"Error: {e}", "danger")
            else:
                print("❌ Form validation failed")
                print(form.errors)

        return render_template("components/add_component_gpu.html", form=form)

    @app.route("/components/add/ram", methods=["GET", "POST"])
    def add_component_ram():
        form = RAMForm()

        with session_factory() as session:
            ram_brands = (
                session.query(Brand)
                .filter_by(component_type="ram")
                .order_by(Brand.name)
                .all()
            )
            memory_types = session.query(MemoryType).all()
            form.brand_id.choices = [(b.id, b.name) for b in ram_brands]
            form.memory_type_id.choices = [(m.id, m.name) for m in memory_types]

        if request.method == "POST":
            if form.validate_on_submit():
                try:
                    with session_factory() as session:
                        ram = RAM(
                            brand_id=form.brand_id.data,
                            model=form.model.data,
                            quantity=form.quantity.data,
                            memory_type_id=form.memory_type_id.data,
                            capacity=form.capacity.data,
                            frequency=form.frequency.data,
                        )
                        session.add(ram)
                        session.commit()
                        flash("RAM added successfully", "success")
                        return redirect(url_for("get_components_page"))
                except Exception as e:
                    flash(f"Error: {e}", "danger")
            else:
                print("❌ Form validation failed")
                print(form.errors)

        return render_template("components/add_component_ram.html", form=form)

    @app.route("/components/add/soundcard", methods=["GET", "POST"])
    def add_component_soundcard():
        form = SoundcardForm()

        with session_factory() as session:
            soundcard_brands = (
                session.query(Brand)
                .filter_by(component_type="soundcard")
                .order_by(Brand.name)
                .all()
            )
            form.brand_id.choices = [(b.id, b.name) for b in soundcard_brands]

        if request.method == "POST":
            if form.validate_on_submit():
                try:
                    with session_factory() as session:
                        soundcard = Soundcard(
                            brand_id=int(form.brand_id.data),
                            model=form.model.data,
                            quantity=(
                                int(form.quantity.data) if form.quantity.data else 1
                            ),
                            channels_quantity=int(form.channels_quantity.data),
                        )
                        session.add(soundcard)
                        session.commit()
                        flash("Soundcard added successfully", "success")
                        return redirect(url_for("get_components_page"))
                except Exception as e:
                    flash(f"Error: {e}", "danger")
            else:
                print("❌ Form validation failed")
                print(form.errors)

        return render_template("components/add_component_soundcard.html", form=form)

    @app.route("/components/<int:component_id>/edit", methods=["GET", "POST"])
    def edit_component(component_id):
        form = None

        with session_factory() as session:
            component = session.get(Component, component_id)

            if not component:
                abort(404, description="Component not found")

            if component.component_type == "motherboard":
                motherboard_brands = (
                    session.query(Brand)
                    .filter_by(component_type="motherboard")
                    .order_by(Brand.name)
                    .all()
                )
                socket_types = session.query(SocketType).order_by(SocketType.name).all()
                memory_types = session.query(MemoryType).order_by(MemoryType.name).all()
                form = MotherboardForm(obj=component)
                form.socket_type_id.choices = [(s.id, s.name) for s in socket_types]
                form.memory_type_id.choices = [(m.id, m.name) for m in memory_types]
                form.brand_id.choices = [(b.id, b.name) for b in motherboard_brands]

            elif component.component_type == "cpu":
                cpu_brands = (
                    session.query(Brand)
                    .filter_by(component_type="cpu")
                    .order_by(Brand.name)
                    .all()
                )
                socket_types = session.query(SocketType).order_by(SocketType.name).all()
                form = CPUForm(obj=component)
                form.socket_type_id.choices = [(s.id, s.name) for s in socket_types]
                form.brand_id.choices = [(b.id, b.name) for b in cpu_brands]

            elif component.component_type == "ram":
                ram_brands = (
                    session.query(Brand)
                    .filter_by(component_type="ram")
                    .order_by(Brand.name)
                    .all()
                )
                memory_types = session.query(MemoryType).order_by(MemoryType.name).all()
                form = RAMForm(obj=component)
                form.memory_type_id.choices = [(m.id, m.name) for m in memory_types]
                form.brand_id.choices = [(b.id, b.name) for b in ram_brands]

            elif component.component_type == "gpu":
                gpu_brands = (
                    session.query(Brand)
                    .filter_by(component_type="gpu")
                    .order_by(Brand.name)
                    .all()
                )
                form = GPUForm(obj=component)
                form.brand_id.choices = [(b.id, b.name) for b in gpu_brands]

            elif component.component_type == "soundcard":
                soundcard_brands = (
                    session.query(Brand)
                    .filter_by(component_type="soundcard")
                    .order_by(Brand.name)
                    .all()
                )
                form = SoundcardForm(obj=component)
                form.brand_id.choices = [(b.id, b.name) for b in soundcard_brands]

            if form is not None and form.validate_on_submit():
                try:
                    form.populate_obj(component)
                    session.commit()
                    flash("The component has been edited successfully.", "success")
                    return redirect(url_for("get_components_page"))
                except Exception as e:
                    session.rollback()
                    flash(f"Error while editing: {str(e)}", "danger")

        return render_template(
            "components/edit_component.html",
            title="Edit component",
            form=form,
            component=component,
            active_page="components",
        )

    @app.route("/components/<int:component_id>/delete", methods=["POST"])
    def delete_component(component_id):
        try:
            with session_factory() as session:
                component = session.get(Component, component_id)

                if not component:
                    abort(404, description="Component not found ")

                if component.assemblies:
                    flash("Cannot delete component: it's used in assemblies.", "danger")
                    return redirect(url_for("get_components_page"))

                if component.component_type == "motherboard":
                    session.execute(
                        delete(Motherboard).where(Motherboard.id == component.id)
                    )
                elif component.component_type == "cpu":
                    session.execute(delete(CPU).where(CPU.id == component.id))
                elif component.component_type == "ram":
                    session.execute(delete(RAM).where(RAM.id == component.id))
                elif component.component_type == "gpu":
                    session.execute(delete(GPU).where(GPU.id == component.id))
                elif component.component_type == "soundcard":
                    session.execute(
                        delete(Soundcard).where(Soundcard.id == component.id)
                    )

                session.delete(component)
                session.commit()
                flash("The component has been successfully removed.", "success")
        except Exception as e:
            session.rollback()
            flash(f"Error while deleting: {str(e)}", "danger")
            current_app.logger.error(f"Error while deleting component: {str(e)}")

        return redirect(url_for("get_components_page"))

    @app.route("/classificators", methods=["GET", "POST"])
    def get_classificators_page():
        brand_form = BrandForm(prefix="brand")
        socket_form = SocketForm(prefix="socket")
        memory_form = MemoryTypeForm(prefix="memory")

        with session_factory() as session:
            if request.method == "POST":
                form_name = request.form.get("form-name")

                if form_name == "brand" and brand_form.validate():
                    new_brand = Brand(
                        name=brand_form.name.data,
                        component_type=brand_form.component_type.data,
                    )
                    try:
                        session.add(new_brand)
                        session.commit()
                        flash("Brand added successfully!", "success")
                    except IntegrityError:
                        session.rollback()
                        flash("This brand already exists!", "danger")
                    return redirect(url_for("get_classificators_page"))

                elif form_name == "socket" and socket_form.validate():
                    new_socket = SocketType(name=socket_form.name.data)
                    try:
                        session.add(new_socket)
                        session.commit()
                        flash("Socket type added successfully!", "success")
                    except IntegrityError:
                        session.rollback()
                        flash("This socket type already exists!", "danger")
                    return redirect(url_for("get_classificators_page"))

                elif form_name == "memory" and memory_form.validate():
                    new_memory = MemoryType(name=memory_form.name.data)
                    try:
                        session.add(new_memory)
                        session.commit()
                        flash("Memory type added successfully!", "success")
                    except IntegrityError:
                        session.rollback()
                        flash("This memory type already exists!", "danger")
                    return redirect(url_for("get_classificators_page"))

            brands = (
                session.query(Brand).order_by(Brand.component_type, Brand.name).all()
            )
            sockets = session.query(SocketType).order_by(SocketType.name).all()
            memories = session.query(MemoryType).order_by(MemoryType.name).all()

        return render_template(
            "classificators/classificators.html",
            brand_form=brand_form,
            socket_form=socket_form,
            memory_form=memory_form,
            brands=brands,
            sockets=sockets,
            memories=memories,
            csrf_token=generate_csrf(),
            active_page="classificators",
        )

    @app.route("/classificators/brand_<int:brand_id>/delete", methods=["POST"])
    def delete_brand(brand_id):
        with session_factory() as session:
            brand = session.query(Brand).get(brand_id)

            if brand is None:
                flash("Brand not found.", "warning")
                return redirect(url_for("get_classificators_page"))

            if brand.components:
                flash("Cannot delete brand: it's used in components.", "danger")
                return redirect(url_for("get_classificators_page"))

            if brand:
                session.delete(brand)
                session.commit()
                flash(f"Brand '{brand.name}' deleted successfully!", "success")
        return redirect(url_for("get_classificators_page"))

    @app.route(
        "/classificators/socket_type_<int:socket_type_id>/delete", methods=["POST"]
    )
    def delete_socket_type(socket_type_id):
        with session_factory() as session:
            socket_type = session.get(SocketType, socket_type_id)

            if not socket_type:
                flash("Socket type not found.", "danger")
                return redirect(url_for("get_classificators_page"))

            if socket_type.cpus or socket_type.motherboards:
                flash("Cannot delete socket type: it's used in components.", "danger")
                return redirect(url_for("get_classificators_page"))

            session.delete(socket_type)
            session.commit()
            flash("Socket type deleted successfully.", "success")
            return redirect(url_for("get_classificators_page"))

    @app.route(
        "/classificators/memory_type_<int:memory_type_id>/delete", methods=["POST"]
    )
    def delete_memory_type(memory_type_id):
        with session_factory() as session:
            memory_type = session.get(MemoryType, memory_type_id)

            if not memory_type:
                flash("Memory type not found.", "danger")
                return redirect(url_for("get_classificators_page"))

            if memory_type.rams or memory_type.motherboards:
                flash("Cannot delete memory type: it's used in components.", "danger")
                return redirect(url_for("get_classificators_page"))

            session.delete(memory_type)
            session.commit()
            flash("Memory type deleted successfully.", "success")
            return redirect(url_for("get_classificators_page"))

    @app.route("/assemblies", methods=["GET", "POST"])
    def get_assemblies_page():
        with session_factory() as session:
            assemblies = (
                session.query(Assembly)
                .options(joinedload(Assembly.components_association))
                .all()
            )
            return render_template(
                "assemblies/assemblies.html",
                assemblies=assemblies,
                csrf_token=generate_csrf(),
            )

    @app.route("/assemblies/add/select", methods=["GET", "POST"])
    def add_assembly():
        form = AssemblySelectForm()

        with session_factory() as session:
            populate_component_choices(form, session)

            if request.method == "POST" and form.validate_on_submit():
                compatible, compatibility_errors = check_compatibility(form, session)
                if not compatible:
                    for error in compatibility_errors:
                        flash(error, "danger")
                    return render_template(
                        "assemblies/add_assembly.html",
                        form=form,
                        csrf_token=generate_csrf(),
                        active_page="assemblies",
                    )

                try:
                    assembly = Assembly(
                        name=form.assembly_name.data,
                        quantity=form.assembly_quantity.data,
                    )

                    component_fields = ["motherboard", "cpu", "gpu", "ram", "soundcard"]
                    selected_components = get_selected_components_from_form(
                        form, component_fields
                    )
                    populate_assembly_components(session, assembly, selected_components)

                    session.add(assembly)
                    session.commit()

                    flash("Assembly created from selected components!", "success")
                    return redirect(url_for("get_assemblies_page"))

                except Exception as e:
                    session.rollback()
                    flash(f"Failed to create assembly: {e}", "danger")

        return render_template(
            "assemblies/add_assembly.html",
            form=form,
            csrf_token=generate_csrf(),
            active_page="assemblies",
        )

    @app.route("/assemblies/<int:assembly_id>")
    def get_assembly(assembly_id):
        with session_factory() as session:
            assembly = session.get(Assembly, assembly_id)

            if not assembly:
                abort(404, description="Assembly not found")

            return render_template(
                "assemblies/assembly_detail.html",
                assembly=assembly,
                get_memory_type_choices=get_memory_type_choices,
                csrf_token=generate_csrf(),
            )

    @app.route("/assemblies/<int:assembly_id>/delete", methods=["POST"])
    def delete_assembly(assembly_id):
        with session_factory() as session:
            assembly = session.get(Assembly, assembly_id)

            if not assembly:
                abort(404, description="Assembly not found")

            session.delete(assembly)
            session.commit()
            return redirect(url_for("get_assemblies_page"))

    @app.route("/assemblies/edit/<int:assembly_id>", methods=["GET", "POST"])
    def edit_assembly(assembly_id):
        form = AssemblySelectForm()

        with session_factory() as session:
            assembly = session.query(Assembly).filter_by(id=assembly_id).first()
            if not assembly:
                flash("Assembly not found.", "danger")
                return redirect(url_for("get_assemblies_page"))

            comp_map = {c.component_type: c for c in assembly.components}

            motherboard = comp_map.get("motherboard")
            motherboard_id = motherboard.id if motherboard is not None else None

            cpu = comp_map.get("cpu")
            cpu_id = cpu.id if cpu is not None else None

            gpu = comp_map.get("gpu")
            gpu_id = gpu.id if gpu is not None else None

            ram = comp_map.get("ram")
            ram_id = ram.id if ram is not None else None

            soundcard = comp_map.get("soundcard")
            soundcard_id = soundcard.id if soundcard is not None else None

            selected_ids = {
                "motherboard_id": motherboard_id,
                "cpu_id": cpu_id,
                "gpu_id": gpu_id,
                "ram_id": ram_id,
                "soundcard_id": soundcard_id,
            }

            populate_component_choices(form, session, selected_ids)

            if request.method == "GET":
                form.assembly_name.data = assembly.name
                form.assembly_quantity.data = assembly.quantity

                comp_map = {c.component_type: c for c in assembly.components}

                motherboard = comp_map.get("motherboard")
                form.motherboard_id.data = (
                    motherboard.id if motherboard is not None else None
                )

                cpu = comp_map.get("cpu")
                form.cpu_id.data = cpu.id if cpu is not None else None

                gpu = comp_map.get("gpu")
                form.gpu_id.data = gpu.id if gpu is not None else None

                ram = comp_map.get("ram")
                form.ram_id.data = ram.id if ram is not None else None

                soundcard = comp_map.get("soundcard")
                form.soundcard_id.data = soundcard.id if soundcard is not None else None

                form.gpu_is_integrated.data = "gpu" not in comp_map

                form.motherboard_quantity.data = (
                    motherboard.quantity if motherboard is not None else 1
                )
                form.cpu_quantity.data = cpu.quantity if cpu is not None else 1
                form.gpu_quantity.data = gpu.quantity if gpu is not None else 1
                form.ram_quantity.data = ram.quantity if ram is not None else 1
                form.soundcard_quantity.data = (
                    soundcard.quantity if soundcard is not None else 1
                )

            elif request.method == "POST" and form.validate_on_submit():
                compatible, compatibility_errors = check_compatibility(form, session)
                if not compatible:
                    for error in compatibility_errors:
                        flash(error, "danger")
                    return render_template(
                        "assemblies/edit_assembly.html",
                        form=form,
                        assembly=assembly,
                        csrf_token=generate_csrf(),
                        active_page="assemblies",
                    )

                try:
                    assembly.name = form.assembly_name.data or ""
                    assembly.quantity = form.assembly_quantity.data or 1

                    assembly.components.clear()

                    component_fields = ["motherboard", "cpu", "gpu", "ram", "soundcard"]
                    selected_components = get_selected_components_from_form(
                        form, component_fields
                    )
                    populate_assembly_components(session, assembly, selected_components)

                    session.add(assembly)
                    session.commit()

                    flash("Assembly updated succesfully!", "success")
                    return redirect(url_for("get_assemblies_page"))

                except Exception as e:
                    session.rollback()
                    flash(f"Failed to update assembly: {e}", "danger")

        return render_template(
            "assemblies/edit_assembly.html",
            form=form,
            assembly=assembly,
            csrf_token=generate_csrf(),
            active_page="assemblies",
        )

    @app.route("/assemblies/<int:assembly_id>/download/xml")
    def download_assembly_xml(assembly_id):
        with session_factory() as session:
            assembly = session.get(Assembly, assembly_id)

            if not assembly:
                abort(404, description="Assembly not found")

            root = Et.Element(
                "assembly", attrib={"id": str(assembly.id), "name": assembly.name}
            )

            for component in assembly.components:
                comp_el = Et.SubElement(
                    root,
                    "component",
                    attrib={
                        "type": component.component_type,
                        "brand": component.brand_rel.name,
                        "model": component.model,
                    },
                )

                if component.component_type == "cpu":
                    Et.SubElement(comp_el, "cores").text = str(component.cores)
                    Et.SubElement(comp_el, "threads").text = str(component.threads)
                    Et.SubElement(comp_el, "integrated_graphics").text = str(
                        component.has_integrated_graphics
                    )

                elif component.component_type == "motherboard":
                    Et.SubElement(comp_el, "socket").text = (
                        component.socket_type_rel.name
                    )
                    Et.SubElement(comp_el, "memory_type").text = (
                        component.memory_type_rel.name
                    )
                    Et.SubElement(comp_el, "integrated_graphics").text = str(
                        component.has_integrated_graphics
                    )

                elif component.component_type == "ram":
                    Et.SubElement(comp_el, "capacity").text = str(component.capacity)
                    Et.SubElement(comp_el, "frequency").text = str(component.frequency)
                    Et.SubElement(comp_el, "memory_type").text = (
                        component.memory_type_rel.name
                    )

                elif component.component_type == "gpu":
                    Et.SubElement(comp_el, "vram").text = str(component.vram)

                elif component.component_type == "soundcard":
                    Et.SubElement(comp_el, "channels").text = str(
                        component.channels_quantity
                    )

            xml_str = Et.tostring(root, encoding="utf-8", method="xml")

            return Response(
                xml_str,
                mimetype="application/xml",
                headers={
                    "Content-Disposition": f"attachment;filename=assembly_{assembly_id}.xml"
                },
            )

    @app.route("/assemblies/<int:assembly_id>/download/json")
    def download_assembly_json(assembly_id):
        with session_factory() as session:
            assembly = session.get(Assembly, assembly_id)

            if not assembly:
                abort(404, description="Assembly not found")

            data = {"id": assembly.id, "name": assembly.name, "components": []}

            for component in assembly.components:
                comp = {
                    "type": component.component_type,
                    "brand": component.brand_rel.name,
                    "model": component.model,
                }

                if component.component_type == "cpu":
                    comp.update(
                        {
                            "cores": component.cores,
                            "threads": component.threads,
                            "integrated_graphics": component.has_integrated_graphics,
                        }
                    )
                elif component.component_type == "motherboard":
                    comp.update(
                        {
                            "socket": component.socket_type_rel.name,
                            "memory_type": component.memory_type_rel.name,
                            "integrated_graphics": component.has_integrated_graphics,
                        }
                    )
                elif component.component_type == "ram":
                    comp.update(
                        {
                            "capacity": component.capacity,
                            "frequency": component.frequency,
                            "memory_type": component.memory_type_rel.name,
                        }
                    )
                elif component.component_type == "gpu":
                    comp.update({"vram": component.vram})
                elif component.component_type == "soundcard":
                    comp.update({"channels": component.channels_quantity})

                data["components"].append(comp)

            json_str = json.dumps(data, indent=2)

            return Response(
                json_str,
                mimetype="application/json",
                headers={
                    "Content-Disposition": f"attachment;filename=assembly_{assembly_id}.json"
                },
            )

    @app.route("/assemblies/<int:assembly_id>/download/txt")
    def download_assembly_txt(assembly_id):
        with session_factory() as session:
            assembly = session.get(Assembly, assembly_id)

            if not assembly:
                abort(404, description="Assembly not found")

            lines = [f"Assembly Name: {assembly.name}", "Components:"]

            for component in assembly.components:
                lines.append(f"\n  - Type: {component.component_type.upper()}")
                lines.append(f"    Brand: {component.brand_rel.name}")
                lines.append(f"    Model: {component.model}")

                if component.component_type == "cpu":
                    lines.append(f"    Cores: {component.cores}")
                    lines.append(f"    Threads: {component.threads}")
                    lines.append(
                        f"    Integrated Graphics: {'Yes' if component.has_integrated_graphics else 'No'}"
                    )

                elif component.component_type == "motherboard":
                    lines.append(f"    Socket: {component.socket_type_rel.name}")
                    lines.append(f"    Memory Type: {component.memory_type_rel.name}")
                    lines.append(
                        f"    Integrated Graphics: {'Yes' if component.has_integrated_graphics else 'No'}"
                    )

                elif component.component_type == "ram":
                    lines.append(f"    Capacity: {component.capacity} GB")
                    lines.append(f"    Frequency: {component.frequency} MHz")
                    lines.append(f"    Memory Type: {component.memory_type_rel.name}")

                elif component.component_type == "gpu":
                    lines.append(f"    VRAM: {component.vram} GB")

                elif component.component_type == "soundcard":
                    lines.append(f"    Channels: {component.channels_quantity}")

            txt_output = "\n".join(lines)

            return Response(
                txt_output,
                mimetype="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename=assembly_{assembly_id}.txt"
                },
            )

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FormField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, InputRequired, NumberRange

from .database import session_factory
from .models import Brand, MemoryType, SocketType


def get_brand_choices_for(component_type: str):
    with session_factory() as session:
        return [
            (b.id, b.name)
            for b in session.query(Brand)
            .filter_by(component_type=component_type)
            .order_by(Brand.name)
            .all()
        ]


def get_socket_type_choices():
    with session_factory() as session:
        return [
            (st.id, st.name)
            for st in session.query(SocketType).order_by(SocketType.name).all()
        ]


def get_memory_type_choices():
    with session_factory() as session:
        return [
            (mt.id, mt.name)
            for mt in session.query(MemoryType).order_by(MemoryType.name).all()
        ]


class BaseComponentForm(FlaskForm):
    model = StringField("Model", validators=[InputRequired()])
    quantity = IntegerField(
        "Quantity",
        validators=[NumberRange(min=1, max=1000)],
        default=1,
    )
    _component_type = None
    submit = SubmitField("Save")


class MotherboardForm(BaseComponentForm):
    brand_id = SelectField("Brand", coerce=int, validators=[DataRequired()])
    socket_type_id = SelectField("Socket Type", coerce=int, validators=[DataRequired()])
    memory_type_id = SelectField("Memory Type", coerce=int, validators=[DataRequired()])
    has_integrated_graphics = BooleanField("Integrated GPU")


class RAMForm(BaseComponentForm):
    brand_id = SelectField("Brand", coerce=int, validators=[DataRequired()])
    memory_type_id = SelectField("Memory Type", coerce=int, validators=[DataRequired()])
    capacity = SelectField(
        "Capacity (GB)",
        coerce=int,
        choices=[
            (4, "4 GB"),
            (8, "8 GB"),
            (16, "16 GB"),
            (32, "32 GB"),
        ],
        validators=[DataRequired()],
    )
    frequency = SelectField(
        "Frequency (MHz)",
        coerce=int,
        choices=[
            (1600, "1600 MHz (DDR3)"),
            (1866, "1866 MHz (DDR3)"),
            (2400, "2400 MHz (DDR4)"),
            (2666, "2666 MHz (DDR4)"),
            (3000, "3000 MHz (DDR4)"),
            (3200, "3200 MHz (DDR4)"),
            (3600, "3600 MHz (DDR4)"),
            (4800, "4800 MHz (DDR5)"),
            (5200, "5200 MHz (DDR5)"),
            (5600, "5600 MHz (DDR5)"),
            (6000, "6000 MHz (DDR5)"),
            (6400, "6400 MHz (DDR5)"),
        ],
        validators=[DataRequired()],
    )


class CPUForm(BaseComponentForm):
    brand_id = SelectField("Brand", coerce=int, validators=[DataRequired()])
    socket_type_id = SelectField("Socket Type", coerce=int, validators=[DataRequired()])
    cores = SelectField(
        "Cores",
        choices=[
            (2, "2 Cores"),
            (4, "4 Cores"),
            (6, "6 Cores"),
            (8, "8 Cores"),
            (10, "10 Cores"),
            (12, "12 Cores"),
            (16, "16 Cores"),
            (24, "24 Cores"),
        ],
        coerce=int,
        validators=[DataRequired()],
    )
    threads = SelectField(
        "Threads",
        choices=[
            (4, "4 Threads"),
            (6, "6 Threads"),
            (8, "8 Threads"),
            (12, "12 Threads"),
            (16, "16 Threads"),
            (20, "20 Threads"),
            (24, "24 Threads"),
            (32, "32 Threads"),
        ],
        coerce=int,
        validators=[DataRequired()],
    )
    has_integrated_graphics = BooleanField("Integrated GPU")


class GPUForm(BaseComponentForm):
    brand_id = SelectField("Brand", coerce=int, validators=[DataRequired()])
    vram = SelectField(
        "Capacity (GB)",
        choices=[
            (2, "2 GB"),
            (3, "3 GB"),
            (4, "4 GB"),
            (6, "6 GB"),
            (8, "8 GB"),
            (10, "10 GB"),
            (12, "12 GB"),
            (16, "16 GB"),
            (20, "20 GB"),
            (24, "24 GB"),
        ],
        coerce=int,
        validators=[DataRequired()],
    )


class SoundcardForm(BaseComponentForm):
    brand_id = SelectField("Brand", coerce=int, validators=[DataRequired()])
    channels_quantity = SelectField(
        "Channels quantity",
        choices=[
            (2, "2 Channels"),
            (4, "4 Channels"),
            (6, "6 Channels"),
            (7, "7 Channels"),
            (8, "8 Channels"),
            (16, "16 Channels"),
        ],
        coerce=int,
        validators=[DataRequired()],
    )


class AssemblyForm(FlaskForm):
    assembly_name = StringField("Assembly Name", validators=[DataRequired()])
    assembly_quantity = IntegerField(
        "Assembly Quantity", validators=[NumberRange(min=1, max=1000)], default=1
    )

    cpu_component = FormField(CPUForm)
    gpu_component = FormField(GPUForm)
    motherboard_component = FormField(MotherboardForm)
    ram_component = FormField(RAMForm)
    soundcard_component = FormField(SoundcardForm)

    submit = SubmitField("Save")


class AssemblySelectForm(FlaskForm):
    assembly_name = StringField("Assembly Name", validators=[DataRequired()])
    assembly_quantity = IntegerField(
        "Assemblies quantity", validators=[NumberRange(min=1, max=1000)], default=1
    )

    motherboard_id = SelectField("Motherboard", coerce=int, validators=[DataRequired()])
    motherboard_quantity = IntegerField(
        "Motherboard quantity", default=1, validators=[NumberRange(min=1, max=100)]
    )

    cpu_id = SelectField("CPU", coerce=int, validators=[DataRequired()])
    cpu_quantity = IntegerField(
        "CPU quantity", default=1, validators=[NumberRange(min=1, max=100)]
    )

    gpu_is_integrated = BooleanField("Use integrated GPU")
    gpu_id = SelectField("Discrete GPU", choices=[], coerce=int, validators=[])
    gpu_quantity = IntegerField("GPU quantity", default=1)

    ram_id = SelectField("RAM", coerce=int, validators=[DataRequired()])
    ram_quantity = IntegerField(
        "RAM quantity", default=1, validators=[NumberRange(min=1, max=100)]
    )

    soundcard_id = SelectField("Soundcard", coerce=int, validators=[DataRequired()])
    soundcard_quantity = IntegerField(
        "Soundcard quantity", default=1, validators=[NumberRange(min=1, max=100)]
    )

    submit = SubmitField("Create Assembly")


class BrandForm(FlaskForm):
    name = StringField("Brand", validators=[DataRequired()])
    component_type = SelectField(
        "Component Type",
        choices=[
            ("motherboard", "Motherboard"),
            ("cpu", "CPU"),
            ("gpu", "GPU"),
            ("ram", "RAM"),
            ("soundcard", "Soundcard"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add brand")


class SocketForm(FlaskForm):
    name = StringField("Socket type", validators=[DataRequired()])
    submit = SubmitField("Add socket type")


class MemoryTypeForm(FlaskForm):
    name = StringField("Memory type", validators=[DataRequired()])
    submit = SubmitField("Add memory type")

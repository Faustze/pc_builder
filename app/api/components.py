from http import HTTPStatus

from flask_restx import Namespace, Resource, fields
from flask_restx.reqparse import RequestParser

<<<<<<< HEAD
from .common_models import register_common_models
=======
from app.common_models import register_common_models
>>>>>>> c5f234ff2ba19e75b2d1e9b596f23c9b79a73b6d

components_ns = Namespace("components", description="Операции с компонентами")
models = register_common_models(components_ns)

components_parser = RequestParser()
components_parser.add_argument("component_type", type=str, help="Тип компонента для фильтрации")
components_parser.add_argument("brand_id", type=int, help="ID бренда для фильтрации")

status_code: dict = {
    "201": HTTPStatus.CREATED,
    "400": HTTPStatus.BAD_REQUEST,
    "404": HTTPStatus.NOT_FOUND,
    "409": HTTPStatus.CONFLICT,
    "500": HTTPStatus.INTERNAL_SERVER_ERROR,
}

base_component_model = components_ns.model(
    "BaseComponent",
    {
        "id": fields.Integer(required=True, description="ID компонента"),
        "brand_id": fields.Integer(required=True, description="ID бренда"),
        "model": fields.String(required=True, description="Модель"),
        "quantity": fields.Integer(required=True, description="Количество"),
        "component_type": fields.String(required=True, description="Тип компонента"),
    },
)

motherboard_model = components_ns.inherit(
    "Motherboard",
    base_component_model,
    {
        "socket_type_id": fields.Integer(required=True, description="ID типа сокета"),
        "memory_type_id": fields.Integer(required=True, description="ID типа памяти"),
        "has_integrated_graphics": fields.Boolean(description="Наличие встроенной графики"),
    },
)

cpu_model = components_ns.inherit(
    "CPU",
    base_component_model,
    {
        "socket_type_id": fields.Integer(required=True, description="ID типа сокета"),
        "cores": fields.Integer(required=True, description="Количество ядер"),
        "threads": fields.Integer(required=True, description="Количество потоков"),
        "has_integrated_graphics": fields.Boolean(description="Наличие встроенной графики"),
    },
)

gpu_model = components_ns.inherit(
    "GPU",
    base_component_model,
    {"vram": fields.Integer(required=True, description="Объем видеопамяти в ГБ")},
)

ram_model = components_ns.inherit(
    "RAM",
    base_component_model,
    {
        "memory_type_id": fields.Integer(required=True, description="ID типа памяти"),
        "capacity": fields.Integer(required=True, description="Объем в ГБ"),
        "frequency": fields.Integer(required=True, description="Частота в МГц"),
    },
)

soundcard_model = components_ns.inherit(
    "Soundcard",
    base_component_model,
    {"channels_quantity": fields.Integer(required=True, description="Количество каналов")},
)

motherboard_input = components_ns.model(
    "MotherboardInput",
    {
        "brand_id": fields.Integer(required=True, description="ID бренда"),
        "model": fields.String(required=True, description="Модель"),
        "quantity": fields.Integer(required=True, description="Количество"),
        "socket_type_id": fields.Integer(required=True, description="ID типа сокета"),
        "memory_type_id": fields.Integer(required=True, description="ID типа памяти"),
        "has_integrated_graphics": fields.Boolean(description="Наличие встроенной графики"),
    },
)

cpu_input = components_ns.model(
    "CPUInput",
    {
        "brand_id": fields.Integer(required=True, description="ID бренда"),
        "model": fields.String(required=True, description="Модель"),
        "quantity": fields.Integer(required=True, description="Количество"),
        "socket_type_id": fields.Integer(required=True, description="ID типа сокета"),
        "cores": fields.Integer(required=True, description="Количество ядер"),
        "threads": fields.Integer(required=True, description="Количество потоков"),
        "has_integrated_graphics": fields.Boolean(description="Наличие встроенной графики"),
    },
)

gpu_input = components_ns.model(
    "GPUInput",
    {
        "brand_id": fields.Integer(required=True, description="ID бренда"),
        "model": fields.String(required=True, description="Модель"),
        "quantity": fields.Integer(required=True, description="Количество"),
        "vram": fields.Integer(required=True, description="Объем видеопамяти в ГБ"),
    },
)

ram_input = components_ns.model(
    "RAMInput",
    {
        "brand_id": fields.Integer(required=True, description="ID бренда"),
        "model": fields.String(required=True, description="Модель"),
        "quantity": fields.Integer(required=True, description="Количество"),
        "memory_type_id": fields.Integer(required=True, description="ID типа памяти"),
        "capacity": fields.Integer(required=True, description="Объем в ГБ"),
        "frequency": fields.Integer(required=True, description="Частота в МГц"),
    },
)

soundcard_input = components_ns.model(
    "SoundcardInput",
    {
        "brand_id": fields.Integer(required=True, description="ID бренда"),
        "model": fields.String(required=True, description="Модель"),
        "quantity": fields.Integer(required=True, description="Количество"),
        "channels_quantity": fields.Integer(required=True, description="Количество каналов"),
    },
)


@components_ns.route("/")
class ComponentsListResource(Resource):
    @components_ns.doc("get_components")
    @components_ns.expect(components_parser)
    @components_ns.marshal_list_with(base_component_model)
    @components_ns.response(200, "Успешно")
    def get(self):
        """Получить список всех компонентов с возможностью фильтрации"""
        pass


@components_ns.route("/add")
class ComponentsAddResource(Resource):
    @components_ns.doc("get_add_component_page")
    @components_ns.response(200, "Страница добавления компонента")
    def get(self):
        """Получить страницу выбора типа компонента для добавления"""
        pass


@components_ns.route("/add/motherboard")
class MotherboardAddResource(Resource):
    @components_ns.doc("get_add_motherboard_form")
    @components_ns.response(200, "Форма добавления материнской платы")
    def get(self):
        """Получить форму для добавления материнской платы"""
        pass

    @components_ns.doc("add_motherboard")
    @components_ns.expect(motherboard_input)
    @components_ns.marshal_with(motherboard_model, code=status_code["201"])
    @components_ns.response(201, "Материнская плата успешно добавлена")
    @components_ns.response(400, "Ошибка валидации")
    @components_ns.response(409, "Конфликт - компонент уже существует")
    def post(self):
        """Добавить новую материнскую плату"""
        pass


@components_ns.route("/add/cpu")
class CPUAddResource(Resource):
    @components_ns.doc("get_add_cpu_form")
    @components_ns.response(200, "Форма добавления процессора")
    def get(self):
        """Получить форму для добавления процессора"""
        pass

    @components_ns.doc("add_cpu")
    @components_ns.expect(cpu_input)
    @components_ns.marshal_with(cpu_model, code=status_code["201"])
    @components_ns.response(201, "Процессор успешно добавлен")
    @components_ns.response(400, "Ошибка валидации")
    def post(self):
        """Добавить новый процессор"""
        pass


@components_ns.route("/add/gpu")
class GPUAddResource(Resource):
    @components_ns.doc("get_add_gpu_form")
    @components_ns.response(200, "Форма добавления видеокарты")
    def get(self):
        """Получить форму для добавления видеокарты"""
        pass

    @components_ns.doc("add_gpu")
    @components_ns.expect(gpu_input)
    @components_ns.marshal_with(gpu_model, code=status_code["201"])
    @components_ns.response(201, "Видеокарта успешно добавлена")
    @components_ns.response(400, "Ошибка валидации")
    def post(self):
        """Добавить новую видеокарту"""
        pass


@components_ns.route("/add/ram")
class RAMAddResource(Resource):
    @components_ns.doc("get_add_ram_form")
    @components_ns.response(200, "Форма добавления оперативной памяти")
    def get(self):
        """Получить форму для добавления оперативной памяти"""
        pass

    @components_ns.doc("add_ram")
    @components_ns.expect(ram_input)
    @components_ns.marshal_with(ram_model, code=status_code["201"])
    @components_ns.response(201, "Оперативная память успешно добавлена")
    @components_ns.response(400, "Ошибка валидации")
    def post(self):
        """Добавить новую оперативную память"""
        pass


@components_ns.route("/add/soundcard")
class SoundcardAddResource(Resource):
    @components_ns.doc("get_add_soundcard_form")
    @components_ns.response(200, "Форма добавления звуковой карты")
    def get(self):
        """Получить форму для добавления звуковой карты"""
        pass

    @components_ns.doc("add_soundcard")
    @components_ns.expect(soundcard_input)
    @components_ns.marshal_with(soundcard_model, code=status_code["201"])
    @components_ns.response(201, "Звуковая карта успешно добавлена")
    @components_ns.response(400, "Ошибка валидации")
    def post(self):
        """Добавить новую звуковую карту"""
        pass


@components_ns.route("/<int:component_id>")
class ComponentResource(Resource):
    @components_ns.doc("get_component")
    @components_ns.marshal_with(base_component_model)
    @components_ns.response(200, "Успешно")
    @components_ns.response(404, "Компонент не найден")
    def get(self, component_id):
        """Получить информацию о компоненте по ID"""
        pass


@components_ns.route("/<int:component_id>/edit")
class ComponentEditResource(Resource):
    @components_ns.doc("get_edit_component_form")
    @components_ns.response(200, "Форма редактирования компонента")
    @components_ns.response(404, "Компонент не найден")
    def get(self, component_id):
        """Получить форму для редактирования компонента"""
        pass

    @components_ns.doc("edit_component")
    @components_ns.response(200, "Компонент успешно обновлен")
    @components_ns.response(400, "Ошибка валидации")
    @components_ns.response(404, "Компонент не найден")
    def post(self, component_id):
        """Обновить информацию о компоненте"""
        pass


@components_ns.route("/<int:component_id>/delete")
class ComponentDeleteResource(Resource):
    @components_ns.doc("delete_component")
    @components_ns.response(200, "Компонент успешно удален")
    @components_ns.response(404, "Компонент не найден")
    @components_ns.response(409, "Невозможно удалить - компонент используется в сборках")
    def post(self, component_id):
        """Удалить компонент"""
        pass

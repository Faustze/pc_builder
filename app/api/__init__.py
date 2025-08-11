from flask import Blueprint
from flask_restx import Api, Resource, fields

from .home import home_ns
from .components import components_ns
from .classificators import classificators_ns
from .assemblies import assemblies_ns


def init_api(app):
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api = Api(
        api_bp,
        version='1.0',
        title='PC Components API',
        description='API для управления компонентами компьютера и сборками',
        doc='/api/'
    )

    api.model('Brand', {
        'id': fields.Integer(required=True, description='ID бренда'),
        'name': fields.String(required=True, description='Название бренда'),
        'component_type': fields.String(required=True, description='Тип компонента')
    })

    api.model('SocketType', {
        'id': fields.Integer(required=True, description='ID типа сокета'),
        'name': fields.String(required=True, description='Название сокета')
    })

    api.model('MemoryType', {
        'id': fields.Integer(required=True, description='ID типа памяти'),
        'name': fields.String(required=True, description='Название типа памяти')
    })

    assembly_model = api.model('Assembly', {
        'id': fields.Integer(required=True, description='ID сборки'),
        'name': fields.String(required=True, description='Название сборки'),
        'quantity': fields.Integer(required=True, description='Количество')
    })

    assembly_input = api.model('AssemblyInput', {
        'assembly_name': fields.String(required=True, description='Название сборки'),
        'assembly_quantity': fields.Integer(required=True, description='Количество'),
        'motherboard_id': fields.Integer(description='ID материнской платы'),
        'motherboard_quantity': fields.Integer(description='Количество материнских плат'),
        'cpu_id': fields.Integer(description='ID процессора'),
        'cpu_quantity': fields.Integer(description='Количество процессоров'),
        'gpu_id': fields.Integer(description='ID видеокарты'),
        'gpu_quantity': fields.Integer(description='Количество видеокарт'),
        'gpu_is_integrated': fields.Boolean(description='Использовать встроенную графику'),
        'ram_id': fields.Integer(description='ID оперативной памяти'),
        'ram_quantity': fields.Integer(description='Количество модулей RAM'),
        'soundcard_id': fields.Integer(description='ID звуковой карты'),
        'soundcard_quantity': fields.Integer(description='Количество звуковых карт')
    })

    api.model('BrandInput', {
        'name': fields.String(required=True, description='Название бренда'),
        'component_type': fields.String(
            required=True,
            description='Тип компонента',
            enum=['motherboard', 'cpu', 'gpu', 'ram', 'soundcard'])
    })

    api.model('SocketInput', {
        'name': fields.String(required=True, description='Название сокета')
    })

    api.model('MemoryInput', {
        'name': fields.String(required=True, description='Название типа памяти')
    })

    api.add_namespace(home_ns, path='/')
    api.add_namespace(components_ns, path='/components')
    api.add_namespace(classificators_ns, path='/classificators')
    api.add_namespace(assemblies_ns, path='/assemblies')

    @assemblies_ns.route('/')
    class AssembliesListResource(Resource):
        @assemblies_ns.doc('get_assemblies')
        @assemblies_ns.marshal_list_with(assembly_model)
        @assemblies_ns.response(200, 'Успешно')
        def get(self):
            """Получить список всех сборок"""
            pass

    @assemblies_ns.route('/add/select')
    class AssemblyAddResource(Resource):
        @assemblies_ns.doc('get_add_assembly_form')
        @assemblies_ns.response(200, 'Форма создания сборки')
        def get(self):
            """Получить форму для создания новой сборки"""
            pass

        @assemblies_ns.doc('add_assembly')
        @assemblies_ns.expect(assembly_input)
        @assemblies_ns.marshal_with(assembly_model, code=201)  # type: ignore
        @assemblies_ns.response(201, 'Сборка успешно создана')
        @assemblies_ns.response(400, 'Ошибка валидации или несовместимые компоненты')
        def post(self):
            """Создать новую сборку из выбранных компонентов"""
            pass

    @assemblies_ns.route('/<int:assembly_id>')
    class AssemblyResource(Resource):
        @assemblies_ns.doc('get_assembly')
        @assemblies_ns.marshal_with(assembly_model)
        @assemblies_ns.response(200, 'Успешно')
        @assemblies_ns.response(404, 'Сборка не найдена')
        def get(self, assembly_id):
            """Получить детальную информацию о сборке"""
            pass

    @assemblies_ns.route('/<int:assembly_id>/delete')
    class AssemblyDeleteResource(Resource):
        @assemblies_ns.doc('delete_assembly')
        @assemblies_ns.response(200, 'Сборка успешно удалена')
        @assemblies_ns.response(404, 'Сборка не найдена')
        def post(self, assembly_id):
            """Удалить сборку"""
            pass

    @assemblies_ns.route('/edit/<int:assembly_id>')
    class AssemblyEditResource(Resource):
        @assemblies_ns.doc('get_edit_assembly_form')
        @assemblies_ns.response(200, 'Форма редактирования сборки')
        @assemblies_ns.response(404, 'Сборка не найдена')
        def get(self, assembly_id):
            """Получить форму для редактирования сборки"""
            pass

        @assemblies_ns.doc('edit_assembly')
        @assemblies_ns.expect(assembly_input)
        @assemblies_ns.marshal_with(assembly_model)
        @assemblies_ns.response(200, 'Сборка успешно обновлена')
        @assemblies_ns.response(400, 'Ошибка валидации или несовместимые компоненты')
        @assemblies_ns.response(404, 'Сборка не найдена')
        def post(self, assembly_id):
            """Обновить сборку"""
            pass

    @assemblies_ns.route('/<int:assembly_id>/download/xml')
    class AssemblyDownloadXMLResource(Resource):
        @assemblies_ns.doc('download_assembly_xml')
        @assemblies_ns.response(200, 'XML файл сборки', headers={'Content-Type': 'application/xml'})
        @assemblies_ns.response(404, 'Сборка не найдена')
        def get(self, assembly_id):
            """Скачать сборку в формате XML"""
            pass

    @assemblies_ns.route('/<int:assembly_id>/download/json')
    class AssemblyDownloadJSONResource(Resource):
        @assemblies_ns.doc('download_assembly_json')
        @assemblies_ns.response(200, 'JSON файл сборки', headers={'Content-Type': 'application/json'})
        @assemblies_ns.response(404, 'Сборка не найдена')
        def get(self, assembly_id):
            """Скачать сборку в формате JSON"""
            pass

    @assemblies_ns.route('/<int:assembly_id>/download/txt')
    class AssemblyDownloadTXTResource(Resource):
        @assemblies_ns.doc('download_assembly_txt')
        @assemblies_ns.response(200, 'TXT файл сборки', headers={'Content-Type': 'text/plain'})
        @assemblies_ns.response(404, 'Сборка не найдена')
        def get(self, assembly_id):
            """Скачать сборку в формате TXT"""
            pass

    return api

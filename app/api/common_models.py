from flask_restx import fields


def register_common_models(api):
    brand_model = api.model('Brand', {
        'id': fields.Integer(required=True, description='ID бренда'),
        'name': fields.String(required=True, description='Название бренда'),
        'component_type': fields.String(required=True, description='Тип компонента')
    })

    brand_input_model = api.model('BrandInput', {
        'name': fields.String(required=True, description='Название бренда'),
        'component_type': fields.String(
            required=True,
            description='Тип компонента',
            enum=['motherboard', 'cpu', 'gpu', 'ram', 'soundcard'])
    })

    socket_type_model = api.model('SocketType', {
        'id': fields.Integer(required=True, description='ID типа сокета'),
        'name': fields.String(required=True, description='Название сокета')
    })

    socket_input_model = api.model('SocketInput', {
        'name': fields.String(required=True, description='Название сокета')
    })

    memory_type_model = api.model('MemoryType', {
        'id': fields.Integer(required=True, description='ID типа памяти'),
        'name': fields.String(required=True, description='Название типа памяти')
    })

    memory_input_model = api.model('MemoryInput', {
        'name': fields.String(required=True, description='Название типа памяти')
    })

    return {
        'Brand': brand_model,
        'BrandInput': brand_input_model,
        'SocketType': socket_type_model,
        'SocketInput': socket_input_model,
        'MemoryType': memory_type_model,
        'MemoryInput': memory_input_model
    }

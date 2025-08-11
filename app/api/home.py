from flask_restx import Namespace, Resource


home_ns = Namespace('home', description='Главная страница')


@home_ns.route('/')
class Home(Resource):
    def get(self):
        return {'message': 'Добро пожаловать в API PC Builder!'}

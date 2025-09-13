from flask_restx import Namespace, Resource

from .common_models import register_common_models

classificators_ns = Namespace("classificators", description="Операции с классификаторами")
models = register_common_models(classificators_ns)


@classificators_ns.route("/")
class ClassificatorsResource(Resource):
    @classificators_ns.doc("get_classificators")
    @classificators_ns.response(200, "Страница управления классификаторами")
    def get(self):
        """Получить страницу управления классификаторами (бренды, сокеты, типы памяти)"""
        pass

    @classificators_ns.doc("add_classificator")
    @classificators_ns.response(201, "Классификатор успешно добавлен")
    @classificators_ns.response(400, "Ошибка валидации")
    @classificators_ns.response(409, "Классификатор уже существует")
    def post(self):
        """Добавить новый классификатор (бренд, сокет или тип памяти)"""
        pass


@classificators_ns.route("/brand_<int:brand_id>/delete")
class BrandDeleteResource(Resource):
    @classificators_ns.doc("delete_brand")
    @classificators_ns.response(200, "Бренд успешно удален")
    @classificators_ns.response(404, "Бренд не найден")
    @classificators_ns.response(409, "Невозможно удалить - бренд используется в компонентах")
    def post(self, brand_id):
        """Удалить бренд"""
        pass


@classificators_ns.route("/socket_type_<int:socket_type_id>/delete")
class SocketTypeDeleteResource(Resource):
    @classificators_ns.doc("delete_socket_type")
    @classificators_ns.response(200, "Тип сокета успешно удален")
    @classificators_ns.response(404, "Тип сокета не найден")
    @classificators_ns.response(409, "Невозможно удалить - тип сокета используется в компонентах")
    def post(self, socket_type_id):
        """Удалить тип сокета"""
        pass


@classificators_ns.route("/memory_type_<int:memory_type_id>/delete")
class MemoryTypeDeleteResource(Resource):
    @classificators_ns.doc("delete_memory_type")
    @classificators_ns.response(200, "Тип памяти успешно удален")
    @classificators_ns.response(404, "Тип памяти не найден")
    @classificators_ns.response(409, "Невозможно удалить - тип памяти используется в компонентах")
    def post(self, memory_type_id):
        """Удалить тип памяти"""
        pass

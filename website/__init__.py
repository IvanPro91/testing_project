import os
from instance.config import *
from flask import Flask, make_response
from .extensions import *
from .includes.database.database_models import *
from .routes.authorization import *
from flask_restful import Api

def load_config(mode=os.environ.get('MODE')):
    """Выбор и загрузка конфигурации."""
    try:
        if mode:
            if 'prod' in mode.lower():
                print(ProductionConfig)
                return ProductionConfig
            elif 'dev' in mode.lower():
                print(DevelopmentConfig)
                return DevelopmentConfig
        else:
            return None
    except ImportError:
        return None


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Конфигурации
    app.config.from_object(load_config())

    # Подключаем маршруты
    api = Api(app, prefix="/api/v1")
    api.add_resource(user_login, '/user_login')
    api.add_resource(user_registration, '/user_registration')

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'status': False, 'error': 'Not found'}), 404)

    db.init_app(app)
    migrate.init_app(app, db)
    return app

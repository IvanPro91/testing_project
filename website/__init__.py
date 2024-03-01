from flask import Flask, make_response
from sqlalchemy import NullPool
from .extensions import *
from .includes.database.database_models import *
from .routes.authorization import *
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    # Конфигурации
    app.secret_key = "agag-sgasasf14112asfafh1sfgksafgkw-wq45ufrjqwrtj"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2222@localhost:5432/TestingProject"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SQLALCHEMY_POOL_SIZE'] = 20  # Количество соединений в пуле
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10  # Время ожидания соединения в секундах
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  # Время переиспользования соединения в секундах
    app.config['SCHEDULER_API_INTERVAL'] = 5  # in seconds
    app.config['SQLALCHEMY_POOL_CLASS'] = NullPool

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
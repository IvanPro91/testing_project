import os
from flask import Flask, make_response, jsonify
from flask_restful import Api
from instance.config import ProductionConfig
from instance.config import DevelopmentConfig
from website.extensions import db, migrate
from website.routes.authorization import user_login, user_registration

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
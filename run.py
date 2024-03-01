from website import *

# Инициализируем зависимости и микрофреймворк flask
app = create_app()

# Используя контекст, создаем таблицы БД в зависимости от конфигурации
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
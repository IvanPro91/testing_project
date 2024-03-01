from ...extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Таблица пользователей
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, comment="Уникальный номер")
    username = db.Column(db.String(), comment="ФИО пользователя")
    login = db.Column(db.String(), nullable=False, unique=True, comment="Уникальное имя пользователя")
    password = db.Column(db.String(), comment="Пароль пользователя")

    def __repr__(self):
        return f"Пользователь: '<{self.id}:{self.username}>'"

    # Установка пароля пользователя
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Метод проверки пароля пользователя
    def check_password(self, password):
        return check_password_hash(self.password, password)
